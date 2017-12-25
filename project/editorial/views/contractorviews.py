# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponse
from django.utils import timezone
from django.views.generic import CreateView, FormView, UpdateView, DetailView, ListView, DeleteView, TemplateView
from django.views.decorators.csrf import csrf_exempt
import datetime
import json
from actstream import action
from django.db.models import Q

from editorial.forms import (
    ContractorProfileForm,
    OrganizationContractorAffiliationForm,
    CallForm,
    PitchForm,
    AssignmentForm,
    SimpleImageForm,
    SimpleDocumentForm,
    SimpleAudioForm,
    SimpleVideoForm,
    PrivateMessageForm,
    ContractorSubscriptionForm,
    )

from editorial.models import (
    ContractorSubscription,
    User,
    ContractorProfile,
    TalentEditorProfile,
    Organization,
    OrganizationContractorAffiliation,
    Call,
    Pitch,
    Assignment,
    SimpleImage,
    SimpleDocument,
    SimpleAudio,
    SimpleVideo,
    PrivateMessage,
    )


#----------------------------------------------------------------------#
#   Contractor Views
#----------------------------------------------------------------------#

class ContractorCreateView(CreateView):
    """After user signup, the user has the option to create an organization or
    a contractor profile.

    This view creates a new contractor profile to associate with user.
    """

    model = ContractorProfile
    form_class = ContractorProfileForm

    def form_valid(self, form):
        """Save -- but first connect to User."""

        self.object = contractor = form.save(commit=False)

        contractor.user = self.request.user

        # create a contractor account subscription for this user.
        subscription = ContractorSubscription.objects.create_subscription(
                                                        user=self.request.user,
                                                        standard=True,
                                                        )
        print "SUBSCRIPTION: ", subscription

        subscription.save()

        contractor.save()
        form.save_m2m()

        return redirect(self.get_success_url())


class ContractorDetailView(DetailView):
    """Display details about a contractor."""

    model = ContractorProfile

    def contractor_assignments(self):
        """Get assignments that are relevant to requesting user."""

        self.object = self.get_object()
        contractor = self.object
        if self.request.user.talenteditorprofile:
            editor = self.request.user.talenteditorprofile
            active_assignments = contractor.get_active_assignments()
            assignments_for_viewer = active_assignments.filter(editor=editor)
        elif self.request.user.contractorprofile:
            assignments_for_viewer = contractor.get_active_assignments()
        else:
            assignments_for_viewer = []
        return assignments_for_viewer

    def contractor_pitches(self):
        """Get pitches that are relevant to requesting user."""

        self.object = self.get_object()
        if self.request.user.talenteditorprofile:
            editor = self.request.user.talenteditorprofile
            active_pitches = self.object.get_active_pitches()
            pitches_for_viewer = active_pitches.filter(recipient=editor)
        elif self.request.user.contractorprofile:
            pitches_for_viewer = self.object.get_active_pitches()
        else:
            pitches_for_viewer = []
        return pitches_for_viewer


class ContractorUpdateView(UpdateView):
    """Edit a contractor's profile."""

    model = ContractorProfile
    form_class = ContractorProfileForm

    def get_success_url(self):
        """Record action for activity stream."""

        action.send(self.request.user, verb="edited", action_object=self.object)
        return super(ContractorUpdateView, self).get_success_url()

# Currently in use as regular Dashboard alternate
# class ContractorDashboardView(DetailView):
#     """A dashboard of relevant content for a contractor."""
#
#     model = ContractorProfile
#     template_name = 'editorial/contractor_dashboard.html'
#
#     def assignments(self):
#         """Return all active assignments for a contractor."""
#
#         self.object = self.get_object()
#         return self.object.get_active_assignments()
#
#     def calls(self):
#         """Return all active calls."""
#
#         return Call.objects.filter(Q(is_active=True)| Q(status="Publised")).order_by('-creation_date')
#
#     def pitches(self):
#         """Return all active pitches from a contractor."""
#
#         self.object = self.get_object()
#         return self.object.get_active_pitches()
#
#     def communication(self):
#         """ Return recent communication relevant for a contractor."""
#
#         return PrivateMessage.objects.filter(recipient=self.object.user).order_by('date')

#----------------------------------------------------------------------#
#   Talent Editor Views
#----------------------------------------------------------------------#

# A profile page for contract editors
class PublicTalentEditorDetailView(DetailView):
    """Display details about an editor that works with contractors."""

    model = TalentEditorProfile
    template_name = 'editorial/talenteditor_detail.html'

    def assignments(self):
        """Get assignments from this editor that are relevant to requesting
        user.
        """

        self.object = self.get_object()
        editor = self.object
        contractor = self.request.user.contractorprofile
        active_assignments = editor.assignment_set.all()
        assignments_for_viewer = active_assignments.filter(contractor=contractor)
        return active_assignments

    def pitches(self):
        """Get pitches to this editor that are relevant to contractor viewing
        this profile."""

        self.object = self.get_object()
        editor = self.object
        contractor = self.request.user.contractorprofile
        active_pitches = editor.pitch_set.all()
        pitches_for_viewer = active_pitches.filter(contractor=contractor)
        return pitches_for_viewer

    def calls(self):
        """Return calls from this editor."""

        self.object = self.get_object()
        calls = self.object.call_set.all()
        return calls


class PublicTalentEditorDashboardView(DetailView):
    """A dashboard of relevant content for a contractor."""

    model = User
    template_name = 'editorial/talenteditor_dashboard.html'

    def assignments(self):
        """Return all active assignments."""

        return self.object.assignment_set.filter(complete=False)

    def calls(self):
        """Return all active calls."""

        self.object = self.get_object()
        return self.object.call_set.all()

    def pitches(self):
        """Return all active pitches from a contractor."""

        self.object = self.get_object()
        return self.object.pitch_set.all()

    def communication(self):
        """ Return recent communication relevant for a talenteditor."""

        contractors = ContractorProfile.objects.all()
        return PrivateMessage.objects.filter(Q(recipient=self.object)).order_by('date')

#----------------------------------------------------------------------#
#   Public Listing Views
#----------------------------------------------------------------------#

class PublicContractorListView(ListView):
    """Listing of all public contractors."""

    context_object_name = "contractors"
    template_name = "editorial/publiccontractor_list.html"

    def get_queryset(self):
        """Return all contractors that have opted into public listing."""

        public_contractors = ContractorProfile.objects.filter(public=True)
        return public_contractors


class PublicTalentEditorListView(ListView):
    """Listing of all public contractors."""

    context_object_name = "editors"
    template_name = "editorial/publictalenteditor_list.html"

    def get_queryset(self):
        """Return all users that are editors or admins that have opted into public listing."""

        public_editors = TalentEditorProfile.objects.filter(Q(public=True))
        return public_editors

#----------------------------------------------------------------------#
#   Organization / Contractor Affiliation Views
#----------------------------------------------------------------------#

class AffiliationListView(ListView):
    """Return all the contractors that an organization has a relationship with."""

    context_object_name = "affiliations"
    template_name='editorial/affiliation_list.html'

    def get_queryset(self):
        """Return all the contractors associated with an organization."""

        affiliations = OrganizationContractorAffiliation.objects.filter(organization=self.request.user.organization)
        return affiliations


class AffiliationCreateView(CreateView):
    """Create a relationship between a contractor and an organization."""

    model = OrganizationContractorAffiliation
    form_class = OrganizationContractorAffiliationForm
    template_name='editorial/affiliation_form.html'

    def form_valid(self, form):
        """Save -- but first connect to organization."""

        self.object = relationship = form.save(commit=False)

        relationship.organization = self.request.user.organization

        relationship.save()
        form.save_m2m()

        return redirect(self.get_success_url())


class AffiliationDetailView(DetailView):
    """Display the details of an affiliation between an organization and a
    contractor.
    """

    model = OrganizationContractorAffiliation
    template_name='editorial/affiliation_detail.html'


class AffiliationUpdateView(UpdateView):
    """ Edit the record of affiliation between an organization and a
    contractor.
    """

    model = OrganizationContractorAffiliation
    form_class = OrganizationContractorAffiliationForm
    template_name='editorial/affiliation_form.html'

    def get_success_url(self):
        """ Record action for activity stream."""

        action.send(self.request.user, verb="edited", action_object=self.object)
        return super(AffiliationUpdateView, self).get_success_url()


#----------------------------------------------------------------------#
#   Pitch Views
#----------------------------------------------------------------------#

class PitchCreateView(CreateView):
    """Create a pitch."""

    model = Pitch
    form_class = PitchForm

    def form_valid(self, form):
        """Save -- but first save some details."""

        self.object = pitch = form.save(commit=False)

        pitch.contractor = self.request.user.contractorprofile

        pitch.save()
        form.save_m2m()

        return redirect(self.get_success_url())


class PitchDetailView(DetailView):
    """Show pitch details."""

    model = Pitch

    def simple_images(self):
        """Return simple images."""

        self.object = self.get_object()
        images = self.object.simple_image_assets.all()
        form = SimpleImageForm()
        return {'images': images, 'form':form,}

    def simple_documents(self):
        """Return simple documents."""

        self.object = self.get_object()
        documents = self.object.simple_document_assets.all()
        form = SimpleDocumentForm()
        return {'documents': documents, 'form':form,}

    def simple_audio(self):
        """Return simple audio."""

        self.object = self.get_object()
        audio = self.object.simple_audio_assets.all()
        form = SimpleAudioForm()
        return {'audio': audio, 'form':form,}


    def simple_video(self):
        """ Return simple video."""

        self.object = self.get_object()
        video = self.object.simple_video_assets.all()
        form = SimpleVideoForm()
        return {'video': video, 'form':form,}


class PitchUpdateView(UpdateView):
    """View and edit a pitch. Add assets to a pitch."""

    model = Pitch
    form_class = PitchForm

    def simple_images(self):
        """Return all the associated simple images and the form to add.
        """

        self.object = self.get_object()
        images = self.object.simple_image_assets.all()
        form = SimpleImageForm()
        return {'images': images, 'form': form}

    def simple_documents(self):
        """Return all the associated simple docs and the form to add.
        """

        self.object = self.get_object()
        documents = self.object.simple_document_assets.all()
        form = SimpleDocumentForm()
        return {'documents': documents, 'form': form}

    def simple_audio(self):
        """Return all the associated simple audio and the form to add.
        """

        self.object = self.get_object()
        audio = self.object.simple_audio_assets.all()
        form = SimpleAudioForm()
        return {'audio': audio, 'form': form}

    def simple_video(self):
        """Return all associated simple video and the form to add.
        """

        self.object = self.get_object()
        videos = self.object.simple_video_assets.all()
        form = SimpleVideoForm()
        return {'videos': videos, 'form': form}


    def get_success_url(self):
        """Record action for activity stream."""

        action.send(self.request.user, verb="edited", action_object=self.object)
        return super(PitchUpdateView, self).get_success_url()


# class PitchDeleteView(DeleteView, FormMessagesMixin):
class PitchDeleteView(DeleteView):
    """Delete a pitch."""
    pass

#----------------------------------------------------------------------#
#   Call Views
#----------------------------------------------------------------------#

class CallCreateView(CreateView):
    """Create a call."""

    model = Call
    form_class = CallForm

    def get_form_kwargs(self):
        """Pass current user organization to the form."""

        kw = super(CallCreateView, self).get_form_kwargs()
        kw.update({'organization': self.request.user.organization})
        return kw

    def form_valid(self, form):
        """Save -- but first save some details."""

        self.object = call = form.save(commit=False)

        call.owner = self.request.user
        call.organization = self.request.user.organization

        call.save()
        form.save_m2m()

        return redirect(self.get_success_url())


class CallDetailView(DetailView):
    """Show call details."""

    model = Call

    def simple_images(self):
        """Return simple images."""

        self.object = self.get_object()
        images = self.object.simple_image_assets.all()
        form = SimpleImageForm()
        return {'images': images, 'form':form,}

    def simple_documents(self):
        """Return simple documents."""

        self.object = self.get_object()
        documents = self.object.simple_document_assets.all()
        form = SimpleDocumentForm()
        return {'documents': documents, 'form':form,}

    def simple_audio(self):
        """Return simple audio."""

        self.object = self.get_object()
        audio = self.object.simple_audio_assets.all()
        form = SimpleAudioForm()
        return {'audio': audio, 'form':form,}


    def simple_video(self):
        """ Return simple video."""

        self.object = self.get_object()
        video = self.object.simple_video_assets.all()
        form = SimpleVideoForm()
        return {'video': video, 'form':form,}


class CallUpdateView(UpdateView):
    """Edit a call."""

    model = Call
    form_class = CallForm

    def get_form_kwargs(self):
        """Pass current user organization to the form."""

        kw = super(CallUpdateView, self).get_form_kwargs()
        kw.update({'organization': self.request.user.organization})
        return kw

    def simple_images(self):
        """Return all the associated simple images and the form to add.
        """

        self.object = self.get_object()
        images = self.object.simple_image_assets.all()
        form = SimpleImageForm()
        return {'images': images, 'form': form}

    def simple_documents(self):
        """Return all the associated simple docs and the form to add.
        """

        self.object = self.get_object()
        documents = self.object.simple_document_assets.all()
        form = SimpleDocumentForm()
        return {'documents': documents, 'form': form}

    def simple_audio(self):
        """Return all the associated simple audio and the form to add.
        """

        self.object = self.get_object()
        audio = self.object.simple_audio_assets.all()
        form = SimpleAudioForm()
        return {'audio': audio, 'form': form}

    def simple_video(self):
        """Return all associated simple video and the form to add.
        """

        self.object = self.get_object()
        videos = self.object.simple_video_assets.all()
        form = SimpleVideoForm()
        return {'videos': videos, 'form': form}

    def get_success_url(self):
        """Record action for activity stream."""

        action.send(self.request.user, verb="edited", action_object=self.object)
        return super(CallUpdateView, self).get_success_url()


# class CallListView(ListView):
#     """List all calls from public talent editors."""
#
#     context_object_name = 'calls'
#
#     def get_queryset(self):
#         """Return all calls from public talent editors."""
#
#         if self.request.user.contractorprofile:
#             calls = Call.objects.filter(Q(is_active=True) & Q(status='Published'))
#         elif self.request.user.talenteditor:
#             calls =



# class CallDeleteView(DeleteView, FormMessagesMixin):
class CallDeleteView(DeleteView):
    """Delete a call."""
    pass

#----------------------------------------------------------------------#
#   Assignment Views
#----------------------------------------------------------------------#

class AssignmentCreateView(CreateView):
    """Create a new assignment."""

    model = Assignment
    form_class = AssignmentForm

    def get_form_kwargs(self):
        """Pass current user organization to the form."""

        kw = super(AssignmentCreateView, self).get_form_kwargs()
        kw.update({'organization': self.request.user.organization})
        return kw

    def form_valid(self, form):
        """Save -- but first same some details."""

        self.object = assignment = form.save(commit=False)

        assignment.editor = self.request.user
        assignment.organization = self.request.organization

        assignment.save()
        form.save_m2m()

        return redirect(self.get_success_url())


class AssignmentDetailView(DetailView):
    """Show assignment details."""

    model = Assignment

    def simple_images(self):
        """Return simple images."""

        self.object = self.get_object()
        images = self.object.simple_image_assets.all()
        form = SimpleImageForm()
        return {'images': images, 'form':form,}

    def simple_documents(self):
        """Return simple documents."""

        self.object = self.get_object()
        documents = self.object.simple_document_assets.all()
        form = SimpleDocumentForm()
        return {'documents': documents, 'form':form,}

    def simple_audio(self):
        """Return simple audio."""

        self.object = self.get_object()
        audio = self.object.simple_audio_assets.all()
        form = SimpleAudioForm()
        return {'audio': audio, 'form':form,}


    def simple_video(self):
        """ Return simple video."""

        self.object = self.get_object()
        video = self.object.simple_video_assets.all()
        form = SimpleVideoForm()
        return {'video': video, 'form':form,}


class AssignmentUpdateView(UpdateView):
    """Edit an assignment."""

    model = Assignment
    form_class = AssignmentForm

    def get_form_kwargs(self):
        """Pass current user organization to the form."""

        kw = super(AssignmentUpdateView, self).get_form_kwargs()
        kw.update({'organization': self.request.user.organization})
        return kw

    def simple_images(self):
        """Return all the associated simple images and the form to add.
        """

        self.object = self.get_object()
        images = self.object.simple_image_assets.all()
        form = SimpleImageForm()
        return {'images': images, 'form': form}

    def simple_documents(self):
        """Return all the associated simple docs and the form to add.
        """

        self.object = self.get_object()
        documents = self.object.simple_document_assets.all()
        form = SimpleDocumentForm()
        return {'documents': documents, 'form': form}

    def simple_audio(self):
        """Return all the associated simple audio and the form to add.
        """

        self.object = self.get_object()
        audio = self.object.simple_audio_assets.all()
        form = SimpleAudioForm()
        return {'audio': audio, 'form': form}

    def simple_video(self):
        """Return all associated simple video and the form to add.
        """

        self.object = self.get_object()
        videos = self.object.simple_video_assets.all()
        form = SimpleVideoForm()
        return {'videos': videos, 'form': form}

    def get_success_url(self):
        """Record action for activity stream."""

        action.send(self.request.user, verb="edited", action_object=self.object)
        return super(AssignmentUpdateView, self).get_success_url()


# class AssignmentDeleteView(DeleteView, FormMessagesMixin):
class AssignmentDeleteView(DeleteView):
    """Delete an assignment."""
    pass
