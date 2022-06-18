from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import PairSerializer
from .models import Pair

# Create your views here.

@api_view(['GET'])
def getPrices(request):
    pairs = Pair.objects.all()
    serializer = PairSerializer(pairs, many=True)
    return Response(serializer.data)

