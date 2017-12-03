# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponse
from django.utils import timezone
from django.views.generic import CreateView, FormView, UpdateView, DetailView, ListView
from django.views.decorators.csrf import csrf_exempt
import datetime
import json
from actstream import action

from editorial.forms import (
    ContractorProfileForm,
    OrganizationContractorRelationshipForm,
    CallForm,
    PitchForm,
    AssignmentForm,
    )

from editorial.models import (
    User,
    ContractorProfile,
    Organization,
    OrganizationContractorAffiliation,
    Call,
    Pitch,
    Assignment,
    SimpleImage,
    SimpleDocument,
    SimpleAudio,
    SimpleVideo,
    )


#----------------------------------------------------------------------#
#   Contractor Profile Views
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

        contractor.save()
        form.save_m2m()

        return redirect(self.get_success_url())


class ContractorDetailView(DetailView):
    """Display details about a contractor."""

    model = ContractorProfile

    def contractor_assignments(self):
        """Get assignments that are relevant to requesting user."""

        self.object = self.get_object()
        editor = self.request.user
        active_assignments = self.object.get_active_assignments()
        assignments_for_viewer = active_assignments.filter(editor=editor)
        return assignments_for_viewer

    def contractor_pitches(self):
        """Get pitches that are relevant to requesting user."""
        self.object = self.get_object()
        recipient = self.request.user
        active_pitches = self.object.get_active_pitches()
        pitches_for_viewer = active_pitches.filter(recipient=recipient)
        return pitches_for_viewer


class ContractorUpdateView(UpdateView):
    """Edit a contractor's profile."""

    model = ContractorProfile
    form_class = ContractorProfileForm

    def get_success_url(self):
        """Record action for activity stream."""

        action.send(self.request.user, verb="edited", action_object=self.object)
        return super(ContractorUpdateView, self).get_success_url()


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


class PitchUpdateView(UpdateView):
    """Edit a pitch."""

    model = Pitch
    form_class = PitchForm

    def get_success_url(self):
        """Record action for activity stream."""

        action.send(self.request.user, verb="edited", action_object=self.object)
        return super(PitchUpdateView, self).get_success_url()


#----------------------------------------------------------------------#
#   Call Views
#----------------------------------------------------------------------#

class CallCreateView(CreateView):
    """Create a call."""

    model = Call
    form_class = CallForm

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


class CallUpdateView(UpdateView):
    """Edit a call."""

    model = Call
    form_class = CallForm

    def get_success_url(self):
        """Record action for activity stream."""

        action.send(self.request.user, verb="edited", action_object=self.object)
        return super(CallUpdateView, self).get_success_url()


#----------------------------------------------------------------------#
#   Assignment Views
#----------------------------------------------------------------------#

class AssignmentCreateView(CreateView):
    """Create a new assignment."""

    model = Assignment
    form_class = AssignmentForm

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


class AssignmentUpdateView(UpdateView):
    """Edit an assignment."""

    model = Assignment
    form_class = AssignmentForm

    def get_success_url(self):
        """Record action for activity stream."""

        action.send(self.request.user, verb="edited", action_object=self.object)
        return super(AssignmentUpdateView, self).get_success_url()
