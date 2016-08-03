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

    return render(request, 'editorial/test.html')


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
    # establish timeliness of content
    today = timezone.now().date()
    tomorrow = today + timedelta(1)
    today_start = datetime.combine(today, time())
    today_end = datetime.combine(tomorrow, time())

    # query for new comments since last_login from any discussions the user has participated in
    recent_comments = User.recent_comments(request.user)
    # if no new comments, display 10 most recent older comments
    older_comments = User.inbox_comments(request.user)[:10]
    all_comments = Comment.objects.all()[:10]
    # query for any new content created since last_login
    new_stories = Story.objects.filter(creation_date__gte=request.user.last_login)[:8]
    # if no new stories, display 10 most recent stories
    old_stories = Story.objects.filter(organization = request.user.organization)[:10]
    # facets where run_date=today
    running_today = []
    webfacet_run_today = WebFacet.objects.filter(run_date__range=(today_start, today_end))
    printfacet_run_today = PrintFacet.objects.filter(run_date__range=(today_start, today_end))
    audiofacet_run_today = AudioFacet.objects.filter(run_date__range=(today_start, today_end))
    videofacet_run_today = VideoFacet.objects.filter(run_date__range=(today_start, today_end))
    running_today.extend(webfacet_run_today)
    running_today.extend(printfacet_run_today)
    running_today.extend(audiofacet_run_today)
    running_today.extend(videofacet_run_today)
    # facets where due_edit=today
    edit_today = []
    webfacet_edit_today = WebFacet.objects.filter(due_edit__range=(today_start, today_end))
    printfacet_edit_today = PrintFacet.objects.filter(due_edit__range=(today_start, today_end))
    audiofacet_edit_today = AudioFacet.objects.filter(due_edit__range=(today_start, today_end))
    videofacet_edit_today = VideoFacet.objects.filter(due_edit__range=(today_start, today_end))
    edit_today.extend(webfacet_edit_today)
    edit_today.extend(printfacet_edit_today)
    edit_today.extend(audiofacet_edit_today)
    edit_today.extend(videofacet_edit_today)

    # TODO: query for other user activity since last_login

    return render(request, 'editorial/dashboard.html', {
        'recent_comments': recent_comments,
        'older_comments': older_comments,
        'all_comments': all_comments,
        'new_stories': new_stories,
        'old_stories': old_stories,
        'running_today': running_today,
        'edit_today': edit_today,
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

    # form for adding a new user to the team
    adduserform = AddUserForm()
    # only visible for admin users

    return render(request, 'editorial/team.html', {
        'organization': organization,
        'networks': networks,
        'adduserform': adduserform,
        })

#----------------------------------------------------------------------#
#   Discussion Views
#----------------------------------------------------------------------#

def discussion(request):
    """ Return discussion inbox.

    Displays comments from SeriesPlan Discussions involving user.
    Displays comments from StoryPlan Discussions involving user.
    Displays comments from any Facet Editing Discussion involving user.
    Displays comments from any PrivateDiscussion involving user.
    """

    comments = User.inbox_comments(request.user)

    private_messages_received = User.private_messages_received(request.user)
    private_messages_sent = User.private_messages_sent(request.user)

    return render(request, 'editorial/discussion.html', {
        'comments': comments,
        'private_messages_received': private_messages_received,
        'private_messages_sent': private_messages_sent,
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
