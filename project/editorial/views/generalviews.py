""" General views for editorial app. """

from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponse
from django.utils import timezone
from django.views.generic import TemplateView , UpdateView, DetailView
from django.views.decorators.csrf import csrf_exempt
import datetime, time
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

    stories = Story.objects.filter(organization=request.user.organization).exclude(archived=True)

    data = {}
    data['success'] = 1
    data['result'] = []

    for story in stories:
        # Web Facet Schedules
        for webfacet in story.webfacetstory.all():
            if webfacet.due_edit:
                edit_event_dict = {}
                edit_event_dict['id'] = webfacet.id
                edit_event_dict['title'] = webfacet.title
                edit_event_dict['url'] = webfacet.get_absolute_url
                edit_event_dict['class'] = 'event_edit'
                edit_event_dict['start'] = time.mktime(webfacet.due_edit.timetuple()) * 1000
                edit_event_dict['end'] = (time.mktime(webfacet.due_edit.timetuple()) * 1000) + 60
                data['result'].append(edit_event_dict)
            if webfacet.run_date:
                run_event_dict = {}
                run_event_dict['id'] = webfacet.id
                run_event_dict['title'] = webfacet.title
                run_event_dict['url'] = webfacet.get_absolute_url
                run_event_dict['class'] = 'event_run'
                run_event_dict['start'] = time.mktime(webfacet.run_date.timetuple()) * 1000
                run_event_dict['end'] = (time.mktime(webfacet.run_date.timetuple()) * 1000) + 60
                data['result'].append(run_event_dict)
        # Print Facet Schedules
        for printfacet in story.printfacetstory.all():
            if printfacet.due_edit:
                edit_event_dict = {}
                edit_event_dict['id'] = printfacet.id
                edit_event_dict['title'] = printfacet.title
                edit_event_dict['url'] = printfacet.get_absolute_url
                edit_event_dict['class'] = 'event_edit'
                edit_event_dict['start'] = time.mktime(printfacet.due_edit.timetuple()) * 1000
                edit_event_dict['end'] = (time.mktime(printfacet.due_edit.timetuple()) * 1000) + 60
                data['result'].append(edit_event_dict)
            if printfacet.run_date:
                run_event_dict = {}
                run_event_dict['id'] = printfacet.id
                run_event_dict['title'] = printfacet.title
                run_event_dict['url'] = printfacet.get_absolute_url
                run_event_dict['class'] = 'event_run'
                run_event_dict['start'] = time.mktime(printfacet.run_date.timetuple()) * 1000
                run_event_dict['end'] = (time.mktime(printfacet.run_date.timetuple()) * 1000) + 60
                data['result'].append(run_event_dict)
        # Audio Facet Schedules
        for audiofacet in story.audiofacetstory.all():
            if audiofacet.due_edit:
                edit_event_dict = {}
                edit_event_dict['id'] = audiofacet.id
                edit_event_dict['title'] = audiofacet.title
                edit_event_dict['url'] = audiofacet.get_absolute_url
                edit_event_dict['class'] = 'event_edit'
                edit_event_dict['start'] = time.mktime(audiofacet.due_edit.timetuple()) * 1000
                edit_event_dict['end'] = (time.mktime(audiofacet.due_edit.timetuple()) * 1000) + 60
                data['result'].append(edit_event_dict)
            if audiofacet.run_date:
                run_event_dict = {}
                run_event_dict['id'] = audiofacet.id
                run_event_dict['title'] = audiofacet.title
                run_event_dict['url'] = audiofacet.get_absolute_url
                run_event_dict['class'] = 'event_run'
                run_event_dict['start'] = time.mktime(audiofacet.run_date.timetuple()) * 1000
                run_event_dict['end'] = (time.mktime(audiofacet.run_date.timetuple()) * 1000) + 60
                data['result'].append(run_event_dict)
        # Video Facet Schedules
        for videofacet in story.videofacetstory.all():
            if videofacet.due_edit:
                edit_event_dict = {}
                edit_event_dict['id'] = videofacet.id
                edit_event_dict['title'] = videofacet.title
                edit_event_dict['url'] = videofacet.get_absolute_url
                edit_event_dict['class'] = 'event_edit'
                edit_event_dict['start'] = time.mktime(videofacet.due_edit.timetuple()) * 1000
                edit_event_dict['end'] = (time.mktime(videofacet.due_edit.timetuple()) * 1000) + 60
                data['result'].append(edit_event_dict)
            if videofacet.run_date:
                run_event_dict = {}
                run_event_dict['id'] = videofacet.id
                run_event_dict['title'] = videofacet.title
                run_event_dict['url'] = videofacet.get_absolute_url
                run_event_dict['class'] = 'event_run'
                run_event_dict['start'] = time.mktime(videofacet.run_date.timetuple()) * 1000
                run_event_dict['end'] = (time.mktime(videofacet.run_date.timetuple()) * 1000) + 60
                data['result'].append(run_event_dict)

    print "DATA: ", data


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
    # query for new comments since last_login from any discussions the user has participated in
    recent_comments = User.recent_comments(request.user)
    # if no new comments, display 10 most recent older comments
    older_comments = User.inbox_comments(request.user)[:10]
    # query for any new content created since last_login
    new_stories = Story.objects.filter(creation_date__gte=request.user.last_login)[:8]
    # if no new stories, display 10 most recent stories
    old_stories = Story.objects.filter(organization = request.user.organization)[:10]

    # TODO: query for other user activity since last_login

    return render(request, 'editorial/dashboard.html', {
        'recent_comments': recent_comments,
        'older_comments': older_comments,
        'new_stories': new_stories,
        'old_stories': old_stories,
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

    series_collaorations = Series.objects.filter(collaborate=True)
    story_collaborations = Story.objects.filter(collaborate=True)

    return render(request, 'editorial/collaborations.html', {
        'series_collaorations': series_collaorations,
        'story_collaborations': story_collaborations,
    })
