""" Download views for editorial app. """

from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponse
from django.utils import timezone
from django.views.generic import TemplateView , UpdateView, DetailView
from django.views.decorators.csrf import csrf_exempt
from cStringIO import StringIO
from zipfile import ZipFile
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

#TODO Refactor queries for better use of Django query methods

#----------------------------------------------------------------------#
#   Download View
#----------------------------------------------------------------------#

def create_download(request, pk):
    """ Process download form to collect objects and create download file."""

    # get the story and associated facets no matter what options are selected
    story_id = request.POST.get('story')
    print "StoryID: ", story_id
    story = get_object_or_404(Story, id=pk)
    webfacet = story.webfacetstory.all()
    printfacet = story.printfacetstory.all()
    audiofacet = story.audiofacetstory.all()
    videofacet = story.videofacetstory.all()
    if webfacet:
        webfacet = webfacet[0]
    if printfacet:
        printfacet = printfacet[0]
    if audiofacet:
        audiofacet = audiofacet[0]
    if videofacet:
        videofacet = videofacet[0]

    # ------------------------------ #
    #          IF SELECT ALL         #
    # ------------------------------ #

    # if select_all is chosen, then all items will be downloaded
    select_all = request.POST.get('select_all')
    print "select all: ", select_all

    if select_all:
        # collect all images
        all_images = []
        if webfacet:
            webfacet_images = WebFacet.get_webfacet_images(webfacet)
            all_images.extend(webfacet_images)
        if printfacet:
            printfacet_images = PrintFacet.get_printfacet_images(printfacet)
            all_images.extend(printfacet_images)
        if audiofacet:
            audiofacet_images = AudioFacet.get_audiofacet_images(audiofacet)
            all_images.extend(audiofacet_images)
        if videofacet:
            videofacet_images = VideoFacet.get_videofacet_images(videofacet)
            all_images.extend(videofacet_images)
        print "ALL Images: ", all_images

        # Zip up all facets and assets including story metadata
        #TODO Add zip up here of any items that exist
        # storymeta.txt
        # webfacet.txt
        # printfacet.txt
        # audiofacet.txt
        # videofacet.txt
        # images.txt
        # image1.jpg

    # user can also select download all items associated with certain facets
    # ------------------------------ #
    #        IF WEBFACET ALL         #
    # ------------------------------ #
    webfacet_sa = request.POST.get('webfacet_sa')
    print "WSA: ", webfacet_sa

    if webfacet_sa:
        webfacet_images = WebFacet.get_webfacet_images(webfacet)
        print "webfacet_images ", webfacet_images

        print "Zip up all webfacet content and assets"
        #TODO Add zip up here
        # storymeta.txt
        # webfacet.txt
        # images.txt
        # image1.jpg

    # ------------------------------ #
    #       IF PRINTFACET ALL        #
    # ------------------------------ #
    printfacet_sa = request.POST.get('printfacet_sa')
    print "PSA: ", printfacet_sa

    if printfacet_sa:
        printfacet_images = PrintFacet.get_printfacet_images(printfacet)
        print "printfacet_images: ", printfacet_images
        print "Zip up all printfacet content and assets"
        #TODO Add zip up here
        # storymeta.txt
        # printfacet.txt
        # images.txt
        # image1.jpg

    # ------------------------------ #
    #       IF AUDIOFACET ALL        #
    # ------------------------------ #
    audiofacet_sa = request.POST.get('audiofacet_sa')
    print "ASA: ", audiofacet_sa

    if audiofacet_sa:
        audiofacet_images = AudioFacet.get_audiofacet_images(audiofacet)
        print "audiofacet_images: ", audiofacet_images
        print "Zip up all audiofacet content and assets"
        #TODO Add zip up here
        # storymeta.txt
        # audiofacet.txt
        # images.txt
        # image1.jpg

    # ------------------------------ #
    #       IF VIDEOFACET ALL        #
    # ------------------------------ #
    videofacet_sa = request.POST.get('videofacet_sa')
    print "VDS: ", videofacet_sa

    if videofacet_sa:
        videofacet_images = VideoFacet.get_videofacet_images(videofacet)
        print "videofacet_images", videofacet_images
        print "Zip up all videofacet content and assets"
        #TODO Add zip up here
        # storymeta.txt
        # videofacet.txt
        # images.txt
        # image1.jpg

    else:
    # if not select all OR facet select all, then user chooses the facet and the images
    # ------------------------------ #
    #      IF WEBFACET SPECIFIC      #
    # ------------------------------ #
        webfacet_only = request.POST.get('webfacet')
        if webfacet_only:
            print "Zip up webfacet content and meta."
            #TODO Add zip up here
            # storymeta.txt
            # webfacet.txt
    # ------------------------------ #
    #    IF PRINTFACET SPECIFIC      #
    # ------------------------------ #
        printfacet_only = request.POST.get('printfacet')
        if printfacet_only:
            print "Zip up printfacet content and meta."
            #TODO Add zip up here
            # storymeta.txt
            # printfacet.txt
    # ------------------------------ #
    #      IF AUDIOFACET SPECIFIC    #
    # ------------------------------ #
        audiofacet_only = request.POST.get('audiofacet')
        if audiofacet_only:
            print "Zip up audiofacet content and meta."
            #TODO Add zip up here
            # storymeta.txt
            # audiofacet.txt
    # ------------------------------ #
    #      IF VIDEOFACET SPECIFIC    #
    # ------------------------------ #
        videofacet_only = request.POST.get('videofacet')
        if videofacet_only:
            print "Zip up videofacet content and meta."
            #TODO Add zip up here
            # storymeta.txt
            # videofacet.txt
    # ------------------------------ #
    #       IF SPECIFIC IMAGES       #
    # ------------------------------ #
        # if not select all, then user chooses the facet and the images
        images = request.POST.getlist('images')
        images = ImageAsset.objects.filter(pk__in=images)
        print "Images: ", images
        if images:
            print "Zip up images and image meta."
            #TODO Add zip up here
            # imagemeta.txt
            # image1.jpg
            #image2.jpg

    # ------------------------------ #
    #         Create download        #
    # ------------------------------ #




    return redirect('story_detail', pk=story.pk)
