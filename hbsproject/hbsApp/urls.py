from django.urls import path
from .views import *
from . import views

app_name = "hbsApp"
urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    #path('',views.saveitem),

]