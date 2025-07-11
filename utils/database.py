import sqlite3
import logging
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

class Database:
    """Database utility for logging and data persistence"""
    
    def __init__(self, db_path: str = 'trading_system.db'):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize all database tables"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # System logs table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS system_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT,
                    level TEXT,
                    module TEXT,
                    message TEXT,
                    data TEXT
                )
            ''')
            
            # Agent decisions table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS agent_decisions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT,
                    symbol TEXT,
                    agent_name TEXT,
                    recommendation TEXT,
                    confidence REAL,
                    reasoning TEXT
                )
            ''')
            
            # Market data cache table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS market_data_cache (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    symbol TEXT,
                    data_type TEXT,
                    timestamp TEXT,
                    data TEXT,
                    UNIQUE(symbol, data_type)
                )
            ''')
            
            conn.commit()
            conn.close()
            logger.info("Database initialized successfully")
            
        except Exception as e:
            logger.error(f"Error initializing database: {e}")
    
    def log_system_event(self, level: str, module: str, message: str, data: Dict = None):
        """Log system events"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO system_logs (timestamp, level, module, message, data)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                datetime.now().isoformat(),
                level,
                module,
                message,
                json.dumps(data) if data else None
            ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"Error logging system event: {e}")
    
    def log_agent_decision(self, symbol: str, agent_name: str, recommendation: str, 
                          confidence: float, reasoning: List[str]):
        """Log agent decisions"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO agent_decisions (timestamp, symbol, agent_name, recommendation, confidence, reasoning)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                datetime.now().isoformat(),
                symbol,
                agent_name,
                recommendation,
                confidence,
                json.dumps(reasoning)
            ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"Error logging agent decision: {e}")
    
    def cache_market_data(self, symbol: str, data_type: str, data: Dict):
        """Cache market data"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT OR REPLACE INTO market_data_cache (symbol, data_type, timestamp, data)
                VALUES (?, ?, ?, ?)
            ''', (
                symbol,
                data_type,
                datetime.now().isoformat(),
                json.dumps(data)
            ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"Error caching market data: {e}")
    
    def get_cached_market_data(self, symbol: str, data_type: str, max_age_minutes: int = 5) -> Optional[Dict]:
        """Get cached market data if recent enough"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT timestamp, data FROM market_data_cache 
                WHERE symbol = ? AND data_type = ?
                ORDER BY timestamp DESC LIMIT 1
            ''', (symbol, data_type))
            
            result = cursor.fetchone()
            conn.close()
            
            if result:
                timestamp_str, data_str = result
                timestamp = datetime.fromisoformat(timestamp_str)
                age_minutes = (datetime.now() - timestamp).total_seconds() / 60
                
                if age_minutes <= max_age_minutes:
                    return json.loads(data_str)
            
            return None
            
        except Exception as e:
            logger.error(f"Error getting cached market data: {e}")
            return None
    
    def get_logs(self, limit: int = 100, level: str = None, module: str = None) -> List[Dict]:
        """Get system logs"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            query = 'SELECT timestamp, level, module, message, data FROM system_logs'
            params = []
            conditions = []
            
            if level:
                conditions.append('level = ?')
                params.append(level)
            
            if module:
                conditions.append('module = ?')
                params.append(module)
            
            if conditions:
                query += ' WHERE ' + ' AND '.join(conditions)
            
            query += ' ORDER BY timestamp DESC LIMIT ?'
            params.append(limit)
            
            cursor.execute(query, params)
            results = cursor.fetchall()
            conn.close()
            
            logs = []
            for row in results:
                log_entry = {
                    'timestamp': row[0],
                    'level': row[1],
                    'module': row[2],
                    'message': row[3],
                    'data': json.loads(row[4]) if row[4] else None
                }
                logs.append(log_entry)
            
            return logs
            
        except Exception as e:
            logger.error(f"Error getting logs: {e}")
            return []
    
    def get_agent_decisions(self, symbol: str = None, limit: int = 50) -> List[Dict]:
        """Get agent decisions"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            if symbol:
                cursor.execute('''
                    SELECT timestamp, symbol, agent_name, recommendation, confidence, reasoning
                    FROM agent_decisions WHERE symbol = ?
                    ORDER BY timestamp DESC LIMIT ?
                ''', (symbol, limit))
            else:
                cursor.execute('''
                    SELECT timestamp, symbol, agent_name, recommendation, confidence, reasoning
                    FROM agent_decisions
                    ORDER BY timestamp DESC LIMIT ?
                ''', (limit,))
            
            results = cursor.fetchall()
            conn.close()
            
            decisions = []
            for row in results:
                decision = {
                    'timestamp': row[0],
                    'symbol': row[1],
                    'agent_name': row[2],
                    'recommendation': row[3],
                    'confidence': row[4],
                    'reasoning': json.loads(row[5]) if row[5] else []
                }
                decisions.append(decision)
            
            return decisions
            
        except Exception as e:
            logger.error(f"Error getting agent decisions: {e}")
            return []
    
    def cleanup_old_data(self, days: int = 30):
        """Clean up old data from database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cutoff_date = datetime.now() - timedelta(days=days)
            cutoff_str = cutoff_date.isoformat()
            
            # Clean old logs
            cursor.execute('DELETE FROM system_logs WHERE timestamp < ?', (cutoff_str,))
            
            # Clean old cached data
            cursor.execute('DELETE FROM market_data_cache WHERE timestamp < ?', (cutoff_str,))
            
            # Keep agent decisions for longer (90 days)
            agent_cutoff = datetime.now() - timedelta(days=90)
            cursor.execute('DELETE FROM agent_decisions WHERE timestamp < ?', (agent_cutoff.isoformat(),))
            
            conn.commit()
            conn.close()
            
            logger.info(f"Cleaned up data older than {days} days")
            
        except Exception as e:
            logger.error(f"Error cleaning up old data: {e}")
    
    def get_database_stats(self) -> Dict:
        """Get database statistics"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            stats = {}
            
            # Count records in each table
            for table in ['system_logs', 'agent_decisions', 'market_data_cache']:
                cursor.execute(f'SELECT COUNT(*) FROM {table}')
                stats[f'{table}_count'] = cursor.fetchone()[0]
            
            conn.close()
            return stats
            
        except Exception as e:
            logger.error(f"Error getting database stats: {e}")
            return {}