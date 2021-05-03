"""
Sanitize volume records
"""
import LunaOptionsDB as db
import time
import schedule
import SandP500List as snp


def sanitize_volume():
    dbase = db.LunaDB()
    for ticker in snp.ticker_list:
        dbase.truncate_table(ticker, '_volume')


def updater():
    """
    The updater that runs constantly
    """
    schedule.every().monday.at("12:30").do(sanitize_volume)

    while True:
        schedule.run_pending()
        time.sleep(1)


updater()