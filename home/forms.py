# myapp/forms.py
from django import forms
from django.forms import ModelForm
from recents.models import Borrowed_Item
from .models import *
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

#Item search form
class SearchForm(forms.Form):
    search_query = forms.CharField(max_length=128, required=False)

#Item borrow form
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

#User form
class UserForm(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=User.objects.all(),
                                  widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['user']
        labels = {
            'user': 'User',
        }

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['user'].label_from_instance = lambda obj: f'{obj.id} - {obj.username}'

#Item addition form
class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        exclude = ['item_id']
        
#Item stock addition form 
class StockForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = '__all__'

#Category addition form
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'
