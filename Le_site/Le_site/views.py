# authentication/views.py
from django.shortcuts import render

from . import authentification


def login_page(request):
    form = authentification.LoginForm()
    if request.method == 'POST':
        form = authentification.LoginForm(request.POST)
        if form.is_valid():
            pass
    return render(request, 'authentication/login.html', context={'form': form})