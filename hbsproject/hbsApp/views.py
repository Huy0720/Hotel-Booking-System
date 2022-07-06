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

def saveitem(request):
    if request.method == "POST":
        if request.POST.get(['country','people','checkin_date','checkout_date']):
            savevalue=SearchDestination()
            savevalue.country = request.POST.get('country')
            savevalue.people = request.POST.get('people')
            savevalue.checkin_date = request.POST.get('checkin_date')
            savevalue.checkout_date = request.POST.get('checkout_date')
            savevalue.save()
            messages.success(request, 'Redirecting to suitable hotels based on your search')
            return render(request,'home.html')
    else:
        return render(request,'home.html')

def index(request):
    template = "templates/index.html"
    return render(request, template)