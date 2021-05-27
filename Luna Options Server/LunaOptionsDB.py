import mysql.connector
from SandP500List import ticker_list as snp
from APIKey import db_password as pw
import ImpliedVolatility as iv


class LunaDB:
    """
    The class for connecting to LunaOptionsDB
    """

    def __init__(self, host='localhost', db_user='server_admin', password=pw, database='lunaoptionsdb'):
        self.host = host
        self.db_user = db_user
        self.password = password
        self.database = database

    def db_connect(self):
        """
        Returns a connection to the LunaOptionsDB
        """
        lunaDB = mysql.connector.connect(
            host=self.host,
            user=self.db_user,
            password=self.password,
            database=self.database,
            auth_plugin='mysql_native_password'
        )

        return lunaDB

    def print_tables(self):
        """
        For debugging
        """
        lunaDB = self.db_connect()
        tables = lunaDB.cursor()
        tables.execute("SHOW TABLES")
        for table in tables:
            print(table)

    def select_column(self, ticker, column, table):
        """
        Selects a specfic column for a requested security and returns the results
        """
        if '.' in ticker:
            ticker = ticker.replace('.', '')
        ticker = ticker.lower()

        lunaDB = self.db_connect()
        tables = lunaDB.cursor()

        sql = "SELECT " + column + " FROM " + ticker + table
        tables.execute(sql)

        column_data = tables.fetchall()
        return column_data

    def update_tables(self, tickers=True):
        """
        Updates the tables in LunarOprtionsDB with the current tickers
        """
        lunaDB = self.db_connect()
        tables = lunaDB.cursor()

        sql = "CREATE TABLE IF NOT EXISTS top_iv_table(id INT AUTO_INCREMENT PRIMARY KEY NOT NULL, ticker varchar(" \
              "255), currentIV decimal(6, 2)) "
        tables.execute(sql)
        sql = "CREATE TABLE IF NOT EXISTS market_sentiment(id INT AUTO_INCREMENT PRIMARY KEY NOT NULL, ticker varchar(" \
              "255), sentiment decimal(6, 2), direction varchar(255)) "
        tables.execute(sql)

        if tickers:
            for ticker in snp:
                if ticker == "ALL" or ticker == "KEY":
                    continue
                if '.' in ticker:
                    ticker = ticker.replace('.', '')
                ticker = ticker.lower()
                sql = "CREATE TABLE IF NOT EXISTS " + ticker + "(id INT AUTO_INCREMENT PRIMARY KEY NOT NULL, " \
                                                               "companyName varchar(255), lastUpdated varchar(32), " \
                                                               "marketSentiment varchar(32), 52WeekHighIV decimal(6, " \
                                                               "2), 52WeekLowIV decimal(6, 2)) "
                tables.execute(sql)
                sql = "CREATE TABLE IF NOT EXISTS " + ticker + "_dailyprice(id INT AUTO_INCREMENT PRIMARY KEY NOT " \
                                                               "NULL, dailyPrice decimal(6,2)) "
                tables.execute(sql)
                sql = "CREATE TABLE IF NOT EXISTS " + ticker + "_dailyhighandlow(id INT AUTO_INCREMENT PRIMARY KEY " \
                                                               "NOT NULL, dailyHigh decimal(6,2), dailyLow decimal(6," \
                                                               "2)) "
                tables.execute(sql)
                sql = "CREATE TABLE IF NOT EXISTS " + ticker.lower() + "_dailyvolume(id INT AUTO_INCREMENT PRIMARY " \
                                                                       "KEY NOT NULL, dailyVolume int) "
                tables.execute(sql)
                sql = "CREATE TABLE IF NOT EXISTS " + ticker + "_volume(id INT AUTO_INCREMENT PRIMARY KEY NOT NULL, " \
                                                               "closeVolume int, averageVolume int, totalVolume " \
                                                               "varchar(255)) "
                tables.execute(sql)
                sql = "CREATE TABLE IF NOT EXISTS " + ticker + "_historicalIV(id INT AUTO_INCREMENT PRIMARY KEY NOT " \
                                                               "NULL, historicalIVs decimal(6,2)) "
                tables.execute(sql)
                sql = "CREATE TABLE IF NOT EXISTS " + ticker + "_options(id INT AUTO_INCREMENT PRIMARY KEY NOT NULL, " \
                                                               "execiseDate date, type varchar(5), strikePrice " \
                                                               "varchar(10), volume int, price decimal(6, 2), " \
                                                               "IV decimal(6, 2)) "
                tables.execute(sql)

    def delete_table(self, table):
        """
        Drop the requested table
        """
        table = table.lower()
        lunaDB = self.db_connect()
        tables = lunaDB.cursor()

        sql = "DROP TABLE " + table

        tables.execute(sql)

    def delete_row(self, ticker, table, column, column_id):
        """
        Deletes row for given ticker, table, and column
        """
        if '.' in ticker:
            ticker = ticker.replace('.', '')
        ticker = ticker.lower()

        lunaDB = self.db_connect()
        tables = lunaDB.cursor()

        sql = "DELETE FROM lunaoptionsdb." + ticker + table + " WHERE " + column + "=" + column_id
        tables.execute(sql)

        lunaDB.commit()

    def drop_all_tables(self):
        """
        WARNING: Will drop all tables in DB
        """
        tables_types = ['_dailyprice', '_dailyhighandlow', '_volume', '_iv', '_options', '']

        for ticker in snp:
            if ticker == "ALL" or ticker == "KEY":
                continue
            if '.' in ticker:
                ticker = ticker.replace('.', '')
            ticker = ticker.lower()
            for table in tables_types:
                self.delete_table(ticker + table)

    def update_daily_price(self, ticker, price, volume):
        """
        Updates the selected ticker for the selected daily price
        """
        if '.' in ticker:
            ticker = ticker.replace('.', '')
        ticker = ticker.lower()

        lunaDB = self.db_connect()
        tables = lunaDB.cursor()

        sql = "INSERT INTO lunaoptionsdb." + ticker + "_dailyprice(dailyPrice) VALUES (" + price + ")"
        tables.execute(sql)
        sql = "INSERT INTO lunaoptionsdb." + ticker + "_dailyvolume(dailyVolume) VALUES (" + volume + ")"
        tables.execute(sql)

        lunaDB.commit()

    def select_daily_prices(self, ticker):
        """
        Selects the daily highest and lowest prices from ticker_dailyPrices and moves them to ticker_dailyhighandlow
        """
        if '.' in ticker:
            ticker = ticker.replace('.', '')
        ticker = ticker.lower()
        lunaDB = self.db_connect()
        tables = lunaDB.cursor()

        sql = "SELECT dailyPrice FROM " + ticker + "_dailyprice"
        tables.execute(sql)

        results = tables.fetchall()
        return results

    def truncate_table(self, ticker, table):
        """
        Clears the daily price table
        """
        if '.' in ticker:
            ticker = ticker.replace('.', '')
        ticker = ticker.lower()
        lunaDB = self.db_connect()
        tables = lunaDB.cursor()

        sql = "TRUNCATE " + ticker + table
        tables.execute(sql)

        lunaDB.commit()

    def get_column_data(self, ticker, table, column):
        """
        Returns the column data for a specified ticker, table, column
        """
        if '.' in ticker:
            ticker = ticker.replace('.', '')
        ticker = ticker.lower()
        lunaDB = self.db_connect()
        tables = lunaDB.cursor()

        sql = "SELECT " + column + " FROM " + ticker + table
        tables.execute(sql)

        results = tables.fetchall()

        return results

    def get_table(self, ticker, table):
        """
        Returns the column data for a specified ticker, table, column
        """
        if '.' in ticker:
            ticker = ticker.replace('.', '')
        ticker = ticker.lower()
        lunaDB = self.db_connect()
        tables = lunaDB.cursor()

        sql = "SELECT *  FROM " + ticker + table
        tables.execute(sql)

        results = tables.fetchall()

        return results

    def get_column_names(self, ticker, table):
        """
        Returns the column names for a specific table
        """
        if '.' in ticker:
            ticker = ticker.replace('.', '')
        ticker = ticker.lower()
        lunaDB = self.db_connect()
        tables = lunaDB.cursor()

        sql = "SELECT COLUMN_NAME  FROM INFORMATION_SCHEMA.COLUMNS WHERE table_name='" + ticker + table + "'"
        tables.execute(sql)

        results = tables.fetchall()

        return results

    def get_column_data_conditional(self, ticker, table, column, condition):
        """
        Returns the column data for a specified ticker, table, column
        """
        if '.' in ticker:
            ticker = ticker.replace('.', '')
        ticker = ticker.lower()
        lunaDB = self.db_connect()
        tables = lunaDB.cursor()

        sql = "SELECT " + column + " FROM " + ticker + table + ' WHERE ' + condition
        tables.execute(sql)

        results = tables.fetchall()

        return results

    def update_column(self, ticker, table, column, value):
        """
        Updates a given column on a given table for a given ticker with a given value
        """
        if '.' in ticker:
            ticker = ticker.replace('.', '')
        ticker = ticker.lower()
        lunaDB = self.db_connect()
        tables = lunaDB.cursor()

        sql = "INSERT INTO lunaoptionsdb." + ticker + table + "(" + column + ") VALUES (" + value + ")"
        tables.execute(sql)

        lunaDB.commit()

    def update_column_conditional(self, ticker, table, column, value, cond_field, cond_value):
        """
        Updates a given column on a given table for a given ticker with a given value
        """
        if '.' in ticker:
            ticker = ticker.replace('.', '')
        ticker = ticker.lower()
        lunaDB = self.db_connect()
        tables = lunaDB.cursor()

        sql = "UPDATE lunaoptionsdb." + ticker + table + " SET " + column + "=" + value + " WHERE " + cond_field + "=" + cond_value
        tables.execute(sql)

        lunaDB.commit()

    def update_ticker_table(self, ticker, company, time, sentiment, high, low):
        """
        Updates ticker table with requested information
        """
        ticker = ticker.lower()
        self.truncate_table(ticker, '')
        self.update_column(ticker, '', 'companyName, lastUpdated, marketSentiment, 52WeekHighIV, 52WeekLowIV',
                           company + ', ' + time + ', ' + sentiment + ', ' + high + ', ' + low)

    def update_high_and_low(self, ticker):
        """
        Updates the daily high and low for the given table.
        """
        if '.' in ticker:
            ticker = ticker.replace('.', '')
        ticker = ticker.lower()
        daily_prices = self.select_daily_prices(ticker)
        high = daily_prices[0][0]
        low = daily_prices[0][0]

        for price in daily_prices:
            if price[0] > high:
                high = price[0]
            elif price[0] < low:
                low = price[0]

        self.update_column(ticker, "_dailyhighandlow", "dailyHigh, dailyLow", str(high) + ", " + str(low))

    def curate_daily_high_and_low(self, ticker):
        """
        Curates the daily high and low to ensure that there are at most 30 entries
        """
        ticker = ticker.lower()
        keys = self.select_column(ticker, "id", '_dailyhighandlow')

        low = keys[0][0]
        high = keys[-1][0]

        difference = high - low - 30

        if difference > 0:
            for i in range(difference + 1):
                self.delete_row(ticker, "_dailyhighandlow", "id", str(i + low))

    def update_and_curate_volume(self, ticker, volume):
        """
        Updates and curates the volume table for a given ticker
        """
        ticker = ticker.lower()
        keys = self.select_column(ticker, 'id', "_volume")

        if keys:
            key = keys[0][0]

            tot_vol_list = self.select_column(ticker, 'totalVolume', '_volume')
            tot_vol = tot_vol_list[0][0]

            tot_vol = int(tot_vol)
            tot_vol += int(volume)
            avg_vol = tot_vol / (key + 1)

            self.update_column(ticker, "_volume", "closeVolume, averageVolume, totalVolume",
                               str(volume) + ", " + str(avg_vol) + ", " + str(tot_vol))
            self.delete_row(ticker, "_volume", 'id', str(key))

        else:
            self.update_column(ticker, "_volume", "closeVolume, averageVolume, totalVolume",
                               str(volume) + ", " + str(volume) + ", " + str(volume))

    def update_and_curate_iv(self, ticker, iv):
        """
        Updates and curates the iv table for a given ticker
        """
        ticker = ticker.lower()
        keys = self.select_column(ticker, 'id', "_iv")
        iv = int(float(iv) // 1)

        if keys:
            key = keys[0][0]

            tot_iv_list = self.select_column(ticker, 'totalIV', '_iv')
            tot_iv = tot_iv_list[0][0]

            tot_iv = int(tot_iv)
            tot_iv += int(iv)
            avg_iv = tot_iv / (key + 1)

            self.update_column(ticker, "_iv", "dailyIV, averageIV, totalIV",
                               str(iv) + ", " + str(avg_iv) + ", " + str(tot_iv))
            self.delete_row(ticker, "_iv", 'id', str(key))

        else:
            self.update_column(ticker, "_iv", "dailyIV, averageIV, totalIV", str(iv) + ", " + str(iv) + ", " + str(iv))

    def option_table(self, ticker, option_data):
        """
        Updates options data for given ticker
        """
        ticker = ticker.lower()
        for option in option_data:
            data = option['contractDescription']
            data = data.split()

            date = data[3]
            date = date.split('/')
            iv_date = date[2] + '-' + date[1] + '-' + date[0]
            date = date[2] + date[1] + date[0]
            type = data[2]
            strike = data[4]
            volume = option['volume']
            price = option['close']
            table = self.get_column_data(ticker, '_dailyprice', 'dailyPrice')
            if table:
                current = table[-1][0]
            else:
                current = 00.00
            implied_volatility = iv.IV(float(price), float(current), float(strike), str(iv_date), str(type))
            implied_volatility_return = implied_volatility.implied_volatility()

            self.update_column(ticker, '_options', 'exerciseDate, type, strikePrice, volume, price, IV',
                               str(date) + ', "' + str(type) + '", ' + str(strike) + ', ' + str(volume) + ', ' + str(
                                   price) + ', ' + str(implied_volatility_return))

    def add_column(self, ticker, table, column, data_type):
        """
        Updates a given column on a given table for a given ticker with a given value
        """
        if '.' in ticker:
            ticker = ticker.replace('.', '')
        ticker = ticker.lower()
        lunaDB = self.db_connect()
        tables = lunaDB.cursor()

        sql = "ALTER TABLE lunaoptionsdb." + ticker + table + " ADD " + column + " " + data_type
        tables.execute(sql)

        lunaDB.commit()

    def drop_column(self, ticker, table, column):
        """
        Drops a given column on a given table for a given ticker
        """
        if '.' in ticker:
            ticker = ticker.replace('.', '')
        ticker = ticker.lower()
        lunaDB = self.db_connect()
        tables = lunaDB.cursor()

        sql = "ALTER TABLE lunaoptionsdb." + ticker + table + " DROP COLUMN " + column
        tables.execute(sql)

        lunaDB.commit()

    def get_ticker_info(self, ticker):
        """
        Gets a specific ticker's information and returns it in a dictionary.
        """
        ticker = ticker.lower()
        return_dict = {}

        table = self.get_table(ticker, '')
        return_dict['comp'] = table[0][1]
        return_dict['last_updated'] = table[0][2]
        return_dict['sentiment'] = table[0][3]
        return_dict['52WeekHighIV'] = float(table[0][4])
        return_dict['52WeekLowIV'] = float(table[0][5])

        table = self.get_column_data(ticker, '_historicalIV', 'historicalIVs')
        return_dict['current_IV'] = float(table[-1][0])

        table = self.get_column_data(ticker, '_dailyprice', 'dailyPrice')
        low = table[0]
        high = table[0]
        current = table[-1][0]

        for price in table:
            if price < low:
                low = price
            elif price > high:
                high = price
        high = high[0]
        low = low[0]
        return_dict['current'] = float(current)
        return_dict['d_high'] = float(high)
        return_dict['d_low'] = float(low)

        table = self.get_table(ticker, '_dailyhighandlow')
        table = table[::-1]
        w_high = table[0][1]
        w_low = table[0][2]
        m_high = table[0][1]
        m_low = table[0][2]

        for i in range(7):
            if i < len(table):
                if table[i][1] > w_high:
                    w_high = table[i][1]
                if table[i][2] < w_low:
                    w_low = table[i][2]

        for i in range(len(table)):
            if table[i][1] > m_high:
                m_high = table[i][1]
            if table[i][2] < m_low:
                m_low = table[i][2]
        return_dict['w_high'] = float(w_high)
        return_dict['w_low'] = float(w_low)
        return_dict['m_high'] = float(m_high)
        return_dict['m_low'] = float(m_low)

        table = self.get_column_data(ticker, '_dailyvolume', 'dailyVolume')
        return_dict['cur_vol'] = table[-1][0]

        table = self.get_column_data(ticker, '_volume', 'averageVolume')
        return_dict['avg_vol'] = table[0][0]

        return return_dict

    def get_options_contracts(self, ticker):
        """
        Gets and returns the option contracts for a ticker in dictionary form.
        """
        ticker = ticker.lower()
        return_dict = {}

        table = self.get_table(ticker, '_options')
        for contract in table:
            return_dict[str(contract[0])] = {
                'exerciseDate': str(contract[1]),
                'type': str(contract[2]),
                'strikePrice': str(contract[3]),
                'volume': str(contract[4]),
                'price': str(contract[5]),
                'IV': str(contract[6])
            }

        return return_dict

    def get_high_low_historical_iv(self, ticker):
        """
        Returns a tuple of the highest and lowest IV in a 52 week period
        """
        ticker = ticker.lower()
        data = self.get_column_data(ticker, '_historicalIV', 'historicalIVs')
        high = data[0][0]
        low = data[0][0]

        for iv in data:
            if iv[0] > high:
                high = iv[0]
            if iv[0] < low:
                low = iv[0]

        return high, low

    def update_high_iv_table(self):
        """
        Updates the high iv table in lunaoptionsDB
        """
        ivs = []

        self.truncate_table('top_iv_table', '')
        for ticker in snp:
            if '.' in ticker:
                ticker = ticker.replace('.', '')
            table = self.get_column_data(ticker, '_historicalIV', 'historicalIVs')

            if table:
                cur_iv = (table[-1][0], ticker)
                ivs.append(cur_iv)

        # Sort IVS
        self.quick_sort(ivs, 0, len(ivs) - 1)

        # Append top 50 IV securities
        counter = 0
        for i in reversed(range(len(ivs))):
            if counter > 50:
                break
            print('ticker, currentIV', str(ivs[i][1]) + ", " + str(ivs[i][0]))
            self.update_column('top_iv_table', '', 'ticker, currentIV',
                               "'" + str(ivs[i][1]) + "'" + ", " + str(ivs[i][0]))
            counter += 1

    def update_market_sentiment_table(self):
        """
        Updates the market sentiment table in lunaoptionsDB
        """
        sentiment = []

        self.truncate_table('market_sentiment', '')
        for ticker in snp:
            if '.' in ticker:
                ticker = ticker.replace('.', '')
            table = self.get_column_data(ticker, '', 'marketSentiment')

            if table:
                ticker_sentiment_split = table[-1][0].split('%')
                if len(ticker_sentiment_split) > 1:
                    ticker_sentiment_split[0] = ticker_sentiment_split[0].strip()
                    ticker_sentiment_split[1] = ticker_sentiment_split[1].strip()
                    ticker_sentiment = (float(ticker_sentiment_split[0]), ticker_sentiment_split[1], ticker)
                    sentiment.append(ticker_sentiment)

        # Sort IVS
        self.quick_sort(sentiment, 0, len(sentiment) - 1)

        # Append top 50 IV securities
        counter = 0
        for i in reversed(range(len(sentiment))):
            if counter > 50:
                break
            self.update_column('market_sentiment', '', 'ticker, sentiment, direction',
                               "'" + str(sentiment[i][2]) + "'" + ", " + str(sentiment[i][0]) + ", '" + str(sentiment[i][1]) + "'")
            counter += 1

    def quick_sort(self, array, low, high):
        """
        Quicksort method
        """
        if len(array) == 1:
            return array
        if low < high:
            mid = self.quick_sort_helper(array, low, high)

            self.quick_sort(array, low, mid - 1)
            self.quick_sort(array, mid + 1, high)

    def quick_sort_helper(self, array, low, high):
        """
        Quicksort method helper
        """
        i = (low - 1)

        pivot = array[high][0]

        for j in range(low, high):
            if array[j][0] <= pivot:
                i = i + 1
                array[i], array[j] = array[j], array[i]

        array[i + 1], array[high] = array[high], array[i + 1]

        return i + 1

    def get_top_50(self, table):
        """
        Returns the top 50 current security IV
        """
        return_data = []
        data = self.get_table(table, '')
        for point in data:
            return_data.append((str(point[1]), str(point[2])))
        return return_data

    def get_top_50_sentiment(self, table):
        """
        Returns the top 50 current security IV
        """
        return_data = []
        data = self.get_table(table, '')
        for point in data:
            return_data.append((str(point[1]), str(point[2]), str(point[3])))
        return return_data

    def update_IV_rank(self, ticker):
        """
        Updates the IV Rank column for a given ticker.
        """
        # Will update when team mate finishes services
        # IV_rank = http_get(ticker)
        # self.update_column_conditional(ticker, '', 'iv_rank', IV_rank, 'id', '1')

        pass
