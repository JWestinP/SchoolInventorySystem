# myapp/forms.py
from django import forms
from django.forms import ModelForm
from recents.models import Borrowed_Item
from .models import *
from django.core.exceptions import ValidationError


    
class SearchForm(forms.Form):
    search_query = forms.CharField(max_length=128, required=False)

class BorrowForm(forms.ModelForm):
    class Meta:
        model = Borrowed_Item
        fields = "__all__"
        
        widgets = {
            'item_date_borrowed' : forms.DateInput(attrs={'type': 'date'}),
            'item_date_returned' : forms.DateInput(attrs={'type': 'date'}),
            'item_stock' : forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['item_stock'].queryset = Stock.objects.all()
        
class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        exclude = ['item_id']
        
class StockForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = '__all__'

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'
