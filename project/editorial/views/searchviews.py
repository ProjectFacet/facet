""" Custom search view for editorial app.

    Subclasses waton get_queryset to filter for only results
    from a user's own organization.
"""

# -*- coding: utf-8 -*-
from __future__ import unicode_literals
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
    Project,
    Network,
    Series,
    Story,
    Facet,
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
        searchable_org_objects = user_org.get_org_searchable_content()
        searchable_user_objects = user.get_user_searchable_content()
        print "**************************************"
        print "SUO: ", searchable_user_objects

        # unpack the querysets from the list of querysets returned
        projects, series, stories, facets, imageassets, networknotes, orgnotes, seriesnotes, storynotes = searchable_org_objects
        usernotes = searchable_user_objects

        # pass all querysets to search method
        return watson.search(self.query, models=[projects, series, stories, facets, imageassets, networknotes, orgnotes, seriesnotes, storynotes, usernotes])
