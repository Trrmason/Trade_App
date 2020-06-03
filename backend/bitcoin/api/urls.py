from django.urls import path, include
from rest_framework import routers
from .views import *

router = routers.DefaultRouter()
router.register(r'coin_pair', CoinPairViewSet)
router.register(r'coin_data', CoinDataViewSet)
router.register(r'executed_trade', ExecutedTradeViewSet)
urlpatterns = [
    path('', include(router.urls)),
]