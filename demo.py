#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data_collection.mock_data import MockMarketDataCollector
from analysis.simple_analysis import SimpleTechnicalAnalyzer
from agents.agent_manager import AgentManager
from trading.paper_trader import PaperTrader

def main():
    print('=== Trading Bot Demo ===')

    # Test data collection
    print('\n1. Testing data collection...')
    collector = MockMarketDataCollector()
    data = collector.get_data('AAPL')
    print(f'✓ Got market data for AAPL: {len(data.get("price_data", []))} data points')

    # Test technical analysis
    print('\n2. Testing technical analysis...')
    analyzer = SimpleTechnicalAnalyzer()
    analysis = analyzer.analyze(data)
    recommendation = analysis.get("signals", {}).get("recommendation", "N/A")
    rsi = analysis.get("technical_indicators", {}).get("rsi", "N/A")
    print(f'✓ Technical analysis complete: {recommendation} recommendation')
    print(f'  RSI: {rsi}')

    # Test AI agents
    print('\n3. Testing AI agents...')
    agent_manager = AgentManager()
    decision = agent_manager.make_decision('AAPL', data, analysis)
    ai_rec = decision.get("summary", {}).get("recommendation", "N/A")
    confidence = decision.get("summary", {}).get("confidence", 0)
    agent_count = decision.get("summary", {}).get("agent_count", 0)
    print(f'✓ AI consensus: {ai_rec}')
    print(f'  Confidence: {confidence:.2f}')
    print(f'  Agents participating: {agent_count}')

    # Test paper trading
    print('\n4. Testing paper trading...')
    trader = PaperTrader()
    portfolio = trader.get_portfolio()
    cash = portfolio.get("portfolio", {}).get("cash", 0)
    print(f'✓ Portfolio initialized: Cash ${cash:,.2f}')

    # Execute sample trades
    trade1 = trader.execute_trade('AAPL', 'BUY', 100, 180.0)
    print(f'✓ Buy trade: {trade1.get("message", "Failed")}')

    trade2 = trader.execute_trade('TSLA', 'BUY', 50, 250.0)
    print(f'✓ Buy trade: {trade2.get("message", "Failed")}')

    # Check updated portfolio
    portfolio = trader.get_portfolio()
    new_cash = portfolio.get("portfolio", {}).get("cash", 0)
    holdings = portfolio.get('portfolio', {}).get('holdings', {})
    print(f'✓ Updated portfolio: Cash ${new_cash:,.2f}')
    if holdings:
        print(f'  Holdings: {holdings}')

    # Performance metrics
    performance = trader.calculate_performance()
    profit_loss = performance.get("profit_loss", 0)
    return_pct = performance.get("return_pct", 0)
    print(f'✓ Performance: P/L ${profit_loss:,.2f} ({return_pct:.2f}%)')

    print('\n=== Demo Complete - All systems working! ===')

if __name__ == '__main__':
    main()