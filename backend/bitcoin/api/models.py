from django.db import models
import datetime


class CoinPair(models.Model):
    pair = models.CharField(primary_key=True, max_length=50)
    def __str__(self):
        return self.pair

class CoinData(models.Model):
    pair = models.ForeignKey(CoinPair, on_delete=models.CASCADE)
    openTime = models.IntegerField()
    openPrice = models.DecimalField(max_digits=40, decimal_places=28)
    highPrice = models.DecimalField(max_digits=40, decimal_places=28)
    lowPrice = models.DecimalField(max_digits=40, decimal_places=28)
    closePrice = models.DecimalField(max_digits=40, decimal_places=28)
    volume = models.DecimalField(max_digits=40, decimal_places=28)
    closeTime = models.IntegerField()

    def __str__(self):
        time = datetime.datetime.fromtimestamp(round(self.closeTime/1000))
        return '{} --- {}  ---  {}'.format(self.pair,round(self.closePrice,12), time)

    class Meta:
        ordering = ['-closeTime']
        unique_together = [
            'closeTime',
            'openTime',
            'pair'
        ]

class ExecutedTrade(models.Model):
    coinData = models.ForeignKey(CoinData, on_delete=models.PROTECT)
    decision = models.IntegerField()
    
    def __str__(self):
        time = datetime.datetime.fromtimestamp(round(self.coinData.closeTime/1000))
        return '{} --- {} --- {}  ---  {}'.format('BUY' if int(self.decision) == 1 else "SELL",
                                                  self.coinData.pair,
                                                  round(self.coinData.closePrice,12), 
                                                  time)
