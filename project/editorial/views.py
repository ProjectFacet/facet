from django.shortcuts import render
from django.http impor HttpResponse
# Create your views here.

def index(request):
    return HttpResponse("Just starting views")
