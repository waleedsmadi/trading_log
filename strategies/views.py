from django.shortcuts import render

# Create your views here.



def show_strategies(request):
    return render(request, 'strategies/strategies.html')