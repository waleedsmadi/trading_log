from django.urls import path
from . import views

app_name = 'deals'


urlpatterns = [
    path('<int:strategy_id>/', views.show_deals, name='show_deals_url'),
]
