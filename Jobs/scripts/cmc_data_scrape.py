from ..config import cmc_scrape_interval, cmc_scrape_conversions
from Util.api.coinmarketcap.get_coin_metrics import get_coin_metrics
from Coin.functions import update_coin_log

from time import sleep

def run():
    while True:
        data = get_coin_metrics(convert=cmc_scrape_conversions, start=0, limit=100)

        for coin_data in data:
            update_coin_log(coin_data, cmc_scrape_conversions)

        sleep(cmc_scrape_interval)
