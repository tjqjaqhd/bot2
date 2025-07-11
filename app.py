from flask import Flask, render_template, jsonify, request
from datetime import datetime
import logging
import os
from data_collection.market_data import MarketDataCollector
from analysis.technical_analysis import TechnicalAnalyzer
from agents.agent_manager import AgentManager
from trading.paper_trader import PaperTrader
from utils.database import Database

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Initialize components
market_data = MarketDataCollector()
analyzer = TechnicalAnalyzer()
agent_manager = AgentManager()
paper_trader = PaperTrader()
db = Database()

@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('index.html')

@app.route('/api/market-data/<symbol>')
def get_market_data(symbol):
    """Get market data for a symbol"""
    try:
        data = market_data.get_data(symbol)
        return jsonify(data)
    except Exception as e:
        logger.error(f"Error getting market data for {symbol}: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/analysis/<symbol>')
def get_analysis(symbol):
    """Get technical analysis for a symbol"""
    try:
        data = market_data.get_data(symbol)
        analysis = analyzer.analyze(data)
        return jsonify(analysis)
    except Exception as e:
        logger.error(f"Error analyzing {symbol}: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/agents/decision/<symbol>')
def get_agent_decision(symbol):
    """Get AI agent decision for a symbol"""
    try:
        data = market_data.get_data(symbol)
        analysis = analyzer.analyze(data)
        decision = agent_manager.make_decision(symbol, data, analysis)
        return jsonify(decision)
    except Exception as e:
        logger.error(f"Error getting agent decision for {symbol}: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/portfolio')
def get_portfolio():
    """Get current portfolio status"""
    try:
        portfolio = paper_trader.get_portfolio()
        return jsonify(portfolio)
    except Exception as e:
        logger.error(f"Error getting portfolio: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/execute-trade', methods=['POST'])
def execute_trade():
    """Execute a paper trade"""
    try:
        data = request.get_json()
        result = paper_trader.execute_trade(
            symbol=data['symbol'],
            action=data['action'],
            quantity=data['quantity'],
            price=data.get('price')
        )
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error executing trade: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/logs')
def get_logs():
    """Get trading logs"""
    try:
        logs = db.get_logs()
        return jsonify(logs)
    except Exception as e:
        logger.error(f"Error getting logs: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)