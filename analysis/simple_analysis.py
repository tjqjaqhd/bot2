from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)

class SimpleTechnicalAnalyzer:
    """Simplified technical analysis using basic calculations"""
    
    def __init__(self):
        """Initialize the analyzer"""
        pass
    
    def calculate_sma(self, prices: List[float], period: int) -> float:
        """Calculate Simple Moving Average"""
        if len(prices) < period:
            return None
        return sum(prices[-period:]) / period
    
    def calculate_rsi(self, prices: List[float], period: int = 14) -> float:
        """Calculate RSI indicator"""
        if len(prices) < period + 1:
            return 50.0  # Neutral
        
        gains = []
        losses = []
        
        for i in range(1, len(prices)):
            change = prices[i] - prices[i-1]
            if change > 0:
                gains.append(change)
                losses.append(0)
            else:
                gains.append(0)
                losses.append(-change)
        
        if len(gains) < period:
            return 50.0
        
        avg_gain = sum(gains[-period:]) / period
        avg_loss = sum(losses[-period:]) / period
        
        if avg_loss == 0:
            return 100.0
        
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        return round(rsi, 2)
    
    def calculate_bollinger_bands(self, prices: List[float], period: int = 20, std_dev: float = 2.0) -> Dict:
        """Calculate Bollinger Bands"""
        if len(prices) < period:
            return {'upper': None, 'lower': None, 'middle': None}
        
        recent_prices = prices[-period:]
        sma = sum(recent_prices) / period
        
        # Calculate standard deviation
        variance = sum((price - sma) ** 2 for price in recent_prices) / period
        std = variance ** 0.5
        
        return {
            'upper': round(sma + (std_dev * std), 2),
            'lower': round(sma - (std_dev * std), 2),
            'middle': round(sma, 2)
        }
    
    def analyze(self, data: Dict) -> Dict:
        """Perform technical analysis on market data"""
        if not data.get('price_data'):
            return {'error': 'No price data available'}
        
        try:
            price_data = data['price_data']
            if not price_data:
                return {'error': 'Empty price data'}
            
            # Extract closing prices
            closes = [float(candle['close']) for candle in price_data]
            volumes = [float(candle['volume']) for candle in price_data]
            
            if len(closes) == 0:
                return {'error': 'No closing prices available'}
            
            current_price = closes[-1]
            
            # Calculate indicators
            sma_20 = self.calculate_sma(closes, 20)
            sma_50 = self.calculate_sma(closes, 50) if len(closes) >= 50 else None
            rsi = self.calculate_rsi(closes)
            bb = self.calculate_bollinger_bands(closes)
            
            # Volume analysis
            avg_volume = sum(volumes[-10:]) / min(10, len(volumes)) if volumes else 0
            current_volume = volumes[-1] if volumes else 0
            volume_ratio = current_volume / avg_volume if avg_volume > 0 else 1
            
            # Generate signals
            signals = []
            bullish_count = 0
            bearish_count = 0
            
            # Price vs SMA signals
            if sma_20:
                if current_price > sma_20:
                    signals.append("Price above SMA(20) - Bullish")
                    bullish_count += 1
                else:
                    signals.append("Price below SMA(20) - Bearish")
                    bearish_count += 1
            
            # RSI signals
            if rsi > 70:
                signals.append("RSI Overbought (>70) - Bearish")
                bearish_count += 1
            elif rsi < 30:
                signals.append("RSI Oversold (<30) - Bullish")
                bullish_count += 1
            else:
                signals.append("RSI in normal range - Neutral")
            
            # Bollinger Bands signals
            if bb['upper'] and bb['lower']:
                if current_price > bb['upper']:
                    signals.append("Price above Upper Bollinger Band - Bearish")
                    bearish_count += 1
                elif current_price < bb['lower']:
                    signals.append("Price below Lower Bollinger Band - Bullish")
                    bullish_count += 1
            
            # Volume signals
            if volume_ratio > 1.5:
                signals.append("High volume activity - Strong signal")
            elif volume_ratio < 0.5:
                signals.append("Low volume activity - Weak signal")
            
            # Overall recommendation
            total_signals = bullish_count + bearish_count
            if total_signals == 0:
                recommendation = 'HOLD'
                strength = 0.5
            else:
                bullish_ratio = bullish_count / total_signals
                if bullish_ratio >= 0.7:
                    recommendation = 'STRONG_BUY'
                    strength = bullish_ratio
                elif bullish_ratio >= 0.6:
                    recommendation = 'BUY'
                    strength = bullish_ratio
                elif bullish_ratio <= 0.3:
                    recommendation = 'STRONG_SELL'
                    strength = 1 - bullish_ratio
                elif bullish_ratio <= 0.4:
                    recommendation = 'SELL'
                    strength = 1 - bullish_ratio
                else:
                    recommendation = 'HOLD'
                    strength = 0.5
            
            return {
                'symbol': data['symbol'],
                'market_type': data['market_type'],
                'analysis_timestamp': data['timestamp'],
                'technical_indicators': {
                    'sma_20': sma_20,
                    'sma_50': sma_50,
                    'rsi': rsi,
                    'bb_upper': bb['upper'],
                    'bb_lower': bb['lower'],
                    'bb_middle': bb['middle'],
                    'volume_ratio': round(volume_ratio, 2),
                    'current_price': current_price
                },
                'signals': {
                    'signals': signals,
                    'bullish_count': bullish_count,
                    'bearish_count': bearish_count,
                    'recommendation': recommendation,
                    'strength': round(strength, 2),
                    'latest_values': {
                        'close': current_price,
                        'rsi': rsi,
                        'volume': current_volume
                    }
                }
            }
            
        except Exception as e:
            logger.error(f"Error in technical analysis: {e}")
            return {'error': str(e)}