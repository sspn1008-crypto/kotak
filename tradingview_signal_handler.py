import hashlib
import hmac
import json
from typing import Dict, Tuple
from datetime import datetime
from config import WEBHOOK_SECRET

class TradingViewSignalHandler:
    """
    Handle and validate TradingView webhook signals
    """
    
    # Symbol mapping from TradingView to Kotak format
    SYMBOL_MAPPING = {
        "SBIN": "SBIN-EQ",
        "RELIANCE": "RELIANCE-EQ",
        "INFY": "INFY-EQ",
        "TCS": "TCS-EQ",
        "WIPRO": "WIPRO-EQ",
        "NIFTY": "NIFTY50-IX",
        "BANKNIFTY": "BANKNIFTY-IX",
        # Add more symbols as needed
    }
    
    def __init__(self):
        self.signal_history = []
    
    @staticmethod
    def validate_webhook_signature(data: str, signature: str) -> bool:
        """
        Validate TradingView webhook signature
        
        Args:
            data: Raw request data
            signature: Signature from TradingView header
            
        Returns:
            Boolean indicating if signature is valid
        """
        expected_signature = hmac.new(
            WEBHOOK_SECRET.encode(),
            data.encode(),
            hashlib.sha256
        ).hexdigest()
        
        return hmac.compare_digest(expected_signature, signature)
    
    def parse_signal(self, payload: Dict) -> Tuple[Dict, bool]:
        """
        Parse TradingView webhook payload
        
        Expected payload format:
        {
            "ticker": "SBIN",
            "action": "BUY" or "SELL",
            "quantity": 1,
            "price": 500.0,  # optional
            "order_type": "MIS" or "CNC",
            "timestamp": "2024-01-10T10:30:00Z"
        }
        
        Returns:
            Tuple of (parsed_signal, is_valid)
        """
        try:
            signal = {
                "ticker": payload.get("ticker", "").upper(),
                "action": payload.get("action", "BUY").upper(),
                "quantity": int(payload.get("quantity", 1)),
                "price": float(payload.get("price", 0)) if payload.get("price") else None,
                "order_type": payload.get("order_type", "MIS").upper(),
                "timestamp": payload.get("timestamp", datetime.utcnow().isoformat())
            }
            
            # Validate signal
            is_valid = self._validate_signal(signal)
            
            if is_valid:
                self.signal_history.append(signal)
                print(f"✓ Signal parsed: {signal['action']} {signal['quantity']} {signal['ticker']}")
            
            return signal, is_valid
            
        except Exception as e:
            print(f"✗ Error parsing signal: {str(e)}")
            return {}, False
    
    def _validate_signal(self, signal: Dict) -> bool:
        """
        Validate signal data
        """
        # Check required fields
        if not signal.get("ticker") or not signal.get("action"):
            print("✗ Missing required fields: ticker or action")
            return False
        
        # Validate action
        if signal["action"] not in ["BUY", "SELL"]:
            print(f"✗ Invalid action: {signal['action']}")
            return False
        
        # Validate quantity
        if signal["quantity"] <= 0:
            print(f"✗ Invalid quantity: {signal['quantity']}")
            return False
        
        # Validate order type
        if signal["order_type"] not in ["MIS", "CNC", "NRML"]:
            print(f"✗ Invalid order type: {signal['order_type']}")
            return False
        
        return True
    
    def get_kotak_symbol(self, tradingview_symbol: str) -> str:
        """
        Convert TradingView symbol to Kotak NEO format
        
        Args:
            tradingview_symbol: Symbol from TradingView
            
        Returns:
            Kotak NEO formatted symbol
        """
        symbol = tradingview_symbol.upper()
        return self.SYMBOL_MAPPING.get(symbol, f"{symbol}-EQ")
    
    def get_signal_history(self, limit: int = 10) -> list:
        """
        Get recent signal history
        """
        return self.signal_history[-limit:]
