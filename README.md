# TradingView → Kotak NEO Order Automation

Automatically receive trading signals from TradingView and execute orders on Kotak NEO trading platform.

## Features

- 🔗 **TradingView Webhook Integration**: Receive real-time trading signals via webhooks
- 📊 **Kotak NEO API Integration**: Execute orders directly on Kotak NEO platform
- 🔐 **Webhook Signature Validation**: Secure signal verification using HMAC-SHA256
- 📱 **Order Management**: Place, track, and cancel orders programmatically
- 📈 **Position Tracking**: Monitor current positions and open orders
- 🔄 **Signal History**: Keep track of received trading signals
- 🏥 **Health Monitoring**: Built-in health check endpoint

## Setup

### Prerequisites

- Python 3.8+
- Kotak NEO trading account with API access
- TradingView account with Pine Script capabilities

### Installation

1. Clone the repository:
```bash
git clone https://github.com/sspn1008-crypto/kotak.git
cd kotak
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure credentials:
```bash
cp .env.example .env
# Edit .env with your Kotak NEO and TradingView credentials
```

### Running the Server

```bash
python main.py
```

The server will start on `http://localhost:5000`

## API Endpoints

### POST `/webhook`
Receive and process TradingView trading signals

**Request body:**
```json
{
  "ticker": "SBIN",
  "action": "BUY",
  "quantity": 1,
  "price": 500.0,
  "order_type": "MIS",
  "timestamp": "2024-01-10T10:30:00Z"
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Order placed: BUY 1 SBIN-EQ",
  "order_id": "12345",
  "signal": {...}
}
```

### GET `/health`
Check server health status

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-10T10:30:00Z",
  "active_orders": 5
}
```

### GET `/orders`
Get list of active orders

**Response:**
```json
{
  "active_orders_count": 3,
  "kotak_orders": [...],
  "tracked_orders": ["12345", "12346"]
}
```

### GET `/positions`
Get current open positions

**Response:**
```json
{
  "positions": [...],
  "position_count": 2
}
```

### GET `/signal-history?limit=10`
Get signal history

**Response:**
```json
{
  "count": 5,
  "signals": [...]
}
```

### DELETE `/order/<order_id>`
Cancel a specific order

**Response:**
```json
{
  "status": "success",
  "message": "Order 12345 cancelled",
  "result": {...}
}
```

## TradingView Pine Script Example

```pine
//@version=5
strategy("Trading Signal to Kotak", overlay=true)

// Your trading logic here
if ta.crossover(ta.sma(close, 50), ta.sma(close, 200))
    strategy.entry("Buy", strategy.long)
    request.security(syminfo.tickerid, "D", request.http_post(
        url="https://your-server.com/webhook",
        headers=array.from("X-Webhook-Signature: your-signature"),
        data=str.format('{"ticker": "{0}", "action": "BUY", "quantity": 1, "order_type": "MIS"}',
            syminfo.basecurrency)
    ))
```

## Configuration

Edit `.env` file with your settings:

```env
# Kotak NEO API Credentials
KOTAK_API_KEY=your_api_key
KOTAK_API_SECRET=your_api_secret
KOTAK_CLIENT_ID=your_client_id
KOTAK_PASSWORD=your_password
KOTAK_CONSUMER_KEY=your_consumer_key
KOTAK_CONSUMER_SECRET=your_consumer_secret

# TradingView Webhook Secret
WEBHOOK_SECRET=your_webhook_secret

# Server Configuration
FLASK_PORT=5000
FLASK_DEBUG=False

# Default Order Settings
DEFAULT_ORDER_QUANTITY=1
STOP_LOSS_PERCENTAGE=2.0
TARGET_PERCENTAGE=5.0
ORDER_TYPE=MARKET
```

## Symbol Mapping

Edit symbol mapping in `tradingview_signal_handler.py` for your subscribed symbols:

```python
SYMBOL_MAPPING = {
    "SBIN": "SBIN-EQ",
    "RELIANCE": "RELIANCE-EQ",
    "INFY": "INFY-EQ",
    # Add more as needed
}
```

## Error Handling

The system includes comprehensive error handling:

- Invalid webhook signatures are rejected
- Signal validation prevents malformed orders
- API errors are logged and returned with descriptive messages
- All exceptions are caught and reported

## Security Considerations

1. **Webhook Signature Validation**: All TradingView webhooks are validated using HMAC-SHA256
2. **Credentials**: Store credentials in `.env` file (never commit to git)
3. **HTTPS**: Use HTTPS in production
4. **Rate Limiting**: Consider implementing rate limiting for production
5. **Authentication**: Add authentication to sensitive endpoints

## Deployment

### Using Gunicorn (Production)

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 main:app
```

### Using Docker

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "main:app"]
```

## Troubleshooting

### Connection Issues
- Verify Kotak NEO API credentials
- Check network connectivity
- Review API endpoint URLs

### Order Failures
- Check symbol format matches Kotak NEO requirements
- Verify account has sufficient funds
- Check market hours (NSE trading time)
- Review order quantity and type

### Webhook Issues
- Verify webhook secret is correctly configured
- Check webhook signature in TradingView alert
- Ensure server is accessible from TradingView
- Review Flask logs for errors

## License

MIT License

## Disclaimer

This software is provided for educational and research purposes. Trading involves risk. Always backtest strategies thoroughly before deploying with real funds. The authors are not responsible for any financial losses.
