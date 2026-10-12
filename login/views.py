from django.shortcuts import render, redirect
from .forms import LoginForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django_ratelimit.decorators import ratelimit
from django.views.decorators.http import require_POST




@ratelimit(key='ip', method='POST', rate='10/m')
def login_view(request):
    if request.user.is_authenticated:
        return redirect('strategies:show_strategies_url')
    form = LoginForm()
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')


            user = authenticate(request=request, username=username, password=password)
            if not user:
                messages.error(request, 'Invalid login')
                return redirect('login:login_view_url')

            login(request, user)
            return redirect('strategies:show_strategies_url')
        else:
            return render(request, 'login/login.html', {'form': form})

    return render(request, 'login/login.html', {'form': form})



@ratelimit(key='ip', method='POST', rate='10/m')
@require_POST
def logout_view(request):
        logout(request)
        return redirect('login:login_view_url')