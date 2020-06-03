from django.contrib import admin
from django.contrib.admin import ModelAdmin
from .models import CoinData, ExecutedTrade, CoinPair
# Register your models here.

@admin.register(CoinData)
class CoinDataAdmin(admin.ModelAdmin):
    list_filter = ('pair__pair',)
    

admin.site.register(CoinPair)
#admin.site.register(CoinDataAdmin)
admin.site.register(ExecutedTrade)