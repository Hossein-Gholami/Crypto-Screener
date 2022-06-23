from django.db import models

# Create your models here.

# class Exchange(models.Model):
#     name = models.CharField(max_length=20, null=True, blank=True, default='binance', unique=True)

#     def __str__(self):
#         return self.name

class Symbol(models.Model):
    exchange = models.CharField(max_length=20, null=True, blank=True, default='binance')
    symbol_name = models.CharField(max_length=20, null=True, blank=True, unique=True)
    last_price = models.DecimalField(max_digits=10, decimal_places=5, default=0.0)

    # @classmethod
    # def create(cls, *args, **kwargs):
    #     if 'exchange' not in kwargs:
    #         kwargs['exchange'] = 'binance'
    #     pair = cls(**kwargs)
    #     return pair

    def __str__(self):
        return f"<{self.exchange}|symbol: {self.symbol_name}|price: {self.last_price}>"
    

