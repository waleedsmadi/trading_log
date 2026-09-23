from django.db import models
from django.contrib.auth.models import User



class Strategy(models.Model):
    user = models.ForeignKey(to=User, related_name='strategies', on_delete=models.CASCADE)
    title = models.CharField(max_length=200, verbose_name='Title')
    rules = models.TextField(verbose_name='Rules')
    balance = models.DecimalField(verbose_name='Balance', max_digits=12, decimal_places=2)
    test_days = models.IntegerField(verbose_name='Test Days')
    created_at = models.DateTimeField(verbose_name='Created At', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Updated At', auto_now=True)

    class Meta:
        ordering = ['-created_at',]
        constraints = [
            models.UniqueConstraint(name='uq_strategy_user_title', fields=['user', 'title']),
            models.CheckConstraint(name='chk_strategy_balance', condition=models.Q(balance__gte=5)),
            models.CheckConstraint(name='chk_strategy_test_days', condition=models.Q(test_days__gte=1))
        ]

        verbose_name = 'Strategy'
        verbose_name_plural = "Strategies"


        def __str__(self):
            return self.title

