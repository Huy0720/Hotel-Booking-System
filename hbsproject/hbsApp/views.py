from asyncio.constants import DEBUG_STACK_DEPTH
import imp
from re import template
from tkinter.messagebox import NO
from warnings import catch_warnings
from django.shortcuts import render, redirect
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
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate,login,logout

from django.http import JsonResponse
from django.template.loader import render_to_string
import time

class HomeView(CreateView):
    template_name = 'home.html'
    form_class = SearchDestinationForm
    success_url = reverse_lazy("hbsApp:home")

    def form_valid(self, form):
        return super().form_valid(form) 

def json_view(request):
    with open("../destinations_filtered.json",'r',encoding='UTF-8') as load_f:
        j = json.load(load_f)
    return JsonResponse(j, safe=False)

def index(request):
    template = "index.html"  
    return render(request, template)


def login(request):
    template = "login.html"
    if request.method=='POST':
        emailadd = request.POST["emailadd"]
        passwd = request.POST["passwd"]
        currUser = authenticate(username= emailadd,password= passwd)
        print(passwd)
        print(currUser)
        if currUser != None:
            login(request,currUser)
            return redirect('./index')
        else:
            return redirect('./register')
    return render(request,template)

def register(request):
    template = "register.html"

    if request.method == "POST":
        emailid = request.POST["email"]
        password = request.POST["password"]
        passwordrepeat = request.POST["passwordrepeat"]

        if password == passwordrepeat:
            newcustomer = User(username= emailid,email= emailid, password= passwordrepeat)
            newcustomer.save()
            profile = Profile(user = newcustomer)
            profile.save()
            return redirect('./index')
        else:
            return redirect('./register')
    return render(request,template)

def logout_call(request):
    logout(request)
    return redirect('./login')

def bookHistory(request):
    template = "bookHistory.html"
    return render(request,template)


def hotelList(request):
    template = "HotelList.html"
    dest = request.POST
    print(dest)
    print(dest['destination'])
    a = dest['destination']
    b = dest['number2']
    c = dest['date1']
    x = read_json()
    y = find_des_id(a,x)
    hotel_l = list()
    if y != False:
        api_1 = concate_url_1(y,b,c)
        api_1_return = read_json_1(api_1)
        for i in api_1_return['hotels']:
            try:
                api_2 = concate_url_2(i['id'])
                print(api_2)
                api_2_return = read_json_2(api_2)
                hotel = image_url(api_2_return)
                hotel.update(i)
                hotel_l.append(hotel)
            except:
                time.sleep(0.005)
                continue
    else:
        hotel_l = []
    return render(request,template,{'hotel_list':hotel_l})


def hotel_list_2(request):
    return


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

def concate_url_1(des_id,num_guests,date):
    x = date
    print(x)
    l = list()
    l.append(x.split(' ')[0])
    l.append(x.split(' ')[1])
    l.append(x.split(' ')[8])
    l.append(x.split(' ')[9])

    date_dict = {'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'May': '05',
                'Jun': '06', 'Jul': '07', 'Aug': '08', 'Sep': '09', 'Oct': '10',
                'Nov': '10', 'Dec': '11'}
    start_month = l[1].split("-")
    start_date = '20'+start_month[1]+'-'+date_dict[start_month[0]]+'-'+l[0]
    end_month = l[3].split("-")
    end_date = '20'+end_month[1]+'-'+date_dict[end_month[0]]+'-'+l[2]
    url = 'https://hotelapi.loyalty.dev/api/hotels/prices?destination_id=' +des_id+ '&checkin='+start_date+'&'+'checkout='+end_date+'&lang=en_US&currency=SGD&country_code=SG&guests='+num_guests+'&partner_id=1'
    return url


def concate_url_2(hotel_id):
    url = 'https://hotelapi.loyalty.dev/api/hotels/'+hotel_id
    return url


def read_json_1(url):
    load_f=requests.get(url).text
    time.sleep(2)
    load_f=requests.get(url).text
    state = json.loads(load_f)
    return state

def read_json_2(url):
    load_f=requests.get(url).text
    state = json.loads(load_f)
    return state


def image_url(i):
    im_url = i['image_details']['prefix']+'0'+i['image_details']['suffix']
    i['image_url'] = im_url
    return i

with open("../destinations_filtered.json",'r',encoding='UTF-8') as load_f:
        j = json.load(load_f)
        type_of_j =type(j)
print(type_of_j)

# x = concate_url_1('YD2Z','2','2022-07-28','2022-07-29')
# y = read_json_2(x)
# print(y['hotels'][0])