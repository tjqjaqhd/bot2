import json
import random
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)

class MockMarketDataCollector:
    """Mock market data collector for demonstration"""
    
    def __init__(self):
        """Initialize mock data collector"""
        pass
    
    def get_data(self, symbol: str, data_type: str = 'auto') -> Dict:
        """Get mock market data for demonstration"""
        
        # Generate mock price data
        base_price = 100.0
        if 'BTC' in symbol.upper():
            base_price = 45000.0
        elif 'ETH' in symbol.upper():
            base_price = 3000.0
        elif 'AAPL' in symbol.upper():
            base_price = 180.0
        elif 'TSLA' in symbol.upper():
            base_price = 250.0
        
        # Generate 30 days of mock OHLCV data
        price_data = []
        current_price = base_price
        
        for i in range(30):
            # Simulate price movement
            change = random.uniform(-0.05, 0.05)  # ±5% daily change
            current_price *= (1 + change)
            
            high = current_price * random.uniform(1.0, 1.03)
            low = current_price * random.uniform(0.97, 1.0)
            open_price = current_price * random.uniform(0.98, 1.02)
            volume = random.randint(100000, 10000000)
            
            price_data.append({
                'timestamp': (datetime.now() - timedelta(days=29-i)).isoformat(),
                'open': round(open_price, 2),
                'high': round(high, 2),
                'low': round(low, 2),
                'close': round(current_price, 2),
                'volume': volume
            })
        
        # Mock news data
        news = [
            {
                'headline': f'{symbol} shows strong performance in latest quarter',
                'summary': 'Company reports better than expected earnings',
                'datetime': datetime.now().isoformat(),
                'source': 'Mock News'
            },
            {
                'headline': f'Analysts upgrade {symbol} target price',
                'summary': 'Market sentiment remains positive',
                'datetime': (datetime.now() - timedelta(hours=6)).isoformat(),
                'source': 'Mock Financial'
            }
        ]
        
        return {
            'symbol': symbol,
            'timestamp': datetime.now().isoformat(),
            'price_data': price_data,
            'news': news,
            'market_type': 'stock'
        }