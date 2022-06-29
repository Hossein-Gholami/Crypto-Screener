# import asyncio
import json
from django.conf import settings
from celery import shared_task
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from screener import redis_client, binance, symbols
from screener.models import Symbol

@shared_task  # (name='fetchPrices')
def fetch_publish_tickers():
    # ts = kucoin.fetch_tickers(symbols=['BTC/USDT', 'ETH/USDT'])
    # symbols = Symbol.objects.values_list('name', flat=True)
    hash_key = settings.APP_SPECIFIC_KEYS['screener']['tickers']
    tickers = redis_client.hgetall(hash_key)
    
    if len(tickers.keys())==0:
        return { 'detail': 'No tickers been subscribed yet!' }
    
    tickers = {ticker.decode():float(tickers[ticker]) for ticker in tickers.keys()}
    symbols = list(tickers.keys())
    tickers = binance.fetch_tickers(symbols=symbols)
    tickers = {symbol:tickers[symbol]['last'] for symbol in tickers.keys()}

    async_to_sync(get_channel_layer().group_send)(
        settings.STREAM_SOCKET_GROUP_NAME,
        {
            'type': 'send_tickers',
            'tickers': tickers,
        }
    )

    redis_client.hset(hash_key, mapping=tickers)

    return { 'tickers': tickers }

@shared_task
def db_update_tickers():
    Symbol.update_prices()
    return {'detail': 'Database is up-to-date!'}

# @shared_task  # (name='add_nums')
# def add(x,y):
#     result = 'result: %s' % str(x+y)
#     channel_layer = get_channel_layer()
#     async_to_sync(channel_layer.group_send)('chat_lalala', {
#         'type': 'chat_message',
#         'message': result,
#         'name': 'Hossein'
#     })
#     return x+y
