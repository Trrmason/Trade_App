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
        fields = ('id', 'decision','coinData')

    def to_representation(self,instance):
        self.fields['coinData'] = CoinDataSerializer(read_only=True)
        return super(ExecutedTradeSerializer, self).to_representation(instance)
