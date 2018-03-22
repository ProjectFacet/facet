""" Media Asset handling views for editorial app.

    editorial/views/assetviews.py
"""

# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.generic import TemplateView , UpdateView, DetailView, ListView, CreateView, FormView, DeleteView, RedirectView
from actstream import action
from braces.views import LoginRequiredMixin, FormMessagesMixin

from editorial.forms import (
    ImageAssetForm,
    DocumentAssetForm,
    AudioAssetForm,
    VideoAssetForm,
    SimpleImageForm,
    SimpleDocumentForm,
    SimpleAudioForm,
    SimpleVideoForm,
    LibraryImageAssociateForm,
    LibraryDocumentAssociateForm,
    LibraryAudioAssociateForm,
    LibraryVideoAssociateForm,
    )

from editorial.models import (
    Facet,
    Call,
    Pitch,
    Assignment,
    Project,
    Story,
    Series,
    Event,
    Task,
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

# ACCESS: Only an org's users should be able to see an organization's asset library
# FUTURE TODO: This is likely another place to add organization/ to url
class AssetLibraryTemplateView(LoginRequiredMixin, TemplateView):
    """ Display media library of all organization assets."""

    template_name = 'editorial/asset_list.html'

    def get_context_data(self):
        """Return all the (complex) assets associated with an organization."""

        organization = self.request.user.organization
        tab = "Recent Assets"
        recentassets = organization.get_org_recent_media()
        print "RECENT ASSETS: ", recentassets
        return {'recentassets': recentassets, 'tab': tab,}


class ImageAssetLibraryTemplateView(LoginRequiredMixin, TemplateView):
    """ Display media library of all organization image assets."""

    template_name = 'editorial/asset_list.html'

    def get_context_data(self):
        """Return all the (complex) assets associated with an organization."""

        tab = "Image Assets"
        organization = self.request.user.organization
        images = organization.get_org_image_library()
        return {'images': images, 'tab': tab,}


class DocumentAssetLibraryTemplateView(LoginRequiredMixin, TemplateView):
    """ Display media library of all organization document assets."""

    template_name = 'editorial/asset_list.html'

    def get_context_data(self):
        """Return all the (complex) assets associated with an organization."""

        tab = "Document Assets"
        organization = self.request.user.organization
        documents = organization.get_org_document_library()
        return {'documents': documents, 'tab': tab,}


class AudioAssetLibraryTemplateView(LoginRequiredMixin, TemplateView):
    """ Display media library of all organization audio assets."""

    template_name = 'editorial/asset_list.html'

    def get_context_data(self):
        """Return all the (complex) assets associated with an organization."""

        tab = "Audio Assets"
        organization = self.request.user.organization
        audio = organization.get_org_audio_library()
        return {'audio': audio, 'tab': tab,}


class VideoAssetLibraryTemplateView(LoginRequiredMixin, TemplateView):
    """ Display media library of all organization video assets."""

    template_name = 'editorial/asset_list.html'

    def get_context_data(self):
        """Return all the (complex) assets associated with an organization."""

        tab = "Video Assets"
        organization = self.request.user.organization
        video = organization.get_org_video_library()
        return {'video': video, 'tab': tab,}


#----------------------------------------------------------------------#
#   Image Asset Views
#----------------------------------------------------------------------#

# ACCESS: Any org user, or user from an organization that is in collaborate_with
# should be able to create an asset for P, Sr, St, F
# Contractors should only be able to do so for PSSF that they have access to
# That should be handled by limiting which PSSF they have access to.
class ImageAssetCreateView(LoginRequiredMixin, CreateView):
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

        return redirect('facet_edit', pk=facet.id, story=facet.story.id)


# ACCESS: Any org user should be able to add an asset for a P, Sr, St, F
# A user from an organization that is in collaborate_with or
# contractors should not be able to do this because doing so requires access to
# an org's entire asset library.
class LibraryImageAssociateView(LoginRequiredMixin, FormView):
    """ Add existing image(s) in the library to another facet."""

    form_class = LibraryImageAssociateForm
    template_name = "editorial/_libraryimage.html"

    def get_form_kwargs(self):
        """Pass some initial things to scaffold form."""
        kwargs = super(LibraryImageAssociateView, self).get_form_kwargs()
        kwargs['organization'] = self.request.user.organization
        return kwargs

    def form_valid(self, form):
        """Handle submission of form."""

        facet = self.kwargs['facet']
        images = form.cleaned_data['images']
        facet = get_object_or_404(Facet, id=facet)
        facet.image_assets.add(*images)
        action.send(self.request.user, verb="added image", target=facet)

        return redirect('facet_edit', pk=facet.id, story=facet.story.id)


# ACCESS: Any org user should be able to update an asset
# A user from an organization that is in collaborate_with should be able to update
# assets they are the owner of.
# contractors should only be able to do this with assets they are the owner of.
class ImageAssetUpdateView(LoginRequiredMixin, UpdateView):
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


# ACCESS: Only users with access to an organization's media library should be
# able to delete items in it.
class ImageAssetDeleteView(LoginRequiredMixin, FormMessagesMixin, DeleteView):
    """View for handling deletion of an image asset.

    Assets can only be deleted from the library.
    """

    model = ImageAsset
    template_name = "editorial/imageasset_delete.html"

    form_valid_message = "Deleted."
    form_invalid_message = "Please check form."

    def get_success_url(self):
        """Post deletion return to the media library."""

        return reverse('asset_library')


#----------------------------------------------------------------------#
#   Document Asset Views
#----------------------------------------------------------------------#

# ACCESS: Any org user, or user from an organization that is in collaborate_with
# should be able to create an asset for P, Sr, St, F
# Contractors should only be able to do so for PSSF that they have access to
# That should be handled by limiting which PSSF they have access to.
class DocumentAssetCreateView(LoginRequiredMixin, CreateView):
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

        # add document asset to facet document_assets
        facet.document_assets.add(document)
        facet.save()

        # record action for activity stream
        action.send(self.request.user, verb="uploaded document", action_object=document, target=facet)

        return redirect('facet_edit', pk=facet.id, story=facet.story.id)


# ACCESS: Any org user should be able to add an asset for a P, Sr, St, F
# A user from an organization that is in collaborate_with or
# contractors should not be able to do this because doing so requires access to
# an org's entire asset library.
class LibraryDocumentAssociateView(LoginRequiredMixin, FormView):
    """ Add existing document(s) in the library to another facet."""

    form_class = LibraryDocumentAssociateForm
    template_name = "editorial/_librarydocument.html"

    def get_form_kwargs(self):
        """Pass some initial things to scaffold form."""

        kwargs = super(LibraryDocumentAssociateView, self).get_form_kwargs()
        kwargs['organization'] = self.request.user.organization
        return kwargs

    def form_valid(self, form):
        """Handle submission of form."""

        facet = self.kwargs['facet']
        documents = form.cleaned_data['documents']
        facet = get_object_or_404(Facet, id=facet)
        facet.document_assets.add(*documents)
        action.send(self.request.user, verb="added document", target=facet)

        return redirect('facet_edit', pk=facet.id, story=facet.story.id)


# ACCESS: Any org user should be able to update an asset
# A user from an organization that is in collaborate_with should be able to update
# assets they are the owner of.
# contractors should only be able to do this with assets they are the owner of.
class DocumentAssetUpdateView(LoginRequiredMixin, UpdateView):
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


# ACCESS: Only users with access to an organization's media library should be
# able to delete items in it.
class DocumentAssetDeleteView(LoginRequiredMixin, FormMessagesMixin, DeleteView):
    """View for handling deletion of a document asset.

    Assets can only be deleted from the library.
    """

    model = DocumentAsset
    template_name = "editorial/documentasset_delete.html"

    form_valid_message = "Deleted."
    form_invalid_message = "Please check form."

    def get_success_url(self):
        """Post deletion return to the media library."""

        return reverse('asset_library')

#----------------------------------------------------------------------#
#   Audio Asset Views
#----------------------------------------------------------------------#

# ACCESS: Any org user, or user from an organization that is in collaborate_with
# should be able to create an asset for P, Sr, St, F
# Contractors should only be able to do so for PSSF that they have access to
# That should be handled by limiting which PSSF they have access to.
class AudioAssetCreateView(LoginRequiredMixin, CreateView):
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

        return redirect('facet_edit', pk=facet.id, story=facet.story.id)


# ACCESS: Any org user should be able to add an asset for a P, Sr, St, F
# A user from an organization that is in collaborate_with or
# contractors should not be able to do this because doing so requires access to
# an org's entire asset library.
class LibraryAudioAssociateView(LoginRequiredMixin, FormView):
    """ Add existing audio in the library to another facet."""

    form_class = LibraryAudioAssociateForm
    template_name = "editorial/_libraryaudio.html"

    def get_form_kwargs(self):
        """Pass some initial things to scaffold form."""
        kwargs = super(LibraryAudioAssociateView, self).get_form_kwargs()
        kwargs['organization'] = self.request.user.organization
        return kwargs

    def form_valid(self, form):
        """Handle submission of form."""

        facet = self.kwargs['facet']
        audio = form.cleaned_data['audio']
        facet = get_object_or_404(Facet, id=facet)
        facet.audio_assets.add(*audio)
        action.send(self.request.user, verb="added audio", target=facet)

        return redirect('facet_edit', pk=facet.id, story=facet.story.id)


# ACCESS: Any org user should be able to update an asset
# A user from an organization that is in collaborate_with should be able to update
# assets they are the owner of.
# contractors should only be able to do this with assets they are the owner of.
class AudioAssetUpdateView(LoginRequiredMixin, UpdateView):
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


# ACCESS: Only users with access to an organization's media library should be
# able to delete items in it.
class AudioAssetDeleteView(LoginRequiredMixin, FormMessagesMixin, DeleteView):
    """View for handling deletion of an audio asset.

    Assets can only be deleted from the library.
    """

    model = AudioAsset
    template_name = "editorial/audioasset_delete.html"

    form_valid_message = "Deleted."
    form_invalid_message = "Please check form."

    def get_success_url(self):
        """Post deletion return to the media library."""

        return reverse('asset_library')

#----------------------------------------------------------------------#
#   Video Asset Views
#----------------------------------------------------------------------#

# ACCESS: Any org user, or user from an organization that is in collaborate_with
# should be able to create an asset for P, Sr, St, F
# Contractors should only be able to do so for PSSF that they have access to
# That should be handled by limiting which PSSF they have access to.
class VideoAssetCreateView(LoginRequiredMixin, CreateView):
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
        action.send(self.request.user, verb="created video", action_object=video, target=facet)

        return redirect('facet_edit', pk=facet.id, story=facet.story.id)


# ACCESS: Any org user should be able to add an asset for a P, Sr, St, F
# A user from an organization that is in collaborate_with or
# contractors should not be able to do this because doing so requires access to
# an org's entire asset library.
class LibraryVideoAssociateView(LoginRequiredMixin, FormView):
    """ Add existing video(s) in the library to another facet."""

    form_class = LibraryVideoAssociateForm
    template_name = "editorial/_libraryvideo.html"

    def get_form_kwargs(self):
        """Pass some initial things to scaffold form."""
        kwargs = super(LibraryVideoAssociateView, self).get_form_kwargs()
        kwargs['organization'] = self.request.user.organization
        return kwargs

    def form_valid(self, form):
        """Handle submission of form."""

        facet = self.kwargs['facet']
        video = form.cleaned_data['video']
        facet = get_object_or_404(Facet, id=facet)
        facet.video_assets.add(*video)
        action.send(self.request.user, verb="added video", target=facet)

        return redirect('facet_edit', pk=facet.id, story=facet.story.id)


# ACCESS: Any org user should be able to update an asset
# A user from an organization that is in collaborate_with should be able to update
# assets they are the owner of.
# contractors should only be able to do this with assets they are the owner of.
class VideoAssetUpdateView(LoginRequiredMixin, UpdateView):
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


# ACCESS: Only users with access to an organization's media library should be
# able to delete items in it.
class VideoAssetDeleteView(LoginRequiredMixin, FormMessagesMixin, DeleteView):
    """View for handling deletion of a video asset.

    Assets can only be deleted from the library.
    """

    model = VideoAsset
    template_name = "editorial/videoasset_delete.html"

    form_valid_message = "Deleted."
    form_invalid_message = "Please check form."

    def get_success_url(self):
        """Post deletion return to the media library."""

        return reverse('asset_library')
#----------------------------------------------------------------------#
#   Simple Asset Views
#----------------------------------------------------------------------#

# ACCESS: Any org user, or user from an organization that is in collaborate_with
# should be able to create a simple asset for P, Sr, St, F
# Contractors should only be able to do so for PSSF that they have access to
# That should be handled by limiting which PSSF they have access to.
class SimpleImageCreateView(LoginRequiredMixin, CreateView):
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

        # set request based attributes
        image.owner = self.request.user
        if self.request.user.organization:
            image.organization = self.request.user.organization
        image.save()

        # get thing that the image is being associated with
        associated_object = self.request.POST.get('association')
        if associated_object == 'project':
            project_id = self.request.POST.get('project')
            project = get_object_or_404(Project, id=project_id)
            # add simple image to the associated object
            project.simple_image_assets.add(image)
            project.save()
            action_target = project
            # record action for activity stream
            action.send(self.request.user, verb="uploaded image", action_object=image, target=action_target)
            # redirect to the associated object
            return HttpResponseRedirect(reverse('project_detail', args=(project.id,)))
        elif associated_object == 'series':
            series_id = self.request.POST.get('series')
            series = get_object_or_404(Series, id=series_id)
            # add simple image to the associated object
            series.simple_image_assets.add(image)
            series.save()
            action_target = series
            # record action for activity stream
            action.send(self.request.user, verb="uploaded image", action_object=image, target=action_target)
            # redirect to the associated object
            return HttpResponseRedirect(reverse('series_detail', args=(series.id,)))
        elif associated_object == 'story':
            story_id = self.request.POST.get('story')
            story = get_object_or_404(Story, id=story_id)
            # add simple image to the associated object
            story.simple_image_assets.add(image)
            story.save()
            action_target = story
            # record action for activity stream
            action.send(self.request.user, verb="uploaded image", action_object=image, target=action_target)
            # redirect to the associated object
            return HttpResponseRedirect(reverse('story_detail', args=(story.id,)))
        elif associated_object == 'task':
            task_id = self.request.POST.get('task')
            task = get_object_or_404(Task, id=task_id)
            # add simple image to the associated object
            task.simple_image_assets.add(image)
            task.save()
            action_target = task
            # record action for activity stream
            action.send(self.request.user, verb="uploaded image", action_object=image, target=action_target)
            # redirect to the associated object
            return HttpResponseRedirect(reverse('task_detail', args=(task.id,)))
        elif associated_object == 'event':
            event_id = self.request.POST.get('event')
            event = get_object_or_404(Event, id=event_id)
            # add simple image to the associated object
            event.simple_image_assets.add(image)
            event.save()
            action_target = event
            # record action for activity stream
            action.send(self.request.user, verb="uploaded image", action_object=image, target=action_target)
            # redirect to the associated object
            return HttpResponseRedirect(reverse('event_detail', args=(event.id,)))
        elif associated_object == 'pitch':
            pitch_id = self.request.POST.get('pitch')
            pitch = get_object_or_404(Pitch, id=pitch_id)
            # add simple image to the associated object
            pitch.simple_image_assets.add(image)
            pitch.save()
            action_target = pitch
            # record action for activity stream
            action.send(self.request.user, verb="uploaded image", action_object=image, target=action_target)
            # redirect to the associated object
            return HttpResponseRedirect(reverse('pitch_detail', args=(pitch.id,)))
        elif associated_object == 'call':
            call_id = self.request.POST.get('call')
            call = get_object_or_404(Call, id=call_id)
            # add simple image to the associated object
            call.simple_image_assets.add(image)
            call.save()
            action_target = call
            # record action for activity stream
            action.send(self.request.user, verb="uploaded image", action_object=image, target=action_target)
            # redirect to the associated object
            return HttpResponseRedirect(reverse('call_detail', args=(call.id,)))
        elif associated_object == 'Assignment':
            assignment_id = self.request.POST.get('assignment')
            assignment = get_object_or_404(Assignment, id=assignment_id)
            # add simple image to the associated object
            assignment.simple_image_assets.add(image)
            assignment.save()
            action_target = assignment
            # record action for activity stream
            action.send(self.request.user, verb="uploaded image", action_object=image, target=action_target)
            # redirect to the associated object
            return HttpResponseRedirect(reverse('assignment_detail', args=(assignment.id,)))


# SAA
class SimpleDocumentCreateView(LoginRequiredMixin, CreateView):
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

        # set request based attributes
        document.owner = self.request.user

        if self.request.user.organization:
            document.organization = self.request.user.organization

        document.save()

        # get thing that the document is being associated with
        associated_object = self.request.POST.get('association')
        if associated_object == 'project':
            project_id = self.request.POST.get('project')
            project = get_object_or_404(Project, id=project_id)
            # add simple document to the associated object
            project.simple_document_assets.add(document)
            project.save()
            action_target = project
            # record action for activity stream
            action.send(self.request.user, verb="uploaded document", action_object=document, target=action_target)
            # redirect to the associated object
            return HttpResponseRedirect(reverse('project_detail', args=(project.id,)))
        elif associated_object == 'series':
            series_id = self.request.POST.get('series')
            series = get_object_or_404(Series, id=series_id)
            # add simple document to the associated object
            series.simple_document_assets.add(document)
            series.save()

            action_target = series
            # record action for activity stream
            action.send(self.request.user, verb="uploaded document", action_object=document, target=action_target)
            # redirect to the associated object
            return HttpResponseRedirect(reverse('series_detail', args=(series.id,)))
        elif associated_object == 'story':
            story_id = self.request.POST.get('story')
            story = get_object_or_404(Story, id=story_id)
            # add simple document to the associated object
            story.simple_document_assets.add(document)
            story.save()
            action_target = story
            # record action for activity stream
            action.send(self.request.user, verb="uploaded document", action_object=document, target=action_target)
            # redirect to the associated object
            return HttpResponseRedirect(reverse('story_detail', args=(story.id,)))
        elif associated_object == 'task':
            task_id = self.request.POST.get('task')
            task = get_object_or_404(Task, id=task_id)
            # add simple document to the associated object
            task.simple_document_assets.add(document)
            task.save()
            action_target = task
            # record action for activity stream
            action.send(self.request.user, verb="uploaded document", action_object=document, target=action_target)
            # redirect to the associated object
            return HttpResponseRedirect(reverse('task_detail', args=(task.id,)))
        elif associated_object == 'event':
            event_id = self.request.POST.get('event')
            event = get_object_or_404(Event, id=event_id)
            # add simple document to the associated object
            event.simple_document_assets.add(document)
            event.save()
            action_target = event
            # record action for activity stream
            action.send(self.request.user, verb="uploaded document", action_object=document, target=action_target)
            # redirect to the associated object
            return HttpResponseRedirect(reverse('event_detail', args=(event.id,)))
        elif associated_object == 'pitch':
            pitch_id = self.request.POST.get('pitch')
            pitch = get_object_or_404(Pitch, id=pitch_id)
            # add simple document to the associated object
            pitch.simple_document_assets.add(document)
            pitch.save()
            action_target = pitch
            # record action for activity stream
            action.send(self.request.user, verb="uploaded document", action_object=document, target=action_target)
            # redirect to the associated object
            return HttpResponseRedirect(reverse('pitch_detail', args=(pitch.id,)))
        elif associated_object == 'call':
            call_id = self.request.POST.get('call')
            call = get_object_or_404(Call, id=call_id)
            # add simple document to the associated object
            call.simple_document_assets.add(document)
            call.save()
            action_target = call
            # record action for activity stream
            action.send(self.request.user, verb="uploaded document", action_object=document, target=action_target)
            # redirect to the associated object
            return HttpResponseRedirect(reverse('call_detail', args=(call.id,)))
        elif associated_object == 'assignment':
            assignment_id = self.request.POST.get('assignment')
            assignment = get_object_or_404(Assignment, id=assignment_id)
            # add simple document to the associated object
            assignment.simple_document_assets.add(document)
            assignment.save()
            action_target = assignment
            # record action for activity stream
            action.send(self.request.user, verb="uploaded document", action_object=document, target=action_target)
            # redirect to the associated object
            return HttpResponseRedirect(reverse('assignment_detail', args=(assignment.id,)))


# SAA
class SimpleAudioCreateView(LoginRequiredMixin, CreateView):
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

        # set request based attributes
        audio.owner = self.request.user
        if self.request.user.organization:
            audio.organization = self.request.user.organization
        audio.save()

        # get thing that the audio is being associated with
        associated_object = self.request.POST.get('association')
        if associated_object == 'project':
            project_id = self.request.POST.get('project')
            project = get_object_or_404(Project, id=project_id)
            # add simple audio to the associated object
            project.simple_audio_assets.add(audio)
            project.save()
            action_target = project
            # record action for activity stream
            action.send(self.request.user, verb="uploaded audio", action_object=audio, target=action_target)
            # redirect to the associated object
            return HttpResponseRedirect(reverse('project_detail', args=(project.id,)))
        elif associated_object == 'series':
            series_id = self.request.POST.get('series')
            series = get_object_or_404(Series, id=series_id)
            # add simple audio to the associated object
            series.simple_audio_assets.add(audio)
            series.save()
            action_target = series
            # record action for activity stream
            action.send(self.request.user, verb="uploaded audio", action_object=audio, target=action_target)
            # redirect to the associated object
            return HttpResponseRedirect(reverse('series_detail', args=(series.id,)))
        elif associated_object == 'story':
            story_id = self.request.POST.get('story')
            story = get_object_or_404(Story, id=story_id)
            # add simple audio to the associated object
            story.simple_audio_assets.add(audio)
            story.save()
            action_target = story
            # record action for activity stream
            action.send(self.request.user, verb="uploaded audio", action_object=audio, target=action_target)
            # redirect to the associated object
            return HttpResponseRedirect(reverse('story_detail', args=(story.id,)))
        elif associated_object == 'task':
            task_id = self.request.POST.get('task')
            task = get_object_or_404(Task, id=task_id)
            # add simple audio to the associated object
            task.simple_audio_assets.add(audio)
            task.save()
            action_target = task
            # record action for activity stream
            action.send(self.request.user, verb="uploaded audio", action_object=audio, target=action_target)
            # redirect to the associated object
            return HttpResponseRedirect(reverse('task_detail', args=(task.id,)))
        elif associated_object == 'event':
            event_id = self.request.POST.get('event')
            event = get_object_or_404(Event, id=event_id)
            # add simple audio to the associated object
            event.simple_audio_assets.add(audio)
            event.save()
            action_target = event
            # record action for activity stream
            action.send(self.request.user, verb="uploaded audio", action_object=audio, target=action_target)
            # redirect to the associated object
            return HttpResponseRedirect(reverse('event_detail', args=(event.id,)))
        elif associated_object == 'pitch':
            pitch_id = self.request.POST.get('pitch')
            pitch = get_object_or_404(Pitch, id=pitch_id)
            # add simple audio to the associated object
            pitch.simple_audio_assets.add(audio)
            pitch.save()
            action_target = pitch
            # record action for activity stream
            action.send(self.request.user, verb="uploaded audio", action_object=audio, target=action_target)
            # redirect to the associated object
            return HttpResponseRedirect(reverse('pitch_detail', args=(pitch.id,)))
        elif associated_object == 'call':
            call_id = self.request.POST.get('call')
            call = get_object_or_404(Call, id=call_id)
            # add simple audio to the associated object
            call.simple_audio_assets.add(audio)
            call.save()
            action_target = call
            # record action for activity stream
            action.send(self.request.user, verb="uploaded audio", action_object=audio, target=action_target)
            # redirect to the associated object
            return HttpResponseRedirect(reverse('call_detail', args=(call.id,)))
        elif associated_object == 'assignment':
            assignment_id = self.request.POST.get('assignment')
            assignment = get_object_or_404(Assignment, id=assignment_id)
            # add simple audio to the associated object
            assignment.simple_audio_assets.add(audio)
            assignment.save()
            action_target = assignment
            # record action for activity stream
            action.send(self.request.user, verb="uploaded audio", action_object=audio, target=action_target)
            # redirect to the associated object
            return HttpResponseRedirect(reverse('assignment_detail', args=(assignment.id,)))


# SAA
class SimpleVideoCreateView(LoginRequiredMixin, CreateView):
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

        # set request based attributes
        video.owner = self.request.user
        if self.request.user.organization:
            video.organization = self.request.user.organization
        video.save()

        # get thing that the video is being associated with
        associated_object = self.request.POST.get('association')
        if associated_object == 'project':
            project_id = self.request.POST.get('project')
            project = get_object_or_404(Project, id=project_id)
            # add simple video to the associated object
            project.simple_video_assets.add(video)
            project.save()
            action_target = project
            # record action for activity stream
            action.send(self.request.user, verb="uploaded video", action_object=video, target=action_target)
            # redirect to the associated object
            return HttpResponseRedirect(reverse('project_detail', args=(project.id,)))
        elif associated_object == 'series':
            series_id = self.request.POST.get('series')
            series = get_object_or_404(Series, id=series_id)
            # add simple video to the associated object
            series.simple_video_assets.add(video)
            series.save()
            action_target = series
            # record action for activity stream
            action.send(self.request.user, verb="uploaded video", action_object=video, target=action_target)
            # redirect to the associated object
            return HttpResponseRedirect(reverse('series_detail', args=(series.id,)))
        elif associated_object == 'story':
            story_id = self.request.POST.get('story')
            story = get_object_or_404(Story, id=story_id)
            # add simple video to the associated object
            story.simple_video_assets.add(video)
            story.save()
            action_target = story
            # record action for activity stream
            action.send(self.request.user, verb="uploaded video", action_object=video, target=action_target)
            # redirect to the associated object
            return HttpResponseRedirect(reverse('story_detail', args=(story.id,)))
        elif associated_object == 'task':
            task_id = self.request.POST.get('task')
            task = get_object_or_404(Task, id=task_id)
            # add simple video to the associated object
            task.simple_video_assets.add(video)
            task.save()
            action_target = task
            # record action for activity stream
            action.send(self.request.user, verb="uploaded video", action_object=video, target=action_target)
            # redirect to the associated object
            return HttpResponseRedirect(reverse('task_detail', args=(task.id,)))
        elif associated_object == 'event':
            event_id = self.request.POST.get('event')
            event = get_object_or_404(Event, id=event_id)
            # add simple video to the associated object
            event.simple_video_assets.add(video)
            event.save()
            action_target = event
            # record action for activity stream
            action.send(self.request.user, verb="uploaded video", action_object=video, target=action_target)
            # redirect to the associated object
            return HttpResponseRedirect(reverse('event_detail', args=(event.id,)))
        elif associated_object == 'pitch':
            pitch_id = self.request.POST.get('pitch')
            pitch = get_object_or_404(Pitch, id=pitch_id)
            # add simple video to the associated object
            pitch.simple_video_assets.add(video)
            pitch.save()
            action_target = pitch
            # record action for activity stream
            action.send(self.request.user, verb="uploaded video", action_object=video, target=action_target)
            # redirect to the associated object
            return HttpResponseRedirect(reverse('pitch_detail', args=(pitch.id,)))
        elif associated_object == 'call':
            call_id = self.request.POST.get('call')
            call = get_object_or_404(Call, id=call_id)
            # add simple video to the associated object
            call.simple_video_assets.add(video)
            call.save()
            action_target = call
            # record action for activity stream
            action.send(self.request.user, verb="uploaded video", action_object=video, target=action_target)
            # redirect to the associated object
            return HttpResponseRedirect(reverse('call_detail', args=(call.id,)))
        elif associated_object == 'Assignment':
            assignment_id = self.request.POST.get('assignment')
            assignment = get_object_or_404(Assignment, id=assignment_id)
            # add simple video to the associated object
            assignment.simple_video_assets.add(video)
            assignment.save()
            action_target = assignment
            # record action for activity stream
            action.send(self.request.user, verb="uploaded video", action_object=video, target=action_target)
            # redirect to the associated object
            return HttpResponseRedirect(reverse('assignment_detail', args=(assignment.id,)))
