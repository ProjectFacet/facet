""" General views for editorial app. """

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
#   Inobx Views
#----------------------------------------------------------------------#

def inbox(request):
    """ Return discussion inbox.

    Displays comments from SeriesPlan Discussions involving user.
    Displays comments from StoryPlan Discussions involving user.
    Displays comments from any Facet Editing Discussion involving user.
    Displays comments from any PrivateDiscussion involving user.
    """

    comments = User.inbox_comments(request.user)

    private_messages_received = User.private_messages_received(request.user)
    private_messages_sent = User.private_messages_sent(request.user)

    return render(request, 'editorial/inbox.html', {
        'comments': comments,
        'private_messages_received': private_messages_received,
        'private_messages_sent': private_messages_sent,
    })


def sent_html(request):
    """Return sent messages"""

    sent_messages = User.private_messages_sent(request.user)

    sent_messages_html = render_to_string('sent-messages.html', {'sent_messages': sent_messages})

    return HttpResponse(sent_messages_html)


def comments_html(request, comment_type):
    """Return comment feeds."""

    print "comment type: ", comment_type
    # returns all comments involving any user of an Organization
    all_comments = Organization.get_org_user_comments(request.user.organization)

    if comment_type=="organization":
    # returns all comments made for an Organization
        comments = Organization.get_org_comments(request.user.organization)
    elif comment_type=="network":
    # returns all comments for any networks an Organization is part of
        comments = Organization.get_network_comments(request.user.organization)
    elif comment_type=="story":
    # returns all comments for any story of an Organization
        comments = Organization.get_story_comments(request.user.organization)
    elif comment_type=="series":
    # returns all comments for any series of an Organization
        comments = Organization.get_series_comments(request.user.organization)
    elif comment_type=="facet":
    # returns all comments for any facets of stories of an Organization
        comments = Organization.get_facet_comments(request.user.organization)

    comments_html = render_to_string('inbox-comments.html', {
                            'comments': comments,
                            'comment_type': comment_type,
    })

    return HttpResponse(comments_html)

# def inbox_important(request):
#     """Return important messages."""
#
#     return render(request, 'editorial/inbox.html')
#
#
# def inbox_trash(request):
#     """Return trashed messages."""
#
#     return render(request, 'editorial/inbox.html')


def message_html(request, pk):
    """Return html for displaying a specific message."""
    message = get_object_or_404(PrivateMessage, id=pk)

    message_html = render_to_string('private-message-content.html', {'message': message})
    return HttpResponse(message_html)
