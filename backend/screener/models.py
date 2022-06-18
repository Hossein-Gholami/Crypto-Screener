from django.db import models

# Create your models here.

class Exchange(models.model):
    name = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.name

class Pair(models.Model):
    exchange = models.ForeignKey(Exchange, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=20, null=True, blank=True)
    last_price = models.DecimalField(max_digits=10, decimal_places=5, default=0.0)
    price_change = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    volume_change = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)

    @classmethod
    def create(cls, *args, **kwargs):
        if 'exchange' not in kwargs:
            kwargs['exchange'] = 'binance'
        pair = cls(**kwargs)
        return pair

    def __str__(self):
        return f"<{self.exchange.name}|{self.name}|{self.last_price}>"
    

