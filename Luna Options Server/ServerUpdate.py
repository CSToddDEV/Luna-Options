"""
Script for server updates, can change based on needs
"""
import APICallScript as api
import LunaOptionsDB as db
import SandP500List as snp
from LunaOptionsDBUpdate import DBUpdate as update


# def update5_14_21():
#     luna = db.LunaDB()
#     api_obj = api.APICalls()
#     for ticker in snp.ticker_list:
#         ticker.lower()
#         columns = luna.get_column_names(ticker, '_options')
#         print(columns)
#         print('Ticker ', ticker)
#         if len(columns) == 5:
#             print('ADDING COLUMN')
#             luna.add_column(ticker, '_options', 'historicalVolatility', 'varchar(32)')
#
#         hv = api_obj.historical_volatility_call(ticker)
#         if hv and 'indicator' in hv.keys():
#             historical_volatility = hv['indicator'][0][0]
#             historical_volatility = float(historical_volatility)
#             historical_volatility = historical_volatility * 100
#             historical_volatility = round(historical_volatility, 2)
#
#         else:
#             historical_volatility = 'N/A'
#         try:
#             luna.update_column_conditional(ticker, '_options', 'historicalVolatility', str(historical_volatility), 'id', '1')
#         except:
#             print('PASSED: ', ticker)
#
#     print('Update Complete!')

# def update5_15_21():
#     """
#     1) Delete IV Tables
#     2) Delete TICKER_dailyvolume tables
#     3) Create new historicalIV tables
#     4) Drop historicalIV column in _options table
#     5) Add price and IV column to _options table
#     6) Add 52WeekHighIV and 52WeekLowIV to ticker table
#     7) Pull Historical IVs
#     8) Pull Options Prices
#     9) Calculate Options IVs
#     10) Update Ticker Table with High and Low IVs
#     """
#
#     print('Update 5.15.21 Started (Good Luck!)')
#
#     luna = db.LunaDB()
#     api_obj = api.APICalls()
#     updater = update.DBUpdate()

    # # 3
    # luna.update_tables()
    # print('# 3 Complete')

    # for ticker in snp.ticker_list:
    #     # 1
    #     if '.' in ticker:
    #         ticker = ticker.replace('.', '')
        # ticker = ticker.lower()
        # iv_table = ticker + '_iv'
        # try:
        #     luna.delete_table(iv_table)
        # except:
        #     print('#1 skipped for ', ticker)

        # 2
        # ticker = ticker.upper()
        # dv_table = ticker + '_dailyvolume'
        # try:
        #     luna.delete_table(dv_table)
        # except:
        #     print('#2 skipped for ', ticker)
    #
    #     # 4
    #     ticker = ticker.lower()
    #     try:
    #         luna.drop_column(ticker, '_options', 'historicalVolatility')
    #     except:
    #         print('#3 skipped for ', ticker)
    #
    #     # 5
    #     try:
    #         luna.add_column(ticker, '_options', 'price', 'decimal(6, 2)')
    #         luna.add_column(ticker, '_options', 'IV', 'decimal(6, 2)')
    #     except:
    #         print('#5 skipped for ', ticker)
    #
    #     # 6
    #     try:
    #         luna.add_column(ticker, '', '52WeekHighIV', 'decimal(6, 2)')
    #         luna.add_column(ticker, '', '52WeekLowIV', 'decimal(6, 2)')
    #     except:
    #         print('#6 skipped for ', ticker)
    #
    # print("#1 - #6 Complete! (Loop Complete!)")

    # 7 - 9
    # updater.update_options()
    # print("#7 - #9 Complete!")

    # 10
    # updater.update_price()
    # updater.update_end_of_day()
    #
    # print("Server update Complete!!!")

# def update_5_17_21():
#     """
#     1) Update lunaoptionsDB with Top IV Security table
#     2) Pull Current list of IV securities and write to table
#     3) Update HTTP request to return list to client
#     """
#     luna = db.LunaDB()
#
#     print(" Server update Started")
#     # 1
#     luna.update_tables(False)
#
#     # 2
#     luna.update_high_iv_table()
#
#     print("Server Update Finished!")

# def update_5_24_21():
#     """
#     # 1 Add tickers SPY, GME, AMC, and QQQ to tables
#     # 2 Add IVRank column
#     """
#     luna = db.LunaDB()
#
#     print("Server Update Started")
#     # 1
#     luna.update_tables()
#
#     # 2
#     for ticker in snp.ticker_list:
#         if '.' in ticker:
#             ticker = ticker.replace('.', '')
#         ticker = ticker.lower()
#         try:
#             luna.add_column(ticker, '', 'iv_rank', 'decimal(6,2)')
#         except:
#             pass
#
#     print("Update Complete!")

# def update_5_27_21():
#     """
#     # 1 Add sentiment table
#     # 2 Update sentiment table
#     """
#     luna = db.LunaDB()
#
#     print("Server Update Started")
#     # # 1
#     # luna.update_tables()
#
#     # 2
#     for ticker in snp.ticker_list:
#         luna.update_IV_rank(ticker)
#
#     print("Update Complete!")

# def update_6_02_21():
#     """
#     # 1 Update Options
#     # 2 Update IV Rank
#     """
#     luna = db.LunaDB()
#
#     print("Server Update Started")
#
#     # 1
#     option_update = update()
#     option_update.update_options()
#
#     for ticker in snp.ticker_list:
#         # 2
#         luna.update_IV_rank(ticker)
#
#     print("Update Complete!")

# def update_6_03_21():
#     """
#     # 1 Update sentiment table
#     """
#     luna = db.LunaDB()
#
#     print("Server Update Started")
#
#     # 1
#     luna.update_market_sentiment_table()
#
#     print("Update Complete!")
#
# update_6_03_21()

