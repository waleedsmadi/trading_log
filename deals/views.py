from django.shortcuts import render, redirect, get_object_or_404
from strategies.models import Strategy
from .models import Deal
from django.contrib.auth.decorators import login_required
from django_ratelimit.decorators import ratelimit
from django.http import HttpResponseForbidden


@login_required(login_url='login:login_view_url')
def show_deals(request, strategy_id):
    strategy = get_object_or_404(Strategy, pk=strategy_id)

    if strategy.user != request.user:
        return HttpResponseForbidden()

    deals = Deal.objects.filter(strategy=strategy)
    the_rules = strategy.rules

    original_balance = strategy.balance
    nums_of_wining = 0
    nums_of_losing = 0
    total_profit = 0
    total_loss = 0
    current_balance = original_balance

    for d in deals:
        if d.result == "PRF":
            nums_of_wining += 1
            current_balance += d.amount
            total_profit += d.amount
        elif d.result == "LOS":
            nums_of_losing += 1
            current_balance -= d.amount
            total_loss += d.amount

         

    return render(request, 'deals/deals.html', {'deals': deals,
                                                "the_rules": the_rules,
                                                "original_balance": original_balance,
                                                "nums_of_wining": nums_of_wining,
                                                "nums_of_losing": nums_of_losing,
                                                'current_balance': current_balance,
                                                "total_profit": total_profit,
                                                "total_loss": total_loss})
   
