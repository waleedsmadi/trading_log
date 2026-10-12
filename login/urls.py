from django.urls import path
from . import views
app_name = 'login'

urlpatterns = [
    path('login/', views.login_view, name='login_view_url'),
    path('logout/', views.logout_view, name='logout_view_url'),
]

