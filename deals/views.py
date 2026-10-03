from django.shortcuts import render, redirect, get_object_or_404
from strategies.models import Strategy
from .models import Deal
from django.contrib.auth.decorators import login_required
from django_ratelimit.decorators import ratelimit
from django.http import HttpResponseForbidden
from .forms import CreateDealForm
from django.contrib import messages

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
                                                'strategy_id': strategy.pk,
                                                "the_rules": the_rules,
                                                "original_balance": original_balance,
                                                "nums_of_wining": nums_of_wining,
                                                "nums_of_losing": nums_of_losing,
                                                'current_balance': current_balance,
                                                "total_profit": total_profit,
                                                "total_loss": total_loss})
   


@ratelimit(key="ip", method="POST", rate="10/m")
@login_required(login_url="login:login_view_url")
def create_deal(request, strategy_id):
    strategy = get_object_or_404(Strategy, pk=strategy_id)

    if strategy.user != request.user:
        return HttpResponseForbidden()

    create_deal_form = CreateDealForm()

    if request.method == "POST":
        create_deal_form = CreateDealForm(request.POST, request.FILES)
        if create_deal_form.is_valid():
            deal = create_deal_form.save(commit=False)
            deal.strategy = strategy
            deal.save()
            return redirect('deals:show_deals_url', strategy_id=strategy.pk)
        else:
            return render(request, 'deals/create_deal.html', {'create_deal_form': create_deal_form})
    return render(request, 'deals/create_deal.html', {'create_deal_form': create_deal_form})



@ratelimit(key='ip', method='POST', rate='10/m')
@login_required(login_url='login:login_view_url')
def edit_deal(request, deal_id):
    deal = get_object_or_404(Deal, pk=deal_id)

    if deal.strategy.user != request.user:
        return HttpResponseForbidden()

    edit_deal_form = CreateDealForm(instance=deal)

    if request.method == "POST":
        edit_deal_form = CreateDealForm(request.POST, request.FILES, instance=deal)
        print("VALID:", edit_deal_form.is_valid())
        print("ERRORS:", edit_deal_form.errors)
        print("NON FIELD:", edit_deal_form.non_field_errors())
        if edit_deal_form.is_valid():
            edit_deal_form.save()
            messages.success(request, 'The deal has been updated!')
            return redirect('deals:edit_deal_url', deal_id=deal.pk)
        else:
            return render(request, 'deals/edit_deal.html', {'edit_deal_form': edit_deal_form, "strategy_id": deal.strategy.pk})

    return render(request, 'deals/edit_deal.html', {'edit_deal_form': edit_deal_form, "strategy_id": deal.strategy.pk})