from dataclasses import fields
from tkinter.ttk import Widget
from django import forms
from .models import *
from .views import * 
from django.forms import ModelForm

class DateInput(forms.DateInput):
    input_type = 'date'

Country_choices = [('destination search','Destination Search'),('india','India'),('china','China'),
('hong kong','Hong Kong'), 
('vietnam', 'Vietnam'),('new zealand', 'New Zealand'),]

class SearchDestinationForm(forms.ModelForm):
    class Meta:
        model = SearchDestination
        fields = ["country","people","checkin_date", "checkout_date"]
        widgets = {
            'checkin_date' : DateInput(),
            'checkout_date' : DateInput(),
            'country': forms.Select(choices=Country_choices),
        }
        
    

    def clean(self):
        cleaned_data = super().clean()
        checkin_date = cleaned_data.get("checkin_date")
        checkout_date = cleaned_data.get("checkout_date")
        if checkin_date > checkout_date:
            raise forms.ValidationError("Checkin date should be lesser than Checkout date.")