from django.shortcuts import render, redirect
from .forms import LoginForm
from django.contrib.auth import login, authenticate
from django.contrib import messages



def login_view(request):
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
            messages.success(request, 'Success')
            return redirect('login:login_view_url')
        else:
            return render(request, 'login/login.html', {'form': form})

    return render(request, 'login/login.html', {'form': form})