from django import forms
from django.forms import ModelForm
from home.models import *
from django.core.exceptions import ValidationError

class ReturnForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['item_pristine_quantity', 'item_damaged_quantity']
        


        