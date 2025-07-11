import json
import sqlite3
from datetime import datetime
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    from flask import Flask, render_template, jsonify, request
except ImportError:
    logger.error("Flask not available, creating mock Flask app")
    
    class MockFlask:
        def __init__(self, name):
            self.routes = {}
        
        def route(self, path, methods=None):
            def decorator(func):
                self.routes[path] = func
                return func
            return decorator
        
        def run(self, **kwargs):
            print(f"Mock Flask app would run on {kwargs.get('host', 'localhost')}:{kwargs.get('port', 5000)}")
    
    Flask = MockFlask
    
    def render_template(template):
        return f"Would render template: {template}"
    
    def jsonify(data):
        return json.dumps(data)
    
    class MockRequest:
        def get_json(self):
            return {}
    
    request = MockRequest()

# Import our simplified modules
from data_collection.mock_data import MockMarketDataCollector
from analysis.simple_analysis import SimpleTechnicalAnalyzer
from agents.agent_manager import AgentManager
from trading.paper_trader import PaperTrader
from utils.database import Database

app = Flask(__name__)

# Initialize components
try:
    market_data = MockMarketDataCollector()
    analyzer = SimpleTechnicalAnalyzer()
    agent_manager = AgentManager()
    paper_trader = PaperTrader()
    db = Database()
    logger.info("All components initialized successfully")
except Exception as e:
    logger.error(f"Error initializing components: {e}")
    # Create minimal fallbacks
    market_data = None
    analyzer = None
    agent_manager = None
    paper_trader = None
    db = None

@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('index.html')

@app.route('/api/market-data/<symbol>')
def get_market_data(symbol):
    """Get market data for a symbol"""
    try:
        if not market_data:
            return jsonify({'error': 'Market data service not available'})
        
        data = market_data.get_data(symbol)
        return jsonify(data)
    except Exception as e:
        logger.error(f"Error getting market data for {symbol}: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/analysis/<symbol>')
def get_analysis(symbol):
    """Get technical analysis for a symbol"""
    try:
        if not market_data or not analyzer:
            return jsonify({'error': 'Analysis service not available'})
        
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
        if not market_data or not analyzer or not agent_manager:
            return jsonify({'error': 'Agent service not available'})
        
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
        if not paper_trader:
            return jsonify({'error': 'Trading service not available'})
        
        portfolio = paper_trader.get_portfolio()
        return jsonify(portfolio)
    except Exception as e:
        logger.error(f"Error getting portfolio: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/execute-trade', methods=['POST'])
def execute_trade():
    """Execute a paper trade"""
    try:
        if not paper_trader:
            return jsonify({'error': 'Trading service not available'})
        
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No trade data provided'})
        
        result = paper_trader.execute_trade(
            symbol=data.get('symbol'),
            action=data.get('action'),
            quantity=float(data.get('quantity', 0)),
            price=float(data.get('price', 0))
        )
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error executing trade: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/logs')
def get_logs():
    """Get trading logs"""
    try:
        if not db:
            # Return mock logs
            mock_logs = [
                {
                    'timestamp': datetime.now().isoformat(),
                    'level': 'INFO',
                    'module': 'system',
                    'message': 'Trading bot system started'
                },
                {
                    'timestamp': datetime.now().isoformat(),
                    'level': 'INFO',
                    'module': 'portfolio',
                    'message': 'Portfolio initialized with $100,000'
                }
            ]
            return jsonify(mock_logs)
        
        logs = db.get_logs()
        return jsonify(logs)
    except Exception as e:
        logger.error(f"Error getting logs: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'running',
        'timestamp': datetime.now().isoformat(),
        'components': {
            'market_data': market_data is not None,
            'analyzer': analyzer is not None,
            'agent_manager': agent_manager is not None,
            'paper_trader': paper_trader is not None,
            'database': db is not None
        }
    })

def create_basic_html():
    """Create a basic HTML page for testing"""
    html_content = """
<!DOCTYPE html>
<html>
<head>
    <title>Trading Bot Dashboard</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        .card { border: 1px solid #ddd; padding: 20px; margin: 20px 0; border-radius: 8px; }
        .button { background: #007bff; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; }
        .button:hover { background: #0056b3; }
        .result { margin-top: 10px; padding: 10px; background: #f8f9fa; border-radius: 4px; }
    </style>
</head>
<body>
    <h1>Trading Bot Dashboard</h1>
    
    <div class="card">
        <h2>Market Analysis</h2>
        <input type="text" id="symbol" placeholder="Enter symbol (e.g., AAPL, BTC)" style="padding: 8px; width: 200px;">
        <button class="button" onclick="analyzeSymbol()">Analyze</button>
        <div id="analysisResult" class="result" style="display: none;"></div>
    </div>
    
    <div class="card">
        <h2>Portfolio</h2>
        <button class="button" onclick="loadPortfolio()">Load Portfolio</button>
        <div id="portfolioResult" class="result" style="display: none;"></div>
    </div>
    
    <div class="card">
        <h2>Execute Trade</h2>
        <input type="text" id="tradeSymbol" placeholder="Symbol" style="padding: 8px; margin: 5px;">
        <select id="tradeAction" style="padding: 8px; margin: 5px;">
            <option value="BUY">Buy</option>
            <option value="SELL">Sell</option>
        </select>
        <input type="number" id="tradeQuantity" placeholder="Quantity" style="padding: 8px; margin: 5px;">
        <input type="number" id="tradePrice" placeholder="Price" style="padding: 8px; margin: 5px;">
        <button class="button" onclick="executeTrade()">Execute</button>
        <div id="tradeResult" class="result" style="display: none;"></div>
    </div>

    <script>
        async function analyzeSymbol() {
            const symbol = document.getElementById('symbol').value;
            if (!symbol) return;
            
            const resultDiv = document.getElementById('analysisResult');
            resultDiv.style.display = 'block';
            resultDiv.innerHTML = 'Loading...';
            
            try {
                const response = await fetch('/api/analysis/' + symbol);
                const data = await response.json();
                
                if (data.error) {
                    resultDiv.innerHTML = 'Error: ' + data.error;
                } else {
                    resultDiv.innerHTML = '<pre>' + JSON.stringify(data, null, 2) + '</pre>';
                }
            } catch (error) {
                resultDiv.innerHTML = 'Error: ' + error.message;
            }
        }
        
        async function loadPortfolio() {
            const resultDiv = document.getElementById('portfolioResult');
            resultDiv.style.display = 'block';
            resultDiv.innerHTML = 'Loading...';
            
            try {
                const response = await fetch('/api/portfolio');
                const data = await response.json();
                resultDiv.innerHTML = '<pre>' + JSON.stringify(data, null, 2) + '</pre>';
            } catch (error) {
                resultDiv.innerHTML = 'Error: ' + error.message;
            }
        }
        
        async function executeTrade() {
            const symbol = document.getElementById('tradeSymbol').value;
            const action = document.getElementById('tradeAction').value;
            const quantity = document.getElementById('tradeQuantity').value;
            const price = document.getElementById('tradePrice').value;
            
            if (!symbol || !quantity || !price) {
                alert('Please fill all fields');
                return;
            }
            
            const resultDiv = document.getElementById('tradeResult');
            resultDiv.style.display = 'block';
            resultDiv.innerHTML = 'Executing...';
            
            try {
                const response = await fetch('/api/execute-trade', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ symbol, action, quantity, price })
                });
                
                const data = await response.json();
                resultDiv.innerHTML = '<pre>' + JSON.stringify(data, null, 2) + '</pre>';
            } catch (error) {
                resultDiv.innerHTML = 'Error: ' + error.message;
            }
        }
    </script>
</body>
</html>
    """
    
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    
    # Write the HTML file
    with open('templates/index.html', 'w') as f:
        f.write(html_content)

if __name__ == '__main__':
    # Create basic HTML template if Flask templates don't exist
    if not os.path.exists('templates/index.html'):
        create_basic_html()
    
    # Log startup
    logger.info("Starting Trading Bot Web Application")
    
    try:
        if hasattr(app, 'run'):
            app.run(debug=True, host='0.0.0.0', port=5000)
        else:
            logger.info("Mock Flask app initialized. In a real environment, this would start a web server.")
            # Demonstrate the functionality
            print("\n=== Trading Bot Demo ===")
            
            if market_data and analyzer:
                print("\n1. Analyzing AAPL...")
                data = market_data.get_data('AAPL')
                analysis = analyzer.analyze(data)
                print(f"Analysis result: {analysis.get('signals', {}).get('recommendation', 'N/A')}")
            
            if paper_trader:
                print("\n2. Getting portfolio...")
                portfolio = paper_trader.get_portfolio()
                print(f"Cash balance: ${portfolio.get('portfolio', {}).get('cash', 0):,.2f}")
                
                print("\n3. Executing sample trade...")
                trade_result = paper_trader.execute_trade('AAPL', 'BUY', 10, 180.0)
                print(f"Trade result: {trade_result.get('message', 'N/A')}")
            
            print("\n=== Demo Complete ===")
            
    except Exception as e:
        logger.error(f"Error starting application: {e}")
        print(f"Application failed to start: {e}")