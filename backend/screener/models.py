from django.conf import settings
from django.db import models

from screener import redis_client

# Create your models here.

# class Exchange(models.Model):
#     name = models.CharField(max_length=20, null=True, blank=True, default='binance', unique=True)

#     def __str__(self):
#         return self.name

class Symbol(models.Model):
    name = models.CharField(max_length=20, primary_key=True, null=False, blank=False)
    price = models.DecimalField(default=0.0, max_digits=10, decimal_places=5)

    def __str__(self):
        return "<%s|price: %d>" % (self.name, self.price)

    # @classmethod
    # def create(cls, *args, **kwargs):
    #     if 'exchange' not in kwargs:
    #         kwargs['exchange'] = 'binance'
    #     pair = cls(**kwargs)
    #     return pair

    def update_prices():
        tickers = redis_client.hgetall(settings.APP_SPECIFIC_KEYS['screener']['tickers'])
        if len(tickers.keys()) != 0:
            tickers = {ticker.decode():float(tickers[ticker]) for ticker in tickers.keys()}
            for ticker, price in tickers.items():
                print("Updating ticker: %s, price: %f..." % (ticker, price))
                _symbol = Symbol.objects.get(pk=ticker)
                _symbol.price = price
                _symbol.save()
    

