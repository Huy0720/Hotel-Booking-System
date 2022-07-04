from django.urls import path
from .views import *

app_nmae = "hbsApp"
urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    

]