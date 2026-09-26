from django.db import models
from strategies.models import Strategy
from django.db.models import Q, F

class DealType(models.TextChoices):
    BUY = "BUY", "Buy"
    SELL = "SELL", "Sell"



class Pairs(models.TextChoices):
    XAU_USD = "XAUUSD", "XAU/USD"
    EUR_GBP = "EURGBP", "EUR/GBP"
    EUR_JPY = "EURJPY", "EUR/JPY"
    EUR_AUD = "EURAUD", "EUR/AUD"
    EUR_CHF = "EURCHF", "EUR/CHF"
    EUR_USD = "EURUSD", "EUR/USD"
    GBP_CHF = "GBPCHF", "GBP/CHF"
    AUD_JPY = "AUDJPY", "AUD/JPY"
    CAD_JPY = "CADJPY", "CAD/JPY"
    NZD_JPY = "NZDJPY", "NZD/JPY"
    USD_TRY = "USDTRY", "USD/TRY"
    USD_ZAR = "USDZAR", "USD/ZAR"
    USD_MXN = "USDMXN", "USD/MXN"
    USD_SGD = "USDSGD", "USD/SGD"
    USD_NOK = "USDNOK", "USD/NOK"

class Result(models.TextChoices):
    profit = "PRF", "Profit"
    loss = "LOS", "Loss"

class Deal(models.Model):
    strategy = models.ForeignKey(
        to=Strategy,
        on_delete=models.CASCADE,
        related_name='deals',
    )


    deal_type = models.CharField(max_length=10, verbose_name='Deal Type', choices=DealType.choices)
    pair = models.CharField(max_length=8, verbose_name='Pair', choices=Pairs.choices)
    from_price = models.DecimalField(verbose_name='From Price', max_digits=8, decimal_places=2)
    to_price = models.DecimalField(verbose_name='To Price', max_digits=10, decimal_places=2)
    is_followed_rules = models.BooleanField(verbose_name='Is Followed Rules', default=True)
    description = models.TextField(verbose_name='Description', null=True, blank=True)
    img = models.ImageField(verbose_name='Chart Image', upload_to='chart/images/%Y%m%d', null=True, blank=True)
    result = models.BooleanField(verbose_name='Result', choices=Result.choices)
    amount = models.DecimalField(verbose_name='Amount', max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(verbose_name='Created At', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Updated At', auto_now=True)


    class Meta:
        ordering = ['-created_at',]
        constraints = [
            models.CheckConstraint(name='chk_deal_from_price_to_price', condition=(
                (Q(from_price__lt=F('to_price')) & Q(deal_type=DealType.BUY)) | 
                (Q(from_price__gt=F('to_price')) & Q(deal_type=DealType.SELL))
            )),

            models.CheckConstraint(name='chk_deal_from_price', condition=Q(from_price__gt=0)),
            models.CheckConstraint(name='chk_deal_to_price', condition=Q(to_price__gt=0)),
            models.CheckConstraint(name='chk_deal_amount', condition=Q(amount__gte=0)),
        ]

    def __str__(self):
        return f'{self.pair}  |  {self.deal_type}'
