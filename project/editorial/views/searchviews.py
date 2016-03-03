""" Custom search view for editorial app.

    Subclasses waton get_queryset to filter for only results
    from a user's own organization.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.http import HttpResponse
from django.utils import timezone
from django.views.generic import TemplateView , UpdateView, DetailView
from django.views.decorators.csrf import csrf_exempt
import datetime
import json

from watson import search as watson
from watson.views import SearchView as BaseWatsonSearchView

# All model imports are included for use in search view
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
    ImageAsset,
    Comment,
    PrivateMessage,
    Discussion,
    NetworkNote,
    OrganizationNote,
    UserNote,
    SeriesNote,
    StoryNote,)

#----------------------------------------------------------------------#
#   Custom Search View
#----------------------------------------------------------------------#

class EditorialSearchView(BaseWatsonSearchView):
    def get_queryset(self):
        """Returns list of querysets containing content a user is allowed to search.

        This is determined by a user's organization.
        """

        user_org = self.request.user.organization
        user = self.request.user

        # retrieve all content a user is allowed to search
        searchable_org_objects = Organization.get_org_searchable_content(user_org)
        searchable_user_objects = User.get_user_searchable_content(user)

        # unpack the querysets from the list of querysets returned
        series, stories, webfacets, printfacets, audiofacets, videofacets, imageassets, networknotes, orgnotes, seriesnotes, storynotes = searchable_org_objects
        usernotes = searchable_user_objects

        # pass all querysets to search method
        return watson.search(self.query, models=[series, stories, webfacets, printfacets, audiofacets, videofacets, imageassets, networknotes, orgnotes, seriesnotes, storynotes, usernotes])
