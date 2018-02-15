from django.db import models

class Currency(models.Model):
    symbol = models.CharField(max_length=8, unique=True)
    full_name = models.CharField(max_length=16, blank=True, null=True)
    text_symbol = models.CharField(max_length=1, blank=True, null=True)

    def __str__(self):
        return '%s (%s)' % (self.full_name, self.symbol)

class CurrencyQuantityProxy(models.Model):
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    quantity = models.FloatField()