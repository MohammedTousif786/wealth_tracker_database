import yfinance as yf
from typing import Dict, Optional
from datetime import datetime

class MarketDataService:
    
    @staticmethod
    def get_current_price(symbol: str) -> Optional[Dict]:
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            current_price = info.get('currentPrice') or info.get('regularMarketPrice')
            
            if current_price:
                return {
                    "symbol": symbol,
                    "price": float(current_price),
                    "timestamp": datetime.utcnow(),
                    "currency": info.get('currency', 'USD')
                }
            return None
        except Exception as e:
            print(f"Error fetching price for {symbol}: {e}")
            return None
    
    @staticmethod
    def get_multiple_prices(symbols: list) -> Dict[str, Optional[Dict]]:
        results = {}
        for symbol in symbols:
            results[symbol] = MarketDataService.get_current_price(symbol)
        return results
    
    @staticmethod
    def get_historical_data(symbol: str, period: str = "1mo") -> Optional[Dict]:
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period=period)
            
            if not hist.empty:
                return {
                    "symbol": symbol,
                    "data": hist.to_dict('records'),
                    "period": period
                }
            return None
        except Exception as e:
            print(f"Error fetching historical data for {symbol}: {e}")
            return None

market_service = MarketDataService()