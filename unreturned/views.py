from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
# test
def show_unreturned_items(response):
    return HttpResponse("This is where unreturned items should show.")