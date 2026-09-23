from django.shortcuts import render
from .models import Strategy
from django.contrib.auth.decorators import login_required




@login_required(login_url='login:login_view_url')
def show_strategies(request):
    strats = Strategy.objects.filter(user=request.user)
    return render(request, 'strategies/strategies.html', {'strats': strats})