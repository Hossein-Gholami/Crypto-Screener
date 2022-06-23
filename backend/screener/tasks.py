# import asyncio
import json
from django.conf import settings
from celery import shared_task
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from screener import binance, symbols
from screener.models import Symbol

@shared_task  # (name='fetchPrices')
def fetch_last_prices():
    # ts = kucoin.fetch_tickers(symbols=['BTC/USDT', 'ETH/USDT'])
    symbols = Symbol.objects.values_list('symbol_name', flat=True)
    if len(symbols)==0:
        return json.dumps({
            'detail': 'no symbols in database'
        })
    tickers = binance.fetch_tickers(symbols=symbols)
    last_prices = {symbol:tickers[symbol]['last'] for symbol in tickers.keys() }
    db_update_last_prices(last_prices)
    async_to_sync(get_channel_layer().group_send)(
        settings.STREAM_SOCKET_GROUP_NAME,
        {
            'type': 'send_prices',
            'tickers': json.dumps(last_prices),
        }
    )
    return json.dumps(last_prices)

def db_update_last_prices(last_prices):
    for _symbol in last_prices.keys():
        symbol = Symbol.objects.get(symbol_name=_symbol)
        symbol.last_price = last_prices[_symbol]
        symbol.save()

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
