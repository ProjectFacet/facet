""" Schedule views for editorial app. """

from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponse
from django.utils import timezone
from django.views.generic import TemplateView , UpdateView, DetailView
from django.views.decorators.csrf import csrf_exempt
import datetime
import json

from editorial.forms import (
    StoryForm,
    WebFacetForm,
    PrintFacetForm,
    AudioFacetForm,
    VideoFacetForm,
    ImageAssetForm,
    AddImageForm,
    StoryCommentForm,
    WebFacetCommentForm,
    PrintFacetCommentForm,
    AudioFacetCommentForm,
    VideoFacetCommentForm,
    StoryNoteForm,)

from editorial.models import (
    Organization,
    Series,
    Story,
    WebFacet,
    PrintFacet,
    AudioFacet,
    VideoFacet,
    StoryNote,
    ImageAsset,
    Comment,
    Discussion,
    StoryNote,)

#----------------------------------------------------------------------#
#   Schedule Views
#----------------------------------------------------------------------#

#TODO These views to be implemented

def schedule(request):
    """ Display schedules of upcoming content.

    Calendar: Longterm view displaying only the name/title of an item with a link-text
    Agenda: Daily in-depth rundown of content for edit/running.
    """

    stories = Story.objects.filter(organization=request.user.organization).exclude(archived=True)

    content_json = {}



    return render(request, 'editorial/schedule.html', {})
