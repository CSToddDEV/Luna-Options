import mysql.connector
from SandP500List import ticker_list as snp
from APIKey import db_password as pw
from datetime import datetime


class LunaDB:
    """
    The class for connecting to LunaOptionsDB
    """
    def __init__(self, host='localhost', db_user='server_admin', password=pw, database='lunaoptionsdb'):
        self.host = host
        self.db_user = db_user
        self.password = password
        self.database = database

    def DB_connect(self):
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
        lunaDB = self.DB_connect()
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

        lunaDB = self.DB_connect()
        tables = lunaDB.cursor()

        sql = "SELECT " + column + " FROM " + ticker + table
        tables.execute(sql)

        column_data = tables.fetchall()
        return column_data

    def update_tables(self):
        """
        Updates the tables in LunarOprtionsDB with the current tickers
        """
        lunaDB = self.DB_connect()
        tables = lunaDB.cursor()

        for ticker in snp:
            if ticker == "ALL" or ticker == "KEY":
                continue
            if '.' in ticker:
                ticker = ticker.replace('.', '')
            ticker = ticker.lower()
            sql = "CREATE TABLE IF NOT EXISTS " + ticker + "(id INT AUTO_INCREMENT PRIMARY KEY NOT NULL, companyName varchar(255), lastUpdated varchar(32), marketSentiment varchar(32))"
            tables.execute(sql)
            sql = "CREATE TABLE IF NOT EXISTS " + ticker + "_dailyprice(id INT AUTO_INCREMENT PRIMARY KEY NOT NULL, dailyPrice decimal(6,2))"
            tables.execute(sql)
            sql = "CREATE TABLE IF NOT EXISTS " + ticker + "_dailyhighandlow(id INT AUTO_INCREMENT PRIMARY KEY NOT NULL, dailyHigh decimal(6,2), dailyLow decimal(6,2))"
            tables.execute(sql)
            sql = "CREATE TABLE IF NOT EXISTS " + ticker + "_dailyvolume(id INT AUTO_INCREMENT PRIMARY KEY NOT NULL, dailyVolume int)"
            tables.execute(sql)
            sql = "CREATE TABLE IF NOT EXISTS " + ticker + "_volume(id INT AUTO_INCREMENT PRIMARY KEY NOT NULL, closeVolume int, averageVolume int, totalVolume varchar(255))"
            tables.execute(sql)
            sql = "CREATE TABLE IF NOT EXISTS " + ticker + "_iv(id INT AUTO_INCREMENT PRIMARY KEY NOT NULL, dailyIV decimal(6,2), averageIV decimal(6,2), totalIV varchar(255))"
            tables.execute(sql)
            sql = "CREATE TABLE IF NOT EXISTS " + ticker + "_options(id INT AUTO_INCREMENT PRIMARY KEY NOT NULL, exerciseDate date, type varchar(5), strikePrice varchar(10), volume int)"
            tables.execute(sql)

    def delete_table(self, table):
        """
        Drop the requested table
        """
        table = table.lower()
        lunaDB = self.DB_connect()
        tables = lunaDB.cursor()

        sql = "DROP TABLE " + table

        tables.execute(sql)

    def delete_row(self, ticker, table, column, id):
        """
        Deletes row for given ticker, table, and column
        """
        if '.' in ticker:
            ticker = ticker.replace('.', '')
        ticker = ticker.lower()

        lunaDB = self.DB_connect()
        tables = lunaDB.cursor()

        sql = "DELETE FROM lunaoptionsdb." + ticker + table + " WHERE " + column + "=" + id
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
            for type in tables_types:
                self.delete_table(ticker + type)

    def update_daily_price(self, ticker, price, volume):
        """
        Updates the selected ticker for the selected daily price
        """
        if '.' in ticker:
            ticker = ticker.replace('.', '')
        ticker = ticker.lower()

        lunaDB = self.DB_connect()
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
        lunaDB = self.DB_connect()
        tables = lunaDB.cursor()

        sql = "SELECT dailyPrice FROM " + ticker + "_dailyprice"
        tables.execute(sql)

        results =tables.fetchall()
        return results

    def truncate_table(self, ticker, table):
        """
        Clears the daily price table
        """
        if '.' in ticker:
            ticker = ticker.replace('.', '')
        ticker = ticker.lower()
        lunaDB = self.DB_connect()
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
        lunaDB = self.DB_connect()
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
        lunaDB = self.DB_connect()
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
        lunaDB = self.DB_connect()
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
        lunaDB = self.DB_connect()
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
        lunaDB = self.DB_connect()
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
        lunaDB = self.DB_connect()
        tables = lunaDB.cursor()

        sql = "UPDATE lunaoptionsdb." + ticker + table + " SET " + column + "=" + value + " WHERE " + cond_field + "=" + cond_value
        tables.execute(sql)

        lunaDB.commit()

    def update_ticker_table(self, ticker, company, time, sentiment):
        """
        Updates ticker table with requested information
        """
        ticker = ticker.lower()
        self.truncate_table(ticker, '')
        self.update_column(ticker, '', 'companyName, lastUpdated, marketSentiment', company + ', ' + time + ', ' + sentiment)

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
            avg_vol = tot_vol/(key + 1)

            self.update_column(ticker, "_volume", "closeVolume, averageVolume, totalVolume", str(volume) + ", " + str(avg_vol) + ", " + str(tot_vol))
            self.delete_row(ticker, "_volume", 'id', str(key))

        else:
            self.update_column(ticker, "_volume", "closeVolume, averageVolume, totalVolume", str(volume) + ", " + str(volume) + ", " + str(volume))

    def update_and_curate_iv(self, ticker, iv):
        """
        Updates and curates the iv table for a given ticker
        """
        ticker = ticker.lower()
        keys = self.select_column(ticker, 'id', "_iv")
        iv = int(float(iv)//1)

        if keys:
            key = keys[0][0]

            tot_iv_list = self.select_column(ticker, 'totalIV', '_iv')
            tot_iv = tot_iv_list[0][0]

            tot_iv = int(tot_iv)
            tot_iv += int(iv)
            avg_iv = tot_iv/(key + 1)

            self.update_column(ticker, "_iv", "dailyIV, averageIV, totalIV", str(iv) + ", " + str(avg_iv) + ", " + str(tot_iv))
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
            date = date[2] + date[1] + date[0]
            type = data[2]
            strike = data[4]
            volume = option['volume']

            self.update_column(ticker, '_options', 'exerciseDate, type, strikePrice, volume', str(date) + ', "' + str(type) + '", ' + str(strike) + ', ' + str(volume))

    def add_column(self, ticker, table, column, data_type):
        """
        Updates a given column on a given table for a given ticker with a given value
        """
        if '.' in ticker:
            ticker = ticker.replace('.', '')
        ticker = ticker.lower()
        lunaDB = self.DB_connect()
        tables = lunaDB.cursor()

        sql = "ALTER TABLE lunaoptionsdb." + ticker + table + " ADD " + column + " " + data_type
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

        table = self.get_table(ticker, '_options')
        return_dict['hist_volatility'] = table[0][5]

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

        table = self.get_table(ticker, '')
        for contract in table:
            if contract[5] != 'Null':
                print('NULL CONTRACT HV')
                pass
            return_dict[contract[0]] = {
                'exerciseDate': contract[1],
                'type': contract[2],
                'strikePrice': contract[3],
                'volume': contract[4]
            }

        return return_dict


# test = LunaDB()
# test.add_column('nflx', '', 'historicalVolatility', 'varchar(32)')

# test.drop_all_tables()
# test.update_tables()

# test_data = [{'ask': 10.4, 'bid': 8.85, 'cfiCode': 'OCAXXX', 'close': 9.29, 'closingPrice': 9.29, 'contractDescription': 'NFLX Option Call 28/05/2021 520 on Ordinary Shares', 'contractName': 'Netflix', 'contractSize': 100, 'currency': 'USD', 'exchangeCode': None, 'exchangeMIC': None, 'exerciseStyle': 'A', 'expirationDate': '20210528', 'figi': 'BBG00ZWHCD25', 'high': 9.29, 'isAdjusted': False, 'lastTradeDate': '2021-04-29', 'lastTradeTime': '21:57:47', 'lastUpdated': '2021-04-29', 'low': 7.65, 'marginPrice': 0, 'open': 7.75, 'openInterest': 129, 'settlementPrice': 0, 'side': 'call', 'strikePrice': 520, 'symbol': 'NFLX', 'type': 'equity', 'volume': 8, 'id': 'NFLX20210528C00520000', 'key': 'NFLX', 'subkey': 'NFLX20210528C00520000', 'date': 1619654400000, 'updated': 1619791798000}, {'ask': 9.2, 'bid': 8.05, 'cfiCode': 'OPAXXX', 'close': 12.22, 'closingPrice': 12.22, 'contractDescription': 'NFLX Option Put 28/05/2021 495 on Ordinary Shares', 'contractName': 'Netflix', 'contractSize': 100, 'currency': 'USD', 'exchangeCode': None, 'exchangeMIC': None, 'exerciseStyle': 'A', 'expirationDate': '20210528', 'figi': 'BBG00ZWHC247', 'high': 12.22, 'isAdjusted': False, 'lastTradeDate': '2021-04-29', 'lastTradeTime': '17:36:24', 'lastUpdated': '2021-04-29', 'low': 10.98, 'marginPrice': 0, 'open': 11.25, 'openInterest': 289, 'settlementPrice': 0, 'side': 'put', 'strikePrice': 495, 'symbol': 'NFLX', 'type': 'equity', 'volume': 3, 'id': 'NFLX20210528P00495000', 'key': 'NFLX', 'subkey': 'NFLX20210528P00495000', 'date': 1619654400000, 'updated': 1619798725000}, {'ask': 21.6, 'bid': 19.5, 'cfiCode': 'OPAXXX', 'close': 24.75, 'closingPrice': 24.75, 'contractDescription': 'NFLX Option Put 28/05/2021 520 on Ordinary Shares', 'contractName': 'Netflix', 'contractSize': 100, 'currency': 'USD', 'exchangeCode': None, 'exchangeMIC': None, 'exerciseStyle': 'A', 'expirationDate': '20210528', 'figi': 'BBG00ZWHCD34', 'high': 24.75, 'isAdjusted': False, 'lastTradeDate': '2021-04-29', 'lastTradeTime': '16:47:04', 'lastUpdated': '2021-04-29', 'low': 24.23, 'marginPrice': 0, 'open': 24.23, 'openInterest': 70, 'settlementPrice': 0, 'side': 'put', 'strikePrice': 520, 'symbol': 'NFLX', 'type': 'equity', 'volume': 3, 'id': 'NFLX20210528P00520000', 'key': 'NFLX', 'subkey': 'NFLX20210528P00520000', 'date': 1619654400000, 'updated': 1619798726000}, {'ask': 8.95, 'bid': 8, 'cfiCode': 'OCAXXX', 'close': 6.99, 'closingPrice': 6.99, 'contractDescription': 'NFLX Option Call 28/05/2021 522.5 on Ordinary Shares', 'contractName': 'Netflix', 'contractSize': 100, 'currency': 'USD', 'exchangeCode': None, 'exchangeMIC': None, 'exerciseStyle': 'A', 'expirationDate': '20210528', 'figi': 'BBG00ZWHCF57', 'high': 6.99, 'isAdjusted': False, 'lastTradeDate': '2021-04-29', 'lastTradeTime': '16:58:02', 'lastUpdated': '2021-04-29', 'low': 6.99, 'marginPrice': 0, 'open': 6.99, 'openInterest': 43, 'settlementPrice': 0, 'side': 'call', 'strikePrice': 522.5, 'symbol': 'NFLX', 'type': 'equity', 'volume': 1, 'id': 'NFLX20210528C00522500', 'key': 'NFLX', 'subkey': 'NFLX20210528C00522500', 'date': 1619654400000, 'updated': 1619798726000}, {'ask': 8.55, 'bid': 7.2, 'cfiCode': 'OCAXXX', 'close': 7.25, 'closingPrice': 7.25, 'contractDescription': 'NFLX Option Call 28/05/2021 525 on Ordinary Shares', 'contractName': 'Netflix', 'contractSize': 100, 'currency': 'USD', 'exchangeCode': None, 'exchangeMIC': None, 'exerciseStyle': 'A', 'expirationDate': '20210528', 'figi': 'BBG00ZWHCG91', 'high': 7.25, 'isAdjusted': False, 'lastTradeDate': '2021-04-29', 'lastTradeTime': '21:45:12', 'lastUpdated': '2021-04-29', 'low': 5.95, 'marginPrice': 0, 'open': 5.95, 'openInterest': 104, 'settlementPrice': 0, 'side': 'call', 'strikePrice': 525, 'symbol': 'NFLX', 'type': 'equity', 'volume': 6, 'id': 'NFLX20210528C00525000', 'key': 'NFLX', 'subkey': 'NFLX20210528C00525000', 'date': 1619654400000, 'updated': 1619798725000}, {'ask': 8.35, 'bid': 7.15, 'cfiCode': 'OPAXXX', 'close': 10.85, 'closingPrice': 10.85, 'contractDescription': 'NFLX Option Put 28/05/2021 492.5 on Ordinary Shares', 'contractName': 'Netflix', 'contractSize': 100, 'currency': 'USD', 'exchangeCode': None, 'exchangeMIC': None, 'exerciseStyle': 'A', 'expirationDate': '20210528', 'figi': '', 'high': 10.85, 'isAdjusted': False, 'lastTradeDate': '2021-04-29', 'lastTradeTime': '17:34:39', 'lastUpdated': '2021-04-29', 'low': 9.27, 'marginPrice': 0, 'open': 9.27, 'openInterest': 12, 'settlementPrice': 0, 'side': 'put', 'strikePrice': 492.5, 'symbol': 'NFLX', 'type': 'equity', 'volume': 3, 'id': 'NFLX20210528P00492500', 'key': 'NFLX', 'subkey': 'NFLX20210528P00492500', 'date': 1619654400000, 'updated': 1619798726000}, {'ask': 23.1, 'bid': 21.4, 'cfiCode': 'OCAXXX', 'close': 21, 'closingPrice': 21, 'contractDescription': 'NFLX Option Call 28/05/2021 495 on Ordinary Shares', 'contractName': 'Netflix', 'contractSize': 100, 'currency': 'USD', 'exchangeCode': None, 'exchangeMIC': None, 'exerciseStyle': 'A', 'expirationDate': '20210528', 'figi': 'BBG00ZWHC238', 'high': 21, 'isAdjusted': False, 'lastTradeDate': '2021-04-29', 'lastTradeTime': '21:15:06', 'lastUpdated': '2021-04-29', 'low': 20.85, 'marginPrice': 0, 'open': 20.85, 'openInterest': 36, 'settlementPrice': 0, 'side': 'call', 'strikePrice': 495, 'symbol': 'NFLX', 'type': 'equity', 'volume': 2, 'id': 'NFLX20210528C00495000', 'key': 'NFLX', 'subkey': 'NFLX20210528C00495000', 'date': 1619654400000, 'updated': 1619798725000}, {'ask': 3.35, 'bid': 2.9, 'cfiCode': 'OPAXXX', 'close': 3.19, 'closingPrice': 3.19, 'contractDescription': 'NFLX Option Put 28/05/2021 470 on Ordinary Shares', 'contractName': 'Netflix', 'contractSize': 100, 'currency': 'USD', 'exchangeCode': None, 'exchangeMIC': None, 'exerciseStyle': 'A', 'expirationDate': '20210528', 'figi': 'BBG00ZZG94K8', 'high': 4.48, 'isAdjusted': False, 'lastTradeDate': '2021-04-29', 'lastTradeTime': '21:37:21', 'lastUpdated': '2021-04-29', 'low': 3.19, 'marginPrice': 0, 'open': 3.65, 'openInterest': 815, 'settlementPrice': 0, 'side': 'put', 'strikePrice': 470, 'symbol': 'NFLX', 'type': 'equity', 'volume': 22, 'id': 'NFLX20210528P00470000', 'key': 'NFLX', 'subkey': 'NFLX20210528P00470000', 'date': 1619654400000, 'updated': 1619798726000}, {'ask': 6.5, 'bid': 5.85, 'cfiCode': 'OCAXXX', 'close': 6.2, 'closingPrice': 6.2, 'contractDescription': 'NFLX Option Call 28/05/2021 530 on Ordinary Shares', 'contractName': 'Netflix', 'contractSize': 100, 'currency': 'USD', 'exchangeCode': None, 'exchangeMIC': None, 'exerciseStyle': 'A', 'expirationDate': '20210528', 'figi': 'BBG00ZWHCJJ4', 'high': 6.2, 'isAdjusted': False, 'lastTradeDate': '2021-04-29', 'lastTradeTime': '21:58:50', 'lastUpdated': '2021-04-29', 'low': 5.15, 'marginPrice': 0, 'open': 5.15, 'openInterest': 181, 'settlementPrice': 0, 'side': 'call', 'strikePrice': 530, 'symbol': 'NFLX', 'type': 'equity', 'volume': 2, 'id': 'NFLX20210528C00530000', 'key': 'NFLX', 'subkey': 'NFLX20210528C00530000', 'date': 1619654400000, 'updated': 1619798726000}, {'ask': 1.71, 'bid': 1.37, 'cfiCode': 'OPAXXX', 'close': 1.67, 'closingPrice': 1.67, 'contractDescription': 'NFLX Option Put 28/05/2021 450 on Ordinary Shares', 'contractName': 'Netflix', 'contractSize': 100, 'currency': 'USD', 'exchangeCode': None, 'exchangeMIC': None, 'exerciseStyle': 'A', 'expirationDate': '20210528', 'figi': 'BBG00ZZG9035', 'high': 2.1, 'isAdjusted': False, 'lastTradeDate': '2021-04-29', 'lastTradeTime': '21:44:40', 'lastUpdated': '2021-04-29', 'low': 1.6, 'marginPrice': 0, 'open': 1.66, 'openInterest': 598, 'settlementPrice': 0, 'side': 'put', 'strikePrice': 450, 'symbol': 'NFLX', 'type': 'equity', 'volume': 17, 'id': 'NFLX20210528P00450000', 'key': 'NFLX', 'subkey': 'NFLX20210528P00450000', 'date': 1619654400000, 'updated': 1619798726000}, {'ask': 0.93, 'bid': 0.62, 'cfiCode': 'OCAXXX', 'close': 0.77, 'closingPrice': 0.77, 'contractDescription': 'NFLX Option Call 28/05/2021 585 on Ordinary Shares', 'contractName': 'Netflix', 'contractSize': 100, 'currency': 'USD', 'exchangeCode': None, 'exchangeMIC': None, 'exerciseStyle': 'A', 'expirationDate': '20210528', 'figi': 'BBG00ZWHD246', 'high': 0.77, 'isAdjusted': False, 'lastTradeDate': '2021-04-29', 'lastTradeTime': '21:57:29', 'lastUpdated': '2021-04-29', 'low': 0.77, 'marginPrice': 0, 'open': 0.77, 'openInterest': 76, 'settlementPrice': 0, 'side': 'call', 'strikePrice': 585, 'symbol': 'NFLX', 'type': 'equity', 'volume': 1, 'id': 'NFLX20210528C00585000', 'key': 'NFLX', 'subkey': 'NFLX20210528C00585000', 'date': 1619654400000, 'updated': 1619798726000}, {'ask': 15.75, 'bid': 14, 'cfiCode': 'OPAXXX', 'close': 14.94, 'closingPrice': 14.94, 'contractDescription': 'NFLX Option Put 28/05/2021 510 on Ordinary Shares', 'contractName': 'Netflix', 'contractSize': 100, 'currency': 'USD', 'exchangeCode': None, 'exchangeMIC': None, 'exerciseStyle': 'A', 'expirationDate': '20210528', 'figi': 'BBG00ZWHC7P3', 'high': 19.16, 'isAdjusted': False, 'lastTradeDate': '2021-04-29', 'lastTradeTime': '21:55:36', 'lastUpdated': '2021-04-29', 'low': 14.94, 'marginPrice': 0, 'open': 17.92, 'openInterest': 115, 'settlementPrice': 0, 'side': 'put', 'strikePrice': 510, 'symbol': 'NFLX', 'type': 'equity', 'volume': 5, 'id': 'NFLX20210528P00510000', 'key': 'NFLX', 'subkey': 'NFLX20210528P00510000', 'date': 1619654400000, 'updated': 1619798725000}, {'ask': 1.19, 'bid': 0.9, 'cfiCode': 'OPAXXX', 'close': 1.09, 'closingPrice': 1.09, 'contractDescription': 'NFLX Option Put 28/05/2021 435 on Ordinary Shares', 'contractName': 'Netflix', 'contractSize': 100, 'currency': 'USD', 'exchangeCode': None, 'exchangeMIC': None, 'exerciseStyle': 'A', 'expirationDate': '20210528', 'figi': 'BBG00ZZG8WS9', 'high': 1.25, 'isAdjusted': False, 'lastTradeDate': '2021-04-29', 'lastTradeTime': '21:09:28', 'lastUpdated': '2021-04-29', 'low': 1.09, 'marginPrice': 0, 'open': 1.25, 'openInterest': 36, 'settlementPrice': 0, 'side': 'put', 'strikePrice': 435, 'symbol': 'NFLX', 'type': 'equity', 'volume': 3, 'id': 'NFLX20210528P00435000', 'key': 'NFLX', 'subkey': 'NFLX20210528P00435000', 'date': 1619654400000, 'updated': 1619798726000}, {'ask': 15.4, 'bid': 14.25, 'cfiCode': 'OCAXXX', 'close': 14.85, 'closingPrice': 14.85, 'contractDescription': 'NFLX Option Call 28/05/2021 507.5 on Ordinary Shares', 'contractName': 'Netflix', 'contractSize': 100, 'currency': 'USD', 'exchangeCode': None, 'exchangeMIC': None, 'exerciseStyle': 'A', 'expirationDate': '20210528', 'figi': 'BBG00ZWHC6J2', 'high': 14.85, 'isAdjusted': False, 'lastTradeDate': '2021-04-29', 'lastTradeTime': '21:38:55', 'lastUpdated': '2021-04-29', 'low': 13, 'marginPrice': 0, 'open': 13, 'openInterest': 108, 'settlementPrice': 0, 'side': 'call', 'strikePrice': 507.5, 'symbol': 'NFLX', 'type': 'equity', 'volume': 3, 'id': 'NFLX20210528C00507500', 'key': 'NFLX', 'subkey': 'NFLX20210528C00507500', 'date': 1619654400000, 'updated': 1619798726000}, {'ask': 10.1, 'bid': 9.2, 'cfiCode': 'OPAXXX', 'close': 11.24, 'closingPrice': 11.24, 'contractDescription': 'NFLX Option Put 28/05/2021 497.5 on Ordinary Shares', 'contractName': 'Netflix', 'contractSize': 100, 'currency': 'USD', 'exchangeCode': None, 'exchangeMIC': None, 'exerciseStyle': 'A', 'expirationDate': '20210528', 'figi': '', 'high': 11.24, 'isAdjusted': False, 'lastTradeDate': '2021-04-29', 'lastTradeTime': '15:56:35', 'lastUpdated': '2021-04-29', 'low': 11.24, 'marginPrice': 0, 'open': 11.24, 'openInterest': 24, 'settlementPrice': 0, 'side': 'put', 'strikePrice': 497.5, 'symbol': 'NFLX', 'type': 'equity', 'volume': 1, 'id': 'NFLX20210528P00497500', 'key': 'NFLX', 'subkey': 'NFLX20210528P00497500', 'date': 1619654400000, 'updated': 1619798725000}, {'ask': 0.81, 'bid': 0.53, 'cfiCode': 'OPAXXX', 'close': 0.7, 'closingPrice': 0.7, 'contractDescription': 'NFLX Option Put 28/05/2021 410 on Ordinary Shares', 'contractName': 'Netflix', 'contractSize': 100, 'currency': 'USD', 'exchangeCode': None, 'exchangeMIC': None, 'exerciseStyle': 'A', 'expirationDate': '20210528', 'figi': 'BBG00ZZG8Q75', 'high': 0.7, 'isAdjusted': False, 'lastTradeDate': '2021-04-29', 'lastTradeTime': '17:24:35', 'lastUpdated': '2021-04-29', 'low': 0.7, 'marginPrice': 0, 'open': 0.7, 'openInterest': 60, 'settlementPrice': 0, 'side': 'put', 'strikePrice': 410, 'symbol': 'NFLX', 'type': 'equity', 'volume': 1, 'id': 'NFLX20210528P00410000', 'key': 'NFLX', 'subkey': 'NFLX20210528P00410000', 'date': 1619654400000, 'updated': 1619798726000}, {'ask': 1.98, 'bid': 1.62, 'cfiCode': 'OPAXXX', 'close': 1.91, 'closingPrice': 1.91, 'contractDescription': 'NFLX Option Put 28/05/2021 455 on Ordinary Shares', 'contractName': 'Netflix', 'contractSize': 100, 'currency': 'USD', 'exchangeCode': None, 'exchangeMIC': None, 'exerciseStyle': 'A', 'expirationDate': '20210528', 'figi': 'BBG00ZZG9179', 'high': 2.67, 'isAdjusted': False, 'lastTradeDate': '2021-04-29', 'lastTradeTime': '21:28:43', 'lastUpdated': '2021-04-29', 'low': 1.91, 'marginPrice': 0, 'open': 2.17, 'openInterest': 201, 'settlementPrice': 0, 'side': 'put', 'strikePrice': 455, 'symbol': 'NFLX', 'type': 'equity', 'volume': 19, 'id': 'NFLX20210528P00455000', 'key': 'NFLX', 'subkey': 'NFLX20210528P00455000', 'date': 1619654400000, 'updated': 1619798725000}, {'ask': 4.1, 'bid': 3.45, 'cfiCode': 'OPAXXX', 'close': 4.02, 'closingPrice': 4.02, 'contractDescription': 'NFLX Option Put 28/05/2021 475 on Ordinary Shares', 'contractName': 'Netflix', 'contractSize': 100, 'currency': 'USD', 'exchangeCode': None, 'exchangeMIC': None, 'exerciseStyle': 'A', 'expirationDate': '20210528', 'figi': 'BBG00ZZG95N2', 'high': 5.32, 'isAdjusted': False, 'lastTradeDate': '2021-04-29', 'lastTradeTime': '21:34:20', 'lastUpdated': '2021-04-29', 'low': 4.02, 'marginPrice': 0, 'open': 4.48, 'openInterest': 756, 'settlementPrice': 0, 'side': 'put', 'strikePrice': 475, 'symbol': 'NFLX', 'type': 'equity', 'volume': 51, 'id': 'NFLX20210528P00475000', 'key': 'NFLX', 'subkey': 'NFLX20210528P00475000', 'date': 1619654400000, 'updated': 1619798726000}, {'ask': 0.32, 'bid': 0.07, 'cfiCode': 'OCAXXX', 'close': 0.11, 'closingPrice': 0.11, 'contractDescription': 'NFLX Option Call 28/05/2021 670 on Ordinary Shares', 'contractName': 'Netflix', 'contractSize': 100, 'currency': 'USD', 'exchangeCode': None, 'exchangeMIC': None, 'exerciseStyle': 'A', 'expirationDate': '20210528', 'figi': 'BBG00ZZG9C57', 'high': 0.11, 'isAdjusted': False, 'lastTradeDate': '2021-04-29', 'lastTradeTime': '15:30:18', 'lastUpdated': '2021-04-29', 'low': 0.11, 'marginPrice': 0, 'open': 0.11, 'openInterest': 23, 'settlementPrice': 0, 'side': 'call', 'strikePrice': 670, 'symbol': 'NFLX', 'type': 'equity', 'volume': 1, 'id': 'NFLX20210528C00670000', 'key': 'NFLX', 'subkey': 'NFLX20210528C00670000', 'date': 1619654400000, 'updated': 1619798726000}, {'ask': 0.35, 'bid': 0.09, 'cfiCode': 'OCAXXX', 'close': 0.15, 'closingPrice': 0.15, 'contractDescription': 'NFLX Option Call 28/05/2021 660 on Ordinary Shares', 'contractName': 'Netflix', 'contractSize': 100, 'currency': 'USD', 'exchangeCode': None, 'exchangeMIC': None, 'exerciseStyle': 'A', 'expirationDate': '20210528', 'figi': 'BBG00ZZG9B13', 'high': 0.15, 'isAdjusted': False, 'lastTradeDate': '2021-04-29', 'lastTradeTime': '15:30:18', 'lastUpdated': '2021-04-29', 'low': 0.15, 'marginPrice': 0, 'open': 0.15, 'openInterest': 134, 'settlementPrice': 0, 'side': 'call', 'strikePrice': 660, 'symbol': 'NFLX', 'type': 'equity', 'volume': 1, 'id': 'NFLX20210528C00660000', 'key': 'NFLX', 'subkey': 'NFLX20210528C00660000', 'date': 1619654400000, 'updated': 1619798726000}, {'ask': 52.55, 'bid': 49.7, 'cfiCode': 'OCAXXX', 'close': 49.88, 'closingPrice': 49.88, 'contractDescription': 'NFLX Option Call 28/05/2021 460 on Ordinary Shares', 'contractName': 'Netflix', 'contractSize': 100, 'currency': 'USD', 'exchangeCode': None, 'exchangeMIC': None, 'exerciseStyle': 'A', 'expirationDate': '20210528', 'figi': 'BBG00ZZG9295', 'high': 49.88, 'isAdjusted': False, 'lastTradeDate': '2021-04-29', 'lastTradeTime': '15:30:18', 'lastUpdated': '2021-04-29', 'low': 49.88, 'marginPrice': 0, 'open': 49.88, 'openInterest': 2, 'settlementPrice': 0, 'side': 'call', 'strikePrice': 460, 'symbol': 'NFLX', 'type': 'equity', 'volume': 1, 'id': 'NFLX20210528C00460000', 'key': 'NFLX', 'subkey': 'NFLX20210528C00460000', 'date': 1619654400000, 'updated': 1619798726000}, {'ask': 6.75, 'bid': 5.8, 'cfiCode': 'OPAXXX', 'close': 6.58, 'closingPrice': 6.58, 'contractDescription': 'NFLX Option Put 28/05/2021 487.5 on Ordinary Shares', 'contractName': 'Netflix', 'contractSize': 100, 'currency': 'USD', 'exchangeCode': None, 'exchangeMIC': None, 'exerciseStyle': 'A', 'expirationDate': '20210528', 'figi': '', 'high': 9, 'isAdjusted': False, 'lastTradeDate': '2021-04-29', 'lastTradeTime': '21:44:03', 'lastUpdated': '2021-04-29', 'low': 6.58, 'marginPrice': 0, 'open': 7.5, 'openInterest': 45, 'settlementPrice': 0, 'side': 'put', 'strikePrice': 487.5, 'symbol': 'NFLX', 'type': 'equity', 'volume': 9, 'id': 'NFLX20210528P00487500', 'key': 'NFLX', 'subkey': 'NFLX20210528P00487500', 'date': 1619654400000, 'updated': 1619798726000}, {'ask': 1.4, 'bid': 1.02, 'cfiCode': 'OCAXXX', 'close': 1.1, 'closingPrice': 1.1, 'contractDescription': 'NFLX Option Call 28/05/2021 570 on Ordinary Shares', 'contractName': 'Netflix', 'contractSize': 100, 'currency': 'USD', 'exchangeCode': None, 'exchangeMIC': None, 'exerciseStyle': 'A', 'expirationDate': '20210528', 'figi': 'BBG00ZWHCYT0', 'high': 1.1, 'isAdjusted': False, 'lastTradeDate': '2021-04-29', 'lastTradeTime': '21:24:14', 'lastUpdated': '2021-04-29', 'low': 1.1, 'marginPrice': 0, 'open': 1.1, 'openInterest': 167, 'settlementPrice': 0, 'side': 'call', 'strikePrice': 570, 'symbol': 'NFLX', 'type': 'equity', 'volume': 3, 'id': 'NFLX20210528C00570000', 'key': 'NFLX', 'subkey': 'NFLX20210528C00570000', 'date': 1619654400000, 'updated': 1619798725000}, {'ask': 18.75, 'bid': 16.9, 'cfiCode': 'OCAXXX', 'close': 17.92, 'closingPrice': 17.92, 'contractDescription': 'NFLX Option Call 28/05/2021 502.5 on Ordinary Shares', 'contractName': 'Netflix', 'contractSize': 100, 'currency': 'USD', 'exchangeCode': None, 'exchangeMIC': None, 'exerciseStyle': 'A', 'expirationDate': '20210528', 'figi': 'BBG00ZWHC4B5', 'high': 17.92, 'isAdjusted': False, 'lastTradeDate': '2021-04-29', 'lastTradeTime': '21:59:06', 'lastUpdated': '2021-04-29', 'low': 14.15, 'marginPrice': 0, 'open': 14.15, 'openInterest': 69, 'settlementPrice': 0, 'side': 'call', 'strikePrice': 502.5, 'symbol': 'NFLX', 'type': 'equity', 'volume': 3, 'id': 'NFLX20210528C00502500', 'key': 'NFLX', 'subkey': 'NFLX20210528C00502500', 'date': 1619654400000, 'updated': 1619798725000}, {'ask': 12, 'bid': 10.8, 'cfiCode': 'OCAXXX', 'close': 9.97, 'closingPrice': 9.97, 'contractDescription': 'NFLX Option Call 28/05/2021 515 on Ordinary Shares', 'contractName': 'Netflix', 'contractSize': 100, 'currency': 'USD', 'exchangeCode': None, 'exchangeMIC': None, 'exerciseStyle': 'A', 'expirationDate': '20210528', 'figi': 'BBG00ZWHC9V2', 'high': 9.97, 'isAdjusted': False, 'lastTradeDate': '2021-04-29', 'lastTradeTime': '19:04:40', 'lastUpdated': '2021-04-29', 'low': 9.4, 'marginPrice': 0, 'open': 9.4, 'openInterest': 92, 'settlementPrice': 0, 'side': 'call', 'strikePrice': 515, 'symbol': 'NFLX', 'type': 'equity', 'volume': 3, 'id': 'NFLX20210528C00515000', 'key': 'NFLX', 'subkey': 'NFLX20210528C00515000', 'date': 1619654400000, 'updated': 1619798726000}, {'ask': 17, 'bid': 15.55, 'cfiCode': 'OCAXXX', 'close': 15.82, 'closingPrice': 15.82, 'contractDescription': 'NFLX Option Call 28/05/2021 505 on Ordinary Shares', 'contractName': 'Netflix', 'contractSize': 100, 'currency': 'USD', 'exchangeCode': None, 'exchangeMIC': None, 'exerciseStyle': 'A', 'expirationDate': '20210528', 'figi': 'BBG00ZWHC5F8', 'high': 15.82, 'isAdjusted': False, 'lastTradeDate': '2021-04-29', 'lastTradeTime': '21:36:05', 'lastUpdated': '2021-04-29', 'low': 12.1, 'marginPrice': 0, 'open': 13, 'openInterest': 1989, 'settlementPrice': 0, 'side': 'call', 'strikePrice': 505, 'symbol': 'NFLX', 'type': 'equity', 'volume': 6, 'id': 'NFLX20210528C00505000', 'key': 'NFLX', 'subkey': 'NFLX20210528C00505000', 'date': 1619654400000, 'updated': 1619798725000}, {'ask': 2.29, 'bid': 1.93, 'cfiCode': 'OCAXXX', 'close': 2.1, 'closingPrice': 2.1, 'contractDescription': 'NFLX Option Call 28/05/2021 555 on Ordinary Shares', 'contractName': 'Netflix', 'contractSize': 100, 'currency': 'USD', 'exchangeCode': None, 'exchangeMIC': None, 'exerciseStyle': 'A', 'expirationDate': '20210528', 'figi': 'BBG00ZWHCVH9', 'high': 2.1, 'isAdjusted': False, 'lastTradeDate': '2021-04-29', 'lastTradeTime': '18:53:59', 'lastUpdated': '2021-04-29', 'low': 1.5, 'marginPrice': 0, 'open': 1.5, 'openInterest': 99, 'settlementPrice': 0, 'side': 'call', 'strikePrice': 555, 'symbol': 'NFLX', 'type': 'equity', 'volume': 3, 'id': 'NFLX20210528C00555000', 'key': 'NFLX', 'subkey': 'NFLX20210528C00555000', 'date': 1619654400000, 'updated': 1619798725000}, {'ask': 1.09, 'bid': 0.79, 'cfiCode': 'OPAXXX', 'close': 0.96, 'closingPrice': 0.96, 'contractDescription': 'NFLX Option Put 28/05/2021 430 on Ordinary Shares', 'contractName': 'Netflix', 'contractSize': 100, 'currency': 'USD', 'exchangeCode': None, 'exchangeMIC': None, 'exerciseStyle': 'A', 'expirationDate': '20210528', 'figi': 'BBG00ZZG8VP4', 'high': 1.01, 'isAdjusted': False, 'lastTradeDate': '2021-04-29', 'lastTradeTime': '21:09:51', 'lastUpdated': '2021-04-29', 'low': 0.96, 'marginPrice': 0, 'open': 1.01, 'openInterest': 46, 'settlementPrice': 0, 'side': 'put', 'strikePrice': 430, 'symbol': 'NFLX', 'type': 'equity', 'volume': 2, 'id': 'NFLX20210528P00430000', 'key': 'NFLX', 'subkey': 'NFLX20210528P00430000', 'date': 1619654400000, 'updated': 1619798725000}, {'ask': 7.55, 'bid': 6.4, 'cfiCode': 'OPAXXX', 'close': 7.62, 'closingPrice': 7.62, 'contractDescription': 'NFLX Option Put 28/05/2021 490 on Ordinary Shares', 'contractName': 'Netflix', 'contractSize': 100, 'currency': 'USD', 'exchangeCode': None, 'exchangeMIC': None, 'exerciseStyle': 'A', 'expirationDate': '20210528', 'figi': 'BBG00ZWHC112', 'high': 10.25, 'isAdjusted': False, 'lastTradeDate': '2021-04-29', 'lastTradeTime': '21:50:24', 'lastUpdated': '2021-04-29', 'low': 7.33, 'marginPrice': 0, 'open': 7.93, 'openInterest': 143, 'settlementPrice': 0, 'side': 'put', 'strikePrice': 490, 'symbol': 'NFLX', 'type': 'equity', 'volume': 20, 'id': 'NFLX20210528P00490000', 'key': 'NFLX', 'subkey': 'NFLX20210528P00490000', 'date': 1619654400000, 'updated': 1619798725000}, {'ask': 42.8, 'bid': 39.95, 'cfiCode': 'OPAXXX', 'close': 46.29, 'closingPrice': 46.29, 'contractDescription': 'NFLX Option Put 28/05/2021 547.5 on Ordinary Shares', 'contractName': 'Netflix', 'contractSize': 100, 'currency': 'USD', 'exchangeCode': None, 'exchangeMIC': None, 'exerciseStyle': 'A', 'expirationDate': '20210528', 'figi': 'BBG00ZWHCS95', 'high': 46.29, 'isAdjusted': False, 'lastTradeDate': '2021-04-29', 'lastTradeTime': '16:59:34', 'lastUpdated': '2021-04-29', 'low': 46.29, 'marginPrice': 0, 'open': 46.29, 'openInterest': 37, 'settlementPrice': 0, 'side': 'put', 'strikePrice': 547.5, 'symbol': 'NFLX', 'type': 'equity', 'volume': 1, 'id': 'NFLX20210528P00547500', 'key': 'NFLX', 'subkey': 'NFLX20210528P00547500', 'date': 1619654400000, 'updated': 1619798725000}, {'ask': 6.3, 'bid': 5.2, 'cfiCode': 'OCAXXX', 'close': 5, 'closingPrice': 5, 'contractDescription': 'NFLX Option Call 28/05/2021 532.5 on Ordinary Shares', 'contractName': 'Netflix', 'contractSize': 100, 'currency': 'USD', 'exchangeCode': None, 'exchangeMIC': None, 'exerciseStyle': 'A', 'expirationDate': '20210528', 'figi': 'BBG00ZWHCKM7', 'high': 5, 'isAdjusted': False, 'lastTradeDate': '2021-04-29', 'lastTradeTime': '21:11:30', 'lastUpdated': '2021-04-29', 'low': 5, 'marginPrice': 0, 'open': 5, 'openInterest': 52, 'settlementPrice': 0, 'side': 'call', 'strikePrice': 532.5, 'symbol': 'NFLX', 'type': 'equity', 'volume': 1, 'id': 'NFLX20210528C00532500', 'key': 'NFLX', 'subkey': 'NFLX20210528C00532500', 'date': 1619654400000, 'updated': 1619798726000}, {'ask': 5, 'bid': 4.25, 'cfiCode': 'OPAXXX', 'close': 5.15, 'closingPrice': 5.15, 'contractDescription': 'NFLX Option Put 28/05/2021 480 on Ordinary Shares', 'contractName': 'Netflix', 'contractSize': 100, 'currency': 'USD', 'exchangeCode': None, 'exchangeMIC': None, 'exerciseStyle': 'A', 'expirationDate': '20210528', 'figi': 'BBG00ZWHBYT1', 'high': 6.97, 'isAdjusted': False, 'lastTradeDate': '2021-04-29', 'lastTradeTime': '21:50:24', 'lastUpdated': '2021-04-29', 'low': 5.15, 'marginPrice': 0, 'open': 5.94, 'openInterest': 365, 'settlementPrice': 0, 'side': 'put', 'strikePrice': 480, 'symbol': 'NFLX', 'type': 'equity', 'volume': 34, 'id': 'NFLX20210528P00480000', 'key': 'NFLX', 'subkey': 'NFLX20210528P00480000', 'date': 1619654400000, 'updated': 1619798725000}, {'ask': 14.85, 'bid': 13, 'cfiCode': 'OCAXXX', 'close': 14, 'closingPrice': 14, 'contractDescription': 'NFLX Option Call 28/05/2021 510 on Ordinary Shares', 'contractName': 'Netflix', 'contractSize': 100, 'currency': 'USD', 'exchangeCode': None, 'exchangeMIC': None, 'exerciseStyle': 'A', 'expirationDate': '20210528', 'figi': 'BBG00ZWHC7N5', 'high': 14, 'isAdjusted': False, 'lastTradeDate': '2021-04-29', 'lastTradeTime': '21:57:04', 'lastUpdated': '2021-04-29', 'low': 10, 'marginPrice': 0, 'open': 12.8, 'openInterest': 478, 'settlementPrice': 0, 'side': 'call', 'strikePrice': 510, 'symbol': 'NFLX', 'type': 'equity', 'volume': 20, 'id': 'NFLX20210528C00510000', 'key': 'NFLX', 'subkey': 'NFLX20210528C00510000', 'date': 1619654400000, 'updated': 1619795190000}, {'ask': 4.3, 'bid': 3.65, 'cfiCode': 'OCAXXX', 'close': 3.85, 'closingPrice': 3.85, 'contractDescription': 'NFLX Option Call 28/05/2021 540 on Ordinary Shares', 'contractName': 'Netflix', 'contractSize': 100, 'currency': 'USD', 'exchangeCode': None, 'exchangeMIC': None, 'exerciseStyle': 'A', 'expirationDate': '20210528', 'figi': 'BBG00ZWHCNY8', 'high': 3.85, 'isAdjusted': False, 'lastTradeDate': '2021-04-29', 'lastTradeTime': '21:38:51', 'lastUpdated': '2021-04-29', 'low': 3.2, 'marginPrice': 0, 'open': 3.2, 'openInterest': 72, 'settlementPrice': 0, 'side': 'call', 'strikePrice': 540, 'symbol': 'NFLX', 'type': 'equity', 'volume': 10, 'id': 'NFLX20210528C00540000', 'key': 'NFLX', 'subkey': 'NFLX20210528C00540000', 'date': 1619654400000, 'updated': 1619795190000}, {'ask': 20.6, 'bid': 18.4, 'cfiCode': 'OCAXXX', 'close': 19.37, 'closingPrice': 19.37, 'contractDescription': 'NFLX Option Call 28/05/2021 500 on Ordinary Shares', 'contractName': 'Netflix', 'contractSize': 100, 'currency': 'USD', 'exchangeCode': None, 'exchangeMIC': None, 'exerciseStyle': 'A', 'expirationDate': '20210528', 'figi': 'BBG00ZWHC363', 'high': 19.37, 'isAdjusted': False, 'lastTradeDate': '2021-04-29', 'lastTradeTime': '21:59:06', 'lastUpdated': '2021-04-29', 'low': 14.55, 'marginPrice': 0, 'open': 16.32, 'openInterest': 1938, 'settlementPrice': 0, 'side': 'call', 'strikePrice': 500, 'symbol': 'NFLX', 'type': 'equity', 'volume': 13, 'id': 'NFLX20210528C00500000', 'key': 'NFLX', 'subkey': 'NFLX20210528C00500000', 'date': 1619654400000, 'updated': 1619795191000}, {'ask': 6.15, 'bid': 5.2, 'cfiCode': 'OPAXXX', 'close': 6.02, 'closingPrice': 6.02, 'contractDescription': 'NFLX Option Put 28/05/2021 485 on Ordinary Shares', 'contractName': 'Netflix', 'contractSize': 100, 'currency': 'USD', 'exchangeCode': None, 'exchangeMIC': None, 'exerciseStyle': 'A', 'expirationDate': '20210528', 'figi': 'BBG00ZWHBZX3', 'high': 8.5, 'isAdjusted': False, 'lastTradeDate': '2021-04-29', 'lastTradeTime': '21:40:18', 'lastUpdated': '2021-04-29', 'low': 6.02, 'marginPrice': 0, 'open': 7.3, 'openInterest': 172, 'settlementPrice': 0, 'side': 'put', 'strikePrice': 485, 'symbol': 'NFLX', 'type': 'equity', 'volume': 36, 'id': 'NFLX20210528P00485000', 'key': 'NFLX', 'subkey': 'NFLX20210528P00485000', 'date': 1619654400000, 'updated': 1619795190000}, {'ask': 38.4, 'bid': 36.45, 'cfiCode': 'OCAXXX', 'close': 35.55, 'closingPrice': 35.55, 'contractDescription': 'NFLX Option Call 28/05/2021 475 on Ordinary Shares', 'contractName': 'Netflix', 'contractSize': 100, 'currency': 'USD', 'exchangeCode': None, 'exchangeMIC': None, 'exerciseStyle': 'A', 'expirationDate': '20210528', 'figi': 'BBG00ZZG95M3', 'high': 36.68, 'isAdjusted': False, 'lastTradeDate': '2021-04-29', 'lastTradeTime': '15:39:22', 'lastUpdated': '2021-04-29', 'low': 35.55, 'marginPrice': 0, 'open': 36.68, 'openInterest': 47, 'settlementPrice': 0, 'side': 'call', 'strikePrice': 475, 'symbol': 'NFLX', 'type': 'equity', 'volume': 2, 'id': 'NFLX20210528C00475000', 'key': 'NFLX', 'subkey': 'NFLX20210528C00475000', 'date': 1619654400000, 'updated': 1619795190000}, {'ask': 3.45, 'bid': 3, 'cfiCode': 'OCAXXX', 'close': 2.76, 'closingPrice': 2.76, 'contractDescription': 'NFLX Option Call 28/05/2021 545 on Ordinary Shares', 'contractName': 'Netflix', 'contractSize': 100, 'currency': 'USD', 'exchangeCode': None, 'exchangeMIC': None, 'exerciseStyle': 'A', 'expirationDate': '20210528', 'figi': 'BBG00ZWHCR51', 'high': 2.77, 'isAdjusted': False, 'lastTradeDate': '2021-04-29', 'lastTradeTime': '20:58:35', 'lastUpdated': '2021-04-29', 'low': 2.76, 'marginPrice': 0, 'open': 2.77, 'openInterest': 65, 'settlementPrice': 0, 'side': 'call', 'strikePrice': 545, 'symbol': 'NFLX', 'type': 'equity', 'volume': 2, 'id': 'NFLX20210528C00545000', 'key': 'NFLX', 'subkey': 'NFLX20210528C00545000', 'date': 1619654400000, 'updated': 1619795190000}, {'ask': 12.15, 'bid': 11, 'cfiCode': 'OPAXXX', 'close': 11.95, 'closingPrice': 11.95, 'contractDescription': 'NFLX Option Put 28/05/2021 502.5 on Ordinary Shares', 'contractName': 'Netflix', 'contractSize': 100, 'currency': 'USD', 'exchangeCode': None, 'exchangeMIC': None, 'exerciseStyle': 'A', 'expirationDate': '20210528', 'figi': 'BBG00ZWHC4C4', 'high': 15.83, 'isAdjusted': False, 'lastTradeDate': '2021-04-29', 'lastTradeTime': '21:47:14', 'lastUpdated': '2021-04-29', 'low': 11.95, 'marginPrice': 0, 'open': 14.75, 'openInterest': 3, 'settlementPrice': 0, 'side': 'put', 'strikePrice': 502.5, 'symbol': 'NFLX', 'type': 'equity', 'volume': 6, 'id': 'NFLX20210528P00502500', 'key': 'NFLX', 'subkey': 'NFLX20210528P00502500', 'date': 1619654400000, 'updated': 1619798726000}, {'ask': 5.25, 'bid': 4.65, 'cfiCode': 'OCAXXX', 'close': 4.8, 'closingPrice': 4.8, 'contractDescription': 'NFLX Option Call 28/05/2021 535 on Ordinary Shares', 'contractName': 'Netflix', 'contractSize': 100, 'currency': 'USD', 'exchangeCode': None, 'exchangeMIC': None, 'exerciseStyle': 'A', 'expirationDate': '20210528', 'figi': 'BBG00ZWHCLQ1', 'high': 4.8, 'isAdjusted': False, 'lastTradeDate': '2021-04-29', 'lastTradeTime': '21:57:47', 'lastUpdated': '2021-04-29', 'low': 3.9, 'marginPrice': 0, 'open': 4.15, 'openInterest': 98, 'settlementPrice': 0, 'side': 'call', 'strikePrice': 535, 'symbol': 'NFLX', 'type': 'equity', 'volume': 7, 'id': 'NFLX20210528C00535000', 'key': 'NFLX', 'subkey': 'NFLX20210528C00535000', 'date': 1619654400000, 'updated': 1619798726000}, {'ask': 1.49, 'bid': 1.19, 'cfiCode': 'OPAXXX', 'close': 1.5, 'closingPrice': 1.5, 'contractDescription': 'NFLX Option Put 28/05/2021 445 on Ordinary Shares', 'contractName': 'Netflix', 'contractSize': 100, 'currency': 'USD', 'exchangeCode': None, 'exchangeMIC': None, 'exerciseStyle': 'A', 'expirationDate': '20210528', 'figi': 'BBG00ZZG8Z02', 'high': 1.5, 'isAdjusted': False, 'lastTradeDate': '2021-04-29', 'lastTradeTime': '18:56:26', 'lastUpdated': '2021-04-29', 'low': 1.5, 'marginPrice': 0, 'open': 1.5, 'openInterest': 99, 'settlementPrice': 0, 'side': 'put', 'strikePrice': 445, 'symbol': 'NFLX', 'type': 'equity', 'volume': 2, 'id': 'NFLX20210528P00445000', 'key': 'NFLX', 'subkey': 'NFLX20210528P00445000', 'date': 1619654400000, 'updated': 1619798726000}, {'ask': 13.3, 'bid': 11.95, 'cfiCode': 'OPAXXX', 'close': 13.7, 'closingPrice': 13.7, 'contractDescription': 'NFLX Option Put 28/05/2021 505 on Ordinary Shares', 'contractName': 'Netflix', 'contractSize': 100, 'currency': 'USD', 'exchangeCode': None, 'exchangeMIC': None, 'exerciseStyle': 'A', 'expirationDate': '20210528', 'figi': 'BBG00ZWHC5G7', 'high': 18.15, 'isAdjusted': False, 'lastTradeDate': '2021-04-29', 'lastTradeTime': '21:31:15', 'lastUpdated': '2021-04-29', 'low': 13.7, 'marginPrice': 0, 'open': 15.05, 'openInterest': 502, 'settlementPrice': 0, 'side': 'put', 'strikePrice': 505, 'symbol': 'NFLX', 'type': 'equity', 'volume': 11, 'id': 'NFLX20210528P00505000', 'key': 'NFLX', 'subkey': 'NFLX20210528P00505000', 'date': 1619654400000, 'updated': 1619798725000}, {'ask': 14.5, 'bid': 12.95, 'cfiCode': 'OPAXXX', 'close': 13.75, 'closingPrice': 13.75, 'contractDescription': 'NFLX Option Put 28/05/2021 507.5 on Ordinary Shares', 'contractName': 'Netflix', 'contractSize': 100, 'currency': 'USD', 'exchangeCode': None, 'exchangeMIC': None, 'exerciseStyle': 'A', 'expirationDate': '20210528', 'figi': 'BBG00ZWHC6K0', 'high': 16.4, 'isAdjusted': False, 'lastTradeDate': '2021-04-29', 'lastTradeTime': '21:59:02', 'lastUpdated': '2021-04-29', 'low': 13.49, 'marginPrice': 0, 'open': 16.4, 'openInterest': 36, 'settlementPrice': 0, 'side': 'put', 'strikePrice': 507.5, 'symbol': 'NFLX', 'type': 'equity', 'volume': 3, 'id': 'NFLX20210528P00507500', 'key': 'NFLX', 'subkey': 'NFLX20210528P00507500', 'date': 1619654400000, 'updated': 1619798726000}, {'ask': 18.55, 'bid': 16.55, 'cfiCode': 'OPAXXX', 'close': 20.14, 'closingPrice': 20.14, 'contractDescription': 'NFLX Option Put 28/05/2021 515 on Ordinary Shares', 'contractName': 'Netflix', 'contractSize': 100, 'currency': 'USD', 'exchangeCode': None, 'exchangeMIC': None, 'exerciseStyle': 'A', 'expirationDate': '20210528', 'figi': 'BBG00ZWHC9W1', 'high': 21.48, 'isAdjusted': False, 'lastTradeDate': '2021-04-29', 'lastTradeTime': '19:27:52', 'lastUpdated': '2021-04-29', 'low': 20.02, 'marginPrice': 0, 'open': 21.48, 'openInterest': 41, 'settlementPrice': 0, 'side': 'put', 'strikePrice': 515, 'symbol': 'NFLX', 'type': 'equity', 'volume': 3, 'id': 'NFLX20210528P00515000', 'key': 'NFLX', 'subkey': 'NFLX20210528P00515000', 'date': 1619654400000, 'updated': 1619798726000}, {'ask': 5.55, 'bid': 4.7, 'cfiCode': 'OPAXXX', 'close': 5.85, 'closingPrice': 5.85, 'contractDescription': 'NFLX Option Put 28/05/2021 482.5 on Ordinary Shares', 'contractName': 'Netflix', 'contractSize': 100, 'currency': 'USD', 'exchangeCode': None, 'exchangeMIC': None, 'exerciseStyle': 'A', 'expirationDate': '20210528', 'figi': '', 'high': 6.11, 'isAdjusted': False, 'lastTradeDate': '2021-04-29', 'lastTradeTime': '21:09:45', 'lastUpdated': '2021-04-29', 'low': 5.85, 'marginPrice': 0, 'open': 6.11, 'openInterest': 0, 'settlementPrice': 0, 'side': 'put', 'strikePrice': 482.5, 'symbol': 'NFLX', 'type': 'equity', 'volume': 5, 'id': 'NFLX20210528P00482500', 'key': 'NFLX', 'subkey': 'NFLX20210528P00482500', 'date': 1619654400000, 'updated': 1619798726000}, {'ask': 1.05, 'bid': 0.77, 'cfiCode': 'OCAXXX', 'close': 0.87, 'closingPrice': 0.87, 'contractDescription': 'NFLX Option Call 28/05/2021 580 on Ordinary Shares', 'contractName': 'Netflix', 'contractSize': 100, 'currency': 'USD', 'exchangeCode': None, 'exchangeMIC': None, 'exerciseStyle': 'A', 'expirationDate': '20210528', 'figi': 'BBG00ZWHD102', 'high': 0.87, 'isAdjusted': False, 'lastTradeDate': '2021-04-29', 'lastTradeTime': '21:57:29', 'lastUpdated': '2021-04-29', 'low': 0.87, 'marginPrice': 0, 'open': 0.87, 'openInterest': 70, 'settlementPrice': 0, 'side': 'call', 'strikePrice': 580, 'symbol': 'NFLX', 'type': 'equity', 'volume': 1, 'id': 'NFLX20210528C00580000', 'key': 'NFLX', 'subkey': 'NFLX20210528C00580000', 'date': 1619654400000, 'updated': 1619798726000}, {'ask': 1.65, 'bid': 1.28, 'cfiCode': 'OCAXXX', 'close': 1.35, 'closingPrice': 1.35, 'contractDescription': 'NFLX Option Call 28/05/2021 565 on Ordinary Shares', 'contractName': 'Netflix', 'contractSize': 100, 'currency': 'USD', 'exchangeCode': None, 'exchangeMIC': None, 'exerciseStyle': 'A', 'expirationDate': '20210528', 'figi': 'BBG00ZWHCXP6', 'high': 1.35, 'isAdjusted': False, 'lastTradeDate': '2021-04-29', 'lastTradeTime': '18:33:22', 'lastUpdated': '2021-04-29', 'low': 1.31, 'marginPrice': 0, 'open': 1.31, 'openInterest': 298, 'settlementPrice': 0, 'side': 'call', 'strikePrice': 565, 'symbol': 'NFLX', 'type': 'equity', 'volume': 2, 'id': 'NFLX20210528C00565000', 'key': 'NFLX', 'subkey': 'NFLX20210528C00565000', 'date': 1619654400000, 'updated': 1619798725000}, {'ask': 1.98, 'bid': 1.52, 'cfiCode': 'OCAXXX', 'close': 1.52, 'closingPrice': 1.52, 'contractDescription': 'NFLX Option Call 28/05/2021 560 on Ordinary Shares', 'contractName': 'Netflix', 'contractSize': 100, 'currency': 'USD', 'exchangeCode': None, 'exchangeMIC': None, 'exerciseStyle': 'A', 'expirationDate': '20210528', 'figi': 'BBG00ZWHCWL2', 'high': 1.52, 'isAdjusted': False, 'lastTradeDate': '2021-04-29', 'lastTradeTime': '17:26:54', 'lastUpdated': '2021-04-29', 'low': 1.52, 'marginPrice': 0, 'open': 1.52, 'openInterest': 164, 'settlementPrice': 0, 'side': 'call', 'strikePrice': 560, 'symbol': 'NFLX', 'type': 'equity', 'volume': 1, 'id': 'NFLX20210528C00560000', 'key': 'NFLX', 'subkey': 'NFLX20210528C00560000', 'date': 1619654400000, 'updated': 1619798726000}, {'ask': 2.77, 'bid': 2.4, 'cfiCode': 'OCAXXX', 'close': 2.35, 'closingPrice': 2.35, 'contractDescription': 'NFLX Option Call 28/05/2021 550 on Ordinary Shares', 'contractName': 'Netflix', 'contractSize': 100, 'currency': 'USD', 'exchangeCode': None, 'exchangeMIC': None, 'exerciseStyle': 'A', 'expirationDate': '20210528', 'figi': 'BBG00ZWHCTC9', 'high': 2.4, 'isAdjusted': False, 'lastTradeDate': '2021-04-29', 'lastTradeTime': '20:48:24', 'lastUpdated': '2021-04-29', 'low': 2.33, 'marginPrice': 0, 'open': 2.4, 'openInterest': 325, 'settlementPrice': 0, 'side': 'call', 'strikePrice': 550, 'symbol': 'NFLX', 'type': 'equity', 'volume': 4, 'id': 'NFLX20210528C00550000', 'key': 'NFLX', 'subkey': 'NFLX20210528C00550000', 'date': 1619654400000, 'updated': 1619798726000}, {'ask': 0.52, 'bid': 0.3, 'cfiCode': 'OPAXXX', 'close': 0.37, 'closingPrice': 0.37, 'contractDescription': 'NFLX Option Put 28/05/2021 370 on Ordinary Shares', 'contractName': 'Netflix', 'contractSize': 100, 'currency': 'USD', 'exchangeCode': None, 'exchangeMIC': None, 'exerciseStyle': 'A', 'expirationDate': '20210528', 'figi': 'BBG00ZX50S02', 'high': 0.37, 'isAdjusted': False, 'lastTradeDate': '2021-04-29', 'lastTradeTime': '15:42:45', 'lastUpdated': '2021-04-29', 'low': 0.37, 'marginPrice': 0, 'open': 0.37, 'openInterest': 90, 'settlementPrice': 0, 'side': 'put', 'strikePrice': 370, 'symbol': 'NFLX', 'type': 'equity', 'volume': 1, 'id': 'NFLX20210528P00370000', 'key': 'NFLX', 'subkey': 'NFLX20210528P00370000', 'date': 1619654400000, 'updated': 1619791798000}, {'ask': 2.76, 'bid': 2.29, 'cfiCode': 'OPAXXX', 'close': 2.55, 'closingPrice': 2.55, 'contractDescription': 'NFLX Option Put 28/05/2021 465 on Ordinary Shares', 'contractName': 'Netflix', 'contractSize': 100, 'currency': 'USD', 'exchangeCode': None, 'exchangeMIC': None, 'exerciseStyle': 'A', 'expirationDate': '20210528', 'figi': 'BBG00ZZG93F6', 'high': 3.35, 'isAdjusted': False, 'lastTradeDate': '2021-04-29', 'lastTradeTime': '21:55:56', 'lastUpdated': '2021-04-29', 'low': 2.55, 'marginPrice': 0, 'open': 2.8, 'openInterest': 295, 'settlementPrice': 0, 'side': 'put', 'strikePrice': 465, 'symbol': 'NFLX', 'type': 'equity', 'volume': 11, 'id': 'NFLX20210528P00465000', 'key': 'NFLX', 'subkey': 'NFLX20210528P00465000', 'date': 1619654400000, 'updated': 1619791798000}, {'ask': 1.33, 'bid': 1.02, 'cfiCode': 'OPAXXX', 'close': 1.3, 'closingPrice': 1.3, 'contractDescription': 'NFLX Option Put 28/05/2021 440 on Ordinary Shares', 'contractName': 'Netflix', 'contractSize': 100, 'currency': 'USD', 'exchangeCode': None, 'exchangeMIC': None, 'exerciseStyle': 'A', 'expirationDate': '20210528', 'figi': 'BBG00ZZG8XX1', 'high': 1.49, 'isAdjusted': False, 'lastTradeDate': '2021-04-29', 'lastTradeTime': '21:44:40', 'lastUpdated': '2021-04-29', 'low': 1.18, 'marginPrice': 0, 'open': 1.2, 'openInterest': 167, 'settlementPrice': 0, 'side': 'put', 'strikePrice': 440, 'symbol': 'NFLX', 'type': 'equity', 'volume': 12, 'id': 'NFLX20210528P00440000', 'key': 'NFLX', 'subkey': 'NFLX20210528P00440000', 'date': 1619654400000, 'updated': 1619791798000}, {'ask': 1.2, 'bid': 0.9, 'cfiCode': 'OCAXXX', 'close': 1.08, 'closingPrice': 1.08, 'contractDescription': 'NFLX Option Call 28/05/2021 575 on Ordinary Shares', 'contractName': 'Netflix', 'contractSize': 100, 'currency': 'USD', 'exchangeCode': None, 'exchangeMIC': None, 'exerciseStyle': 'A', 'expirationDate': '20210528', 'figi': 'BBG00ZWHCZX2', 'high': 1.08, 'isAdjusted': False, 'lastTradeDate': '2021-04-29', 'lastTradeTime': '15:31:05', 'lastUpdated': '2021-04-29', 'low': 1.08, 'marginPrice': 0, 'open': 1.08, 'openInterest': 311, 'settlementPrice': 0, 'side': 'call', 'strikePrice': 575, 'symbol': 'NFLX', 'type': 'equity', 'volume': 1, 'id': 'NFLX20210528C00575000', 'key': 'NFLX', 'subkey': 'NFLX20210528C00575000', 'date': 1619654400000, 'updated': 1619791798000}, {'ask': 11.1, 'bid': 9.65, 'cfiCode': 'OPAXXX', 'close': 10.67, 'closingPrice': 10.67, 'contractDescription': 'NFLX Option Put 28/05/2021 500 on Ordinary Shares', 'contractName': 'Netflix', 'contractSize': 100, 'currency': 'USD', 'exchangeCode': None, 'exchangeMIC': None, 'exerciseStyle': 'A', 'expirationDate': '20210528', 'figi': 'BBG00ZWHC372', 'high': 15, 'isAdjusted': False, 'lastTradeDate': '2021-04-29', 'lastTradeTime': '21:59:45', 'lastUpdated': '2021-04-29', 'low': 10.6, 'marginPrice': 0, 'open': 12.3, 'openInterest': 477, 'settlementPrice': 0, 'side': 'put', 'strikePrice': 500, 'symbol': 'NFLX', 'type': 'equity', 'volume': 14, 'id': 'NFLX20210528P00500000', 'key': 'NFLX', 'subkey': 'NFLX20210528P00500000', 'date': 1619654400000, 'updated': 1619798726000}, {'ask': 57.55, 'bid': 54.35, 'cfiCode': 'OCAXXX', 'close': 47.7, 'closingPrice': 47.7, 'contractDescription': 'NFLX Option Call 28/05/2021 455 on Ordinary Shares', 'contractName': 'Netflix', 'contractSize': 100, 'currency': 'USD', 'exchangeCode': None, 'exchangeMIC': None, 'exerciseStyle': 'A', 'expirationDate': '20210528', 'figi': 'BBG00ZZG9160', 'high': 47.7, 'isAdjusted': False, 'lastTradeDate': '2021-04-29', 'lastTradeTime': '17:40:21', 'lastUpdated': '2021-04-29', 'low': 47.7, 'marginPrice': 0, 'open': 47.7, 'openInterest': 1, 'settlementPrice': 0, 'side': 'call', 'strikePrice': 455, 'symbol': 'NFLX', 'type': 'equity', 'volume': 1, 'id': 'NFLX20210528C00455000', 'key': 'NFLX', 'subkey': 'NFLX20210528C00455000', 'date': 1619654400000, 'updated': 1619798726000}, {'ask': 2.32, 'bid': 2, 'cfiCode': 'OPAXXX', 'close': 2.15, 'closingPrice': 2.15, 'contractDescription': 'NFLX Option Put 28/05/2021 460 on Ordinary Shares', 'contractName': 'Netflix', 'contractSize': 100, 'currency': 'USD', 'exchangeCode': None, 'exchangeMIC': None, 'exerciseStyle': 'A', 'expirationDate': '20210528', 'figi': 'BBG00ZZG92B2', 'high': 3.07, 'isAdjusted': False, 'lastTradeDate': '2021-04-29', 'lastTradeTime': '21:55:56', 'lastUpdated': '2021-04-29', 'low': 2.15, 'marginPrice': 0, 'open': 2.77, 'openInterest': 515, 'settlementPrice': 0, 'side': 'put', 'strikePrice': 460, 'symbol': 'NFLX', 'type': 'equity', 'volume': 25, 'id': 'NFLX20210528P00460000', 'key': 'NFLX', 'subkey': 'NFLX20210528P00460000', 'date': 1619654400000, 'updated': 1619798725000}]
#
# test.option_table('nflx', test_data)