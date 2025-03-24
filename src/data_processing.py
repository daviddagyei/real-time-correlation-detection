import time
import pandas as pd
import numpy as np
from datetime import datetime

from data_collection import FinnhubClient
from data_storage import create_table, store_data

def add_new_data(df, timestamp, symbol_data):
    """
    Append new data to the DataFrame.
    
    Args:
        df (pd.DataFrame): The existing DataFrame with price data.
        timestamp (datetime): The current timestamp.
        symbol_data (dict): Dictionary containing symbol-price pairs
    
    Returns:
        pd.DataFrame: Updated DataFrame.
    """
    new_row = {"timestamp": timestamp}
    new_row.update(symbol_data)
    return df._append(new_row, ignore_index=True)

def calculate_returns(df, symbol):
    """
    Calculate percentage returns for the specified asset.
    
    Args:
        df (pd.DataFrame): DataFrame with price data.
        symbol (str): Column name for the asset (e.g., "AAPL").
    
    Returns:
        pd.Series: Percentage returns.
    """
    return df[symbol].pct_change()

def compute_rolling_correlation(df, symbol1, symbol2, window=10):
    """
    Compute the rolling correlation between two asset return series.
    
    Args:
        df (pd.DataFrame): DataFrame containing price data.
        symbol1 (str): Column name for the first asset.
        symbol2 (str): Column name for the second asset.
        window (int): The rolling window size.
    
    Returns:
        pd.Series: Rolling correlation values.
    """
    returns1 = calculate_returns(df, symbol1)
    returns2 = calculate_returns(df, symbol2)
    return returns1.rolling(window=window).corr(returns2)

def detect_anomalies(rolling_corr, threshold=2.0):
    """
    Detect anomalies in the rolling correlation using a z-score threshold.
    
    Args:
        rolling_corr (pd.Series): The rolling correlation series.
        threshold (float): Z-score threshold for flagging an anomaly.
    
    Returns:
        bool: True if the latest rolling correlation value is an anomaly, otherwise False.
    """
    mean_corr = rolling_corr.mean()
    std_corr = rolling_corr.std()
    if std_corr == 0:
        return False
    z_score = (rolling_corr.iloc[-1] - mean_corr) / std_corr
    return abs(z_score) > threshold

def main():

    create_table()

    symbol1 = "AAPL"
    symbol2 = "MSFT"
    
    data = pd.DataFrame(columns=["timestamp", symbol1, symbol2])
    
    api_key = "cvfp66pr01qtu9s63ei0cvfp66pr01qtu9s63eig"
    

    with FinnhubClient(api_key) as client:
        while True:
            try:
                quote1 = client.get_quote(symbol1)
                quote2 = client.get_quote(symbol2)
                price1 = quote1.get("c")
                price2 = quote2.get("c")
                current_time = datetime.now()
                
    
                symbol_data = {symbol1: price1, symbol2: price2}
                data = add_new_data(data, current_time, symbol_data)

                store_data(current_time, symbol_data)
                
                print(f"New data at {current_time}: {symbol_data}")
                
                if len(data) >= 100:
                    rolling_corr = compute_rolling_correlation(data, symbol1, symbol2, window=10)
                    anomaly_flag = detect_anomalies(rolling_corr, threshold=2.0)
                    
                    print("Latest rolling correlation:", rolling_corr.iloc[-1])
                    if anomaly_flag:
                        print("Anomaly detected!")
                    else:
                        print("No anomaly detected.")
                    break
                else:
                    print(f"Collecting data... ({len(data)} points collected)")
            
            except Exception as e:
                print("Error during data fetching or processing:", e)
            
            time.sleep(1)

if __name__ == "__main__":
    main()
