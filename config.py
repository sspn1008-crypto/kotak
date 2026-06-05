import os
from dotenv import load_dotenv

load_dotenv()

# Kotak NEO Configuration
KOTAK_API_KEY = os.getenv('KOTAK_API_KEY')
KOTAK_API_SECRET = os.getenv('KOTAK_API_SECRET')
KOTAK_CLIENT_ID = os.getenv('KOTAK_CLIENT_ID')
KOTAK_PASSWORD = os.getenv('KOTAK_PASSWORD')
KOTAK_CONSUMER_KEY = os.getenv('KOTAK_CONSUMER_KEY')
KOTAK_CONSUMER_SECRET = os.getenv('KOTAK_CONSUMER_SECRET')

# TradingView Webhook Configuration
WEBHOOK_SECRET = os.getenv('WEBHOOK_SECRET', 'your-webhook-secret')
FLASK_PORT = int(os.getenv('FLASK_PORT', 5000))
FLASK_DEBUG = os.getenv('FLASK_DEBUG', 'False') == 'True'

# Order Configuration
DEFAULT_ORDER_QUANTITY = int(os.getenv('DEFAULT_ORDER_QUANTITY', 1))
STOP_LOSS_PERCENTAGE = float(os.getenv('STOP_LOSS_PERCENTAGE', 2.0))
TARGET_PERCENTAGE = float(os.getenv('TARGET_PERCENTAGE', 5.0))
ORDER_TYPE = os.getenv('ORDER_TYPE', 'MARKET')  # MARKET or LIMIT
