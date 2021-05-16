"""
Implied Volatility and other Greeks Class
"""
import py_vollib.black.implied_volatility as iv
import datetime


class IV:
    """
    Class for calculating IV for an underlying security and other metrics
    """
    def __init__(self, option_price, ticker_price, strike_price, exercise_date, call_or_put):
        self._option_price = option_price
        self._ticker_price = ticker_price
        self._strike_price = strike_price
        self._exercise_date = exercise_date
        self._type = call_or_put

    def convert_datetime(self, date):
        """
        Converts to a date time object
        """
        date = date.split('-')

        return datetime.date(int(date[0]), int(date[1]), int(date[2]))

    def days_until_exp(self):
        """
        Returns the days until expiration for the option in terms of a year
        """
        today = datetime.date.today()
        expiration = self.convert_datetime(self._exercise_date)

        days_until_expiration = expiration - today

        return days_until_expiration.days/365

    def implied_volatility(self):
        """
        Returns IV for the options contract
        """
        expiration = self.days_until_exp()
        if self._type.lower() == 'call':
            flag = 'c'
        else:
            flag = 'p'

        implied_volatility = iv.implied_volatility_of_undiscounted_option_price(self._option_price, self._ticker_price, self._strike_price, expiration, flag) * 100

        return round(implied_volatility, 2)
