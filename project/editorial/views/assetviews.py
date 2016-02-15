""" Media Asset handling views for editorial app.

    editorial/views/assetviews.py
"""

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
    ImageAssetForm,
    AddImageForm,)

from editorial.models import (
    WebFacet,
    PrintFacet,
    AudioFacet,
    VideoFacet,
    ImageAsset,)

#----------------------------------------------------------------------#
#   Upload Image Asset Views
#----------------------------------------------------------------------#

def upload_webfacet_image(request):
    """ Add image to a webfacet."""

    if request.method == 'POST':
        imageform=ImageAssetForm(request.POST, request.FILES)
        if imageform.is_valid():
            webimage = imageform.save(commit=False)
            # retrieve the webfacet the image should be associated with
            webfacet_id = request.POST.get('webfacet')
            webfacet = get_object_or_404(WebFacet, id=webfacet_id)
            # set request based attributes
            webimage.owner = request.user
            webimage.organization = request.user.organization
            webimage.save()
            # add image asset to webfacet image_assets
            webfacet.image_assets.add(webimage)
            webfacet.save()
    return redirect('story_detail', pk=webfacet.story.id)

def upload_printfacet_image(request):
    """ Add image to a printfacet."""

    if request.method == 'POST':
        imageform=ImageAssetForm(request.POST, request.FILES)
        if imageform.is_valid():
            printimage = imageform.save(commit=False)
            # retrieve the printfacet the image should be associated with
            printfacet_id = request.POST.get('printfacet')
            printfacet = get_object_or_404(PrintFacet, id=printfacet_id)
            # set request based attributes
            printimage.owner = request.user
            printimage.organization = request.user.organization
            printimage.save()
            # add image asset to printfacet image_assets
            printfacet.image_assets.add(printimage)
            printfacet.save()
    return redirect('story_detail', pk=printfacet.story.id)

def upload_audiofacet_image(request):
    """ Add image to a audiofacet."""

    if request.method == 'POST':
        imageform=ImageAssetForm(request.POST, request.FILES)
        if imageform.is_valid():
            audioimage = imageform.save(commit=False)
            # retrieve the audiofacet the image should be associated with
            audiofacet_id = request.POST.get('audiofacet')
            audiofacet = get_object_or_404(AudioFacet, id=audiofacet_id)
            # set request based attributes
            audioimage.owner = request.user
            audioimage.organization = request.user.organization
            audioimage.save()
            # add image asset to audiofacet image_assets
            audiofacet.image_assets.add(audioimage)
            audiofacet.save()
    return redirect('story_detail', pk=audiofacet.story.id)

def upload_videofacet_image(request):
    """ Add image to a videofacet."""

    if request.method == 'POST':
        imageform=ImageAssetForm(request.POST, request.FILES)
        if imageform.is_valid():
            videoimage = imageform.save(commit=False)
            # retrieve the videofacet the image should be associated with
            videofacet_id = request.POST.get('videofacet')
            videofacet = get_object_or_404(VideoFacet, id=videofacet_id)
            # set request based attributes
            videoimage.owner = request.user
            videoimage.organization = request.user.organization
            videoimage.save()
            # add image asset to videofacet image_assets
            videofacet.image_assets.add(videoimage)
            videofacet.save()
    return redirect('story_detail', pk=videofacet.story.id)


#----------------------------------------------------------------------#
#   Add Image Asset Views
#----------------------------------------------------------------------#

def add_webfacet_image(request):
    """ Add existing image(s) in the library to another webfacet."""

    if request.method == "POST":
        add_image_form = AddImageForm(request.POST, request=request)
        if add_image_form.is_valid():
            webfacet_id = request.POST.get('webfacet')
            print "WEBFACETid: ", webfacet_id
            webfacet = get_object_or_404(WebFacet, id=webfacet_id)
            images = request.POST.getlist('images')
            print "IMAGES: ", images
            for image in images:
                img_ins = get_object_or_404(ImageAsset, id=image)
                print "IMGins: ", img_ins
                webfacet.image_assets.add(img_ins)
            webfacet.save()
    return redirect('story_detail', pk=webfacet.story.id)


def add_printfacet_image(request):
    """ Add existing image(s) in the library to another printfacet."""

    if request.method == "POST":
        add_image_form = AddImageForm(request.POST, request=request)
        if add_image_form.is_valid():
            printfacet_id = request.POST.get('printfacet')
            print "printFACETid: ", printfacet_id
            printfacet = get_object_or_404(PrintFacet, id=printfacet_id)
            images = request.POST.getlist('images')
            print "IMAGES: ", images
            for image in images:
                img_ins = get_object_or_404(ImageAsset, id=image)
                print "IMGins: ", img_ins
                printfacet.image_assets.add(img_ins)
            printfacet.save()
    return redirect('story_detail', pk=printfacet.story.id)


def add_audiofacet_image(request):
    """ Add existing image(s) in the library to another audiofacet."""

    if request.method == "POST":
        add_image_form = AddImageForm(request.POST, request=request)
        if add_image_form.is_valid():
            audiofacet_id = request.POST.get('audiofacet')
            print "audioFACETid: ", audiofacet_id
            audiofacet = get_object_or_404(AudioFacet, id=audiofacet_id)
            images = request.POST.getlist('images')
            print "IMAGES: ", images
            for image in images:
                img_ins = get_object_or_404(ImageAsset, id=image)
                print "IMGins: ", img_ins
                audiofacet.image_assets.add(img_ins)
            audiofacet.save()
    return redirect('story_detail', pk=audiofacet.story.id)


def add_videofacet_image(request):
    """ Add existing image(s) in the library to another videofacet."""

    if request.method == "POST":
        add_image_form = AddImageForm(request.POST, request=request)
        if add_image_form.is_valid():
            videofacet_id = request.POST.get('videofacet')
            print "videoFACETid: ", videofacet_id
            videofacet = get_object_or_404(VideoFacet, id=videofacet_id)
            images = request.POST.getlist('images')
            print "IMAGES: ", images
            for image in images:
                img_ins = get_object_or_404(ImageAsset, id=image)
                print "IMGins: ", img_ins
                videofacet.image_assets.add(img_ins)
            videofacet.save()
    return redirect('story_detail', pk=videofacet.story.id)
