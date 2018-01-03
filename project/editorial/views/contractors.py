# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.core.urlresolvers import reverse
from django.views.generic import CreateView, FormView, UpdateView, DetailView, ListView, DeleteView, TemplateView
from actstream import action
from django.db.models import Q
from braces.views import LoginRequiredMixin, FormMessagesMixin

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

# ACCESS: Any user not affiliated with an organization should be able to create
class ContractorCreateView(LoginRequiredMixin, CreateView):
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
                                                        )

        subscription.save()

        contractor.save()
        form.save_m2m()

        return redirect(self.get_success_url())


# ACCESS: Any org user with talenteditorprofile
# Contractors should see their own profiles
# Future: Contractors can see each other/message each other (eventually collaborate as individuals)
class ContractorDetailView(LoginRequiredMixin, DetailView):
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
        contractor = self.object
        if self.request.user.talenteditorprofile:
            editor = self.request.user.talenteditorprofile
            active_pitches = self.object.get_active_pitches()
            pitches_for_viewer = active_pitches.filter(recipient=editor)
        elif self.request.user.contractorprofile:
            pitches_for_viewer = self.object.get_active_pitches()
        else:
            pitches_for_viewer = []
        return pitches_for_viewer


# ACCESS: Only a contractor can update their profile
class ContractorUpdateView(LoginRequiredMixin, UpdateView):
    """Edit a contractor's profile."""

    model = ContractorProfile
    form_class = ContractorProfileForm

    def get_success_url(self):
        """Record action for activity stream."""

        action.send(self.request.user, verb="edited", action_object=self.object)
        return super(ContractorUpdateView, self).get_success_url()


#----------------------------------------------------------------------#
#   Talent Editor Views
#----------------------------------------------------------------------#

# ACCESS: All org users with a publictalenteditor profile should see the
# other ones from their org.
# All contractors should be able to see
class PublicTalentEditorDetailView(LoginRequiredMixin, DetailView):
    """A public profile page for talent editors. Displays details about an editor
    that works with contractors.
    Contractors see assignments and calls from this editor and pitches they've submitted.
    """

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


# ACCESS: Only the user associated with the profile
class PublicTalentEditorDashboardView(LoginRequiredMixin, DetailView):
    """A dashboard of relevant content for a contractor."""

    model = TalentEditorProfile
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

        self.object = self.get_object()
        user = get_object_or_404(User, id=self.object.user.id)
        contractors = ContractorProfile.objects.all()
        return PrivateMessage.objects.filter(Q(recipient=user)).order_by('date')


#----------------------------------------------------------------------#
#   Public Listing Views
#----------------------------------------------------------------------#

# ACCESS: Only users with talenteditorprofile
# FUTURE contractors will be able to see each other (future functionality for individual collaborations)
class PublicContractorListView(LoginRequiredMixin, ListView):
    """Listing of all public contractors."""

    context_object_name = "contractors"
    template_name = "editorial/publiccontractor_list.html"

    def get_queryset(self):
        """Return all contractors that have opted into public listing."""

        public_contractors = ContractorProfile.objects.filter(public=True)
        return public_contractors


# ACCESS: Contractors can access
# TalentEditors can only see other editors from their org
class PublicTalentEditorListView(LoginRequiredMixin, ListView):
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

# ACCESS: TalentEditors and admin can access an org's affiliation list
# Future: May be another view to include organization/pk/ in url
class AffiliationListView(LoginRequiredMixin, ListView):
    """Return all the contractors that an organization has a relationship with."""

    context_object_name = "affiliations"
    template_name='editorial/affiliation_list.html'

    def get_queryset(self):
        """Return all the contractors associated with an organization."""

        affiliations = OrganizationContractorAffiliation.objects.filter(organization=self.request.user.organization)
        return affiliations


# ACCESS: Only TalentEditors can access
class AffiliationCreateView(LoginRequiredMixin, CreateView):
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


# ACCESS: Only TalentEditors, admins can access an org's affiliations
class AffiliationDetailView(LoginRequiredMixin, DetailView):
    """Display the details of an affiliation between an organization and a
    contractor.
    """

    model = OrganizationContractorAffiliation
    template_name='editorial/affiliation_detail.html'


# ACCESS: Only TalentEditors, admins from an org can edit affiliations of that org
class AffiliationUpdateView(LoginRequiredMixin, UpdateView):
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

# ACCESS: Only contractorprofile users
class PitchCreateView(LoginRequiredMixin, CreateView):
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

# ACCESS: Contractorprofile users, talenteditor recipient
# FUTURE should be possible for a talenteditor to share/show a pitch with another user
# from their own org
class PitchDetailView(LoginRequiredMixin, DetailView):
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


# ACCESS: Only contractorprofile users
class PitchUpdateView(LoginRequiredMixin, UpdateView):
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
        """Return all associated simple video and the form to add."""

        self.object = self.get_object()
        videos = self.object.simple_video_assets.all()
        form = SimpleVideoForm()
        return {'videos': videos, 'form': form}

    def get_success_url(self):
        """Record action for activity stream."""

        action.send(self.request.user, verb="edited", action_object=self.object)
        return super(PitchUpdateView, self).get_success_url()


# ACCESS: Only contractorprofile users
class PitchListView(LoginRequiredMixin, ListView):
    """Return all of a contractor's pitches."""

    context_object_name = 'pitches'

    def get_queryset(self):
        """Return all pitches related to the requesting user."""

        user = self.request.user
        user = get_object_or_404(User, id=user.id)
        contractorprofile = ContractorProfile.objects.filter(user=user)
        talenteditorprofile = TalentEditorProfile.objects.filter(user=user)
        if talenteditorprofile:
            pitches = Pitch.objects.filter(recipient=talenteditorprofile)
        elif contractorprofile:
            pitches = user.contractorprofile.get_active_pitches()
        else:
            pitches = []
        return pitches


# ACCESS: Only contractorprofile users
# class PitchDeleteView(DeleteView, FormMessagesMixin):
class PitchDeleteView(LoginRequiredMixin, DeleteView):
    """Delete a pitch.

    In this project, we expect deletion to be done via a JS pop-up UI; we don't expect to
    actually use the "do you want to delete this?" Django-generated page. However, this is
    available if useful.
    """

    # FIXME: this would be a great place to use braces' messages; usage commented out for now

    model = Pitch
    template_name = "editorial/pitch_delete.html'"

    # form_valid_message = "Deleted."
    # form_invalid_message = "Please check form."

    def get_success_url(self):
        """Post-deletion, return to the pitch list."""

        return reverse('pitch_list')


#----------------------------------------------------------------------#
#   Call Views
#----------------------------------------------------------------------#

# ACCESS: Only talenteditor users
class CallCreateView(LoginRequiredMixin, CreateView):
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


# ACCESS: TalentEditor users + admins from the org
# All contractorprofile users
class CallDetailView(LoginRequiredMixin, DetailView):
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


# ACCESS: TalentEditor User that owns it (Maybe other TE from same org?)
class CallUpdateView(LoginRequiredMixin, UpdateView):
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


# ACCESS: TalentEditors should only see calls from their own org
# Contractors see all calls
class CallListView(LoginRequiredMixin, ListView):
    """List all calls from public talent editors."""

    context_object_name = 'calls'

    def get_queryset(self):
        """Return all callss related to the requesting user."""

        user = self.request.user
        user = get_object_or_404(User, id=user.id)
        contractorprofile = ContractorProfile.objects.filter(user=user)
        talenteditorprofile = TalentEditorProfile.objects.filter(user=user)
        # talent editor, view all org calls. Editors from different orgs
        # shouldn't be able to see other org calls.
        if talenteditorprofile:
            calls = Call.objects.filter(organization=user.organization)
        # if contractor, view all calls from all editors
        elif contractorprofile:
            calls = Call.objects.filter(Q(is_active=True) & Q(status='Published'))
        else:
            calls = []
        return calls


# ACCESS: The TalentEditor that owns it or an admin of the organization
# class CallDeleteView(DeleteView, FormMessagesMixin):
class CallDeleteView(LoginRequiredMixin, DeleteView):
    """Delete a call.

    In this project, we expect deletion to be done via a JS pop-up UI; we don't expect to
    actually use the "do you want to delete this?" Django-generated page. However, this is
    available if useful.
    """

    # FIXME: this would be a great place to use braces' messages; usage commented out for now

    model = Call
    template_name = "editorial/call_delete.html'"

    # form_valid_message = "Deleted."
    # form_invalid_message = "Please check form."

    def get_success_url(self):
        """Post-deletion, return to the call list."""

        return reverse('call_list')


#----------------------------------------------------------------------#
#   Assignment Views
#----------------------------------------------------------------------#

# ACCESS: Only talenteditor users
class AssignmentCreateView(LoginRequiredMixin, CreateView):
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


# ACCESS: TalentEditor users + admins from the org
# The Contractor connected to the assignment
class AssignmentDetailView(LoginRequiredMixin, DetailView):
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


# ACCESS: TalentEditor users + admins from the org
class AssignmentUpdateView(LoginRequiredMixin, UpdateView):
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


# ACCESS: TalentEditor sees all of their assignments
# Contractor sees all of their assignments
class AssignmentListView(LoginRequiredMixin, ListView):
    """Return all the assignments dependent on viewer."""

    context_object_name = 'assignments'

    def get_queryset(self):
        """Return all assignments related to the requesting user."""

        user = self.request.user
        user = get_object_or_404(User, id=user.id)
        contractorprofile = ContractorProfile.objects.filter(user=user)
        talenteditorprofile = TalentEditorProfile.objects.filter(user=user)
        if talenteditorprofile:
            assignments = user.talenteditorprofile.assignment_set.all()
        elif contractorprofile:
            assignments = user.contractorprofile.get_active_assignments()
        else:
            assignments = []
        return assignments


# ACCESS: The TalentEditor that owns it or an admin of the organization
# class AssignmentDeleteView(DeleteView, FormMessagesMixin):
class AssignmentDeleteView(LoginRequiredMixin, DeleteView):
    """Delete an assignment.

    In this project, we expect deletion to be done via a JS pop-up UI; we don't expect to
    actually use the "do you want to delete this?" Django-generated page. However, this is
    available if useful.
    """

    # FIXME: this would be a great place to use braces' messages; usage commented out for now

    model = Assignment
    template_name = "editorial/assignment_delete.html'"

    # form_valid_message = "Deleted."
    # form_invalid_message = "Please check form."

    def get_success_url(self):
        """Post-deletion, return to the assignment list."""

        return reverse('assignment_list')
