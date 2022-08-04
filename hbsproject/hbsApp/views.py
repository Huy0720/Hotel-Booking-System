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

from pymongo import MongoClient
import pymongo
from cryptography.fernet import Fernet

import re

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
        if currUser == None:
            # login(request,currUser)
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
    print(dest['hotel_name'])
    a = dest['hotel_name']
    b = dest['hotel_guest']
    c = dest['hotel_date']
    d = dest['hotel_rooms']
    e = int(dest['number1'])
    x = read_json()
    y = find_des_id(a,x)
    hotel_l = list()
    per_page = 5
    page_num = 0
    if y != False:
        api_1 = concate_url_1(y,b,c,d)
        api_1_return = read_json_1(api_1)
        hotel_total = [api_1_return['hotels'][i:i + per_page] for i in range(0, len(api_1_return['hotels']), per_page)]
        page_num = len(hotel_total)

        if e>=page_num:
            hotel_l = []
            return render(request,template,{'hotel_list':hotel_l,'book_dest':y,'book_date':c,'num_of_guest':b,'page_num':page_num,'hotel_rooms':d,'hotel_name':a ,'number1':e})

        elif e<=0:
            hotel_l = []
            return render(request,template,{'hotel_list':hotel_l,'book_dest':y,'book_date':c,'num_of_guest':b,'page_num':page_num,'hotel_rooms':d,'hotel_name':a ,'number1':e})

        else:
            api_1_return['hotels'] = hotel_total[e]

        
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
    return render(request,template,{'hotel_list':hotel_l,'book_dest':y,'book_date':c,'num_of_guest':b,'page_num':page_num,'hotel_rooms':d,'hotel_name':a ,'number1':e})


def hotelDetail(request):
    template = "HotelDetail.html"
    dest = request.POST
    print(dest)
    a = dest['hotel_info']
    b = dest['hotel_dest']
    c = dest['hotel_date']
    d = dest['hotel_guest']
    api_2 = concate_url_2(a)

    print(api_2)
    api_2_return = read_json_2(api_2)
    pattern = re.compile(r'<[^>]+>',re.S)
    api_2_return['description'] = pattern.sub('',api_2_return['description'] )
    api_2_return = image_url(api_2_return)
    api_2_return = image_url_more(api_2_return)
    api_3 = concate_url_3(b,d,c,a)
    print(api_3)
    api_3_return = read_json_1(api_3)
    return render(request,template,{'hotel_detail':api_2_return,'room_detail':api_3_return})

def check_out(request):
    template = "checkout.html"
    dest = request.POST
    room_type = dest['room_type']
    hotel_name = dest['hotel_name']
    return render(request, template,{'room_type':room_type, "hotel_name":hotel_name})

def booking_successful(request):
    template = "SuccessfulBooking.html"
    dest = request.POST
    key = Fernet.generate_key()
    info = {
            "Salutation": dest["salutation"] + ' '+ dest["fname"] + ' ' + dest["lname"],
            "Email": encrypt(dest["email"],key)[1],
            "Phone": encrypt(dest["phone"],key)[1],
            "Special Request": dest["message"],
            "Credit Card Number": encrypt(dest["card_number"],key)[1],
            "Expiry": dest["exp_month"] + ' ' + dest["exp_year"],
            "CVV/CVC": encrypt(dest["CVV"],key)[1],
            "Bliing Address": dest["billing_address"]
            }

    CONNECTION_STRING = "mongodb+srv://huy:sutd@cluster0.xifad.mongodb.net/?retryWrites=true&w=majority"
    client = MongoClient(CONNECTION_STRING)
    db = client.get_database("gfg")
    col = db.get_collection("details")
    col.insert_one(info)
    
    return render(request, template)

def encrypt(data, sym_key):
    #key = Fernet.generate_key()
    fernet = Fernet(sym_key)
    encMessage = fernet.encrypt(data.encode())
    hidden_data = hide_info(data)
    return [encMessage, hidden_data]

def decrypt(data, sym_key):
    fernet = Fernet(sym_key)
    decMessage = fernet.decrypt(data).decode()
    return decMessage

def hide_info(data):
    #Card Number
    if len(data) == 16 and "@" not in data:
        return data[0:6] + "******" + data[-4:]
    #Email
    elif "@" in data:
        return "****@gmail.com"
    #CCV
    elif len(data) == 3:
        return "***"
    #Phone Number
    else:
        remainder = len(data) - 4
        return ('*'*remainder + data[-4:]) 


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

def concate_url_1(des_id,num_guests,date,room_num):
    x = date
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
    if room_num == 1:
        url = 'https://hotelapi.loyalty.dev/api/hotels/prices?destination_id=' +des_id+ '&checkin='+start_date+'&'+'checkout='+end_date+'&lang=en_US&currency=SGD&country_code=SG&guests='+num_guests+'&partner_id=1'
    else:
        y = num_guests + '|'
        num_guests = y*int(room_num)
        url = 'https://hotelapi.loyalty.dev/api/hotels/prices?destination_id=' +des_id+ '&checkin='+start_date+'&'+'checkout='+end_date+'&lang=en_US&currency=SGD&country_code=SG&guests='+num_guests+'&partner_id=1'
    return url


def concate_url_2(hotel_id):
    url = 'https://hotelapi.loyalty.dev/api/hotels/'+hotel_id
    return url

def concate_url_3(des_id,num_guests,date,hotel_id):
    x = date
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
    url = 'https://hotelapi.loyalty.dev/api/hotels/'+hotel_id+'/price?destination_id=' +des_id+ '&checkin='+start_date+'&'+'checkout='+end_date+'&lang=en_US&currency=SGD&country_code=SG&guests='+num_guests+'&partner_id=1'
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

def image_url_more(i):
    im_url_1 = i['image_details']['prefix']+'1'+i['image_details']['suffix']
    i['image_url_1'] = im_url_1
    im_url_2 = i['image_details']['prefix']+'2'+i['image_details']['suffix']
    i['image_url_2'] = im_url_2
    im_url_3 = i['image_details']['prefix']+'3'+i['image_details']['suffix']
    i['image_url_3'] = im_url_3
    im_url_4 = i['image_details']['prefix']+'4'+i['image_details']['suffix']
    i['image_url_4'] = im_url_4
    return i


with open("../destinations_filtered.json",'r',encoding='UTF-8') as load_f:
        j = json.load(load_f)
        type_of_j =type(j)
print(type_of_j)

# x = concate_url_1('YD2Z','2','2022-07-28','2022-07-29')
# y = read_json_2(x)
# print(y['hotels'][0])