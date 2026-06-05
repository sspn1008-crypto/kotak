import requests
from typing import Dict, Optional, List
from config import (
    KOTAK_API_KEY,
    KOTAK_API_SECRET,
    KOTAK_CLIENT_ID,
    KOTAK_PASSWORD,
    KOTAK_CONSUMER_KEY,
    KOTAK_CONSUMER_SECRET
)

class KotakNEOClient:
    """
    Kotak NEO API Client for placing and managing orders
    """
    
    def __init__(self):
        self.base_url = "https://api.kotaksecurities.com/v1"
        self.auth_token = None
        self.session = requests.Session()
        self.initialize()
    
    def initialize(self) -> bool:
        """
        Initialize and authenticate with Kotak NEO API
        """
        try:
            auth_payload = {
                "client_id": KOTAK_CLIENT_ID,
                "password": KOTAK_PASSWORD,
                "consumer_key": KOTAK_CONSUMER_KEY,
                "consumer_secret": KOTAK_CONSUMER_SECRET
            }
            
            response = requests.post(
                f"{self.base_url}/auth/login",
                json=auth_payload
            )
            
            if response.status_code == 200:
                self.auth_token = response.json().get('auth_token')
                print("✓ Kotak NEO authentication successful")
                return True
            else:
                print(f"✗ Authentication failed: {response.text}")
                return False
                
        except Exception as e:
            print(f"✗ Authentication error: {str(e)}")
            return False
    
    def _get_headers(self) -> Dict:
        """
        Get headers for API requests
        """
        return {
            "Authorization": f"Bearer {self.auth_token}",
            "Content-Type": "application/json",
            "X-API-KEY": KOTAK_API_KEY
        }
    
    def place_order(
        self,
        symbol: str,
        order_type: str,
        quantity: int,
        price: Optional[float] = None,
        order_side: str = "BUY"
    ) -> Dict:
        """
        Place an order on Kotak NEO
        
        Args:
            symbol: Trading symbol (e.g., 'SBIN-EQ', 'RELIANCE-EQ')
            order_type: 'MIS' (intraday), 'CNC' (delivery), 'NRML' (normal)
            quantity: Number of shares
            price: Price for limit orders (None for market)
            order_side: 'BUY' or 'SELL'
            
        Returns:
            Order response dictionary
        """
        try:
            payload = {
                "symbol": symbol,
                "quantity": quantity,
                "side": order_side.upper(),
                "order_type": "MARKET" if price is None else "LIMIT",
                "order_variety": order_type,
                "price": price or 0
            }
            
            response = self.session.post(
                f"{self.base_url}/orders",
                json=payload,
                headers=self._get_headers()
            )
            
            if response.status_code in [200, 201]:
                order_data = response.json()
                print(f"✓ Order placed: {order_side} {quantity} {symbol}")
                return order_data
            else:
                print(f"✗ Order placement failed: {response.text}")
                return {"error": response.text}
                
        except Exception as e:
            print(f"✗ Order placement error: {str(e)}")
            return {"error": str(e)}
    
    def cancel_order(self, order_id: str) -> Dict:
        """
        Cancel an existing order
        """
        try:
            response = self.session.delete(
                f"{self.base_url}/orders/{order_id}",
                headers=self._get_headers()
            )
            
            if response.status_code == 200:
                print(f"✓ Order cancelled: {order_id}")
                return response.json()
            else:
                print(f"✗ Cancel failed: {response.text}")
                return {"error": response.text}
                
        except Exception as e:
            print(f"✗ Cancel error: {str(e)}")
            return {"error": str(e)}
    
    def get_orders(self) -> List[Dict]:
        """
        Get list of all orders
        """
        try:
            response = self.session.get(
                f"{self.base_url}/orders",
                headers=self._get_headers()
            )
            
            if response.status_code == 200:
                return response.json().get('orders', [])
            else:
                print(f"✗ Failed to fetch orders: {response.text}")
                return []
                
        except Exception as e:
            print(f"✗ Error fetching orders: {str(e)}")
            return []
    
    def get_positions(self) -> List[Dict]:
        """
        Get current open positions
        """
        try:
            response = self.session.get(
                f"{self.base_url}/positions",
                headers=self._get_headers()
            )
            
            if response.status_code == 200:
                return response.json().get('positions', [])
            else:
                print(f"✗ Failed to fetch positions: {response.text}")
                return []
                
        except Exception as e:
            print(f"✗ Error fetching positions: {str(e)}")
            return []
