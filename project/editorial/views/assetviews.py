""" Media Asset handling views for editorial app.

    editorial/views/assetviews.py
"""

# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponse
from django.utils import timezone
from django.views.generic import TemplateView , UpdateView, DetailView
from django.views.decorators.csrf import csrf_exempt
import datetime
import json
from actstream import action

from editorial.forms import (
    ImageAssetForm,
    AddImageForm,
    DocumentAssetForm,
    AddDocumentForm,
    AudioAssetForm,
    AddAudioForm,
    VideoAssetForm,
    AddVideoForm,
    )

from editorial.models import (
    WebFacet,
    PrintFacet,
    AudioFacet,
    VideoFacet,
    ImageAsset,
    DocumentAsset,
    AudioAsset,
    VideoAsset)


#----------------------------------------------------------------------#
#   Asset Library Views
#----------------------------------------------------------------------#

def asset_library(request):
    """ Display media library of all organization assets."""

    images = ImageAsset.objects.filter(organization=request.user.organization)
    documents = DocumentAsset.objects.filter(organization=request.user.organization)
    audiofiles = AudioAsset.objects.filter(organization=request.user.organization)
    videos = VideoAsset.objects.filter(organization=request.user.organization)

    return render(request, 'editorial/assets.html', {
        'images': images,
        'documents': documents,
        'audiofiles': audiofiles,
        'videos': videos,
    })

#----------------------------------------------------------------------#
#   Asset Detail Views
#----------------------------------------------------------------------#

def image_asset_detail(request, pk):
    """ Display detail information for a specific image asset."""

    image = get_object_or_404(ImageAsset, id=pk)
    image_usage = image.get_image_usage()

    if request.method =="POST":
        editimageform = ImageAssetForm(data=request.POST, instance=image)
        if editimageform.is_valid():
            editimageform.save()
            #record action for activity stream
            action.send(request.user, verb="updated", action_object=image)
            return redirect('image_asset_detail', pk=image.id)
    else:
        editimageform = ImageAssetForm(instance=image)

    return render(request, 'editorial/assetdetail_image.html', {
        'image': image,
        'image_usage': image_usage,
        'editimageform': editimageform,
    })


def document_asset_detail(request, pk):
    """ Display detail information for a specific document asset."""

    document = get_object_or_404(DocumentAsset, id=pk)
    document_usage = DocumentAsset.get_document_usage(document)


    if request.method =="POST":
        editdocumentform = ImageDocumentForm(data=request.POST, instance=document)
        if editdocumentform.is_valid():
            editdocumentform.save()
            #record action for activity stream
            action.send(request.user, verb="updated", action_object=document)
            return redirect('asset_detail', pk=document.id)
    else:
        editdocumentform = DocumentAssetForm(instance=document)

    return render(request, 'editorial/assetdetail_document.html', {
        'document': document,
        'document_usage': document_usage,
        'editdocumentform': editdocumentform,
    })


def audio_asset_detail(request, pk):
    """ Display detail information for a specific audio asset."""

    audio = get_object_or_404(AudioAsset, id=pk)
    audio_usage = AudioAsset.get_audio_usage(audio)

    if request.method =="POST":
        editaudioform = AudioAssetForm(data=request.POST, instance=audio)
        if editaudioform.is_valid():
            editaudioform.save()
            #record action for activity stream
            action.send(request.user, verb="updated", action_object=audio)
            return redirect('asset_detail', pk=audio.id)
    else:
        editaudioform = AudioAssetForm(instance=audio)

    return render(request, 'editorial/assetdetail_audio.html', {
        'audio': audio,
        'audio_usage': audio_usage,
        'editaudioform': editaudioform,
    })


def video_asset_detail(request, pk):
    """ Display detail information for a specific video asset."""

    video = get_object_or_404(VideoAsset, id=pk)
    video_usage = VideoAsset.get_video_usage(video)

    if request.method =="POST":
        editvideoform = VideoAssetForm(data=request.POST, instance=video)
        if editvideoform.is_valid():
            editvideoform.save()
            #record action for activity stream
            action.send(request.user, verb="updated", action_object=video)
            return redirect('asset_detail', pk=video.id)
    else:
        editvideoform = VideoAssetForm(instance=video)

    return render(request, 'editorial/assetdetail_video.html', {
        'video': video,
        'video_usage': video_usage,
        'editvideoform': editvideoform,
    })


#----------------------------------------------------------------------#
#   Image Asset Views
#----------------------------------------------------------------------#

def upload_image(request):
    """ Add image to a facet."""

    if request.method == 'POST':
        imageform=ImageAssetForm(request.POST, request.FILES)
        if imageform.is_valid():
            image = imageform.save(commit=False)

            # retrieve the facet the image should be associated with
            facet_type = request.POST.get('type')
            if facet_type == "webfacet":
                facet_id = request.POST.get('webfacet')
                facet = get_object_or_404(WebFacet, id=facet_id)
            elif facet_type == "printfacet":
                facet_id = request.POST.get('printfacet')
                facet = get_object_or_404(PrintFacet, id=facet_id)
            elif facet_type == "audiofacet":
                facet_id = request.POST.get('audiofacet')
                facet = get_object_or_404(AudioFacet, id=facet_id)
            elif facet_type == "videofacet":
                facet_id = request.POST.get('videofacet')
                facet = get_object_or_404(VideoFacet, id=facet_id)

            # set request based attributes
            image.owner = request.user
            image.organization = request.user.organization
            image.save()

            # add image asset to facet image_assets
            facet.image_assets.add(image)
            facet.save()

            # record action for activity stream
            action.send(request.user, verb="uploaded image", action_object=image, target=facet)

    return redirect('story_detail', pk=facet.story.id)


def add_image(request):
    """ Add existing image(s) in the library to another facet."""

    if request.method == "POST":
        add_image_form = AddImageForm(request.POST, request=request)
        if add_image_form.is_valid():
            images = request.POST.getlist('images')

            # retrieve the facet the images should be associated with
            facet_type = request.POST.get('type')
            if facet_type == "webfacet":
                facet_id = request.POST.get('webfacet')
                facet = get_object_or_404(WebFacet, id=facet_id)
            elif facet_type == "printfacet":
                facet_id = request.POST.get('printfacet')
                facet = get_object_or_404(PrintFacet, id=facet_id)
            elif facet_type == "audiofacet":
                facet_id = request.POST.get('audiofacet')
                facet = get_object_or_404(AudioFacet, id=facet_id)
            elif facet_type == "videofacet":
                facet_id = request.POST.get('videofacet')
                facet = get_object_or_404(VideoFacet, id=facet_id)

            #create list of img instances
            img_instances = []
            # connect image to facet
            for image in images:
                img_ins = get_object_or_404(ImageAsset, id=image)
                img_instances.append(img_ins)
                facet.image_assets.add(img_ins)
            facet.save()

            action_image=get_object_or_404(ImageAsset, id=images[0])

            # record action for activity stream
            action.send(request.user, verb="added image", action_object=action_image, target=facet)

    return redirect('story_detail', pk=facet.story.id)


#----------------------------------------------------------------------#
#   Document Asset Views
#----------------------------------------------------------------------#

def upload_document(request):
    """ Add document to a facet."""

    if request.method == 'POST':
        documentform=DocumentAssetForm(request.POST, request.FILES)
        if documentform.is_valid():
            document = documentform.save(commit=False)

            # retrieve the facet the document should be associated with
            facet_type = request.POST.get('type')
            if facet_type == "webfacet":
                facet_id = request.POST.get('webfacet')
                facet = get_object_or_404(WebFacet, id=facet_id)
            elif facet_type == "printfacet":
                facet_id = request.POST.get('printfacet')
                facet = get_object_or_404(PrintFacet, id=facet_id)
            elif facet_type == "audiofacet":
                facet_id = request.POST.get('audiofacet')
                facet = get_object_or_404(AudioFacet, id=facet_id)
            elif facet_type == "videofacet":
                facet_id = request.POST.get('videofacet')
                facet = get_object_or_404(VideoFacet, id=facet_id)

            # set request based attributes
            document.owner = request.user
            document.organization = request.user.organization
            document.save()

            # add document asset to webfacet document_assets
            facet.document_assets.add(document)
            facet.save()

            # record action for activity stream
            action.send(request.user, verb="uploaded document", action_object=document, target=facet)

    return redirect('story_detail', pk=facet.story.id)


def add_document(request):
    """ Add existing document(s) in the library to another facet."""

    if request.method == "POST":
        add_document_form = AddDocumentForm(request.POST, request=request)
        if add_document_form.is_valid():
            documents = request.POST.getlist('documents')

            # retrieve the facet the document should be associated with
            facet_type = request.POST.get('type')
            if facet_type == "webfacet":
                facet_id = request.POST.get('webfacet')
                facet = get_object_or_404(WebFacet, id=facet_id)
            elif facet_type == "printfacet":
                facet_id = request.POST.get('printfacet')
                facet = get_object_or_404(PrintFacet, id=facet_id)
            elif facet_type == "audiofacet":
                facet_id = request.POST.get('audiofacet')
                facet = get_object_or_404(AudioFacet, id=facet_id)
            elif facet_type == "videofacet":
                facet_id = request.POST.get('videofacet')
                facet = get_object_or_404(VideoFacet, id=facet_id)

            # connect document to facet
            for document in documents:
                doc_ins = get_object_or_404(DocumentAsset, id=document)
                facet.document_assets.add(doc_ins)
            facet.save()

            action_doc = get_object_or_404(DocumentAsset, id=documents[0])

            # record action for activity stream
            action.send(request.user, verb="added document", action_object=action_doc, target=facet)

    return redirect('story_detail', pk=facet.story.id)


#----------------------------------------------------------------------#
#   Audio Asset Views
#----------------------------------------------------------------------#

def upload_audio(request):
    """ Add audio to a facet."""

    if request.method == 'POST':
        audioform=AudioAssetForm(request.POST, request.FILES)
        if audioform.is_valid():
            audio = audioform.save(commit=False)

            # retrieve the facet the audio should be associated with
            facet_type = request.POST.get('type')
            if facet_type == "webfacet":
                facet_id = request.POST.get('webfacet')
                facet = get_object_or_404(WebFacet, id=facet_id)
            elif facet_type == "printfacet":
                facet_id = request.POST.get('printfacet')
                facet = get_object_or_404(PrintFacet, id=facet_id)
            elif facet_type == "audiofacet":
                facet_id = request.POST.get('audiofacet')
                facet = get_object_or_404(AudioFacet, id=facet_id)
            elif facet_type == "videofacet":
                facet_id = request.POST.get('videofacet')
                facet = get_object_or_404(VideoFacet, id=facet_id)

            # set request based attributes
            audio.owner = request.user
            audio.organization = request.user.organization
            audio.save()

            # add audio asset to webfacet audio_assets
            facet.audio_assets.add(audio)
            facet.save()

            # record action for activity stream
            action.send(request.user, verb="uploaded audio", action_object=audio, target=facet)

    return redirect('story_detail', pk=facet.story.id)


def add_audio(request):
    """ Add existing audio(s) in the library to another facet."""

    if request.method == "POST":
        add_audio_form = AddAudioForm(request.POST, request=request)
        if add_audio_form.is_valid():
            audio_list = request.POST.getlist('audio')

            # retrieve the facet the audio should be associated with
            facet_type = request.POST.get('type')
            if facet_type == "webfacet":
                facet_id = request.POST.get('webfacet')
                facet = get_object_or_404(WebFacet, id=facet_id)
            elif facet_type == "printfacet":
                facet_id = request.POST.get('printfacet')
                facet = get_object_or_404(PrintFacet, id=facet_id)
            elif facet_type == "audiofacet":
                facet_id = request.POST.get('audiofacet')
                facet = get_object_or_404(AudioFacet, id=facet_id)
            elif facet_type == "videofacet":
                facet_id = request.POST.get('videofacet')
                facet = get_object_or_404(VideoFacet, id=facet_id)

            # connect audio to facet
            for audio in audio_list:
                audio_ins = get_object_or_404(AudioAsset, id=audio)
                facet.audio_assets.add(audio_ins)
            facet.save()

            action_audio=get_object_or_404(AudioAsset, id=audio_list[0])

            # record action for activity stream
            action.send(request.user, verb="added audio", action_object=action_audio, target=facet)

    return redirect('story_detail', pk=facet.story.id)


#----------------------------------------------------------------------#
#   Video Asset Views
#----------------------------------------------------------------------#

def upload_video(request):
    """ Add video to a facet."""

    if request.method == 'POST':
        videoform=VideoAssetForm(request.POST, request.FILES)
        if videoform.is_valid():
            video = videoform.save(commit=False)

            # retrieve the facet the video should be associated with
            facet_type = request.POST.get('type')
            if facet_type == "webfacet":
                facet_id = request.POST.get('webfacet')
                facet = get_object_or_404(WebFacet, id=facet_id)
            elif facet_type == "printfacet":
                facet_id = request.POST.get('printfacet')
                facet = get_object_or_404(PrintFacet, id=facet_id)
            elif facet_type == "audiofacet":
                facet_id = request.POST.get('audiofacet')
                facet = get_object_or_404(AudioFacet, id=facet_id)
            elif facet_type == "videofacet":
                facet_id = request.POST.get('videofacet')
                facet = get_object_or_404(VideoFacet, id=facet_id)

            # set request based attributes
            video.owner = request.user
            video.organization = request.user.organization
            video.save()

            # add video asset to facet video_assets
            facet.video_assets.add(video)
            facet.save()

            # record action for activity stream
            action.send(request.user, verb="uploaded video", action_object=video, target=facet)

    return redirect('story_detail', pk=facet.story.id)


def add_video(request):
    """ Add existing video(s) in the library to another facet."""

    if request.method == "POST":
        add_video_form = AddVideoForm(request.POST, request=request)
        if add_video_form.is_valid():
            videos = request.POST.getlist('videos')

            # retrieve the facet the video should be associated with
            facet_type = request.POST.get('type')
            if facet_type == "webfacet":
                facet_id = request.POST.get('webfacet')
                facet = get_object_or_404(WebFacet, id=facet_id)
            elif facet_type == "printfacet":
                facet_id = request.POST.get('printfacet')
                facet = get_object_or_404(PrintFacet, id=facet_id)
            elif facet_type == "audiofacet":
                facet_id = request.POST.get('audiofacet')
                facet = get_object_or_404(AudioFacet, id=facet_id)
            elif facet_type == "videofacet":
                facet_id = request.POST.get('videofacet')
                facet = get_object_or_404(VideoFacet, id=facet_id)

            # connect video to facet
            for video in videos:
                video_ins = get_object_or_404(VideoAsset, id=video)
                facet.video_assets.add(video_ins)
            facet.save()

            action_video=get_object_or_404(VideoAsset, id=videos[0])

            # record action for activity stream
            action.send(request.user, verb="added video", action_object=action_video, target=facet)

    return redirect('story_detail', pk=facet.story.id)
