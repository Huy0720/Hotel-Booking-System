from asyncio.constants import DEBUG_STACK_DEPTH
from re import template
from warnings import catch_warnings
from django.shortcuts import render
from django.views.generic import CreateView
from .forms import *
from django.urls import reverse_lazy
from .forms import SearchDestinationForm
from .models import *
from django.contrib import messages
import json
from re import template
import requests
from django.views import generic

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


def hotelList(request):
    template = "HotelList.html"
    dest = request.POST 
    print(dest)
    print(dest['destination'])
    a = dest['destination']
    x = read_json()
    y = find_des_id(a,x)
    if y != False:
        z = concate_url(y)
        h = read_json_2(z)
        f = image_url(h)
    else:
        f = []
    # image_1 = f['image_details']['prefix']+'0'+f['image_details']['suffix']
    # hotelName_1=f['name']
    # hotelAddress_1 = f['address']
    # hotelRating_1 = f['rating']

    return render(request,template,{'hotel_list':f})



def read_json():
    with open("../destinations.json",'r',encoding='UTF-8') as load_f:
        j = json.load(load_f)
    return j

def find_des_id(des, des_l):
    for i in des_l:
        try:
            if i['term'] == des:
                return i['uid']
        except:
            return False
    return False

def concate_url(des_id):
    url = 'https://hotelapi.loyalty.dev/api/hotels?destination_id='+des_id
    return url

def read_json_2(url):
    load_f=requests.get(url).text
    state = json.loads(load_f)
    # print(state[3])
    # print(state[3]['id'])
    # print(state[3]['name'])
    # print(state[3]['address'])
    # print(state[3]['rating'])
    # print(state[3]['image_details']['prefix'])
    # print(state[3]['image_details']['count'])
    # print(state[3]['image_details']['suffix'])

    # print(state[3]['image_details']['suffix'])
    return state

# x = read_json()
# y = find_des_id('London, England, UK (LGW-Gatwick)',x)
# z = concate_url(y)
# read_json_2(z)

def image_url(state):
    for i in state:
        im_url = i['image_details']['prefix']+'0'+i['image_details']['suffix']
        i['image_url'] = im_url
    return state