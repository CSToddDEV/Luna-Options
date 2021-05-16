"""
Script to perform DB updates
"""
import LunaOptionsDB as db
import APICallScript as api
import SandP500List as snp
from datetime import date, datetime
import time
import schedule

class DBUpdate:
    """
    Luna Options Database Update Class
    """
    def __init__(self):
        self.db = db.LunaDB()
        self.api = api.APICalls()
        self.snp = snp
        self.market_days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday']

    def add_historical_volatility_column(self):
        """
        Adds HV column to ticker tables in lunaoptionsdb
        """
        for ticker in self.snp.ticker_list:
            self.db.add_column(ticker, '_options', 'historicalVolatility', 'varchar(32)')

    def update_price_open(self):
        """
        Pulls and updates price at open
        """
        print("Open Update Started!")
        time = None
        for ticker in self.snp.ticker_list:
            ticker = ticker.lower()
            print(ticker)
            quote = self.api.security_quote_call(ticker)

            if quote:
                self.db.truncate_table(ticker, '_dailyprice')
                self.db.truncate_table(ticker, '_dailyvolume')
                time = str(datetime.now()).split('.')
                price = quote['latestPrice']
                company = quote['companyName']
                company = company.replace('.', '')
                volume = quote['volume']
                sentiment = self.market_sentiment(ticker)
                self.db.update_daily_price(ticker, str(price), str(volume))
                self.db.update_ticker_table(ticker, '"' + company + '"', '"' + time[0] + '"', '"' + sentiment + '"')

        print("Open update finished at ", time)

    def update_price(self):
        """
        Pulls and updates price
        """
        print("Hourly Update Started!")
        time = None
        for ticker in self.snp.ticker_list:
            ticker = ticker.lower()
            quote = self.api.security_quote_call(ticker)

            if quote:
                time = str(datetime.now()).split('.')
                price = quote['latestPrice']
                company = quote['companyName']
                company.replace('.', '')
                volume = quote['volume']
                try:
                    high, low = self.db.get_high_low_historical_iv(ticker)
                except:
                    high, low = 0, 0
                sentiment = self.market_sentiment(ticker)
                self.db.update_daily_price(ticker, str(price), str(volume))
                self.db.update_ticker_table(ticker, '"' + company + '"', '"' + time[0] + '"', '"' + sentiment + '"', '"' + str(high) + '"', '"' + str(low) + '"')

        print("Hourly update finished at ", time)

    def update_end_of_day(self):
        """
        Pulls and updates volume and price at end of day
        """
        print("End of day Started!")
        for ticker in self.snp.ticker_list:
            ticker = ticker.lower()
            quote = self.api.security_quote_call(ticker)

            if quote:
                time = str(datetime.now()).split('.')
                company = quote['companyName']
                company.replace('.', '')
                price = quote['latestPrice']
                volume = quote['volume']
                sentiment = self.market_sentiment(ticker)
                try:
                    high, low = self.db.get_high_low_historical_iv(ticker)
                except:
                    high, low = 0, 0
                self.db.update_daily_price(ticker, str(price), str(volume))
                self.db.update_ticker_table(ticker, '"' + company + '"', '"' + time[0] + '"', '"' + sentiment + '"', '"' + str(high) + '"', '"' + str(low) + '"')
                self.db.update_high_and_low(ticker)
                self.db.curate_daily_high_and_low(ticker)
                self.db.update_and_curate_volume(ticker, str(volume))

        now = datetime.now()
        today = datetime.today()

        current_time = now.strftime("%H:%M:%S")
        print("End of Day finished at ", current_time, " on ", str(today))

    def update_options(self):
        """
        Pulls and updates Options
        """
        print("Options update Started!")
        # Create the bound date 2 months out
        today = date.today()
        today = str(today).replace('-', '')
        bound = int(today) + 200
        bound = str(bound)
        if bound[5] != '0' and bound[5] != '1' and bound[5] != '2' and bound[4] == '1':
            bound = int(bound) - 12

        for ticker in self.snp.ticker_list:
            ticker = ticker.lower()
            self.db.truncate_table(ticker, '_options')
            hv = self.api.historical_volatility_call(ticker)
            if hv and 'indicator' in hv.keys():
                for iv in hv['indicator'][0]:
                    if iv is not None:
                        iv = iv * 100
                        round(iv, 2)
                        self.db.update_column(ticker, '_historicalIV', 'historicalIVs', str(iv))

            option_calls = []
            exercise_dates = self.api.options_expiration_call(ticker)
            if exercise_dates:
                # Check to see which option dates are before the bound date
                for ex_date in exercise_dates:
                    if ex_date < bound:
                        option_calls.append(ex_date)

                # Get actual options data and add to database
                for ex_date in option_calls:
                    options = self.api.options_date_call(ticker, str(ex_date))
                    self.db.option_table(ticker, options)

        now = datetime.now()
        today = datetime.today()

        current_time = now.strftime("%H:%M:%S")
        print("Update Options finished at ", current_time, " on ", str(today))

    def market_sentiment(self, ticker):
        """
        Calculates and returns market sentiment based on options activity
        """
        puts = self.db.get_column_data_conditional(ticker, '_options', 'volume', 'type = "Put"')
        total_puts = 0
        for put in puts:
            total_puts += put[0]

        calls = self.db.get_column_data_conditional(ticker, '_options', 'volume', 'type = "Call"')
        total_calls = 0
        for call in calls:
            total_calls += call[0]

        if total_calls > total_puts:
            if total_puts > 0:
                percent = total_calls / total_puts
                round(percent, 2)
                return str(percent) + '% Bullish'
            else:
                return 'No Options'
        else:
            if total_calls != 0:
                percent = total_puts / total_calls
                round(percent, 2)
                return str(percent) + '% Bearish'
            else:
                return 'No Options'


    def updater(self):
        """
        The updater that runs constantly
        """

        schedule.every().monday.at("06:30").do(self.update_price_open)
        schedule.every().monday.at("07:30").do(self.update_price)
        schedule.every().monday.at("08:30").do(self.update_price)
        schedule.every().monday.at("09:30").do(self.update_price)
        schedule.every().monday.at("10:30").do(self.update_price)
        schedule.every().monday.at("11:30").do(self.update_price)
        schedule.every().monday.at("12:30").do(self.update_price)
        schedule.every().monday.at("13:15").do(self.update_end_of_day)
        schedule.every().monday.at("16:00").do(self.update_options)

        schedule.every().tuesday.at("06:30").do(self.update_price_open)
        schedule.every().tuesday.at("07:30").do(self.update_price)
        schedule.every().tuesday.at("08:30").do(self.update_price)
        schedule.every().tuesday.at("09:30").do(self.update_price)
        schedule.every().tuesday.at("10:30").do(self.update_price)
        schedule.every().tuesday.at("11:30").do(self.update_price)
        schedule.every().tuesday.at("12:30").do(self.update_price)
        schedule.every().tuesday.at("13:15").do(self.update_end_of_day)

        schedule.every().wednesday.at("06:30").do(self.update_price_open)
        schedule.every().wednesday.at("07:30").do(self.update_price)
        schedule.every().wednesday.at("08:30").do(self.update_price)
        schedule.every().wednesday.at("09:30").do(self.update_price)
        schedule.every().wednesday.at("10:30").do(self.update_price)
        schedule.every().wednesday.at("11:30").do(self.update_price)
        schedule.every().wednesday.at("12:30").do(self.update_price)
        schedule.every().wednesday.at("13:15").do(self.update_end_of_day)

        schedule.every().thursday.at("06:30").do(self.update_price_open)
        schedule.every().thursday.at("07:30").do(self.update_price)
        schedule.every().thursday.at("08:30").do(self.update_price)
        schedule.every().thursday.at("09:30").do(self.update_price)
        schedule.every().thursday.at("10:30").do(self.update_price)
        schedule.every().thursday.at("11:30").do(self.update_price)
        schedule.every().thursday.at("12:30").do(self.update_price)
        schedule.every().thursday.at("13:15").do(self.update_end_of_day)

        schedule.every().friday.at("06:30").do(self.update_price_open)
        schedule.every().friday.at("07:30").do(self.update_price)
        schedule.every().friday.at("08:30").do(self.update_price)
        schedule.every().friday.at("09:30").do(self.update_price)
        schedule.every().friday.at("10:30").do(self.update_price)
        schedule.every().friday.at("11:30").do(self.update_price)
        schedule.every().friday.at("12:30").do(self.update_price)
        schedule.every().friday.at("13:15").do(self.update_end_of_day)

        while True:
            schedule.run_pending()
            time.sleep(1)


test = DBUpdate()
# test.updater()

