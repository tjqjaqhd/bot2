from typing import Dict, List, Optional
import logging
from datetime import datetime
import json

logger = logging.getLogger(__name__)

class BaseAgent:
    """Base class for all trading agents"""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.confidence = 0.0
    
    def analyze(self, symbol: str, market_data: Dict, technical_analysis: Dict) -> Dict:
        """Analyze data and provide recommendation"""
        raise NotImplementedError

class StockComparisonAgent(BaseAgent):
    """Agent1: 종목비교 (Stock Comparison)"""
    
    def __init__(self):
        super().__init__("Stock Comparison Agent", "Compares multiple stocks and finds relative value")
    
    def analyze(self, symbol: str, market_data: Dict, technical_analysis: Dict) -> Dict:
        """Compare stocks and provide relative analysis"""
        try:
            recommendation = "HOLD"
            confidence = 0.5
            reasoning = []
            
            # Get technical signals
            tech_signals = technical_analysis.get('signals', {})
            tech_recommendation = tech_signals.get('recommendation', 'HOLD')
            tech_strength = tech_signals.get('strength', 0)
            
            # Simple comparison logic based on technical strength
            if tech_recommendation in ['STRONG_BUY', 'BUY'] and tech_strength > 0.6:
                recommendation = "BUY"
                confidence = min(tech_strength + 0.1, 0.9)
                reasoning.append(f"Strong technical signals: {tech_recommendation}")
            elif tech_recommendation in ['STRONG_SELL', 'SELL'] and tech_strength > 0.6:
                recommendation = "SELL"
                confidence = min(tech_strength + 0.1, 0.9)
                reasoning.append(f"Weak technical signals: {tech_recommendation}")
            else:
                reasoning.append("Mixed or neutral technical signals")
            
            # Check RSI for momentum
            rsi = technical_analysis.get('technical_indicators', {}).get('rsi')
            if rsi:
                if rsi < 30:
                    reasoning.append("RSI indicates oversold condition - potential buy opportunity")
                    if recommendation != "SELL":
                        recommendation = "BUY"
                        confidence = min(confidence + 0.2, 0.9)
                elif rsi > 70:
                    reasoning.append("RSI indicates overbought condition - potential sell opportunity")
                    if recommendation != "BUY":
                        recommendation = "SELL"
                        confidence = min(confidence + 0.2, 0.9)
            
            self.confidence = confidence
            
            return {
                'agent': self.name,
                'recommendation': recommendation,
                'confidence': confidence,
                'reasoning': reasoning,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error in StockComparisonAgent: {e}")
            return {
                'agent': self.name,
                'recommendation': 'HOLD',
                'confidence': 0.0,
                'reasoning': [f"Error in analysis: {str(e)}"],
                'timestamp': datetime.now().isoformat()
            }

class MarketSentimentAgent(BaseAgent):
    """Agent2: 시장심리 (Market Sentiment)"""
    
    def __init__(self):
        super().__init__("Market Sentiment Agent", "Analyzes market sentiment and news")
    
    def analyze(self, symbol: str, market_data: Dict, technical_analysis: Dict) -> Dict:
        """Analyze market sentiment"""
        try:
            recommendation = "HOLD"
            confidence = 0.5
            reasoning = []
            
            # Analyze news sentiment (simplified)
            news = market_data.get('news', [])
            if news:
                positive_news = 0
                negative_news = 0
                
                for article in news[:5]:  # Check top 5 news
                    headline = article.get('headline', '').lower()
                    # Simple keyword-based sentiment analysis
                    positive_keywords = ['up', 'rise', 'gain', 'profit', 'growth', 'positive', 'bull', 'strong']
                    negative_keywords = ['down', 'fall', 'loss', 'decline', 'negative', 'bear', 'weak', 'drop']
                    
                    pos_count = sum(1 for word in positive_keywords if word in headline)
                    neg_count = sum(1 for word in negative_keywords if word in headline)
                    
                    if pos_count > neg_count:
                        positive_news += 1
                    elif neg_count > pos_count:
                        negative_news += 1
                
                if positive_news > negative_news:
                    recommendation = "BUY"
                    confidence = 0.6 + (positive_news - negative_news) * 0.1
                    reasoning.append(f"Positive news sentiment: {positive_news} positive vs {negative_news} negative")
                elif negative_news > positive_news:
                    recommendation = "SELL"
                    confidence = 0.6 + (negative_news - positive_news) * 0.1
                    reasoning.append(f"Negative news sentiment: {negative_news} negative vs {positive_news} positive")
                else:
                    reasoning.append("Neutral news sentiment")
            else:
                reasoning.append("No recent news available for sentiment analysis")
            
            # Volume sentiment analysis
            volume_ratio = technical_analysis.get('technical_indicators', {}).get('volume_ratio')
            if volume_ratio:
                if volume_ratio > 1.5:
                    reasoning.append("High volume activity suggests strong interest")
                    confidence = min(confidence + 0.1, 0.9)
                elif volume_ratio < 0.5:
                    reasoning.append("Low volume activity suggests weak interest")
                    if confidence > 0.3:
                        confidence -= 0.1
            
            self.confidence = min(confidence, 0.9)
            
            return {
                'agent': self.name,
                'recommendation': recommendation,
                'confidence': self.confidence,
                'reasoning': reasoning,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error in MarketSentimentAgent: {e}")
            return {
                'agent': self.name,
                'recommendation': 'HOLD',
                'confidence': 0.0,
                'reasoning': [f"Error in analysis: {str(e)}"],
                'timestamp': datetime.now().isoformat()
            }

class RiskManagementAgent(BaseAgent):
    """Agent3: 리스크조절 (Risk Management)"""
    
    def __init__(self):
        super().__init__("Risk Management Agent", "Evaluates and manages trading risks")
    
    def analyze(self, symbol: str, market_data: Dict, technical_analysis: Dict) -> Dict:
        """Analyze and manage risks"""
        try:
            recommendation = "HOLD"
            confidence = 0.5
            reasoning = []
            risk_level = "MEDIUM"
            
            # Volatility analysis using ATR
            atr = technical_analysis.get('technical_indicators', {}).get('atr')
            if atr:
                # Simplified volatility assessment
                price = technical_analysis.get('signals', {}).get('latest_values', {}).get('close', 100)
                if price > 0:
                    volatility_ratio = atr / price
                    if volatility_ratio > 0.05:  # 5% daily volatility
                        risk_level = "HIGH"
                        reasoning.append("High volatility detected - increased risk")
                        confidence = max(confidence - 0.2, 0.1)
                    elif volatility_ratio < 0.02:  # 2% daily volatility
                        risk_level = "LOW"
                        reasoning.append("Low volatility detected - reduced risk")
                        confidence = min(confidence + 0.1, 0.9)
            
            # RSI-based risk assessment
            rsi = technical_analysis.get('technical_indicators', {}).get('rsi')
            if rsi:
                if rsi > 80 or rsi < 20:
                    reasoning.append("Extreme RSI levels indicate high risk")
                    risk_level = "HIGH"
                    recommendation = "HOLD"  # Conservative approach
                elif 30 <= rsi <= 70:
                    reasoning.append("RSI in normal range - moderate risk")
            
            # Bollinger Bands risk assessment
            bb_upper = technical_analysis.get('technical_indicators', {}).get('bb_upper')
            bb_lower = technical_analysis.get('technical_indicators', {}).get('bb_lower')
            price = technical_analysis.get('signals', {}).get('latest_values', {}).get('close')
            
            if all([bb_upper, bb_lower, price]):
                bb_width = (bb_upper - bb_lower) / price if price > 0 else 0
                if bb_width > 0.1:  # Wide bands indicate high volatility
                    risk_level = "HIGH"
                    reasoning.append("Wide Bollinger Bands indicate high volatility risk")
                elif bb_width < 0.03:  # Narrow bands
                    reasoning.append("Narrow Bollinger Bands indicate low volatility")
            
            # Risk-adjusted recommendation
            if risk_level == "HIGH":
                recommendation = "HOLD"
                confidence = 0.3
                reasoning.append("High risk environment - recommend holding position")
            elif risk_level == "LOW":
                # Allow other agents' recommendations to have more weight
                tech_rec = technical_analysis.get('signals', {}).get('recommendation', 'HOLD')
                if tech_rec in ['BUY', 'STRONG_BUY']:
                    recommendation = "BUY"
                    confidence = 0.7
                elif tech_rec in ['SELL', 'STRONG_SELL']:
                    recommendation = "SELL"
                    confidence = 0.7
                reasoning.append("Low risk environment - technical signals can be followed")
            
            self.confidence = confidence
            
            return {
                'agent': self.name,
                'recommendation': recommendation,
                'confidence': confidence,
                'risk_level': risk_level,
                'reasoning': reasoning,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error in RiskManagementAgent: {e}")
            return {
                'agent': self.name,
                'recommendation': 'HOLD',
                'confidence': 0.0,
                'risk_level': 'HIGH',
                'reasoning': [f"Error in analysis: {str(e)}"],
                'timestamp': datetime.now().isoformat()
            }

class ConsensusAgent(BaseAgent):
    """Agent4: 최종합의 (Final Consensus)"""
    
    def __init__(self):
        super().__init__("Consensus Agent", "Makes final trading decision based on all agents")
    
    def analyze(self, symbol: str, market_data: Dict, technical_analysis: Dict, agent_decisions: List[Dict]) -> Dict:
        """Make final consensus decision"""
        try:
            if not agent_decisions:
                return {
                    'agent': self.name,
                    'final_recommendation': 'HOLD',
                    'confidence': 0.0,
                    'reasoning': ['No agent decisions available'],
                    'timestamp': datetime.now().isoformat()
                }
            
            # Weighted voting system
            buy_votes = 0
            sell_votes = 0
            hold_votes = 0
            total_confidence = 0
            reasoning = []
            
            # Process each agent's decision
            for decision in agent_decisions:
                rec = decision.get('recommendation', 'HOLD')
                conf = decision.get('confidence', 0)
                agent_name = decision.get('agent', 'Unknown')
                
                # Weight votes by confidence
                if rec in ['BUY', 'STRONG_BUY']:
                    buy_votes += conf
                elif rec in ['SELL', 'STRONG_SELL']:
                    sell_votes += conf
                else:
                    hold_votes += conf
                
                total_confidence += conf
                reasoning.append(f"{agent_name}: {rec} (confidence: {conf:.2f})")
            
            # Determine final recommendation
            if buy_votes > sell_votes and buy_votes > hold_votes:
                final_recommendation = "BUY"
                final_confidence = buy_votes / len(agent_decisions) if agent_decisions else 0
            elif sell_votes > buy_votes and sell_votes > hold_votes:
                final_recommendation = "SELL"
                final_confidence = sell_votes / len(agent_decisions) if agent_decisions else 0
            else:
                final_recommendation = "HOLD"
                final_confidence = hold_votes / len(agent_decisions) if agent_decisions else 0
            
            # Apply consensus threshold
            if final_confidence < 0.6:
                final_recommendation = "HOLD"
                reasoning.append("Confidence below threshold - defaulting to HOLD")
            
            # Check for risk management override
            risk_agent_decision = next((d for d in agent_decisions if 'Risk' in d.get('agent', '')), None)
            if risk_agent_decision and risk_agent_decision.get('risk_level') == 'HIGH':
                if final_recommendation != 'HOLD':
                    reasoning.append("Risk management override - high risk detected")
                    final_recommendation = "HOLD"
                    final_confidence = min(final_confidence, 0.4)
            
            self.confidence = min(final_confidence, 0.9)
            
            return {
                'agent': self.name,
                'final_recommendation': final_recommendation,
                'confidence': self.confidence,
                'agent_votes': {
                    'buy_votes': round(buy_votes, 2),
                    'sell_votes': round(sell_votes, 2),
                    'hold_votes': round(hold_votes, 2)
                },
                'reasoning': reasoning,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error in ConsensusAgent: {e}")
            return {
                'agent': self.name,
                'final_recommendation': 'HOLD',
                'confidence': 0.0,
                'reasoning': [f"Error in consensus: {str(e)}"],
                'timestamp': datetime.now().isoformat()
            }