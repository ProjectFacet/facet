from django.shortcuts import render
from django.http impor HttpResponse
# Create your views here.

def home(request):
    # return static homepage for now
    return render(request, 'editorial/home.html')
