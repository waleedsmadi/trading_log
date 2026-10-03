from django.urls import path
from . import views

app_name = 'deals'


urlpatterns = [
    path('<int:strategy_id>/', views.show_deals, name='show_deals_url'),
    path('<int:strategy_id>/create/', views.create_deal, name='create_deal_url'),
    path('<int:deal_id>/edit/', views.edit_deal, name='edit_deal_url'),
]
