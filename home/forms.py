# myapp/forms.py
from django import forms
from django.forms import ModelForm
from recents.models import Borrowed_Item

class SearchForm(forms.Form):
    search_query = forms.CharField(max_length=128, required=False)

class BorrowForm(ModelForm):
    class Meta:
        model = Borrowed_Item
        fields = "__all__"
        
        widgets = {
        'item_date_borrowed' : forms.DateInput(attrs={'type': 'date'}),
        'item_date_returned' : forms.DateInput(attrs={'type': 'date'}),
        'item_stock': forms.HiddenInput(),
    }
    