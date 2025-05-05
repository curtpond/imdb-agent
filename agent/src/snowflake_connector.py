"""Snowflake connection manager."""

import snowflake.connector
from typing import Any, Dict, List, Optional
from ..config.snowflake_config import SNOWFLAKE_CONFIG

class SnowflakeConnector:
    def __init__(self):
        self.conn = None
        self.cursor = None

    def connect(self, password: str) -> None:
        """Establish connection to Snowflake."""
        self.conn = snowflake.connector.connect(
            account=SNOWFLAKE_CONFIG['account'],
            user=SNOWFLAKE_CONFIG['user'],
            password=password,
            warehouse=SNOWFLAKE_CONFIG['warehouse'],
            database=SNOWFLAKE_CONFIG['database'],
            schema=SNOWFLAKE_CONFIG['schema']
        )
        self.cursor = self.conn.cursor()

    def execute_query(self, query: str, params: Optional[Dict[str, Any]] = None) -> List[tuple]:
        """Execute a query and return results."""
        try:
            self.cursor.execute(query, params or {})
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Error executing query: {e}")
            raise

    def close(self) -> None:
        """Close the Snowflake connection."""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
