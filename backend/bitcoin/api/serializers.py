from rest_framework import serializers
from .models import CoinData, ExecutedTrade, CoinPair


class CoinPairSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CoinPair
        fields = '__all__'

class CoinDataSerializer(serializers.ModelSerializer):

    class Meta:
        model = CoinData
        fields = "__all__"

class ExecutedTradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExecutedTrade
        fields = "__all__"