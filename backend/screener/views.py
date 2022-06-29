# from django.shortcuts import render
# from django.http import HttpResponse
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

# from asgiref.sync import async_to_sync
# from channels.layers import get_channel_layer

from .serializers import SymbolSerializer
from .models import Symbol
from screener import redis_client, binance, symbols

# Create your views here.

# @api_view(['GET'])
# def getStat(request):
#     symbols = Symbol.objects.all()
#     serializer = SymbolSerializer(symbols, many=True)
#     return Response(serializer.data)

@api_view(['POST'])
def add(request):
    data = request.data
    name = data['name']
    if name not in symbols:
        message = {'detail': 'binance doesn\'t have this pair.'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)

    _symbol = Symbol.objects.filter(pk=name)
    if not _symbol.exists():
        price = binance.fetch_ticker(name)['last']
        _symbol = Symbol.objects.create(name=name, price=price)
    else:
        _symbol = _symbol.get()

    hash_key = settings.APP_SPECIFIC_KEYS['screener']['tickers']
    tickers = redis_client.hgetall(hash_key)
    tickers = {ticker.decode():float(tickers[ticker]) for ticker in tickers.keys()}
    tickers[str(_symbol.name)] = float(_symbol.price)
    redis_client.hset(hash_key, mapping=tickers)
    
    serializer = SymbolSerializer(_symbol, many=False)
    return Response(serializer.data)

# def index(request):
#     return render(request, 'screener/index.html', context={})

# def run(request):
#     add.apply_async((10, 13), countdown=5)
#     # # print(channel_layer.group_channels('chat_lalala'))
#     async_to_sync(get_channel_layer().group_send)('chat_lalala', {
#         'type': 'chat_message',
#         'message': 'RUNNING',
#         'name': 'Hossein'
#     })
#     return HttpResponse('task executed!')


# def room(request, room_name):
#     return render(request, 'screener/room.html', {'room_name': room_name})
