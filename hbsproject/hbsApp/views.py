from re import template
from django.shortcuts import render
from django.views.generic import CreateView
from .forms import *
from django.urls import reverse_lazy
from .forms import SearchDestinationForm
from .models import *
from django.contrib import messages

class HomeView(CreateView):
    template_name = 'home.html'
    form_class = SearchDestinationForm
    success_url = reverse_lazy("hbsApp:home")

    def form_valid(self, form):
        return super().form_valid(form) 

def index(request):
    template = "index.html"
    return render(request, template)

def login(request):
    template = "login.html"
    return render(request,template)

def register(request):
    template = "register.html"
    return render(request,template)

def bookHistory(request):
    template = "bookHistory.html"
    return render(request,template)