# Trading Bot Web Application

A comprehensive trading bot web application built with Flask that provides:

## Features

### 📊 Data Collection
- **Cryptocurrency data** via CCXT (Binance)
- **Stock data** via Yahoo Finance (yfinance)
- **Forex data** via Yahoo Finance
- **News data** via Finnhub API

### 📈 Technical Analysis
- Multiple technical indicators using pandas-ta
- RSI, MACD, Bollinger Bands, Moving Averages
- Volume analysis and ATR
- Automated signal generation

### 🤖 AI Agents System
- **Agent 1**: Stock Comparison - Relative value analysis
- **Agent 2**: Market Sentiment - News and sentiment analysis
- **Agent 3**: Risk Management - Risk assessment and control
- **Agent 4**: Consensus - Final decision making

### 💰 Paper Trading
- Simulated trading with virtual portfolio
- Position management and tracking
- P&L calculation and performance metrics
- Trade history and logging

### 🗄️ Data Management
- SQLite database for logging
- CSV export capabilities
- Portfolio snapshots
- System event logging

### 🌐 Web Interface
- Real-time dashboard
- Interactive charts and analysis
- Portfolio management
- Trade execution interface

## Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd bot2
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure environment**
```bash
cp .env.example .env
# Edit .env with your API keys
```

4. **Run the application**
```bash
python app.py
```

5. **Access the web interface**
Open your browser to `http://localhost:5000`

## API Endpoints

### Market Data
- `GET /api/market-data/<symbol>` - Get market data for symbol
- `GET /api/analysis/<symbol>` - Get technical analysis

### AI Agents
- `GET /api/agents/decision/<symbol>` - Get AI agent decision

### Portfolio
- `GET /api/portfolio` - Get portfolio status
- `POST /api/execute-trade` - Execute paper trade

### Logging
- `GET /api/logs` - Get system logs

## Configuration

### API Keys Required
- **Finnhub API**: Free tier available at [finnhub.io](https://finnhub.io)
- **Binance API**: Optional, for crypto data (testnet recommended)

### Environment Variables
See `.env.example` for all available configuration options.

## Usage

### Analyzing Symbols
1. Enter a symbol (e.g., AAPL, BTC/USDT, EURUSD=X)
2. Click "Analyze" to get technical analysis
3. View AI agent recommendations

### Paper Trading
1. Navigate to Trading section
2. Enter trade details (symbol, action, quantity, price)
3. Execute trade to update virtual portfolio

### Monitoring
- View portfolio performance in Portfolio section
- Check system logs in Logs section
- Monitor AI agent decisions and reasoning

## Architecture

```
Data Collection (ccxt, yfinance, finnhub)
           ↓
Technical Analysis (pandas, numpy, pandas-ta)
           ↓
AI Agents (LangChain-style decision making)
           ↓
Paper Trading (position management)
           ↓
Logging (SQLite, CSV)
```

## Safety Features

- **Paper trading only** - No real money at risk
- **Testnet mode** - Uses sandbox APIs when available
- **Comprehensive logging** - All actions tracked
- **Risk management** - Built-in risk assessment

## Technologies Used

- **Backend**: Flask, Python
- **Data**: ccxt, yfinance, finnhub-python
- **Analysis**: pandas, numpy, pandas-ta
- **Database**: SQLite, SQLAlchemy
- **Frontend**: HTML5, Bootstrap 5, JavaScript
- **Charts**: Plotly.js (ready for integration)

## Contributing

This is a demonstration implementation. For production use, consider:
- Enhanced security measures
- Real-time data streaming
- Advanced ML models
- Professional charting
- Live trading capabilities (with extreme caution)

## Disclaimer

This software is for educational and demonstration purposes only. Do not use for actual trading without proper testing, risk management, and regulatory compliance. Trading involves significant financial risk.