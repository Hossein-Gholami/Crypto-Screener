import redis
from django.conf import settings
import ccxt

redis_client = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)

binance = ccxt.binance()
_ = binance.load_markets()
symbols = binance.symbols

__all__ = ('redis_client', 'binance', 'symbols',)