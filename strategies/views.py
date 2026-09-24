from django.shortcuts import render, redirect, get_object_or_404
from .models import Strategy
from django.contrib.auth.decorators import login_required
from .forms import CreateStrategyForm
from django_ratelimit.decorators import ratelimit
from django.views.decorators.http import require_POST
from django.http import HttpResponseForbidden
from django.contrib import messages



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

            # Check if there is a duplicated title
            if Strategy.objects.filter(user=request.user, title=strategy.title).exists():
                create_strategy_form.add_error('title', f'This title `{strategy.title}` already exists!')
                return render(request, 'strategies/create_strategy.html', {'create_strategy_form': create_strategy_form})
            
            strategy.user = request.user
            strategy.save()
            return redirect('strategies:show_strategies_url')
        else:
            return render(request, 'strategies/create_strategy.html', {'create_strategy_form': create_strategy_form})
    return render(request, 'strategies/create_strategy.html', {'create_strategy_form': create_strategy_form})
    




@ratelimit(key='ip', method='POST', rate='10/m')
@login_required(login_url='login:login_view_url')
def edit_strategy(request, strategy_id):
    strategy = get_object_or_404(Strategy, pk=strategy_id)
    if strategy.user != request.user:
        return HttpResponseForbidden

    edit_strategy_form = CreateStrategyForm(instance=strategy)
    if request.method == 'POST':
        edit_strategy_form = CreateStrategyForm(request.POST, instance=strategy)
        if edit_strategy_form.is_valid():
            strategy = edit_strategy_form.save(commit=False)

            # Check if there is a duplicated title execept the current strategy!
            if Strategy.objects.filter(user=request.user, title=strategy.title).exclude(pk=strategy.pk).exists():
                edit_strategy_form.add_error('title', f'This title `{strategy.title}` already exists!')
                return render(request, 'strategies/edit_strategy.html', {'edit_strategy_form': edit_strategy_form})

            strategy.save()
            messages.success(request, 'The strategy has been updated!')
            return redirect('strategies:edit_strategy_url', strategy_id=strategy.pk)
        return render(request, 'strategies/edit_strategy.html', {'edit_strategy_form': edit_strategy_form})
    return render(request, 'strategies/edit_strategy.html', {'edit_strategy_form': edit_strategy_form})







@ratelimit(key='ip', method='POST', rate='10/m')
@login_required(login_url='login:login_view_url')
@require_POST
def remove_strategy(request, strategy_id):
    strategy = get_object_or_404(Strategy, pk=strategy_id)
    if strategy.user != request.user:
        return HttpResponseForbidden
    
    strategy.delete()
    return redirect('strategies:show_strategies_url')