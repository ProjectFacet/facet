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

# def org_new(request):
#     """ A user can create an organization after signing up.
#     Ex. A member of a news organization creates an organization account for the newsroom.
#     Ex. A freelancer can create their own organization to form a network with any newsroom
#     they regularly contribute to.
#     """
#
#     orgform = OrganizationForm()
#     if request.method == "POST":
#         orgform = OrganizationForm(request.POST, request.FILES)
#         if orgform.is_valid():
#             organization = orgform.save(commit=False)
#             organization.owner = request.user
#             organization.creation_date = timezone.now()
#             organization.logo = request.FILES['logo']
#             discussion = Discussion.objects.create_discussion("ORG")
#             organization.discussion = discussion
#             organization.save()
#             # update user to connect them to the organization
#             current_user = get_object_or_404(User, pk=request.user.id)
#             current_user.organization = organization
#             current_user.save()
#             return redirect('org_detail', pk=organization.pk)
#     else:
#         form = OrganizationForm()
#     return render(request, 'editorial/organizationnew.html', {
#             'orgform': orgform,
#             })

class OrganizationCreateView(generic.CreateView):
    """Create a new organization."""

    model = Organization
    form_class = OrganizationForm

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(OrganizationCreateView, self).form_valid(form)

    def get_success_url(self):
        # TODO: move this to model
        # discussion = Discussion.objects.create_discussion("ORG")
        # self.object.discussion = discussion

        self.request.user.organization = self.object
        self.request.user.save()
        return reverse('org_detail', kwargs={'pk': self.object.pk})



class OrganizationUpdateView(generic.UpdateView):
    """Create a new organization."""

    model = Organization
    form_class = OrganizationForm

    def get_context_data(self, **kwargs):
        """Add related info."""

        # in template:    {{ teamembers }}
        context = super(OrganizationUpdateView, self).get_context_data(**kwargs)
        # context['team_members'] = Organization.get_org_users(self.object)
        context['team_members'] = self.object.get_org_users()
        return context

    # def teamembers(self):
    #     # in template:    {{ view.teammembers }}
    #     return ....

# def org_detail(request, pk):
#     """ The public profile of an organization.
#
#     Visible to users/organizations in the same networks.
#     Displays the organization's name, logo, description, team members, most recent
#     shared content, admin email addresses.
#     """
#
#     organization = get_object_or_404(Organization, pk=pk)
#     organizationnoteform = OrganizationNoteForm()
#     organizationnotes = OrganizationNote.objects.filter(organization=organization)[:5]
#     users = Organization.get_org_users(organization)
#     organizationcomments = Comment.objects.filter(discussion=organization.discussion).order_by('-date')
#     organizationcommentform = OrganizationCommentForm()
#
#     return render(request, 'editorial/organizationdetail.html', {
#         'organization': organization,
#         'organizationnoteform': organizationnoteform,
#         'organizationnotes': organizationnotes,
#         'organizationcomments': organizationcomments,
#         'organizationcommentform': organizationcommentform,
#         })


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



# def org_edit(request, pk):
#     """ Edit organization page."""
#
#     organization = get_object_or_404(Organization, pk=pk)
#     team_members = Organization.get_org_users(organization)
#
#     if request.method == "POST":
#         orgform = OrganizationForm(request.POST, request.FILES, instance=organization)
#         if orgform.is_valid():
#             orgform.save()
#             return redirect('org_detail', pk=organization.id)
#     else:
#         orgform = OrganizationForm(instance=organization)
#
#     return render(request, 'editorial/organizationedit.html', {
#             'organization': organization,
#             'orgform': orgform,
#             'team': team_members,
#     })
