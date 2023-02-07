import os
from django.shortcuts import render

ui = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'ui_resources')

def home(request):
    return render(request, os.path.join(ui, 'home.html'))