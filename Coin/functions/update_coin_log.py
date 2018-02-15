from datetime import datetime
from pytz import UTC

from ..models import Coin, Currency, CurrencyQuantityProxy, Log
from Util.functions import creative_get

def update_coin_log(coin_data, conversions):
    coin_data['cmc_id'] = coin_data.pop('id')
    coin = creative_get(Coin, coin_data)

    last_log = coin.get_latest_log()
    coin_data['datetime'] = datetime.fromtimestamp(int(coin_data['last_updated'])).replace(tzinfo=UTC)

    if not last_log or last_log.datetime.timestamp() != coin_data['datetime'].timestamp():
        log = Log()
        log.datetime = coin_data['datetime']
        log.coin_name = coin.name
        log.coin_symbol = coin.symbol

        log.rank = int(coin_data['rank'])
        log.available_supply = float(coin_data['available_supply'])
        log.total_supply = float(coin_data['total_supply'])

        try:
            log.percent_change_1h = float(coin_data['percent_change_1h'])
        except KeyError:
            pass
        except TypeError:
            pass
        try:
            log.percent_change_24h = float(coin_data['percent_change_24h'])
        except KeyError:
            pass
        except TypeError:
            pass
        try:
            log.percent_change_7d = float(coin_data['percent_change_7d'])
        except KeyError:
            pass
        except TypeError:
            pass

        try:
            log.max_supply = float(coin_data['max_supply'])
        except KeyError:
            pass
        except TypeError:
            pass

        log.save()

        for currency_symbol in conversions + ['USD', 'BTC']:
            currency = creative_get(Currency, {'symbol': currency_symbol})

            try:
                price_cqp = CurrencyQuantityProxy()
                price_cqp.currency = currency
                price_cqp.quantity = float(coin_data['price_' + currency_symbol.lower()])
                price_cqp.save()
                log.price.add(price_cqp)
            except KeyError:
                pass

            try:
                market_cap_cqp = CurrencyQuantityProxy()
                market_cap_cqp.currency = currency
                market_cap_cqp.quantity = float(coin_data['market_cap_' + currency_symbol.lower()])
                market_cap_cqp.save()
                log.price.add(market_cap_cqp)
            except KeyError:
                pass

            try:
                volume_cqp = CurrencyQuantityProxy()
                volume_cqp.currency = currency
                volume_cqp.quantity = float(coin_data['volume_' + currency_symbol.lower()])
                volume_cqp.save()
                log.price.add(volume_cqp)
            except KeyError:
                pass

        log.save()
        coin.logs.add(log)
        coin.save()
