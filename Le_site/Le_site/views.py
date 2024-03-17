from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout

from . import authentification, forms


def login_page(request):
    form = authentification.LoginForm()
    if request.method == 'POST':
        form = authentification.LoginForm(request.POST)
        if form.is_valid():
            pass
    return render(request, 'LITRevu/login.html', context={'form': form})