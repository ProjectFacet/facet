"""General views for editorial app."""

# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from django.utils import timezone
from django.views.generic import TemplateView , UpdateView, DetailView, ListView, CreateView
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta, time
import json
from django.template.loader import render_to_string
from django.db.models import Q, Count
from braces.views import LoginRequiredMixin, FormMessagesMixin

# All imports are included for use in test view

from editorial.forms import (
    AddUserForm,
    UserProfileForm,
    OrganizationForm,
    NetworkForm,
    StoryForm,
    ImageAssetForm,
    DocumentAssetForm,
    AddToNetworkForm,
    InviteToNetworkForm,
    PrivateMessageForm,
    CommentForm,
    NoteForm,
    )

from editorial.models import (
    User,
    Organization,
    Network,
    Project,
    Story,
    Task,
    Event,
    Call,
    Pitch,
    Assignment,
    Facet,
    Note,
    ImageAsset,
    DocumentAsset,
    AudioAsset,
    VideoAsset,
    Comment,
    PrivateMessage,
    Discussion,
    StoryCopyDetail,
    )


#----------------------------------------------------------------------#
#   Initial View
#----------------------------------------------------------------------#

# This is the only general view that does not require login
class LandingTemplateView(TemplateView):
    """Return static homepage for pre-login users."""

    template_name = 'editorial/home.html'


#----------------------------------------------------------------------#
#   Dashboard View
#----------------------------------------------------------------------#

# ACCESS: All users have access to dashboard
class DashboardTemplateView(LoginRequiredMixin, TemplateView):
    """ Returns user's unique dashboard."""

    template_name = 'editorial/dashboard.html'

    def get_context_data(self):
        """Return all the assorted items associated with a user's dashboard."""
        # placeholder of data for now to maintain status quo

        user = self.request.user

        if user.organization:
            org = user.organization
            older_comments = user.inbox_comments()[:4]
            all_comments = org.get_org_comments()
            networks = org.get_org_networks()
            running_today = org.get_org_stories_running_today()
            edit_today = org.get_org_stories_due_for_edit_today()

            shared_networkstories = (org.get_org_network_content()
                                     .exclude(organization=org)
                                     .annotate(num_facets=Count('facet'))
                                     .distinct())
            # shared_networkstories = [story for story in shared_networkstories if story.organization != org]
            networkstories = set(shared_networkstories)

            # query for any new content created since last_login
            new_stories = Story.objects.filter(creation_date__gte=user.last_login)[:8]
            # new_projects = Project.objects.filter(creation_date__gte = self.request.user.last_login)[:8]

            # if no new, display 10 most recent stories
            recent_stories = Story.objects.filter(organization=org)[:10]
            # recent_projects = Project.objects.filter(organization = self.request.user.organization)[:10]

            copied_shared_stories = StoryCopyDetail.objects.filter(original_org=org)

            print "*******************************"
            print all_comments
            print older_comments

            return {
                'networks': networks,
                'older_comments': older_comments,
                'all_comments': all_comments,
                'new_stories': new_stories,
                'recent_stories': recent_stories,
                'running_today': running_today,
                'edit_today': edit_today,
                'shared_networkstories': shared_networkstories,
                'copied_shared_stories': copied_shared_stories,
                'networkstories': networkstories,
                # 'shared_networkstory_facets': shared_networkstory_facets,
            }

        elif user.contractorprofile:
            contractor = user.contractorprofile
            assignments = contractor.get_active_assignments()
            calls = Call.objects.filter(Q(is_active=True)| Q(status="Published")).order_by('-creation_date')
            pitches = contractor.get_active_pitches()
            communication = PrivateMessage.objects.filter(recipient=user).order_by('date')
            return {
                'assignments': assignments,
                'calls': calls,
                'pitches': pitches,
                'communication': communication,
            }

        elif not user.organization and not user.contractorprofile:
            return HttpResponseRedirect('account_selection')


#----------------------------------------------------------------------#
#   Team Views
#----------------------------------------------------------------------#

# ACCESS: All org users have access to team view for their organization
class TeamTemplateView(LoginRequiredMixin, TemplateView):
    """ Return teams list.

    Displays team members from the user's own organization.
    Displays team members from any network that the user's organization is part of.
    """

    template_name = 'editorial/team.html'

    def get_context_data(self):
        """Retrieve team of org and partner orgs."""

        # the user's organization
        organization = self.request.user.organization
        networks = organization.get_org_networks()
        partners = organization.get_org_collaborators_vocab()

        # form for adding a new user to the team
        adduserform = AddUserForm()
        # only visible for admin users

        return {
            'organization': organization,
            'networks': networks,
            'partners': partners,
            'adduserform': adduserform,
        }


#----------------------------------------------------------------------#
#   Collaborations View
#----------------------------------------------------------------------#

# ACCESS: All org users have access to their org's list of collaborations.
class CollaborationTemplateView(LoginRequiredMixin, TemplateView):
    """Return dashboard of projects and stories that are part of a collaboration."""

    template_name = 'editorial/collaborations.html'

    def get_context_data(self):
        external_collaborations = self.request.user.organization.get_org_external_collaborations()
        return {
            'external_collaborations': external_collaborations,
        }
