from rest_framework import viewsets
from .serializers import *
from .models import *
from django_filters.rest_framework import DjangoFilterBackend

class CoinPairViewSet(viewsets.ModelViewSet):
    queryset = CoinPair.objects.all()
    serializer_class = CoinPairSerializer

class CoinDataViewSet(viewsets.ModelViewSet):
    queryset = CoinData.objects.all().order_by('-closeTime')
    serializer_class = CoinDataSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ("pair",)

class ExecutedTradeViewSet(viewsets.ModelViewSet):
    queryset = ExecutedTrade.objects.all().order_by('-id')
    serializer_class = ExecutedTradeSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ("coinData__pair",)
