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
    template = "templates/index.html"
    return render(request, template)