from flask import Flask, request, jsonify
import hmac
import hashlib
from tradingview_signal_handler import TradingViewSignalHandler
from kotak_neo_client import KotakNEOClient
from config import WEBHOOK_SECRET, FLASK_PORT, FLASK_DEBUG, DEFAULT_ORDER_QUANTITY
from datetime import datetime

app = Flask(__name__)
signal_handler = TradingViewSignalHandler()
kotak_client = KotakNEOClient()

# Store active orders for reference
active_orders = {}


@app.route('/webhook', methods=['POST'])
def handle_tradingview_signal():
    """
    TradingView webhook endpoint
    Receives trading signals and executes orders via Kotak NEO
    """
    try:
        # Validate webhook signature
        signature = request.headers.get('X-Webhook-Signature')
        data = request.get_data(as_text=True)
        
        if signature and not TradingViewSignalHandler.validate_webhook_signature(data, signature):
            return jsonify({"error": "Invalid signature"}), 401
        
        # Parse the signal
        payload = request.get_json()
        signal, is_valid = signal_handler.parse_signal(payload)
        
        if not is_valid:
            return jsonify({"error": "Invalid signal"}), 400
        
        # Convert symbol to Kotak format
        kotak_symbol = signal_handler.get_kotak_symbol(signal['ticker'])
        
        # Place order
        order_response = kotak_client.place_order(
            symbol=kotak_symbol,
            order_type=signal['order_type'],
            quantity=signal.get('quantity', DEFAULT_ORDER_QUANTITY),
            price=signal.get('price'),
            order_side=signal['action']
        )
        
        if 'error' in order_response:
            return jsonify({"error": order_response['error']}), 400
        
        # Store order reference
        order_id = order_response.get('order_id')
        if order_id:
            active_orders[order_id] = {
                "symbol": kotak_symbol,
                "signal": signal,
                "timestamp": datetime.utcnow().isoformat(),
                "response": order_response
            }
        
        return jsonify({
            "status": "success",
            "message": f"Order placed: {signal['action']} {signal['quantity']} {kotak_symbol}",
            "order_id": order_id,
            "signal": signal
        }), 200
        
    except Exception as e:
        print(f"✗ Webhook error: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint
    """
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "active_orders": len(active_orders)
    }), 200


@app.route('/orders', methods=['GET'])
def get_orders():
    """
    Get list of active orders
    """
    try:
        kotak_orders = kotak_client.get_orders()
        return jsonify({
            "active_orders_count": len(active_orders),
            "kotak_orders": kotak_orders,
            "tracked_orders": list(active_orders.keys())
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/positions', methods=['GET'])
def get_positions():
    """
    Get current positions from Kotak NEO
    """
    try:
        positions = kotak_client.get_positions()
        return jsonify({
            "positions": positions,
            "position_count": len(positions)
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/signal-history', methods=['GET'])
def signal_history():
    """
    Get signal history
    """
    limit = request.args.get('limit', 10, type=int)
    history = signal_handler.get_signal_history(limit)
    return jsonify({
        "count": len(history),
        "signals": history
    }), 200


@app.route('/order/<order_id>', methods=['DELETE'])
def cancel_order(order_id):
    """
    Cancel a specific order
    """
    try:
        result = kotak_client.cancel_order(order_id)
        
        if 'error' in result:
            return jsonify({"error": result['error']}), 400
        
        # Remove from active orders
        if order_id in active_orders:
            del active_orders[order_id]
        
        return jsonify({
            "status": "success",
            "message": f"Order {order_id} cancelled",
            "result": result
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Endpoint not found"}), 404


@app.errorhandler(500)
def server_error(e):
    return jsonify({"error": "Internal server error"}), 500


if __name__ == '__main__':
    print("="*50)
    print("TradingView → Kotak NEO Signal Router")
    print("="*50)
    print(f"Starting server on port {FLASK_PORT}...")
    print(f"Debug mode: {FLASK_DEBUG}")
    print("\nWebhook endpoint: POST /webhook")
    print("="*50)
    
    app.run(
        host='0.0.0.0',
        port=FLASK_PORT,
        debug=FLASK_DEBUG
    )
