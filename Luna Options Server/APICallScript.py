"""
Script to make IEXCloud API calls for Luna Options
"""
import APIKey as api
import requests


class APICalls:
    """
    Luna Options Class for API calls
    """
    def __init__(self):
        self.iex_key = api.iex_key
        self.iex_secret_key = api.iex_key_secret
        self.quand_key = api.quand_key

    def inflation_rate_call(self):
        """
        Calls and returns current inflation rate from Quandl
        """
        response = requests.get("https://www.quandl.com/api/v3/datasets/RATEINF/CPI_USA.json?api_key=" + self.quand_key)

        if response.status_code == 200:
            return response.json()
        else:
            print("Inflation Rate Called failed with the following error: ", response.status_code)

    def bond_rate_call(self):
        """
        Calls and returns bond interest rate from Quandl
        """
        response = requests.get("https://www.quandl.com/api/v3/datasets/USTREASURY/YIELD.json?api_key=" + self.quand_key)

        if response.status_code == 200:
            return response.json()
        else:
            print("Bond Rate Call failed with the following error: ", response.status_code)

    def security_quote_call(self, ticker):
        """
        Calls and returns passed security's quote from IEXCloud
        """
        response = requests.get("https://cloud.iexapis.com/stable/stock/" + ticker + "/quote?token=" + self.iex_key)

        if response.status_code == 200:
            return response.json()
        else:
            print("The following ticker failed with the following error: ", ticker, response.status_code)

    def options_expiration_call(self, ticker):
        """
        Calls and returns passed security's option expiration list from IEXCloud
        """
        response = requests.get("https://cloud.iexapis.com/stable/stock/" + ticker + "/options?token=" + self.iex_key)

        if response.status_code == 200:
            return response.json()
        else:
            print("The following ticker failed to get Options Expiration with the following error: ", ticker, response.status_code)

    def options_date_call(self, ticker, expiration):
        """
        Calls and returns passed security's option expiration list from IEXCloud
        """
        response = requests.get("https://cloud.iexapis.com/stable/stock/" + ticker + "/options/" + expiration + "?token=" + self.iex_key)

        if response.status_code == 200:
            return response.json()
        else:
            print("The following ticker for options failed with the following error: ", ticker, expiration, response.status_code)

    def historical_volatility_call(self, ticker):
        """
        Calls and returns passed security's historical volatility from IEXCloud
        """
        response = requests.get("https://cloud.iexapis.com/stable/stock/" + ticker + "/indicator/volatility/?range=1y&indicatorOnly=true&token=" + self.iex_key)

        if response.status_code == 200:
            return response.json()
        else:
            print("The following ticker for historical volatility failed with the following error: ", ticker, response.status_code)


class APIError(Exception):
    """
    Custom API Error Class
    """
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


call = APICalls()
print(call.historical_volatility_call("nflx"))
