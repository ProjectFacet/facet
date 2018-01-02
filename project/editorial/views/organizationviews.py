""" Organization views for editorial app.

    editorial/views/organization.py
"""

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponse
from django.utils import timezone
from django.views.generic import TemplateView , UpdateView, DetailView, ListView, CreateView, DeleteView
from django.views.decorators.csrf import csrf_exempt
from django.views import generic
import datetime
import json
from actstream import action
from django.core.urlresolvers import reverse
from django.db.models import Q
from braces.views import LoginRequiredMixin, FormMessagesMixin, UserPassesTestMixin

from editorial.forms import (
    CommentForm,
    OrganizationForm,
    NoteForm,
    OrganizationSubscriptionForm,)

from editorial.models import (
    User,
    Organization,
    OrganizationSubscription,
    ImageAsset,
    Comment,
    Discussion,
    Note,
    )

# Org notes are managed in notes.py

#----------------------------------------------------------------------#
#   Organization Views
#----------------------------------------------------------------------#


class UserMatchesOrgMixin(UserPassesTestMixin):
    """User must be a member of this organization to view this content.

    This also requires that a user be logged in, so it's not needed to use this
    with LoginRequiredMixin.
    """

    def test_func(self, user):
        """Test user.

        If there is no logged in user, go to login page.
        If there is a user, but not in this org, raise Unauthorized.
        """

        if user.is_authenticated():
            self.object = self.get_object()
            if user.organization != self.object:
                raise PermissionDenied("Not in organization %s" % self.object.id)
            else:
                return True

        return False


class OrganizationCreateView(UserMatchesOrgMixin, CreateView):
    """Create a new organization."""

    model = Organization
    form_class = OrganizationForm

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(OrganizationCreateView, self).form_valid(form)

    def get_success_url(self):

        # set the user org to the newly created org
        self.request.user.organization = self.object
        # set the user type to admin
        self.request.user.user_type = 'Admin'
        # create an organization subscription for the admin user and organization.
        subscription = OrganizationSubscription.objects.create_subscription(
                                                        organization=self.object,
                                                        collaborations=True,
                                                        contractors=False,
                                                        )
        subscription.save()

        self.request.user.save()
        return reverse('org_detail', kwargs={'pk': self.object.pk})


class OrganizationUpdateView(UserMatchesOrgMixin, UpdateView):
    """Edit an organization."""

    model = Organization
    form_class = OrganizationForm

    def get_context_data(self, **kwargs):
        """Add related info."""

        context = super(OrganizationUpdateView, self).get_context_data(**kwargs)
        context['team_members'] = self.object.get_org_users()
        return context


class OrganizationDetailView(UserMatchesOrgMixin, DetailView):
    """Detail view of an organization."""

    model = Organization

    def get_context_data(self, **kwargs):
        """Add related info."""

        context = super(OrganizationDetailView, self).get_context_data(**kwargs)

        form = NoteForm()
        notes = self.object.notes.order_by('-creation_date')[:4]
        users = Organization.get_org_users(self.object)
        organizationcomments = Comment.objects.filter(discussion=self.object.discussion).order_by('-date')
        organizationcommentform = CommentForm()

        context.update({
                'form': form,
                'notes': notes,
                'organizationcomments': organizationcomments,
                'organizationcommentform': organizationcommentform,
        })

        return context
