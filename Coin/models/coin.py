from django.db import models

from .log import Log

class Coin(models.Model):
    cmc_id = models.CharField(max_length=32, unique=True)
    name = models.CharField(max_length=32, unique=True)
    symbol = models.CharField(max_length=8, unique=True)
    icon = models.TextField(blank=True, null=True)

    logs = models.ManyToManyField(Log)

    def __str__(self) -> str:
        return '%s (%s)' % (self.name, self.symbol)

    def get_latest_log(self) -> Log:
        try:
            return self.logs.all().order_by('-datetime')[0]
        except IndexError:
            return None
