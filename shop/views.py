from django.shortcuts import render
from django.views.generic import ListView, DetailView, View

from shop.models import Item

# Create your views here.
class homePage(ListView):
    model = Item
    paginate_by=2
    template_name='home.html'