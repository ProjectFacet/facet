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
from django.views.generic import TemplateView , UpdateView, DetailView, ListView, CreateView
from django.views.decorators.csrf import csrf_exempt
import datetime
import json
from actstream import action

from editorial.forms import (
    ImageAssetForm,
    DocumentAssetForm,
    AudioAssetForm,
    VideoAssetForm,
    SimpleImageForm,
    SimpleDocumentForm,
    SimpleAudioForm,
    SimpleVideoForm,
    )

from editorial.models import (
    Facet,
    ImageAsset,
    DocumentAsset,
    AudioAsset,
    VideoAsset,
    SimpleImage,
    SimpleDocument,
    SimpleAudio,
    SimpleVideo,
    )


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
#   Image Asset Views
#----------------------------------------------------------------------#

class ImageAssetCreateView(CreateView):
    """ Upload image to a facet."""

    model = ImageAsset
    form_class = ImageAssetForm

    def form_valid(self, form):
        """Save -- but first add owner and organization to the image and
        add the image to the facet.
        """

        self.object = image = form.save(commit=False)
        facet_id = self.request.POST.get('facet')
        facet = get_object_or_404(Facet, id=facet_id)

        # set request based attributes
        image.owner = self.request.user
        image.organization = self.request.user.organization
        image.save()

        # add image asset to facet image_assets
        facet.image_assets.add(image)
        facet.save()

        # record action for activity stream
        action.send(self.request.user, verb="uploaded image", action_object=image, target=facet)

        # FIXME redirect to facet the image was uploaded to.
        return redirect(self.get_success_url())


# FIXME Q for J on best practices for how this is handled.
# It's not a model form, just one from the html that returns an
# array of asset ids to be connected to a facet.
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


#----------------------------------------------------------------------#
#   Document Asset Views
#----------------------------------------------------------------------#

class DocumentAssetCreateView(CreateView):
    """Upload a document to a facet."""

    model = DocumentAsset
    form_class = DocumentAssetForm

    def form_valid(self, form):
        """Save -- but first add owner and organization to the document and
        add the document to the facet.
        """

        self.object = document = form.save(commit=False)
        facet_id = self.request.POST.get('facet')
        facet = get_object_or_404(Facet, id=facet_id)

        # set request based attributes
        document.owner = self.request.user
        document.organization = self.request.user.organization
        document.save()

        # add image asset to facet image_assets
        facet.document_assets.add(document)
        facet.save()

        # record action for activity stream
        action.send(self.request.user, verb="uploaded document", action_object=document, target=facet)

        # FIXME redirect to facet the image was uploaded to.
        return redirect(self.get_success_url())


# FIXME Q for J on best practices for how this is handled.
# It's not a model form, just one from the html that returns an
# array of asset ids to be connected to a facet.
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


#----------------------------------------------------------------------#
#   Audio Asset Views
#----------------------------------------------------------------------#

class AudioAssetCreateView(CreateView):
    """ Upload audio to a facet."""

    model = AudioAsset
    form_class = AudioAssetForm

    def form_valid(self, form):
        """Save -- but first add owner and organization to the audio and
        add the audio to the facet.
        """

        self.object = audio = form.save(commit=False)
        facet_id = self.request.POST.get('facet')
        facet = get_object_or_404(Facet, id=facet_id)

        # set request based attributes
        audio.owner = self.request.user
        audio.organization = self.request.user.organization
        audio.save()

        # add audio asset to facet audio_assets
        facet.audio_assets.add(audio)
        facet.save()

        # record action for activity stream
        action.send(self.request.user, verb="uploaded audio", action_object=audio, target=facet)

        # FIXME redirect to facet the audio was uploaded to.
        return redirect(self.get_success_url())


# FIXME Q for J on best practices for how this is handled.
# It's not a model form, just one from the html that returns an
# array of asset ids to be connected to a facet.
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


#----------------------------------------------------------------------#
#   Video Asset Views
#----------------------------------------------------------------------#

class VideoAssetCreateView(CreateView):
    """ Upload video to a facet."""

    model = VideoAsset
    form_class = VideoAssetForm

    def form_valid(self, form):
        """Save -- but first add owner and organization to the video and
        add the video to the facet.
        """

        self.object = video = form.save(commit=False)
        facet_id = self.request.POST.get('facet')
        facet = get_object_or_404(Facet, id=facet_id)

        # set request based attributes
        video.owner = self.request.user
        video.organization = self.request.user.organization
        video.save()

        # add video asset to facet video_assets
        facet.video_assets.add(video)
        facet.save()

        # record action for activity stream
        action.send(self.request.user, verb="uploaded video", action_object=video, target=facet)

        # FIXME redirect to facet the video was uploaded to.
        return redirect(self.get_success_url())


# FIXME Q for J on best practices for how this is handled.
# It's not a model form, just one from the html that returns an
# array of asset ids to be connected to a facet.
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
#   Simple Asset Views
#----------------------------------------------------------------------#

class SimpleImageCreateView(CreateView):
    """Upload a simple image."""

    model = SimpleImage
    form_class = SimpleImageForm

    def form_valid(self,form):
        """Save -- but first add owner and org to the image.
        And then connect the image to whatever object it is associated with.

        Simple images can be connected to Projects, Series, Stories, Tasks, Events.
        Pitches, Calls and Assignments.
        """

        self.object = image = form.save(commit=False)

        # get thing that the image is being associated with
        associated_object = self.request.POST.get('assocation')
        if associated_object == 'Project':
            project_id = self.request.POST.get('project')
            project = get_object_or_404(Project, id=project_id)
            # add simple image to the associated object
            # project.image_assets.add(image)
            # project.save()
            action_target = project
        elif associated_object == 'Series':
            series_id = self.request.POST.get('series')
            series = get_object_or_404(Series, id=series_id)
            # add simple image to the associated object
            # series.image_assets.add(image)
            # series.save()
            action_target = series
        elif associated_object == 'Story':
            story_id = self.request.POST.get('story')
            story = get_object_or_404(Story, id=story_id)
            # add simple image to the associated object
            # story.image_assets.add(image)
            # story.save()
            action_target = story
        elif associated_object == 'Task':
            task_id = self.request.POST.get('task')
            task = get_object_or_404(Task, id=task_id)
            # add simple image to the associated object
            # task.image_assets.add(image)
            # task.save()
            action_target = task
        elif associated_object == 'Event':
            event_id = self.request.POST.get('event')
            event = get_object_or_404(Event, id=event_id)
            # add simple image to the associated object
            # event.image_assets.add(image)
            # event.save()
            action_target = event
        elif associated_object == 'Pitch':
            pitch_id = self.request.POST.get('pitch')
            pitch = get_object_or_404(Pitch, id=pitch_id)
            # add simple image to the associated object
            pitch.image_assets.add(image)
            pitch.save()
            action_target = pitch
        elif associated_object == 'Call':
            call_id = self.request.POST.get('call')
            call = get_object_or_404(Call, id=call_id)
            # add simple image to the associated object
            # call.image_assets.add(image)
            # call.save()
            action_target = call
        elif associated_object == 'Assignment':
            assignment_id = self.request.POST.get('assignment')
            assignment = get_object_or_404(Assignment, id=assignment_id)
            # add simple image to the associated object
            # assignment.image_assets.add(image)
            # assignment.save()
            action_target = assignment

        # set request based attributes
        image.owner = self.request.user
        if self.request.user.organization:
            image.organization = self.request.user.organization
        image.save()

        # record action for activity stream
        action.send(self.request.user, verb="uploaded image", action_object=image, target=action_target)

        return redirect(self.get_success_url())


class SimpleDocumentCreateView(CreateView):
    """Upload a simple document."""

    model = SimpleDocument
    form_class = SimpleDocumentForm

    def form_valid(self,form):
        """Save -- but first add owner and org to the document.
        And then connect the document to whatever object it is associated with.

        Simple documents can be connected to Projects, Series, Stories, Tasks, Events.
        Pitches, Calls and Assignments.
        """

        self.object = document = form.save(commit=False)

        # get thing that the document is being associated with
        associated_object = self.request.POST.get('assocation')
        if associated_object == 'Project':
            project_id = self.request.POST.get('project')
            project = get_object_or_404(Project, id=project_id)
            # add simple document to the associated object
            # project.document_assets.add(document)
            # project.save()
            action_target = project
        elif associated_object == 'Series':
            series_id = self.request.POST.get('series')
            series = get_object_or_404(Series, id=series_id)
            # add simple document to the associated object
            # series.document_assets.add(document)
            # series.save()
            action_target = series
        elif associated_object == 'Story':
            story_id = self.request.POST.get('story')
            story = get_object_or_404(Story, id=story_id)
            # add simple document to the associated object
            # story.document_assets.add(document)
            # story.save()
            action_target = story
        elif associated_object == 'Task':
            task_id = self.request.POST.get('task')
            task = get_object_or_404(Task, id=task_id)
            # add simple document to the associated object
            # task.document_assets.add(document)
            # task.save()
            action_target = task
        elif associated_object == 'Event':
            event_id = self.request.POST.get('event')
            event = get_object_or_404(Event, id=event_id)
            # add simple document to the associated object
            # event.document_assets.add(document)
            # event.save()
            action_target = event
        elif associated_object == 'Pitch':
            pitch_id = self.request.POST.get('pitch')
            pitch = get_object_or_404(Pitch, id=pitch_id)
            # add simple document to the associated object
            pitch.document_assets.add(document)
            pitch.save()
            action_target = pitch
        elif associated_object == 'Call':
            call_id = self.request.POST.get('call')
            call = get_object_or_404(Call, id=call_id)
            # add simple document to the associated object
            # call.document_assets.add(document)
            # call.save()
            action_target = call
        elif associated_object == 'Assignment':
            assignment_id = self.request.POST.get('assignment')
            assignment = get_object_or_404(Assignment, id=assignment_id)
            # add simple document to the associated object
            # assignment.document_assets.add(document)
            # assignment.save()
            action_target = assignment

        # set request based attributes
        document.owner = self.request.user
        if self.request.user.organization:
            document.organization = self.request.user.organization
        document.save()

        # record action for activity stream
        action.send(self.request.user, verb="uploaded document", action_object=document, target=action_target)

        return redirect(self.get_success_url())


class SimpleAudioCreateView(CreateView):
    """Upload a simple audio."""

    model = SimpleAudio
    form_class = SimpleAudioForm

    def form_valid(self,form):
        """Save -- but first add owner and org to the audio.
        And then connect the audio to whatever object it is associated with.

        Simple audio can be connected to Projects, Series, Stories, Tasks, Events.
        Pitches, Calls and Assignments.
        """

        self.object = audio = form.save(commit=False)

        # get thing that the audio is being associated with
        associated_object = self.request.POST.get('assocation')
        if associated_object == 'Project':
            project_id = self.request.POST.get('project')
            project = get_object_or_404(Project, id=project_id)
            # add simple audio to the associated object
            # project.audio_assets.add(audio)
            # project.save()
            action_target = project
        elif associated_object == 'Series':
            series_id = self.request.POST.get('series')
            series = get_object_or_404(Series, id=series_id)
            # add simple audio to the associated object
            # series.audio_assets.add(audio)
            # series.save()
            action_target = series
        elif associated_object == 'Story':
            story_id = self.request.POST.get('story')
            story = get_object_or_404(Story, id=story_id)
            # add simple audio to the associated object
            # story.audio_assets.add(audio)
            # story.save()
            action_target = story
        elif associated_object == 'Task':
            task_id = self.request.POST.get('task')
            task = get_object_or_404(Task, id=task_id)
            # add simple audio to the associated object
            # task.audio_assets.add(audio)
            # task.save()
            action_target = task
        elif associated_object == 'Event':
            event_id = self.request.POST.get('event')
            event = get_object_or_404(Event, id=event_id)
            # add simple audio to the associated object
            # event.audio_assets.add(audio)
            # event.save()
            action_target = event
        elif associated_object == 'Pitch':
            pitch_id = self.request.POST.get('pitch')
            pitch = get_object_or_404(Pitch, id=pitch_id)
            # add simple audio to the associated object
            pitch.audio_assets.add(audio)
            pitch.save()
            action_target = pitch
        elif associated_object == 'Call':
            call_id = self.request.POST.get('call')
            call = get_object_or_404(Call, id=call_id)
            # add simple audio to the associated object
            # call.audio_assets.add(audio)
            # call.save()
            action_target = call
        elif associated_object == 'Assignment':
            assignment_id = self.request.POST.get('assignment')
            assignment = get_object_or_404(Assignment, id=assignment_id)
            # add simple audio to the associated object
            # assignment.audio_assets.add(audio)
            # assignment.save()
            action_target = assignment

        # set request based attributes
        audio.owner = self.request.user
        if self.request.user.organization:
            audio.organization = self.request.user.organization
        audio.save()

        # record action for activity stream
        action.send(self.request.user, verb="uploaded audio", action_object=audio, target=action_target)

        return redirect(self.get_success_url())


class SimpleVideoCreateView(CreateView):
    """Upload a simple video."""

    model = SimpleVideo
    form_class = SimpleVideoForm

    def form_valid(self,form):
        """Save -- but first add owner and org to the video.
        And then connect the video to whatever object it is associated with.

        Simple videos can be connected to Projects, Series, Stories, Tasks, Events.
        Pitches, Calls and Assignments.
        """

        self.object = video = form.save(commit=False)

        # get thing that the video is being associated with
        associated_object = self.request.POST.get('assocation')
        if associated_object == 'Project':
            project_id = self.request.POST.get('project')
            project = get_object_or_404(Project, id=project_id)
            # add simple video to the associated object
            # project.video_assetss.add(video)
            # project.save()
            action_target = project
        elif associated_object == 'Series':
            series_id = self.request.POST.get('series')
            series = get_object_or_404(Series, id=series_id)
            # add simple video to the associated object
            # series.video_assetss.add(video)
            # series.save()
            action_target = series
        elif associated_object == 'Story':
            story_id = self.request.POST.get('story')
            story = get_object_or_404(Story, id=story_id)
            # add simple video to the associated object
            # story.video_assetss.add(video)
            # story.save()
            action_target = story
        elif associated_object == 'Task':
            task_id = self.request.POST.get('task')
            task = get_object_or_404(Task, id=task_id)
            # add simple video to the associated object
            # task.video_assetss.add(video)
            # task.save()
            action_target = task
        elif associated_object == 'Event':
            event_id = self.request.POST.get('event')
            event = get_object_or_404(Event, id=event_id)
            # add simple video to the associated object
            # event.video_assetss.add(video)
            # event.save()
            action_target = event
        elif associated_object == 'Pitch':
            pitch_id = self.request.POST.get('pitch')
            pitch = get_object_or_404(Pitch, id=pitch_id)
            # add simple video to the associated object
            pitch.video_assetss.add(video)
            pitch.save()
            action_target = pitch
        elif associated_object == 'Call':
            call_id = self.request.POST.get('call')
            call = get_object_or_404(Call, id=call_id)
            # add simple video to the associated object
            # call.video_assetss.add(video)
            # call.save()
            action_target = call
        elif associated_object == 'Assignment':
            assignment_id = self.request.POST.get('assignment')
            assignment = get_object_or_404(Assignment, id=assignment_id)
            # add simple video to the associated object
            # assignment.video_assetss.add(video)
            # assignment.save()
            action_target = assignment

        # set request based attributes
        video.owner = self.request.user
        if self.request.user.organization:
            video.organization = self.request.user.organization
        video.save()

        # record action for activity stream
        action.send(self.request.user, verb="uploaded video", action_object=video, target=action_target)

        return redirect(self.get_success_url())
