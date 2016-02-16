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

from editorial.forms import StoryDownloadForm

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

def create_download(request, pk):
    """ Process download form to collect objects and create download file."""

    # get the story id no matter what options are selected
    story_id = request.POST.get('story')
    print "StoryID: ", story_id

    # if select_all is chosen, then all items will be downloaded
    select_all = request.POST.get('select_all')
    print "select all: ", select_all

    # user can also select to download all items associated with certain facets
    webfacet_sa = request.POST.get('webfacet_sa')
    printfacet_sa = request.POST.get('printfacet_sa')
    audiofacet_sa = request.POST.get('audiofacet_sa')
    videofacet_sa = request.POST.get('videofacet_sa')
    print "WSA: ", webfacet_sa
    print "PSA: ", printfacet_sa
    print "ASA: ", audiofacet_sa
    print "VDS: ", videofacet_sa

    # if not select all, then user chooses the facet and the images
    images = request.POST.getlist('images')
    print "Images: ", images

    story = get_object_or_404(Story, id=pk)
    webfacet = story.webfacetstory.all()
    printfacet = story.printfacetstory.all()
    audiofacet = story.audiofacetstory.all()
    videofacet = story.videofacetstory.all()
    print "facets: ", webfacet, printfacet, audiofacet, videofacet

    if select_all:
        # collect all images
        d_images = []
        if webfacet:
            webfacet_images = WebFacet.get_webfacet_images(webfacet[0])
            d_images.extend(webfacet_images)
        if printfacet:
            printfacet_images = PrintFacet.get_printfacet_images(printfacet[0])
            d_images.extend(printfacet_images)
        if audiofacet:
            audiofacet_images = AudioFacet.get_audiofacet_images(audiofacet[0])
            d_images.extend(audiofacet_images)
        if videofacet:
            videofacet_images = VideoFacet.get_videofacet_images(videofacet[0])
            d_images.extend(videofacet_images)
        print "DImages: ", d_images

    elif webfacet and webfacet_sa:
        webfacet_images = WebFacet.get_webfacet_images(webfacet[0])
        print "webfacet_images", webfacet_images

    elif printfacet and printfacet_sa:
        printfacet_images = PrintFacet.get_printfacet_images(printfacet[0])
        print "printfacet_images", printfacet_images

    elif audiofacet and audiofacet_sa:
        audiofacet_images = AudioFacet.get_audiofacet_images(audiofacet[0])
        print "audiofacet_images", audiofacet_images

    elif videofacet and videofacet_sa:
        videofacet_images = VideoFacet.get_videofacet_images(videofacet[0])
        print "videofacet_images", videofacet_images

    # elif: #only specific items selected


    return render(request, 'editorial/test.html')
