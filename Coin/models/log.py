from django.db import models

from .currency import CurrencyQuantityProxy

class Log(models.Model):
    datetime = models.DateTimeField()
    coin_name = models.CharField(max_length=32)
    coin_symbol = models.CharField(max_length=8)

    rank = models.IntegerField()

    price = models.ManyToManyField(CurrencyQuantityProxy, related_name='coin_price')
    volume = models.ManyToManyField(CurrencyQuantityProxy, related_name='coin_volume')
    market_cap = models.ManyToManyField(CurrencyQuantityProxy, related_name='coin_market_cap')

    available_supply = models.FloatField()
    total_supply = models.FloatField()
    max_supply = models.FloatField(blank=True, null=True)

    percent_change_1h = models.FloatField(blank=True, null=True)
    percent_change_24h = models.FloatField(blank=True, null=True)
    percent_change_7d = models.FloatField(blank=True, null=True)

    def __str__(self):
        return '%s @ %s' % (self.coin_name, self.iso_time())

    def iso_time(self):
        return self.datetime.strftime('%Y-%m-%dT%H:%M:%SZ')

    def timestamp(self):
        return self.datetime.timestamp()