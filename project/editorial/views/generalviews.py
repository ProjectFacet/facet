""" General views for editorial app. """

# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponse
from django.utils import timezone
from django.views.generic import TemplateView , UpdateView, DetailView, ListView, CreateView
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta, time
import json
from django.template.loader import render_to_string
from django.db.models import Q

# All imports are included for use in test view

from editorial.forms import (
    AddUserForm,
    UserProfileForm,
    OrganizationForm,
    NetworkForm,
    SeriesForm,
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
    Series,
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

class LandingTemplateView(TemplateView):
    """Return static homepage for prelogin users."""

    template_name = 'editorial/home.html'

    # def get_context_data(self):
    #


#----------------------------------------------------------------------#
#   Test View
#----------------------------------------------------------------------#

class TestTemplateView(TemplateView):
    """ Use for rapid testing of new pages."""

    template_name = 'editorial/test.html'

    def get_context_data(self):
        # the user's organization
        organization = self.request.user.organization
        tasks = Task.objects.filter(organization=organization)

        return {
            'organization': organization,
            'tasks': tasks,
        }


#----------------------------------------------------------------------#
#   Dashboard View
#----------------------------------------------------------------------#

class DashboardTemplateView(TemplateView):
    """ Returns user's unique dashboard.

    Displays new comments since last_login from any discussions including user.
    Ex: Felicity S. replied to Series: "Palmer Tech Innovation Conference" discussion
    Displays table of new content created since last_login
    Displays any content with deadlines sameday/next day for any content where user is part of team.
    Displays log of other user activity since last_login
    Ex: Oliver Q. added "Dhark Indicted" to Story: "Star City Organized Crime Leader Arrested"
    """

    template_name = 'editorial/dashboard.html'

    def get_context_data(self):
        """Return all the assorted items associated with a team user dashboard."""

        # placeholder of data for now to maintain status quo
        # some rethinking about what goes here tbd

        if self.request.user.organization:
            organization = self.request.user.organization
            recent_comments = self.request.user.recent_comments()
            older_comments = self.request.user.inbox_comments()[:4]

            all_comments = organization.get_org_comments()
            networks = organization.get_org_networks()
            running_today = organization.get_org_stories_running_today()
            edit_today = organization.get_org_stories_due_for_edit_today()

            shared_networkstories = organization.get_org_network_content()
            shared_networkstories = [story for story in shared_networkstories if story.organization != organization]
            networkstories = set(shared_networkstories)
            # query for any new content created since last_login
            new_stories = Story.objects.filter(creation_date__gte = self.request.user.last_login)[:8]
            # if no new stories, display 10 most recent stories
            old_stories = Story.objects.filter(organization = self.request.user.organization)[:10]

            copied_shared_stories = StoryCopyDetail.objects.filter(original_org=self.request.user.organization)

            return {
                'networks': networks,
                'recent_comments': recent_comments,
                'older_comments': older_comments,
                'all_comments': all_comments,
                'new_stories': new_stories,
                'old_stories': old_stories,
                'running_today': running_today,
                'edit_today': edit_today,
                'shared_networkstories': shared_networkstories,
                'copied_shared_stories': copied_shared_stories,
                'networkstories': networkstories,
                # 'shared_networkstory_facets': shared_networkstory_facets,
            }
        elif self.request.user.contractorprofile:
            contractor = self.request.user.contractorprofile
            assignments = contractor.get_active_assignments()
            print assignments
            calls = Call.objects.filter(Q(is_active=True)| Q(status="Publised")).order_by('-creation_date')
            pitches = contractor.get_active_pitches()
            communication = PrivateMessage.objects.filter(recipient=self.request.user).order_by('date')
            return {
                'assignments': assignments,
                'calls': calls,
                'pitches': pitches,
                'communication': communication,
            }

#----------------------------------------------------------------------#
#   Team Views
#----------------------------------------------------------------------#

class TeamTemplateView(TemplateView):
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

class CollaborationTemplateView(TemplateView):
    """ Return dashboard of series and stories that are part of a collaboration.
    """

    template_name = 'editorial/collaborations.html'

    def get_context_data(self):
        series_collaborations = Series.objects.filter(collaborate=True)
        story_collaborations = self.request.user.organization.get_org_collaborative_content()
        return {
            'series_collaborations': series_collaborations,
            'story_collaborations': story_collaborations,
        }
