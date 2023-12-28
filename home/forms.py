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
        'item_id' : forms.HiddenInput(),
        'item_name' : forms.HiddenInput(),
        'item_photo' : forms.HiddenInput(),
        'item_borrower' : forms.HiddenInput(),
    }
        #exclude = ['item_id', 'item_name', 'item_returned', 'item_photo', 'item_borrower']