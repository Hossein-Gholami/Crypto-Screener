# from django.shortcuts import render
# from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

# from asgiref.sync import async_to_sync
# from channels.layers import get_channel_layer

from .serializers import SymbolSerializer
from .models import Symbol
from screener import binance, symbols

# Create your views here.

@api_view(['GET'])
def getStat(request):
    symbols = Symbol.objects.all()
    serializer = SymbolSerializer(symbols, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def addSymbol(request):
    data = request.data
    if data['name'] not in symbols:
        message = {'detail':'Binance doesn\' have this pair!'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
    _symbol = None
    if data['name'] in Symbol.objects.values_list('symbol_name', flat=True):
        _symbol = Symbol.objects.get(symbol_name=data['name'])
    else:
        last_price = binance.fetch_ticker(data['name'])['last']
        _symbol = Symbol.objects.create(symbol_name=data['name'], last_price=last_price)
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
