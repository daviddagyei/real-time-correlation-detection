import requests
import time

API_KEY = "3D46OBQR2HJU9X0Y"
BASE_URL = 'https://www.alphavantage.co/query'

def fetch_stock_data(symbol):
    """Fetches intraday stock data for a given symbol"""
    params = {
        'function':'TIME_SERIES_INTRADAY',
        'symbol':symbol,
        'interval':'15min',
        'apikey':API_KEY
    }
    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        print(data)
    else:
        print("Error fetching data: ", response.status_code)
    

def main():
    symbol = 'IBM'
    while True:
        data = fetch_stock_data(symbol)
        if data:
            print("Fetched data for", symbol)

        time.sleep(60)

if __name__ == '__main__':
    main()