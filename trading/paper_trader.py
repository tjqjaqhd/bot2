from typing import Dict, List, Optional
import logging
from datetime import datetime
import json
import sqlite3
import os

logger = logging.getLogger(__name__)

class Position:
    """Represents a trading position"""
    
    def __init__(self, symbol: str, action: str, quantity: float, price: float, timestamp: str = None):
        self.symbol = symbol
        self.action = action  # 'BUY' or 'SELL'
        self.quantity = quantity
        self.price = price
        self.timestamp = timestamp or datetime.now().isoformat()
        self.id = f"{symbol}_{self.timestamp}"
    
    def to_dict(self):
        return {
            'id': self.id,
            'symbol': self.symbol,
            'action': self.action,
            'quantity': self.quantity,
            'price': self.price,
            'timestamp': self.timestamp,
            'value': self.quantity * self.price
        }

class Portfolio:
    """Manages portfolio holdings and cash"""
    
    def __init__(self, initial_cash: float = 100000.0):
        self.cash = initial_cash
        self.initial_cash = initial_cash
        self.holdings = {}  # symbol -> quantity
        self.positions = []  # list of Position objects
    
    def add_position(self, position: Position):
        """Add a new position to the portfolio"""
        self.positions.append(position)
        
        if position.action == 'BUY':
            self.cash -= position.quantity * position.price
            self.holdings[position.symbol] = self.holdings.get(position.symbol, 0) + position.quantity
        elif position.action == 'SELL':
            self.cash += position.quantity * position.price
            self.holdings[position.symbol] = self.holdings.get(position.symbol, 0) - position.quantity
            
            # Remove symbol if quantity is 0 or negative
            if self.holdings[position.symbol] <= 0:
                del self.holdings[position.symbol]
    
    def get_holding(self, symbol: str) -> float:
        """Get current holding quantity for a symbol"""
        return self.holdings.get(symbol, 0)
    
    def can_sell(self, symbol: str, quantity: float) -> bool:
        """Check if we can sell the specified quantity"""
        return self.get_holding(symbol) >= quantity
    
    def can_buy(self, quantity: float, price: float) -> bool:
        """Check if we have enough cash to buy"""
        return self.cash >= quantity * price
    
    def to_dict(self):
        return {
            'cash': round(self.cash, 2),
            'initial_cash': self.initial_cash,
            'holdings': self.holdings,
            'total_positions': len(self.positions),
            'profit_loss': round(self.cash - self.initial_cash, 2)
        }

class PaperTrader:
    """Paper trading system for backtesting and simulation"""
    
    def __init__(self, initial_cash: float = 100000.0):
        self.portfolio = Portfolio(initial_cash)
        self.db_path = 'trading_log.db'
        self.init_database()
        logger.info(f"PaperTrader initialized with ${initial_cash:,}")
    
    def init_database(self):
        """Initialize SQLite database for logging"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Create trades table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS trades (
                    id TEXT PRIMARY KEY,
                    symbol TEXT,
                    action TEXT,
                    quantity REAL,
                    price REAL,
                    value REAL,
                    timestamp TEXT,
                    portfolio_cash REAL,
                    profit_loss REAL
                )
            ''')
            
            # Create portfolio snapshots table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS portfolio_snapshots (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT,
                    cash REAL,
                    holdings TEXT,
                    total_value REAL,
                    profit_loss REAL
                )
            ''')
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"Error initializing database: {e}")
    
    def log_trade(self, position: Position):
        """Log trade to database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO trades (id, symbol, action, quantity, price, value, timestamp, portfolio_cash, profit_loss)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                position.id,
                position.symbol,
                position.action,
                position.quantity,
                position.price,
                position.quantity * position.price,
                position.timestamp,
                self.portfolio.cash,
                self.portfolio.cash - self.portfolio.initial_cash
            ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"Error logging trade: {e}")
    
    def log_portfolio_snapshot(self):
        """Log current portfolio state"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO portfolio_snapshots (timestamp, cash, holdings, total_value, profit_loss)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                datetime.now().isoformat(),
                self.portfolio.cash,
                json.dumps(self.portfolio.holdings),
                self.portfolio.cash,  # Simplified - would need current prices for accurate total
                self.portfolio.cash - self.portfolio.initial_cash
            ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"Error logging portfolio snapshot: {e}")
    
    def execute_trade(self, symbol: str, action: str, quantity: float, price: Optional[float] = None) -> Dict:
        """Execute a paper trade"""
        try:
            action = action.upper()
            
            # Validate inputs
            if action not in ['BUY', 'SELL']:
                return {'success': False, 'error': 'Action must be BUY or SELL'}
            
            if quantity <= 0:
                return {'success': False, 'error': 'Quantity must be positive'}
            
            if price is None or price <= 0:
                return {'success': False, 'error': 'Valid price is required'}
            
            # Check if trade is possible
            if action == 'BUY':
                if not self.portfolio.can_buy(quantity, price):
                    return {
                        'success': False, 
                        'error': f'Insufficient cash. Need ${quantity * price:,.2f}, have ${self.portfolio.cash:,.2f}'
                    }
            elif action == 'SELL':
                if not self.portfolio.can_sell(symbol, quantity):
                    current_holding = self.portfolio.get_holding(symbol)
                    return {
                        'success': False, 
                        'error': f'Insufficient holdings. Need {quantity}, have {current_holding}'
                    }
            
            # Execute the trade
            position = Position(symbol, action, quantity, price)
            self.portfolio.add_position(position)
            
            # Log the trade
            self.log_trade(position)
            self.log_portfolio_snapshot()
            
            logger.info(f"Trade executed: {action} {quantity} {symbol} @ ${price}")
            
            return {
                'success': True,
                'position': position.to_dict(),
                'portfolio': self.portfolio.to_dict(),
                'message': f'Successfully {action.lower()}ed {quantity} shares of {symbol} at ${price}'
            }
            
        except Exception as e:
            logger.error(f"Error executing trade: {e}")
            return {'success': False, 'error': str(e)}
    
    def get_portfolio(self) -> Dict:
        """Get current portfolio status"""
        return {
            'portfolio': self.portfolio.to_dict(),
            'recent_positions': [pos.to_dict() for pos in self.portfolio.positions[-10:]],  # Last 10 positions
            'timestamp': datetime.now().isoformat()
        }
    
    def get_position_history(self, symbol: Optional[str] = None) -> List[Dict]:
        """Get position history, optionally filtered by symbol"""
        positions = self.portfolio.positions
        if symbol:
            positions = [pos for pos in positions if pos.symbol == symbol]
        return [pos.to_dict() for pos in positions]
    
    def calculate_performance(self) -> Dict:
        """Calculate trading performance metrics"""
        try:
            total_trades = len(self.portfolio.positions)
            if total_trades == 0:
                return {'total_trades': 0, 'profit_loss': 0, 'return_pct': 0}
            
            current_value = self.portfolio.cash
            profit_loss = current_value - self.portfolio.initial_cash
            return_pct = (profit_loss / self.portfolio.initial_cash) * 100
            
            # Simple win/loss calculation
            profitable_trades = 0
            for i in range(1, len(self.portfolio.positions)):
                pos = self.portfolio.positions[i]
                if pos.action == 'SELL':
                    # Find corresponding buy position
                    for j in range(i-1, -1, -1):
                        prev_pos = self.portfolio.positions[j]
                        if prev_pos.symbol == pos.symbol and prev_pos.action == 'BUY':
                            if pos.price > prev_pos.price:
                                profitable_trades += 1
                            break
            
            return {
                'total_trades': total_trades,
                'profit_loss': round(profit_loss, 2),
                'return_pct': round(return_pct, 2),
                'profitable_trades': profitable_trades,
                'win_rate': round((profitable_trades / (total_trades/2)) * 100, 2) if total_trades > 1 else 0
            }
            
        except Exception as e:
            logger.error(f"Error calculating performance: {e}")
            return {'error': str(e)}
    
    def reset_portfolio(self, initial_cash: float = None):
        """Reset portfolio to initial state"""
        if initial_cash is None:
            initial_cash = self.portfolio.initial_cash
        
        self.portfolio = Portfolio(initial_cash)
        logger.info(f"Portfolio reset with ${initial_cash:,}")
        return {'success': True, 'message': f'Portfolio reset with ${initial_cash:,}'}