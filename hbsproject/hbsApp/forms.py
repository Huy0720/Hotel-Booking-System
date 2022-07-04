from dataclasses import fields
from tkinter.ttk import Widget
from django import forms
from .models import *
from .views import * 
from django.forms import ModelForm

class DateInput(forms.DateInput):
    input_type = 'date'


class SearchDestinationForm(forms.ModelForm):
    class Meta:
        model = SearchDestination
        fields = ["country","people","checkin_date", "checkout_date"]
        widgets = {
            'checkin_date' : DateInput(),
            'checkout_date' : DateInput()
        }

    def clean(self):
        cleaned_data = super().clean()
        checkin_date = cleaned_data.get("checkin_date")
        checkout_date = cleaned_data.get("checkout_date")
        if checkin_date > checkout_date:
            raise forms.ValidationError("Checkin date should be lesser than Checkout date.")