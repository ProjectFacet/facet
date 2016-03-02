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
from watson.views import SearchMixin

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

class EditorialSearchView(SearchMixin):
    def get_queryset(self):
        """Returns custom queryset."""

        # user_org = self.request.user.organization
        # return watson.search(self.query, models=self.get_models().organization=user_org, exlude=self.get_exclude())

        return watson.search(self.query, models=self.get_models(), exclude=self.get_exclude())
