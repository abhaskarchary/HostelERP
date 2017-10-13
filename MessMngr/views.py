from django.shortcuts import render
from django.http import HttpResponse
import re
# Create your views here.

def mess_home(request):
    return render(request, 'mess_home.html')

def add_items(request):
    return render(request, 'add_items.html')