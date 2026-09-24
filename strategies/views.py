from django.shortcuts import render, redirect
from .models import Strategy
from django.contrib.auth.decorators import login_required
from .forms import CreateStrategyForm
from django_ratelimit.decorators import ratelimit
from django.views.decorators.http import require_POST



@login_required(login_url='login:login_view_url')
def show_strategies(request):
    strats = Strategy.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'strategies/strategies.html', {'strats': strats})





@ratelimit(key='ip', method='POST', rate='10/m')
@login_required(login_url='login:login_view_url')
def create_strategy(request):
    create_strategy_form = CreateStrategyForm()
    if request.method == "POST":
        create_strategy_form = CreateStrategyForm(request.POST)
        if create_strategy_form.is_valid():
            strategy = create_strategy_form.save(commit=False)
            strategy.user = request.user
            strategy.save()
            return redirect('strategies:show_strategies_url')
        else:
            return render(request, 'strategies/create_strategy.html', {'create_strategy_form': create_strategy_form})
    return render(request, 'strategies/create_strategy.html', {'create_strategy_form': create_strategy_form})
    
