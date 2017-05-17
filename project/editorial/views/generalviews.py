""" General views for editorial app. """

# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponse
from django.utils import timezone
from django.views.generic import TemplateView , UpdateView, DetailView
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta, time
import json
from django.template.loader import render_to_string

# All imports are included for use in test view

from editorial.forms import (
    AddUserForm,
    UserProfileForm,
    OrganizationForm,
    NetworkForm,
    SeriesForm,
    StoryForm,
    WebFacetForm,
    PrintFacetForm,
    AudioFacetForm,
    VideoFacetForm,
    ImageAssetForm,
    DocumentAssetForm,
    AddImageForm,
    AddToNetworkForm,
    InviteToNetworkForm,
    PrivateMessageForm,
    OrganizationCommentForm,
    NetworkCommentForm,
    SeriesCommentForm,
    StoryCommentForm,
    WebFacetCommentForm,
    PrintFacetCommentForm,
    AudioFacetCommentForm,
    VideoFacetCommentForm,
    NetworkNoteForm,
    OrganizationNoteForm,
    UserNoteForm,
    SeriesNoteForm,
    StoryNoteForm,
    StoryDownloadForm,)

from editorial.models import (
    User,
    Organization,
    Network,
    Series,
    Story,
    WebFacet,
    PrintFacet,
    AudioFacet,
    VideoFacet,
    SeriesNote,
    StoryNote,
    ImageAsset,
    DocumentAsset,
    AudioAsset,
    VideoAsset,
    Comment,
    PrivateMessage,
    Discussion,
    StoryCopyDetail,
    WebFacetCopyDetail,
    PrintFacetCopyDetail,
    AudioFacetCopyDetail,
    VideoFacetCopyDetail,
    NetworkNote,
    OrganizationNote,
    UserNote,
    SeriesNote,
    StoryNote,)

#----------------------------------------------------------------------#
#   Initial View
#----------------------------------------------------------------------#

# class HomeView(DetailView)
#     # return static homepage for now
#     template_name = "editorial/home.html"

# function based view
def index(request):
   """ Return static homepage."""

   return render(request, 'editorial/home.html')

#----------------------------------------------------------------------#
#   Test View
#----------------------------------------------------------------------#

def test(request):
    """ Use for rapid testing of new pages."""

    # the user's organization
    organization = request.user.organization

    return render(request, 'editorial/test.html', {
        'organization': organization,
    })


#----------------------------------------------------------------------#
#   Dashboard View
#----------------------------------------------------------------------#

def dashboard(request):
    """ Returns user's unique dashboard.

    Displays new comments since last_login from any discussions including user.
    Ex: Felicity S. replied to Series: "Palmer Tech Innovation Conference" discussion
    Displays table of new content created since last_login
    Displays any content with deadlines sameday/next day for any content where user is part of team.
    Displays log of other user activity since last_login
    Ex: Oliver Q. added "Dhark Indicted" to Story: "Star City Organized Crime Leader Arrested"
    """
    # get user organization
    organization = request.user.organization
    # query for new comments since last_login from any discussions the user has participated in
    recent_comments = User.recent_comments(request.user)
    # if no new comments, display 10 most recent older comments
    older_comments = User.inbox_comments(request.user)[:4]

    if organization:
        # retrieve all organization comments
        all_comments = Organization.get_org_comments(organization)
        # query for new stories shared to network
        networks = Organization.get_org_networks(organization)
        # facets where run_date=today
        running_today = Organization.get_org_stories_running_today(organization)
        # facets where due_edit=today
        edit_today = Organization.get_org_stories_due_for_edit_today(organization)
    else:
        all_comments = []
        networks = []
        running_today = []
        edit_today = []

    shared_networkstories = []
    for network in networks:
        stories = Network.get_network_shared_stories(network)
        shared_networkstories.extend(stories)
    shared_networkstories = [story for story in shared_networkstories if story.organization != organization]
    networkstories = set(shared_networkstories)

    shared_networkstory_facets = []
    for story in networkstories:
        ns_facet = story.get_story_facets()
        shared_networkstory_facets.extend(ns_facet)

    # query for any new content created since last_login
    new_stories = Story.objects.filter(creation_date__gte=request.user.last_login)[:8]
    # if no new stories, display 10 most recent stories
    old_stories = Story.objects.filter(organization = request.user.organization)[:10]

    copied_shared_stories = StoryCopyDetail.objects.filter(original_org=request.user.organization)

    # TODO: query for other user activity since last_login

    return render(request, 'editorial/dashboard.html', {
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
        'shared_networkstory_facets': shared_networkstory_facets,
    })

#----------------------------------------------------------------------#
#   Team Views
#----------------------------------------------------------------------#

def team_list(request):
    """ Return teams list.

    Displays team members from the user's own organization.
    Displays team members from any network that the user's organization is part of.
    """

    # the user's organization
    organization = request.user.organization
    networks = Organization.get_org_networks(organization)
    partners = Organization.get_org_collaborators(organization)

    # form for adding a new user to the team
    adduserform = AddUserForm()
    # only visible for admin users

    return render(request, 'editorial/team.html', {
        'organization': organization,
        'networks': networks,
        'partners': partners,
        'adduserform': adduserform,
        })

#----------------------------------------------------------------------#
#   Collaborations View
#----------------------------------------------------------------------#

def collaborations(request):
    """ Return dashboard of series and stories that are part of a collaboration.
    """

    series_collaborations = Series.objects.filter(collaborate=True)
    story_collaborations = Organization.get_org_collaborative_content(request.user.organization)

    return render(request, 'editorial/collaborations.html', {
        'series_collaborations': series_collaborations,
        'story_collaborations': story_collaborations,
    })
