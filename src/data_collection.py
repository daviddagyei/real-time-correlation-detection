import requests
import json


class FinnhubClient:
    """
    A simple client for interacting with Finnhub's API.

    Attributes:
        BASE_URL (str): The base URL for Finnhub API endpoints.
        DEFAULT_TIMEOUT (int): Default timeout in seconds for API requests.
        session (requests.Session): A persistent session used for making API calls.
        api_key (str): The API key used for authentication.
    """

    BASE_URL = 'https://api.finnhub.io/api/v1'
    DEFAULT_TIMEOUT = 60

    def __init__(self, api_key, proxies=None):
        """
        Initialize the FinnhubClient with the given API key and optional proxy settings.

        Args:
            api_key (str): Finnhub API key.
            proxies (dict, optional): A dictionary of proxy settings.
        """
        
        self.api_key = api_key
        self.session = self._init_session(api_key, proxies)

    def _init_session(self, api_key, proxies):
        """
        Initialize and configure a requests.Session for making API calls.


        Args:
            api_key (str): Finnhub API key.
            proxies (dict, optional): A dictionary of proxy settings.

        Returns:
            requests.Session: A configured session object.
        """
        session = requests.Session()
        session.headers.update({
            "Accept": "application/json",
            "User-Agent": "finnhub/python"         
        })
        session.params["token"] = api_key
        if proxies:
            session.proxies.update(proxies)
        return session
    
    def close(self):
        """
        Close the underlying HTTP session.
        """
        self.session.close()

    def __enter__(self):
        """
        Enable usage of the client as a context manager.

        Returns:
            FinnhubClient: The current instance.
        """
        return self
    
    def __exit__(self, exc_typ, exc_value, tracebak):
        """
        Ensure the HTTP session is closed when exiting a context.
        """
        self.close()

    def _get(self, endpoint, params=None):
        """
        Send a GET request to the specified Finnhub API endpoint.

        Args:
            endpoint (str): The API endpoint 
            params (dict, optional): Additional query parameters for the request.

        Returns:
            dict: Parsed JSON response from the API.

        Raises:
            Exception: If the request fails or an unexpected content type is received.
        """
        url = f"{self.BASE_URL}{endpoint}"
        response = self.session.get(url, params=params, timeout=self.DEFAULT_TIMEOUT)
        if not response.ok:
            raise Exception(f"Request failed with status {response.status_code}: {response.text}")
        content_type = response.headers.get("Content-Type", "")

        if "application/json" in content_type:
            return response.json()
        else:
            raise Exception(f"Unexpected content type: {content_type}")


    def get_quote(self, symbol):
        """
        Fetches the current stock quote for a given symbol.
        Example response keys:
          - c: current price
          - h: high price of the day
          - l: low price of the day
          - o: open price of the day
          - pc: previous close price
          - t: timestamp of the quote
        """
        return self._get("/quote", params={"symbol": symbol})

    def get_stock_candles(self, symbol, resolution, _from, to):
        """
        Fetch historical candlestick (OHLC) data for a stock.

        Args:
            symbol (str): The stock symbol 
            resolution (str): The time resolution of the candles 
            _from (int): UNIX timestamp (in seconds) for the start of the period.
            to (int): UNIX timestamp (in seconds) for the end of the period.

        Returns:
            dict: A dictionary containing candlestick data.
        """
        return self._get("/stock/candle", params={
            "symbol": symbol,
            "resolution": resolution,
            "from": _from,
            "to": to
        })

if __name__ == "__main__":
    api_key = "cvfp66pr01qtu9s63ei0cvfp66pr01qtu9s63eig"
    symbol = "AAPL"

    # Using the client as a context manager
    with FinnhubClient(api_key) as client:
        try:
            quote = client.get_quote(symbol)
            print(f"Quote for {symbol}: {quote}")
        except Exception as e:
            print("Error fetching quote:", e)
