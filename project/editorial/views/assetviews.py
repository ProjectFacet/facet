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
    AudioAsset)


#----------------------------------------------------------------------#
#   Asset Library Views
#----------------------------------------------------------------------#

def asset_library(request):
    """ Display media library of all organization assets."""

    images = ImageAsset.objects.filter(organization=request.user.organization)
    documents = DocumentAsset.objects.filter(organization=request.user.organization)
    audiofiles = AudioAsset.objects.filter(organization=request.user.organization)

    return render(request, 'editorial/assets.html', {
        'images': images,
        'documents': documents,
        'audiofiles': audiofiles,
    })

#----------------------------------------------------------------------#
#   Asset Detail Views
#----------------------------------------------------------------------#

def image_asset_detail(request, pk):
    """ Display detail information for a specific image asset."""

    image = get_object_or_404(ImageAsset, id=pk)
    image_usage = ImageAsset.get_image_usage(image)

    if request.method =="POST":
        editimageform = ImageAssetForm(data=request.POST, instance=image)
        if editimageform.is_valid():
            editimageform.save()
            return redirect('asset_detail', pk=image.id)
    else:
        editimageform = ImageAssetForm(instance=image)

    return render(request, 'editorial/imageassetdetail.html', {
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
            return redirect('asset_detail', pk=document.id)
    else:
        editdocumentform = DocumentAssetForm(instance=document)

    return render(request, 'editorial/documentassetdetail.html', {
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
            return redirect('asset_detail', pk=audio.id)
    else:
        editaudioform = AudioAssetForm(instance=audio)

    return render(request, 'editorial/audioassetdetail.html', {
        'audio': audio,
        'audio_usage': audio_usage,
        'editaudioform': editaudioform,
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

            for image in images:
                img_ins = get_object_or_404(ImageAsset, id=image)
                facet.image_assets.add(img_ins)
            facet.save()

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
            # retrieve the webfacet the document should be associated with
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
    return redirect('story_detail', pk=facet.story.id)


def add_document(request):
    """ Add existing document(s) in the library to another facet."""

    if request.method == "POST":
        add_document_form = AddDocumentForm(request.POST, request=request)
        if add_document_form.is_valid():
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

            documents = request.POST.getlist('documents')
            for document in documents:
                doc_ins = get_object_or_404(DocumentAsset, id=document)
                facet.document_assets.add(doc_ins)
            facet.save()
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
            # retrieve the webfacet the audio should be associated with
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
    return redirect('story_detail', pk=facet.story.id)


def add_audio(request):
    """ Add existing audio(s) in the library to another facet."""

    if request.method == "POST":
        add_audio_form = AddAudioForm(request.POST, request=request)
        if add_audio_form.is_valid():
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

            audio_list = request.POST.getlist('audio')
            for audio in audio_list:
                audio_ins = get_object_or_404(AudioAsset, id=audio)
                facet.audio_assets.add(audio_ins)
            facet.save()
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
            # add video asset to webfacet video_assets
            facet.video_assets.add(video)
            facet.save()
        else:
            print "VALID"
    return redirect('story_detail', pk=facet.story.id)


def add_video(request):
    """ Add existing video(s) in the library to another facet."""

    if request.method == "POST":
        add_video_form = AddVideoForm(request.POST, request=request)
        if add_video_form.is_valid():
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
            videos = request.POST.getlist('videos')
            for video in videos:
                video_ins = get_object_or_404(VideoAsset, id=video)
                facet.video_assets.add(video_ins)
            facet.save()
    return redirect('story_detail', pk=facet.story.id)
