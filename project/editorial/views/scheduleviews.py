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

from .forms import (
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
    StoryNoteForm,)

from models import (
    User,
    Organization,
    Network,
    NetworkOrganization,
    Series,
    Story,
    WebFacet,
    PrintFacet,
    AudioFacet,
    VideoFacet,
    SeriesNote,
    StoryNote,
    ImageAsset,
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
#   Schedule Views
#----------------------------------------------------------------------#

#TODO These views to be implemented
