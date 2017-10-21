""" Organization views for editorial app.

    editorial/views/organization.py
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
from django.views import generic
import datetime
import json
from actstream import action
from django.core.urlresolvers import reverse


from editorial.forms import (
    OrganizationForm,
    OrganizationCommentForm,
    OrganizationNoteForm,)

from editorial.models import (
    User,
    Organization,
    ImageAsset,
    Comment,
    Discussion,
    OrganizationNote,)

# Org notes are managed in notes.py

#----------------------------------------------------------------------#
#   Organization Views
#----------------------------------------------------------------------#

class OrganizationCreateView(generic.CreateView):
    """Create a new organization."""

    model = Organization
    form_class = OrganizationForm

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(OrganizationCreateView, self).form_valid(form)

    def get_success_url(self):

        self.request.user.organization = self.object
        self.request.user.save()
        return reverse('org_detail', kwargs={'pk': self.object.pk})


class OrganizationUpdateView(generic.UpdateView):
    """Create a new organization."""

    model = Organization
    form_class = OrganizationForm

    def get_context_data(self, **kwargs):
        """Add related info."""

        context = super(OrganizationUpdateView, self).get_context_data(**kwargs)
        context['team_members'] = self.object.get_org_users()
        return context


class OrganizationDetailView(generic.DetailView):
    """Detail view of an organization."""

    model = Organization

    def get_context_data(self, **kwargs):
        """Add related info."""

        context = super(OrganizationDetailView, self).get_context_data(**kwargs)

        organizationnoteform = OrganizationNoteForm()
        organizationnotes = OrganizationNote.objects.filter(organization=self.object)[:5]
        users = Organization.get_org_users(self.object)
        organizationcomments = Comment.objects.filter(discussion=self.object.discussion).order_by('-date')
        organizationcommentform = OrganizationCommentForm()

        context.update({
                'organizationnoteform': organizationnoteform,
                'organizationnotes': organizationnotes,
                'organizationcomments': organizationcomments,
                'organizationcommentform': organizationcommentform,
        })

        return context
