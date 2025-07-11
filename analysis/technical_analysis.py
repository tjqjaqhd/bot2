import pandas as pd
import numpy as np
import pandas_ta as ta
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)

class TechnicalAnalyzer:
    """Technical analysis using pandas-ta indicators"""
    
    def __init__(self):
        """Initialize the technical analyzer"""
        pass
    
    def calculate_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calculate various technical indicators"""
        if df.empty:
            return df
        
        try:
            # Ensure we have the required columns
            required_cols = ['open', 'high', 'low', 'close', 'volume']
            if not all(col in df.columns for col in required_cols):
                logger.error("Missing required OHLCV columns")
                return df
            
            # Moving Averages
            df['sma_20'] = ta.sma(df['close'], length=20)
            df['sma_50'] = ta.sma(df['close'], length=50)
            df['ema_12'] = ta.ema(df['close'], length=12)
            df['ema_26'] = ta.ema(df['close'], length=26)
            
            # MACD
            macd = ta.macd(df['close'])
            df = pd.concat([df, macd], axis=1)
            
            # RSI
            df['rsi'] = ta.rsi(df['close'], length=14)
            
            # Bollinger Bands
            bb = ta.bbands(df['close'], length=20)
            df = pd.concat([df, bb], axis=1)
            
            # Stochastic
            stoch = ta.stoch(df['high'], df['low'], df['close'])
            df = pd.concat([df, stoch], axis=1)
            
            # Volume indicators
            df['volume_sma'] = ta.sma(df['volume'], length=20)
            
            # ATR (Average True Range)
            df['atr'] = ta.atr(df['high'], df['low'], df['close'], length=14)
            
            # Williams %R
            df['willr'] = ta.willr(df['high'], df['low'], df['close'], length=14)
            
            return df
            
        except Exception as e:
            logger.error(f"Error calculating indicators: {e}")
            return df
    
    def generate_signals(self, df: pd.DataFrame) -> Dict:
        """Generate trading signals based on indicators"""
        if df.empty:
            return {'signals': [], 'strength': 0, 'recommendation': 'HOLD'}
        
        signals = []
        bullish_count = 0
        bearish_count = 0
        
        try:
            latest = df.iloc[-1]
            prev = df.iloc[-2] if len(df) > 1 else latest
            
            # Price vs Moving Averages
            if 'sma_20' in df.columns and not pd.isna(latest['sma_20']):
                if latest['close'] > latest['sma_20']:
                    signals.append("Price above SMA(20) - Bullish")
                    bullish_count += 1
                else:
                    signals.append("Price below SMA(20) - Bearish")
                    bearish_count += 1
            
            # MACD Signal
            if 'MACD_12_26_9' in df.columns and 'MACDs_12_26_9' in df.columns:
                if not pd.isna(latest['MACD_12_26_9']) and not pd.isna(latest['MACDs_12_26_9']):
                    if latest['MACD_12_26_9'] > latest['MACDs_12_26_9']:
                        signals.append("MACD above signal line - Bullish")
                        bullish_count += 1
                    else:
                        signals.append("MACD below signal line - Bearish")
                        bearish_count += 1
            
            # RSI Analysis
            if 'rsi' in df.columns and not pd.isna(latest['rsi']):
                if latest['rsi'] > 70:
                    signals.append("RSI Overbought (>70) - Bearish")
                    bearish_count += 1
                elif latest['rsi'] < 30:
                    signals.append("RSI Oversold (<30) - Bullish")
                    bullish_count += 1
                elif 40 <= latest['rsi'] <= 60:
                    signals.append("RSI Neutral - No clear signal")
            
            # Bollinger Bands
            if all(col in df.columns for col in ['BBL_20_2.0', 'BBU_20_2.0']):
                if not pd.isna(latest['BBL_20_2.0']) and not pd.isna(latest['BBU_20_2.0']):
                    if latest['close'] > latest['BBU_20_2.0']:
                        signals.append("Price above Upper Bollinger Band - Bearish")
                        bearish_count += 1
                    elif latest['close'] < latest['BBL_20_2.0']:
                        signals.append("Price below Lower Bollinger Band - Bullish")
                        bullish_count += 1
            
            # Volume Analysis
            if 'volume_sma' in df.columns and not pd.isna(latest['volume_sma']):
                if latest['volume'] > latest['volume_sma'] * 1.5:
                    signals.append("High volume activity - Strong signal")
                elif latest['volume'] < latest['volume_sma'] * 0.5:
                    signals.append("Low volume activity - Weak signal")
            
            # Calculate overall recommendation
            total_signals = bullish_count + bearish_count
            if total_signals == 0:
                recommendation = 'HOLD'
                strength = 0
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
                'signals': signals,
                'bullish_count': bullish_count,
                'bearish_count': bearish_count,
                'strength': round(strength, 2),
                'recommendation': recommendation,
                'latest_values': {
                    'close': latest['close'],
                    'rsi': latest.get('rsi'),
                    'macd': latest.get('MACD_12_26_9'),
                    'volume': latest['volume']
                }
            }
            
        except Exception as e:
            logger.error(f"Error generating signals: {e}")
            return {'signals': [], 'strength': 0, 'recommendation': 'HOLD'}
    
    def analyze(self, data: Dict) -> Dict:
        """Complete technical analysis of market data"""
        if not data.get('price_data'):
            return {'error': 'No price data available'}
        
        try:
            # Convert price data to DataFrame
            df = pd.DataFrame(data['price_data'])
            if df.empty:
                return {'error': 'Empty price data'}
            
            # Calculate indicators
            df_with_indicators = self.calculate_indicators(df)
            
            # Generate signals
            signals = self.generate_signals(df_with_indicators)
            
            # Prepare result
            result = {
                'symbol': data['symbol'],
                'market_type': data['market_type'],
                'analysis_timestamp': data['timestamp'],
                'technical_indicators': {},
                'signals': signals
            }
            
            # Add latest indicator values
            if not df_with_indicators.empty:
                latest = df_with_indicators.iloc[-1]
                result['technical_indicators'] = {
                    'sma_20': latest.get('sma_20'),
                    'sma_50': latest.get('sma_50'),
                    'rsi': latest.get('rsi'),
                    'macd': latest.get('MACD_12_26_9'),
                    'macd_signal': latest.get('MACDs_12_26_9'),
                    'bb_upper': latest.get('BBU_20_2.0'),
                    'bb_lower': latest.get('BBL_20_2.0'),
                    'atr': latest.get('atr'),
                    'volume_ratio': latest['volume'] / latest.get('volume_sma', 1) if latest.get('volume_sma') else None
                }
            
            return result
            
        except Exception as e:
            logger.error(f"Error in technical analysis: {e}")
            return {'error': str(e)}