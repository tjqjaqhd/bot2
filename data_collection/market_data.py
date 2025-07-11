import ccxt
import yfinance as yf
import finnhub
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import logging
import os
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

class MarketDataCollector:
    """Collects market data from various sources"""
    
    def __init__(self):
        """Initialize data sources"""
        # Initialize CCXT exchange (using Binance as default)
        self.exchange = ccxt.binance({
            'apiKey': os.getenv('BINANCE_API_KEY'),
            'secret': os.getenv('BINANCE_SECRET'),
            'sandbox': True,  # Use testnet for safety
            'enableRateLimit': True,
        })
        
        # Initialize Finnhub (for news and additional data)
        self.finnhub_client = finnhub.Client(api_key=os.getenv('FINNHUB_API_KEY', 'demo'))
        
    def get_crypto_data(self, symbol: str, timeframe: str = '1h', limit: int = 100) -> pd.DataFrame:
        """Get cryptocurrency data from CCXT"""
        try:
            ohlcv = self.exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
            df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            df.set_index('timestamp', inplace=True)
            return df
        except Exception as e:
            logger.error(f"Error fetching crypto data for {symbol}: {e}")
            return pd.DataFrame()
    
    def get_stock_data(self, symbol: str, period: str = '1mo') -> pd.DataFrame:
        """Get stock data from Yahoo Finance"""
        try:
            ticker = yf.Ticker(symbol)
            df = ticker.history(period=period)
            df.columns = [col.lower() for col in df.columns]
            return df
        except Exception as e:
            logger.error(f"Error fetching stock data for {symbol}: {e}")
            return pd.DataFrame()
    
    def get_forex_data(self, symbol: str, period: str = '1mo') -> pd.DataFrame:
        """Get forex data from Yahoo Finance"""
        try:
            # Convert symbol to Yahoo Finance format (e.g., 'EURUSD' -> 'EURUSD=X')
            if '=' not in symbol:
                symbol = f"{symbol}=X"
            return self.get_stock_data(symbol, period)
        except Exception as e:
            logger.error(f"Error fetching forex data for {symbol}: {e}")
            return pd.DataFrame()
    
    def get_news(self, symbol: str, limit: int = 10) -> List[Dict]:
        """Get news data from Finnhub"""
        try:
            # Get current date and one week ago
            to_date = datetime.now().strftime('%Y-%m-%d')
            from_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
            
            news = self.finnhub_client.company_news(symbol, _from=from_date, to=to_date)
            return news[:limit] if news else []
        except Exception as e:
            logger.error(f"Error fetching news for {symbol}: {e}")
            return []
    
    def get_data(self, symbol: str, data_type: str = 'auto') -> Dict:
        """Get comprehensive data for a symbol"""
        result = {
            'symbol': symbol,
            'timestamp': datetime.now().isoformat(),
            'price_data': None,
            'news': [],
            'market_type': None
        }
        
        # Auto-detect market type if not specified
        if data_type == 'auto':
            if '/' in symbol:  # Crypto pairs (e.g., 'BTC/USDT')
                data_type = 'crypto'
            elif symbol.endswith('=X'):  # Forex pairs
                data_type = 'forex'
            else:  # Assume stock
                data_type = 'stock'
        
        result['market_type'] = data_type
        
        # Get price data based on type
        if data_type == 'crypto':
            result['price_data'] = self.get_crypto_data(symbol).to_dict('records')
        elif data_type == 'forex':
            result['price_data'] = self.get_forex_data(symbol).to_dict('records')
        else:  # stock
            result['price_data'] = self.get_stock_data(symbol).to_dict('records')
            # Get news for stocks
            result['news'] = self.get_news(symbol)
        
        return result
    
    def get_multiple_symbols(self, symbols: List[str]) -> Dict:
        """Get data for multiple symbols"""
        results = {}
        for symbol in symbols:
            results[symbol] = self.get_data(symbol)
        return results