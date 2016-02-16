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

# from editorial.forms import (
# )

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

    # story = request.POST.get('story')
    # select_all = request.POST.get('select_all')
    # webfacet_sa = request.POST.get('webfacet_sa')
    # printfacet_sa = request.POST.get('printfacet_sa')
    # audiofacet_sa = request.POST.get('audiofacet_sa')
    # videofacet_sa = request.POST.get('videofacet_sa')
    #
    # # handle webfacet
    # webfacet = story.webfacetstory.all
    # if webfacet_sa:
    #     webfacet_images = WebFacet.get_webfacet_images(webfacet)
    #
    # # handle printfacet
    # printfacet = story.printfacetstory.all
    # if printfacet_sa:
    #     printfacet_images = PrintFacet.get_printfacet_images(printfacet)
    #
    # # handle audiofacet
    # audiofacet = story.audiofacetstory.all
    # if audiofacet_sa:
    #     audiofacet_images = AudioFacet.get_audiofacet_images(audiofacet)
    #
    # # handle videofacet
    # videofacet = story.videofacetstory.all
    # if videofacet_sa:
    #     videofacet_images = VideoFacet.get_videofacet_images(videofacet)
    #
    # images = request.POST.getlist('images')

    pass
