""" Download views for editorial app. """

from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponse
from django.utils import timezone
from django.views.generic import TemplateView , UpdateView, DetailView
from django.views.decorators.csrf import csrf_exempt
import datetime
import json

from editorial.forms import (
)

from editorial.models import (
    Story,
    WebFacet,
    PrintFacet,
    AudioFacet,
    VideoFacet,
    ImageAsset,
)

#----------------------------------------------------------------------#
#   Download View
#----------------------------------------------------------------------#

def create_download(request):
    """ Process download form to collect objects and create download file."""

    # select_all = request.POST.get('select_all')
    # webfacet = request.POST.get('webfacet')
    # printfacet = request.POST.get('printfacet')
    # audiofacet = request.POST.get('audiofacet')
    # videofacet = request.POST.get('videofacet')
    # images = request.POST.getlist('images')

    pass
