import streamlit as st
import pandas as pd
from data_storage import load_data

st.title("Real-Time Market Data Dashboard")
st.write("This dashboard displays live asset prices for AAPL and MSFT, along with their rolling correlation.")

if st.button("Refresh Data"):
    st.write("Please refresh your browser (or click the refresh icon) to reload the data.")

try:
    data = load_data(limit=100)
except Exception as e:
    st.error(f"Error loading data: {e}")
    data = pd.DataFrame()

if data.empty:
    st.write("No data available yet. Please ensure data is being collected and stored.")
else:
    data["timestamp"] = pd.to_datetime(data["timestamp"])
    data.sort_values("timestamp", inplace=True)

    st.subheader("Asset Prices")
    st.line_chart(data.set_index("timestamp")[["AAPL", "MSFT"]])
    

    if len(data) >= 10:
        aapl_returns = data["AAPL"].pct_change()
        msft_returns = data["MSFT"].pct_change()
        rolling_corr = aapl_returns.rolling(window=10).corr(msft_returns)
        
        st.subheader("Rolling Correlation (AAPL vs. MSFT)")
        st.line_chart(rolling_corr)
    else:
        st.write("Not enough data to compute rolling correlation (need at least 10 records).")
