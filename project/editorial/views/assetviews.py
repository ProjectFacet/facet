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
from django.views.generic import TemplateView , UpdateView, DetailView, ListView
from django.views.decorators.csrf import csrf_exempt
import datetime
import json
from actstream import action

from editorial.forms import (
    ImageAssetForm,
    DocumentAssetForm,
    AudioAssetForm,
    VideoAssetForm,
    )

from editorial.models import (
    Facet,
    ImageAsset,
    DocumentAsset,
    AudioAsset,
    VideoAsset)


#----------------------------------------------------------------------#
#   Asset Library Views
#----------------------------------------------------------------------#

class AssetLibraryTemplateView(TemplateView):
    """ Display media library of all organization assets."""

    template_name = 'editorial/asset_list.html'

    def get_context_data(self):
        """Return all the (complex) assets associated with an organization."""

        organization = self.request.user.organization
        images = organization.get_org_image_library()
        documents = organization.get_org_document_library()
        audio = organization.get_org_audio_library()
        video = organization.get_org_video_library()
        return {'images': images, 'documents': documents, 'audio': audio, 'video': video,}


#----------------------------------------------------------------------#
#   Asset Detail Views
#----------------------------------------------------------------------#

class ImageAssetUpdateView(UpdateView):
    """ Display editable detail information for a specific image asset."""

    model = ImageAsset
    form_class = ImageAssetForm

    def image_usage(self):
        """Get all facets an image is associated with."""
        return self.object.get_image_usage()

    def get_success_url(self):
        """Record edit activity for activity stream."""

        action.send(self.request.user, verb="edited", action_object=self.object)
        return super(ImageAssetUpdateView, self).get_success_url()


class DocumentAssetUpdateView(UpdateView):
    """ Display editable detail information for a specific document asset."""

    model = DocumentAsset
    form_class = DocumentAssetForm

    def document_usage(self):
        """Get all facets a document is associated with."""
        return self.object.get_document_usage()

    def get_success_url(self):
        """Record edit activity for activity stream."""

        action.send(self.request.user, verb="edited", action_object=self.object)
        return super(DocumentAssetUpdateView, self).get_success_url()


class AudioAssetUpdateView(UpdateView):
    """ Display editable detail information for a specific audio asset."""

    model = AudioAsset
    form_class = AudioAssetForm

    def audio_usage(self):
        """Get all facets a audio is associated with."""
        return self.object.get_audio_usage()

    def get_success_url(self):
        """Record edit activity for activity stream."""

        action.send(self.request.user, verb="edited", action_object=self.object)
        return super(AudioAssetUpdateView, self).get_success_url()


class VideoAssetUpdateView(UpdateView):
    """ Display editable detail information for a specific video asset."""

    model = VideoAsset
    form_class = VideoAssetForm

    def video_usage(self):
        """Get all facets an video is associated with."""
        return self.object.get_video_usage()

    def get_success_url(self):
        """Record edit activity for activity stream."""

        action.send(self.request.user, verb="edited", action_object=self.object)
        return super(VideoAssetUpdateView, self).get_success_url()


#----------------------------------------------------------------------#
#   Image Asset Views
#----------------------------------------------------------------------#

def upload_image(request):
    """ Upload image to a facet."""

    if request.method == 'POST':
        imageform=ImageAssetForm(request.POST, request.FILES)
        if imageform.is_valid():
            image = imageform.save(commit=False)

            # retrieve the facet the image should be associated with
            facet_id = request.POST.get('facet')
            facet = get_object_or_404(Facet, id=facet_id)

            # set request based attributes
            image.owner = request.user
            image.organization = request.user.organization
            image.save()

            # add image asset to facet image_assets
            facet.image_assets.add(image)
            facet.save()

            # record action for activity stream
            action.send(request.user, verb="uploaded image", action_object=image, target=facet)

    return redirect('facet_edit', pk=facet.id)


def add_image(request):
    """ Add existing image(s) in the library to another facet."""

    if request.method == "POST":
        images = request.POST.getlist('images')

        # retrieve the facet the image should be associated with
        facet_id = request.POST.get('facet')
        facet = get_object_or_404(Facet, id=facet_id)

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

    return redirect('facet_edit', pk=facet.id)


#----------------------------------------------------------------------#
#   Document Asset Views
#----------------------------------------------------------------------#

def upload_document(request):
    """ Add document to a facet."""

    if request.method == 'POST':
        documentform=DocumentAssetForm(request.POST, request.FILES)
        if documentform.is_valid():
            document = documentform.save(commit=False)

            # retrieve the facet the image should be associated with
            facet_id = request.POST.get('facet')
            facet = get_object_or_404(Facet, id=facet_id)

            # set request based attributes
            document.owner = request.user
            document.organization = request.user.organization
            document.save()

            # add document asset to webfacet document_assets
            facet.document_assets.add(document)
            facet.save()

            # record action for activity stream
            action.send(request.user, verb="uploaded document", action_object=document, target=facet)

    return redirect('facet_edit', pk=facet.id)


def add_document(request):
    """ Add existing document(s) in the library to another facet."""

    if request.method == "POST":
        documents = request.POST.getlist('documents')

        # retrieve the facet the image should be associated with
        facet_id = request.POST.get('facet')
        facet = get_object_or_404(Facet, id=facet_id)

        # connect document to facet
        for document in documents:
            doc_ins = get_object_or_404(DocumentAsset, id=document)
            facet.document_assets.add(doc_ins)
        facet.save()

        action_doc = get_object_or_404(DocumentAsset, id=documents[0])

        # record action for activity stream
        action.send(request.user, verb="added document", action_object=action_doc, target=facet)

    return redirect('facet_edit', pk=facet.id)


#----------------------------------------------------------------------#
#   Audio Asset Views
#----------------------------------------------------------------------#

def upload_audio(request):
    """ Add audio to a facet."""

    if request.method == 'POST':
        audioform=AudioAssetForm(request.POST, request.FILES)
        if audioform.is_valid():
            audio = audioform.save(commit=False)

            # retrieve the facet the image should be associated with
            facet_id = request.POST.get('facet')
            facet = get_object_or_404(Facet, id=facet_id)

            # set request based attributes
            audio.owner = request.user
            audio.organization = request.user.organization
            audio.save()

            # add audio asset to webfacet audio_assets
            facet.audio_assets.add(audio)
            facet.save()

            # record action for activity stream
            action.send(request.user, verb="uploaded audio", action_object=audio, target=facet)

    return redirect('facet_edit', pk=facet.id)


def add_audio(request):
    """ Add existing audio(s) in the library to another facet."""

    if request.method == "POST":
        audio_list = request.POST.getlist('audio')

        # retrieve the facet the image should be associated with
        facet_id = request.POST.get('facet')
        facet = get_object_or_404(Facet, id=facet_id)

        # connect audio to facet
        for audio in audio_list:
            audio_ins = get_object_or_404(AudioAsset, id=audio)
            facet.audio_assets.add(audio_ins)
        facet.save()

        action_audio=get_object_or_404(AudioAsset, id=audio_list[0])

        # record action for activity stream
        action.send(request.user, verb="added audio", action_object=action_audio, target=facet)

    return redirect('facet_edit', pk=facet.id)


#----------------------------------------------------------------------#
#   Video Asset Views
#----------------------------------------------------------------------#

def upload_video(request):
    """ Add video to a facet."""

    if request.method == 'POST':
        videoform=VideoAssetForm(request.POST, request.FILES)
        if videoform.is_valid():
            video = videoform.save(commit=False)

            # retrieve the facet the image should be associated with
            facet_id = request.POST.get('facet')
            facet = get_object_or_404(Facet, id=facet_id)

            # set request based attributes
            video.owner = request.user
            video.organization = request.user.organization
            video.save()

            # add video asset to facet video_assets
            facet.video_assets.add(video)
            facet.save()

            # record action for activity stream
            action.send(request.user, verb="uploaded video", action_object=video, target=facet)

    return redirect('facet_edit', pk=facet.id)


def add_video(request):
    """ Add existing video(s) in the library to another facet."""

    if request.method == "POST":
        videos = request.POST.getlist('video')

        # retrieve the facet the image should be associated with
        facet_id = request.POST.get('facet')
        facet = get_object_or_404(Facet, id=facet_id)

        # connect video to facet
        for video in videos:
            video_ins = get_object_or_404(VideoAsset, id=video)
            facet.video_assets.add(video_ins)
        facet.save()

        # record action for activity stream
        action_video=get_object_or_404(VideoAsset, id=videos[0])
        action.send(request.user, verb="added video", action_object=action_video, target=facet)

    return redirect('facet_edit', pk=facet.id)
