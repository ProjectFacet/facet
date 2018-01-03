""" Organization views for editorial app.

    editorial/views/organization.py
"""

# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from braces.views import SuperuserRequiredMixin
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.views.generic import UpdateView, DetailView, CreateView
from editorial.forms import (
    CommentForm,
    OrganizationForm,
    NoteForm,
)
from editorial.models import (
    User,
    Organization,
    OrganizationSubscription,
    Comment,
)
from editorial.views import CustomUserTest


# Org notes are managed in notes.py

#----------------------------------------------------------------------#
#   Organization Views
#----------------------------------------------------------------------#

class OrganizationCreateView(SuperuserRequiredMixin, CreateView):
    """Create a new organization."""

    model = Organization
    form_class = OrganizationForm

    def form_valid(self, form):
        """Set owner of org to current user."""

        form.instance.owner = self.request.user
        return super(OrganizationCreateView, self).form_valid(form)

    def get_success_url(self):
        """Fix up user/subscription adn redirect back to org detail page."""

        # Set current user's org to new org, and make them an admin
        user = self.request.user
        user.organization = self.object
        user.user_type = 'Admin'
        user.save()

        # create an organization subscription for the admin user and organization.
        subscription = OrganizationSubscription.objects.create_subscription(
                                                        organization=self.object,
                                                        collaborations=True,
                                                        contractors=False,
                                                        )
        subscription.save()

        return reverse('org_detail', kwargs={'pk': self.object.pk})


class OrganizationUpdateView(CustomUserTest, UpdateView):
    """Edit an organization."""

    model = Organization
    form_class = OrganizationForm

    def test_user(self, user):
        """"User must be admin of this org to edit it."""

        self.object = self.get_object()

        if user.organization == self.object and user.user_type == User.ADMIN:
            return True

        raise PermissionDenied()

    def get_context_data(self, **kwargs):
        """Add related info."""

        context = super(OrganizationUpdateView, self).get_context_data(**kwargs)
        context['team_members'] = self.object.get_org_users()
        return context


class OrganizationDetailView(CustomUserTest, DetailView):
    """Detail view of an organization."""

    model = Organization

    def test_user(self, user):
        """"User must be member of this org to edit it."""

        self.object = self.get_object()

        if user.organization == self.object:
            return True

        raise PermissionDenied()

    def get_context_data(self, **kwargs):
        """Add related info."""

        context = super(OrganizationDetailView, self).get_context_data(**kwargs)

        form = NoteForm()
        notes = self.object.notes.order_by('-creation_date')[:4]
        # users = Organization.get_org_users(self.object)
        organizationcomments = Comment.objects.filter(discussion=self.object.discussion).order_by('-date')
        organizationcommentform = CommentForm()

        context.update({
                'form': form,
                'notes': notes,
                'organizationcomments': organizationcomments,
                'organizationcommentform': organizationcommentform,
        })

        return context
