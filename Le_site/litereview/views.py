from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.template import loader


# Create your views here.
def index(request):
    template = loader.get_template('base.html')
    return HttpResponse(template.render())
