from typing import Dict, List
import logging
from .agents import StockComparisonAgent, MarketSentimentAgent, RiskManagementAgent, ConsensusAgent

logger = logging.getLogger(__name__)

class AgentManager:
    """Manages all trading agents and coordinates their decisions"""
    
    def __init__(self):
        """Initialize all agents"""
        self.agents = {
            'stock_comparison': StockComparisonAgent(),
            'market_sentiment': MarketSentimentAgent(),
            'risk_management': RiskManagementAgent(),
            'consensus': ConsensusAgent()
        }
        logger.info("AgentManager initialized with all agents")
    
    def make_decision(self, symbol: str, market_data: Dict, technical_analysis: Dict) -> Dict:
        """Coordinate all agents to make a trading decision"""
        try:
            agent_decisions = []
            
            # Get decisions from each agent (except consensus)
            for agent_name, agent in self.agents.items():
                if agent_name != 'consensus':
                    try:
                        decision = agent.analyze(symbol, market_data, technical_analysis)
                        agent_decisions.append(decision)
                        logger.info(f"{agent_name} decision: {decision.get('recommendation')} "
                                  f"(confidence: {decision.get('confidence', 0):.2f})")
                    except Exception as e:
                        logger.error(f"Error getting decision from {agent_name}: {e}")
                        # Add fallback decision
                        agent_decisions.append({
                            'agent': agent.name,
                            'recommendation': 'HOLD',
                            'confidence': 0.0,
                            'reasoning': [f"Agent error: {str(e)}"],
                            'timestamp': agent_decisions[0]['timestamp'] if agent_decisions else None
                        })
            
            # Get final consensus
            consensus_decision = self.agents['consensus'].analyze(
                symbol, market_data, technical_analysis, agent_decisions
            )
            
            # Compile full decision report
            full_decision = {
                'symbol': symbol,
                'timestamp': consensus_decision['timestamp'],
                'individual_agents': agent_decisions,
                'final_decision': consensus_decision,
                'summary': {
                    'recommendation': consensus_decision['final_recommendation'],
                    'confidence': consensus_decision['confidence'],
                    'agent_count': len(agent_decisions),
                    'consensus_reasoning': consensus_decision.get('reasoning', [])
                }
            }
            
            return full_decision
            
        except Exception as e:
            logger.error(f"Error in AgentManager.make_decision: {e}")
            return {
                'symbol': symbol,
                'timestamp': None,
                'individual_agents': [],
                'final_decision': {
                    'agent': 'Consensus Agent',
                    'final_recommendation': 'HOLD',
                    'confidence': 0.0,
                    'reasoning': [f"AgentManager error: {str(e)}"]
                },
                'summary': {
                    'recommendation': 'HOLD',
                    'confidence': 0.0,
                    'agent_count': 0,
                    'consensus_reasoning': [f"System error: {str(e)}"]
                }
            }
    
    def get_agent_status(self) -> Dict:
        """Get status of all agents"""
        status = {}
        for name, agent in self.agents.items():
            status[name] = {
                'name': agent.name,
                'description': agent.description,
                'last_confidence': getattr(agent, 'confidence', 0.0)
            }
        return status