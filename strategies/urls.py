from django.urls import path
from . import views

app_name = 'strategies'

urlpatterns = [
    path('', views.show_strategies, name='show_strategies_url'),
    path('create/', views.create_strategy, name='create_strategy_url'),
]
