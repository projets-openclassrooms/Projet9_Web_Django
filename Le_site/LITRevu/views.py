from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Review


# Create your views here.
# def home(request):
#     return render(request, "base.html")

class HomeView(ListView):
    model = Review
    template_name = 'base.html'

