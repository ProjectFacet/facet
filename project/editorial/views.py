from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def index(request):
    # return static homepage for now
    return render(request, 'editorial/home.html')
