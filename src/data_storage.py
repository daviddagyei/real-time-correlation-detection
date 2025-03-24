import os
import sqlite3
from datetime import datetime
import pandas as pd

DB_NAME = os.path.join(os.path.dirname(__file__), "market_data.db")

def create_table():
    """
    Create the 'prices' table in the SQLite database if it doesn't already exist.
    
    The table includes:
        - timestamp (TEXT): The timestamp of the data record.
        - AAPL (REAL): Price for AAPL.
        - MSFT (REAL): Price for MSFT.
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS prices (
            timestamp TEXT,
            AAPL REAL,
            MSFT REAL
        )
    """)
    conn.commit()
    conn.close()

def store_data(timestamp, symbol_data):
    """
    Insert a new row of market data into the database.
    
    Args:
        timestamp (datetime): The timestamp when the data was recorded.
        symbol_data (dict): Dictionary containing symbol prices, e.g., {"AAPL": price1, "MSFT": price2}.
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO prices (timestamp, AAPL, MSFT) VALUES (?, ?, ?)",
                   (timestamp.isoformat(), symbol_data.get("AAPL"), symbol_data.get("MSFT")))
    conn.commit()
    conn.close()

def load_data(limit=100):
    """
    Load the most recent 'limit' rows of market data from the database.
    
    Args:
        limit (int): Number of rows to load (default is 100).
    
    Returns:
        pd.DataFrame: A DataFrame with the loaded data, where the 'timestamp' column is parsed as datetime.
    """
    conn = sqlite3.connect(DB_NAME)
    query = f"SELECT * FROM prices ORDER BY timestamp DESC LIMIT {limit}"
    df = pd.read_sql_query(query, conn)
    conn.close()
    if not df.empty:
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        df.sort_values("timestamp", inplace=True)
    return df

if __name__ == "__main__":
    create_table()
    print("Database and table created (if not already present).")
