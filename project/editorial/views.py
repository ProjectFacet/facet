""" Views for editorial app."""

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
    Asset,
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

    organization = request.user.organization
    print "ORG: ", organization
    test = Organization.get_org_collaborators(organization)
    print "TEST: ", test

    return render(request, 'editorial/test.html', {
        }
    )

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
#   Schedule Views
#----------------------------------------------------------------------#

# TODO: After finishing story dashboard, reuse content here but displayed via calendar/agenda

#----------------------------------------------------------------------#
#   Organization Views
#----------------------------------------------------------------------#

def org_new(request):
    """ A user can create an organization after signing up.
    Ex. A member of a news organization creates an organization account for the newsroom.
    Ex. A freelancer can create their own organization to form a network with any newsroom
    they regularly contribute to.
    """

    orgform = OrganizationForm()
    if request.method == "POST":
        import pdb; pdb.set_trace()
        orgform = OrganizationForm(request.POST, request.FILES)
        if orgform.is_valid():
            organization = orgform.save(commit=False)
            organization.owner = request.user
            organization.creation_date = timezone.now()
            organization.logo = request.FILES['logo']
            discussion = Discussion.objects.create_discussion("ORG")
            organization.discussion = discussion
            organization.save()
            # update user to connect them to the organization
            current_user = get_object_or_404(User, pk=request.user.id)
            current_user.organization = organization
            current_user.save()
            return redirect('org_detail', pk=organization.pk)
    else:
        form = OrganizationForm()
    return render(request, 'editorial/organizationnew.html', {
            'orgform': orgform,
            })


def org_detail(request, pk):
    """ The public profile of an organization.

    Visible to users/organizations in the same networks.
    Displays the organization's name, logo, description, team members, most recent
    shared content, admin email addresses.
    """

    organization = get_object_or_404(Organization, pk=pk)
    organizationnoteform = OrganizationNoteForm()
    organizationnotes = OrganizationNote.objects.filter(organization=organization)[:5]
    users = Organization.get_org_users(organization)
    organizationcomments = Comment.objects.filter(discussion=organization.discussion).order_by('-date')
    organizationcommentform = OrganizationCommentForm()

    return render(request, 'editorial/organizationdetail.html', {
        'organization': organization,
        'organizationnoteform': organizationnoteform,
        'organizationnotes': organizationnotes,
        'organizationcomments': organizationcomments,
        'organizationcommentform': organizationcommentform,
        })


def org_edit(request, pk):
    """ Edit organization page."""

    organization = get_object_or_404(Organization, pk=pk)

    if request.method == "POST":
        orgform = OrganizationForm(request.POST, request.FILES, instance=organization)
        if orgform.is_valid():
            orgform.save()
            return redirect('org_detail', pk=organization.id)
    else:
        orgform = OrganizationForm(instance=organization)

    return render(request, 'editorial/organizationedit.html', {
            'organization': organization,
            'orgform': orgform,
    })


def organization_notes(request, pk):
    """ Display all of the notes for an organization. """

    organization = get_object_or_404(Organization, pk=pk)
    organizationnotes = OrganizationNote.objects.filter(organization_id=organization.id)

    return render(request, 'editorial/organizationnotes.html', {
        'organizationnotes': organizationnotes,
    })


def create_organization_note(request):
    """ Post a note to an organization."""

    organization = request.user.organization
    if request.method == "POST":
        form = OrganizationNoteForm(request.POST or None)
        if form.is_valid():
            organizationnote = form.save(commit=False)
            organizationnote.owner = request.user
            organizationnote.organization = organization
            organizationnote.save()
            return redirect('organization_detail', pk=organization.id)

#----------------------------------------------------------------------#
#   User Views
#----------------------------------------------------------------------#

def user_new(request):
    """ Quick form for making a new user and inviting them to login. """

    if request.method == "POST":
        form = AddUserForm(request.POST or None)
        if form.is_valid():
            user = form.save(commit=False)
            user.organization = request.user.organization
            user.save()
            mail_subject = "New Facet User Details"
            message = "You've been added to Facet. Your login is your email and your password is please."
            print message
            recipient = [user.email]
            sender_email = request.user.email
            send_mail(mail_subject, message, settings.EMAIL_HOST_USER, recipient, fail_silently=False)
            return redirect('team_list')
    else:
        form=AddUserForm()
    return render(request, 'editorial/usernew.html', {'form': form})


def user_detail(request, pk):
    """ The public profile of a user.

    Displays the user's organization, title, credit name, email, phone,
    bio, expertise, profile photo, social media links and most recent content.
    """

    user = get_object_or_404(User, pk=pk)
    user_stories = User.get_user_stories(user)
    user_content = User.get_user_content(user)
    usernotes = UserNote.objects.filter(owner_id=user.id)[:4]
    usernoteform = UserNoteForm()

    content = user.get_user_content()

    return render(request, 'editorial/userdetail.html', {
        'user': user,
        'user_stories': user_stories,
        'user_content': user_content,
        'usernotes': usernotes,
        'usernoteform': usernoteform
        })


def user_edit(request, pk):
    """ Edit the user's profile."""

    user = get_object_or_404(User, pk=pk)

    if request.method == "POST":
        userform = UserProfileForm(request.POST, request.FILES, instance=user)
        if userform.is_valid():
            userform.save()
            return redirect('user_detail', pk = user.id)
    else:
        userform = UserProfileForm(instance=user)

    return render(request, 'editorial/useredit.html', {
            'user': user,
            'userform': userform
    })


def user_notes(request,pk):
    """ Display all of the notes for a user. """

    usernotes = UserNote.objects.filter(owner_id=request.user)
    return render(request, 'editorial/userdetail.html', {
        'usernotes': usernotes,
    })


def create_user_note(request):
    """ Post a note to a user."""

    if request.method == "POST":
        form = UserNoteForm(request.POST or None)
        if form.is_valid():
            usernote = form.save(commit=False)
            usernote.owner = request.user
            usernote.save()
            return redirect('user_notes', pk=request.user.pk)

#----------------------------------------------------------------------#
#   Series Views
#----------------------------------------------------------------------#

def series_list(request):
    """ Displays a filterable table of series.

    Initial display organizes content by series name.
    """

    series = Series.objects.filter(organization=request.user.organization)

    return render(request, 'editorial/serieslist.html', {'series': series})


def series_new(request):
    """ A logged in user can create a series.

    Series serve as a linking mechanism to connect related stories and to share
    assets between them. Series allow users to create planning notes at a series level
    have planning discussions and upload assets. Assets are always associated with a series
    so they are easily accessible to stories and all facets. This means that even single
    stories technically have a series, but in that case the user does not interact with any
    series interface.
    """

    seriesform = SeriesForm()
    if request.method == "POST":
        seriesform = SeriesForm(request.POST or None)
    if seriesform.is_valid():
        series = seriesform.save(commit=False)
        series.owner = request.user
        series.organization = request.user.organization
        series.creation_date = timezone.now()
        discussion = Discussion.objects.create_discussion("SER")
        series.discussion = discussion
        series.save()
        seriesform.save_m2m()
        return redirect('series_detail', pk=series.pk)
    else:
        form = SeriesForm()
    return render(request, 'editorial/seriesnew.html', {'seriesform': seriesform})


def series_detail(request, pk):
    """ The detail page for a series.

    Displays the series' planning notes, discussion, assets, share and collaboration status
    and sensivity status.
    """

    series = get_object_or_404(Series, pk=pk)
    seriesnoteform = SeriesNoteForm()
    seriesnotes = SeriesNote.objects.filter(series=series)[:10]
    seriescommentform = SeriesCommentForm()
    seriescomments = Comment.objects.filter(discussion=series.discussion).order_by('-date')

    return render(request, 'editorial/seriesdetail.html', {
        'series': series,
        'seriesnoteform': seriesnoteform,
        'seriesnotes': seriesnotes,
        'seriescomments': seriescomments,
        'seriescommentform': seriescommentform,
    })


def series_edit(request, pk):
    """ Edit series page."""

    series = get_object_or_404(Series, pk=pk)

    if request.method =="POST":
        seriesform = SeriesForm(data=request.POST, instance=series)
        if seriesform.is_valid():
            seriesform.save()
            return redirect('series_detail', pk=series.id)
    else:
        seriesform = SeriesForm(instance=series)

    return render(request, 'editorial/seriesedit.html', {
        'series': series,
        'seriesform': seriesform,
        })

def series_notes(request, pk):
    """ Display all of the notes for an series. """

    series = get_object_or_404(Series, pk=pk)
    seriesnotes = SeriesNote.objects.filter(series_id=series.id)

    return render(request, 'editorial/seriesnotes.html', {
        'seriesnotes': seriesnotes,
    })


def create_series_note(request):
    """ Post a note to an series."""

    if request.method == "POST":
        form = SeriesNoteForm(request.POST or None)
        if form.is_valid():
            series_id = request.POST.get('series')
            series = get_object_or_404(Series, pk=series_id)
            seriesnote = form.save(commit=False)
            seriesnote.owner = request.user
            seriesnote.series = series
            seriesnote.save()
            return redirect('series_detail', pk=series.id)


#----------------------------------------------------------------------#
#   Story Views
#----------------------------------------------------------------------#

def story_list(request):
    """ Displays a filterable table of stories.

    Initial display organizes content by story>facet>est. run date
    Filterable by story name, facet type, facet name, due for edit, est. run date, credit,
    editor, status.
    """

    stories = Story.objects.filter(organization=request.user.organization).exclude(archived=True)

    return render(request, 'editorial/storylist.html', {
        'stories': stories,
        }
    )


def story_new(request):
    """ Create story page. """

    series = Series.objects.all()
    storyform = StoryForm()
    if request.method == "POST":
        storyform = StoryForm(request.POST or None)
        #import pdb; pdb.set_trace()
        if storyform.is_valid():
            story = storyform.save(commit=False)
            story.owner = request.user
            story.organization = request.user.organization
            discussion = Discussion.objects.create_discussion("STO")
            story.discussion = discussion
            story.save()
            storyform.save_m2m()
            return redirect('story_detail', pk=story.pk)
    else:
        storyform = StoryForm()
    return render(request, 'editorial/storynew.html', {
        'storyform': storyform,
        'series': series
        })


def story_edit(request, pk):
    """ Edit story page. """

    story = get_object_or_404(Story, pk=pk)

    if request.method == "POST":
        storyform = StoryForm(data=request.POST, instance=story)
        if storyform.is_valid():
            storyform.save()
            return redirect('story_detail', pk=story.id)
    else:
        storyform = StoryForm(instance=story)

    return render(request, 'editorial/storyedit.html', {
        'story': story,
        'storyform': storyform,
    })


def story_detail(request, pk):
    """ The detail page for a story.

    Displays the story's planning notes, discussion, assets, share and collaboration status
    and sensivity status. From here the user can also see any facets, edit them and add new ones.
    """

    story = get_object_or_404(Story, pk=pk)
    storynoteform = StoryNoteForm()
    storynotes = StoryNote.objects.filter(story=story)
    storycommentform = StoryCommentForm()
    storydiscussion = get_object_or_404(Discussion, id=story.discussion.id)
    storycomments = Comment.objects.filter(discussion=storydiscussion).order_by('-date')
    notes = StoryNote.objects.filter(story=story)

# ------------------------------ #
#           webfacet             #
# ------------------------------ #

    # create these here for efficiency
    webform=WebFacetForm()
    webcommentform=WebFacetCommentForm()

    try:
        webfacet = get_object_or_404(WebFacet, story=story)
        print "WEBFACET CREDIT", webfacet.credit.all()

        # IF WEBFACET EXISTS DO ALL OF THE FOLLOWING
        # rebind webform to include webfacet instance
        webform = WebFacetForm(instance=webfacet)
        # retrieve discussion and comments
        webfacetdiscussion = get_object_or_404(Discussion, id=webfacet.discussion.id)
        webcomments = Comment.objects.filter(discussion=webfacetdiscussion).order_by('-date')[:3]
        # retrieve history
        webhistory = webfacet.edit_history.all()[:5]
        # update an existing webfacet
        if request.method == "POST":
            print "WF Try If Post"
            if 'webform' in request.POST:
                print "WF Try If Post If webform"
                webform = WebFacetForm(data=request.POST, instance=webfacet)
                #import pdb; pdb.set_trace()
                if webform.is_valid():
                    print "WF Try If Post If Webform Valid"
                    webform.save()
                    print "webfacet updated"
                    return redirect('story_detail', pk=story.pk)
    except:
        print "WF Except"
    # except WebFacet.DoesNotExist:
        # display form and save a new webfacet
        webcomments = []
        webhistory = []
        if request.method == "POST":
            print "WF Except Post"
            if 'webform' in request.POST:
                print "WF Except Post If webform"
                webform = WebFacetForm(request.POST or None)
                if webform.is_valid():
                    # #import pdb; pdb.set_trace()
                    print "WF Except Post If webform Valid"
                    webfacet = webform.save(commit=False)
                    print "webfacet = webform.save(commit=False)"
                    webfacet.story = story
                    webfacet.owner = request.user
                    webfacet.organization = request.user.organization
                    webfacet.creation_date = timezone.now()
                    discussion = Discussion.objects.create_discussion("WF")
                    webfacet.discussion = discussion
                    webfacet.save()
                    webform.save_m2m()
                    print "webfacet created"
                    # create history of the webfacet
                    webhistory = webfacet.edit_history.all()[:5]
                    return redirect('story_detail', pk=story.pk)

# ------------------------------ #
#           printfacet           #
# ------------------------------ #

    # create these here for efficiency
    printform=PrintFacetForm()
    printcommentform=PrintFacetCommentForm()

    try:
        print "PF Try"
        printfacet = get_object_or_404(PrintFacet, story=story)
        # IF PRINTFACET EXISTS DO ALL OF THE FOLLOWING
        printform = PrintFacetForm(instance=printfacet)
        # retrieve discussion and comments
        printfacetdiscussion = get_object_or_404(Discussion, id=printfacet.discussion.id)
        printcomments = Comment.objects.filter(discussion=printfacetdiscussion).order_by('-date')[:3]
        # retrieve history
        printhistory = printfacet.edit_history.all()[:5]
        # update an existing printfacet
        if request.method == "POST":
            print "PF Try If Post"
            if 'printform' in request.POST:
                print "PF Try If Post If printform"
                #import pdb; pdb.set_trace()
                printform = PrintFacetForm(data=request.POST, instance=printfacet)
                if printform.is_valid():
                    print "PF Try If Post If printform Valid"
                    printform.save()
                    print "printfacet updated"
                    return redirect('story_detail', pk=story.pk)
    except:
        print "PF Except"
    # except PrintFacet.DoesNotExist:
        # display form and save a new printfacet
        printcomments = []
        printhistory = []
        if request.method == "POST":
            print "PF Except If Post"
            if 'printform' in request.POST:
                print "PF Except If Post If printform"
                # #import pdb; pdb.set_trace()
                printform = PrintFacetForm(request.POST or None)
                if printform.is_valid():
                    print "PF Except If Post If printform Valid"
                    printfacet = printform.save(commit=False)
                    print "printfacet = printform.save(commit=False)"
                    printfacet.story = story
                    printfacet.owner = request.user
                    printfacet.organization = request.user.organization
                    printfacet.creation_date = timezone.now()
                    discussion = Discussion.objects.create_discussion("WF")
                    printfacet.discussion = discussion
                    printfacet.save()
                    printform.save_m2m()
                    print "printfacet created"
                    # create history of the printfacet
                    printhistory = printfacet.edit_history.all()[:5]
                    return redirect('story_detail', pk=story.pk)

# ------------------------------ #
#           audiofacet           #
# ------------------------------ #

    # create these here for efficiency
    audioform=AudioFacetForm()
    audiocommentform=AudioFacetCommentForm()

    try:
        print "AF Try"
        audiofacet = get_object_or_404(AudioFacet, story=story)
        print "AUDIOFACET CREDIT: ", audiofacet.credit.all()
        # IF WEBFACET EXISTS DO ALL OF THE FOLLOWING
        audioform = AudioFacetForm(instance=audiofacet)
        # retrieve discussion and comments
        audiofacetdiscussion = get_object_or_404(Discussion, id=audiofacet.discussion.id)
        audiocomments = Comment.objects.filter(discussion=audiofacetdiscussion).order_by('-date')[:3]
        # retrieve history
        audiohistory = audiofacet.edit_history.all()[:5]
        # update an existing audiofacet
        if request.method == "POST":
            print "AF Try If Post"
            if 'audioform' in request.POST:
                print "AF Try If Post If Audioform"
                # #import pdb; pdb.set_trace()
                audioform = AudioFacetForm(data=request.POST, instance=audiofacet)
                if audioform.is_valid():
                    print "AF Try If Post If Audioform Valid"
                    audioform.save()
                    print "audiofacet updated"
                    return redirect('story_detail', pk=story.pk)
    except:
        print "AF Except"
    # except AudioFacet.DoesNotExist:
        # display form and save a new audiofacet
        audiocomments = []
        audiohistory = []
        if request.method == "POST":
            print "AF Except If Post"
            if 'audioform' in request.POST:
                print "AF Except If Post If Audioform"
                # #import pdb; pdb.set_trace()
                audioform = AudioFacetForm(request.POST or None)
                if audioform.is_valid():
                    print "AF Except If Post If Audioform Valid"
                    audiofacet = audioform.save(commit=False)
                    print "audiofacet = audioform.save(commit=False)"
                    audiofacet.story = story
                    audiofacet.owner = request.user
                    audiofacet.organization = request.user.organization
                    audiofacet.creation_date = timezone.now()
                    discussion = Discussion.objects.create_discussion("WF")
                    audiofacet.discussion = discussion
                    audiofacet.save()
                    audioform.save_m2m()
                    print "audiofacet created"
                    # create history of the audiofacet
                    audiohistory = audiofacet.edit_history.all()[:5]
                    return redirect('story_detail', pk=story.pk)

# ------------------------------ #
#           videofacet           #
# ------------------------------ #

    # create these here for efficiency
    videoform=VideoFacetForm()
    videocommentform=VideoFacetCommentForm()

    try:
        print "VF Try"
        videofacet = get_object_or_404(VideoFacet, story=story)
        # IF WEBFACET EXISTS DO ALL OF THE FOLLOWING
        videoform = VideoFacetForm(instance=videofacet)
        # retrieve discussion and comments
        videofacetdiscussion = get_object_or_404(Discussion, id=videofacet.discussion.id)
        videocomments = Comment.objects.filter(discussion=videofacetdiscussion).order_by('-date')[:3]
        # retrieve history
        videohistory = videofacet.edit_history.all()[:5]
        # update an existing videofacet
        if request.method == "POST":
            print "VF Try If Post"
            if 'videoform' in request.POST:
                print "VF Try If Post If Videoform"
                # # #import pdb; pdb.set_trace()
                videoform = VideoFacetForm(data=request.POST, instance=videofacet)
                if videoform.is_valid():
                    print "VF Try If Post If Videoform Valid"
                    videoform.save()
                    print "videofacet updated"
                    return redirect('story_detail', pk=story.pk)
    except:
        print "VF Except If Post If Videoform Valid"
    # except VideoFacet.DoesNotExist:
        # display form and save a new videofacet
        videocomments = []
        videohistory = []
        if request.method == "POST":
            print "VF Except If Post"
            if 'videoform' in request.POST:
                print "VF Except If Post If Videoform"
                videoform = VideoFacetForm(request.POST or None)
                if videoform.is_valid():
                    # #import pdb; pdb.set_trace()
                    print "VF Except If Post If Videoform Valid"
                    videofacet = videoform.save(commit=False)
                    print "videofacet = videoform.save(commit=False)"
                    videofacet.story = story
                    videofacet.owner = request.user
                    videofacet.organization = request.user.organization
                    videofacet.creation_date = timezone.now()
                    discussion = Discussion.objects.create_discussion("VF")
                    videofacet.discussion = discussion
                    videofacet.save()
                    videoform.save_m2m()
                    print "videofacet created"
                    # create history of the videofacet
                    videohistory = videofacet.edit_history.all()[:5]
                    return redirect('story_detail', pk=story.pk)

    return render(request, 'editorial/storydetail.html', {
        'story': story,
        'storynoteform': storynoteform,
        'storynotes': storynotes,
        'storycommentform': storycommentform,
        'storycomments': storycomments,
        'webform': webform,
        'webcomments': webcomments,
        'webhistory': webhistory,
        'webcommentform': webcommentform,
        'printform': printform,
        'printcomments': printcomments,
        'printhistory': printhistory,
        'printcommentform': printcommentform,
        'audioform': audioform,
        'audiocomments': audiocomments,
        'audiohistory': audiohistory,
        'audiocommentform': audiocommentform,
        'videoform': videoform,
        'videocomments': videocomments,
        'videohistory': videohistory,
        'videocommentform': videocommentform,
        })


def story_notes(request, pk):
    """ Display all of the notes for an story. """

    story = get_object_or_404(Series, pk=pk)
    storynotes = SeriesNote.objects.filter(story_id=story.id)

    return render(request, 'editorial/storynotes.html', {
        'storynotes': storynotes,
    })


def create_story_note(request):
    """ Post a note to an story."""

    if request.method == "POST":
        form = StoryNoteForm(request.POST or None)
        if form.is_valid():
            story_id = request.POST.get('story')
            story = get_object_or_404(Story, pk=story_id)
            storynote = form.save(commit=False)
            storynote.owner = request.user
            storynote.story = story
            storynote.save()
            return redirect('story_detail', pk=story.id)

#----------------------------------------------------------------------#
#   Comments Views
#----------------------------------------------------------------------#

#TODO: Refactor to reduce repetitiveness/use AJAX for submission

def private_message_new(request):
    """ Private messaging method. """

    if request.method == 'POST':
        privatemessageform=PrivateMessageForm(request.POST or None)
        if privatemessageform.is_valid():
            message_subject = request.POST.get('subject')
            message_text = request.POST.get('text')
            send_to = request.POST.get('recipient')
            recipient = get_object_or_404(User, id=send_to)
            discussion = Discussion.objects.create_discussion('PRI')
            message = PrivateMessage.objects.create_private_message(user=request.user, recipient=recipient, discussion=discussion, subject=message_subject, text=message_text)
            message.save()
    return redirect('/discussion')


def create_privatecomment_reply(request):
    """ Reply to a private message."""
    pass


def create_orgcomment(request):
    """ Regular form posting method."""

    if request.method == 'POST':
        comment_text = request.POST.get('text')
        organization = request.user.organization
        discussion = get_object_or_404(Discussion, id=organization.discussion.id)
        comment = Comment.objects.create_comment(user=request.user, discussion=discussion, text=comment_text)
        comment.save()

        return redirect('org_detail', pk=organization.id)


def create_networkcomment(request):
    """ Regular form posting method."""

    if request.method == 'POST':
        comment_text = request.POST.get('text')
        network_id = request.POST.get('network')
        network = get_object_or_404(Network, id=network_id)
        discussion = get_object_or_404(Discussion, id=network.discussion.id)
        comment = Comment.objects.create_comment(user=request.user, discussion=discussion, text=comment_text)
        comment.save()

        return redirect('network_detail', pk=network.id)


def create_seriescomment(request):
    """ Regular form posting method."""

    if request.method == 'POST':
        comment_text = request.POST.get('text')
        series_id = request.POST.get('series')
        series = get_object_or_404(Series, id=series_id)
        discussion = get_object_or_404(Discussion, id=series.discussion.id)
        comment = Comment.objects.create_comment(user=request.user, discussion=discussion, text=comment_text)
        comment.save()

        return redirect('series_detail', pk=series.id)


def create_storycomment(request):
    """ Regular form posting method."""

    if request.method == 'POST':
        comment_text = request.POST.get('text')
        story_id = request.POST.get('story')
        story = get_object_or_404(Story, id=story_id)
        discussion = get_object_or_404(Discussion, id=story.discussion.id)
        comment = Comment.objects.create_comment(user=request.user, discussion=discussion, text=comment_text)
        comment.save()

        return redirect('story_detail', pk=story.id)

def create_webcomment(request):
    """ Regular form posting method."""

    if request.method == 'POST':
        comment_text = request.POST.get('text')
        story_id = request.POST.get('story')
        story = get_object_or_404(Story, id=story_id)
        webfacet = get_object_or_404(WebFacet, story=story)
        discussion = get_object_or_404(Discussion, id=webfacet.discussion.id)
        comment = Comment.objects.create_comment(user=request.user, discussion=discussion, text=comment_text)
        comment.save()

        return redirect('story_detail', pk=story.id)


def create_printcomment(request):
    """ Regular form posting method."""

    if request.method == 'POST':
        comment_text = request.POST.get('text')
        story_id = request.POST.get('story')
        story = get_object_or_404(Story, id=story_id)
        printfacet = get_object_or_404(PrintFacet, story=story)
        discussion = get_object_or_404(Discussion, id=printfacet.discussion.id)
        comment = Comment.objects.create_comment(user=request.user, discussion=discussion, text=comment_text)
        comment.save()

        return redirect('story_detail', pk=story.id)


def create_audiocomment(request):
    """ Regular form posting method."""

    if request.method == 'POST':
        comment_text = request.POST.get('text')
        story_id = request.POST.get('story')
        story = get_object_or_404(Story, id=story_id)
        audiofacet = get_object_or_404(AudioFacet, story=story)
        discussion = get_object_or_404(Discussion, id=audiofacet.discussion.id)
        comment = Comment.objects.create_comment(user=request.user, discussion=discussion, text=comment_text)
        comment.save()

        return redirect('story_detail', pk=story.id)


def create_videocomment(request):
    """ Regular form posting method."""

    if request.method == 'POST':
        comment_text = request.POST.get('text')
        story_id = request.POST.get('story')
        story = get_object_or_404(Story, id=story_id)
        videofacet = get_object_or_404(VideoFacet, story=story)
        discussion = get_object_or_404(Discussion, id=videofacet.discussion.id)
        comment = Comment.objects.create_comment(user=request.user, discussion=discussion, text=comment_text)
        comment.save()

        return redirect('story_detail', pk=story.id)


# FIXME: Needs further debugging before replacing above sections
# def create_webcomment(request):
#     """ Receive AJAX Post for creating a comment on a webfacet. """
#
#     if request.method == 'POST':
#         comment_text = request.POST.get('text')
#         story = request.POST.get('story')
#         webfacet = get_object_or_404(WebFacet, story=story)
#         discussion = get_object_or_404(Discussion, id=webfacet.discussion.id)
#
#         response_data = {}
#
#         # comment = Comment(text=comment_text, user=request.user, discussion = discussion)
#         comment = Comment.objects.create_comment(user=request.user, discussion=discussion, text=comment_text)
#         comment.save()
#
#         response_data['result'] = 'Create post successful!'
#         response_data['commentpk'] = comment.pk
#         response_data['text'] = comment.text
#         response_data['user'] = comment.user.credit_name
#
#         return HttpResponse(
#             json.dumps(response_data),
#             content_type="application/json"
#         )
#     else:
#         return HttpResponse(
#             json.dumps({"nothing to see": "this isn't happening"}),
#             content_type="application/json"
#         )

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

#----------------------------------------------------------------------#
#   Network Views
#----------------------------------------------------------------------#

def network_new(request):
    """ Create a new network. """

    networkform = NetworkForm()
    owner_org = request.user.organization
    if request.method == "POST":
        networkform = NetworkForm(request.POST or None)
        if networkform.is_valid():
            network = networkform.save(commit=False)
            network.owner_organization = owner_org
            network.creation_date = timezone.now()
            discussion = Discussion.objects.create_discussion("NET")
            network.discussion = discussion
            network.save()
            owner_membership = NetworkOrganization.objects.create(network=network, organization=owner_org)
            return redirect('network_detail', pk=network.pk)
    else:
        networkform = NetworkForm()
    return render(request, 'editorial/networknew.html', {
            'networkform': networkform
        })


def delete_network(request, pk):
    """ Delete a network and dependent records."""

    if request == "POST":
        network = get_object_or_404(Network, pk=pk)
        # if request.user == network.owner_organization
        network.delete()
        return redirect('network_list')


def send_network_invite(request):
    """ Send private message with link to join a network."""

    network = request.POST.get('network')
    print "Post Network", network
    network = get_object_or_404(Network, id=network)
    user_email = request.POST.get('invited_user')
    print "USER EMAIL", user_email
    user = get_object_or_404(User, email=user_email)
    print "USER: ", user
    organization = get_object_or_404(Organization, id=user.organization_id)
    print "ORG: ", organization
    message_subject = "Invitation for {organization} to join {network}".format(organization = organization.name, network=network.name)
    print "MESSAGE SUBJECT", message_subject
    message_text = '<form action="/network/invitation/accept/" method="POST" class="post-form"><input type="hidden" name="network" value="{network}" /><button type="submit" class="btn btn-primary">Accept Invitation</button></form>'.format(network=network.id)
    print "MESSAGE TEXT: ", message_text
    discussion = Discussion.objects.create_discussion('PRI')
    invitation_message = PrivateMessage.objects.create_private_message(user=request.user, recipient=user, discussion=discussion, subject=message_subject, text=message_text)
    print "Successfully joined Network!"
    return redirect('network_detail', pk=network.pk)


@csrf_exempt
def confirm_network_invite(request):
    """ Receive confirmed networkwork invitation and create new NetworkOrganization
    connection."""

    network_id = request.POST.get('network')
    network = get_object_or_404(Network, id=network_id)
    organization = request.user.organization
    new_connection = NetworkOrganization.objects.create(network=network, organization=organization)
    print "Successfully joined Network!"
    return redirect('network_detail', pk=network.pk)


def org_to_network(request, pk):
    """ Form to add an organization to a network. """

    network = get_object_or_404(Network, pk=pk)

    if request.method == "POST":
        form = AddToNetworkForm(request.POST or None)
        if form.is_valid():
            connection = form.save(commit=False)
            return redirect('network_detail', pk=network.pk)
    else:
        form = AddToNetworkForm()
    return render(request, 'editorial/networkdetail.html', {'form': form})


def network_detail(request, pk):
    """ Public profile of a network. """

    network = get_object_or_404(Network, pk=pk)
    network_members = Network.get_network_organizations(network)
    networknoteform = NetworkNoteForm()
    networkinvitationform = InviteToNetworkForm()
    networknotes = NetworkNote.objects.filter(network=network)
    networkcomments = Comment.objects.filter(discussion=network.discussion).order_by('-date')
    networkcommentform = NetworkCommentForm()

    return render(request, 'editorial/networkdetail.html', {
        'network': network,
        'network_members': network_members,
        'networkinvitationform': networkinvitationform,
        'networknoteform': networknoteform,
        'networknotes': networknotes,
        'networkcomments': networkcomments,
        'networkcommentform': networkcommentform,
        })


def network_edit(request, pk):
    """ Edit network page. """

    network = get_object_or_404(Network, pk=pk)

    if request.method == "POST":
        networkform = NetworkForm(data=request.POST, instance=network)
        if networkform.is_valid():
            networkform.save()
            return redirect('network_detail', pk=network.id)
    else:
        networkform = NetworkForm(instance=network)

    return render(request, 'editorial/networkedit.html', {
            'network': network,
            'networkform': networkform,
        })


def network_list(request):
    """ Table of networks your org is member of."""

    organization = request.user.organization
    print "org id: ", organization
    network_list = Organization.get_org_networks(organization)
    print "network_list: ", network_list

    return render(request, 'editorial/networklist.html', {'network_list': network_list})


def network_stories(request):
    """ Displays a filterable table of stories marked as shared/ready to share by any
    organizations that a user's organization is a part of.

    Initial display organizes content by story>facet>est. run date
    Filterable by story name, facet type, facet name, due for edit, est. run date, credit,
    editor, status.

    Stories marked as share appear but are greyed out/inaccessible until the owner marks
    them as Ready to Share. (This is so partners know it will exist and can plan to incorporate
    it once it becomes available.)
    """

    org_id = request.user.organization_id
    organization = get_object_or_404(Organization, id=org_id)

    networks = Organization.get_org_networks(organization)

    shared_networkstories = []
    for network in networks:
        stories = Network.get_network_shared_stories(network)
        shared_networkstories.extend(stories)

    networkstories = set(shared_networkstories)

    return render(request, 'editorial/networkstories.html', {
        'networkstories': networkstories,
        })


def copy_network_story(request, pk):
    """ Copy a story and related facets. """

    original_story = get_object_or_404(Story, pk=pk)
    original_org = original_story.organization

    original_webfacet = original_story.webfacetstory.all()
    original_printfacet = original_story.printfacetstory.all()
    original_audiofacet = original_story.audiofacetstory.all()
    original_videofacet = original_story.videofacetstory.all()

    user = request.user
    organization = request.user.organization
    partner = request.user.organization

    if request.method == "POST":

        #Create a copy of the story and a storycopydetail record
        copied_story = Story.copy_story(original_story)
        copied_story.owner = user
        copied_story.organization = organization
        copied_story.save()
        partner_story = copied_story
        story_copy_record = StoryCopyDetail.objects.create_story_copy_record(
            original_org=original_org,
            partner=partner,
            original_story=original_story,
            partner_story=partner_story
            )
        print "Story Copied"

        # Create copy of facets if they exist
        if original_webfacet:
            print original_webfacet[0]
            copied_webfacet = WebFacet.copy_webfacet(original_webfacet[0])
            copied_webfacet.story = partner_story
            copied_webfacet.owner = user
            copied_webfacet.organization = organization
            copied_webfacet.save()
            partner_webfacet = copied_webfacet
            webfacet_copy_record = WebFacetCopyDetail.objects.create_webfacet_copy_record(
                original_org=original_org,
                partner=partner,
                original_webfacet=original_webfacet[0],
                partner_webfacet=partner_webfacet
            )
            print "Webfacet Copied"

        if original_printfacet:
            print original_printfacet[0]
            copied_printfacet = PrintFacet.copy_printfacet(original_printfacet[0])
            copied_printfacet.story = partner_story
            copied_printfacet.owner = user
            copied_printfacet.organization = organization
            copied_printfacet.save()
            partner_printfacet = copied_printfacet
            printfacet_copy_record = PrintFacetCopyDetail.objects.create_printfacet_copy_record(
                original_org=original_org,
                partner=partner,
                original_printfacet=original_printfacet,
                partner_printfacet=partner_printfacet
            )
            print "Printfacet Copied"

        if original_audiofacet:
            print original_audiofacet[0]
            copied_audiofacet = AudioFacet.copy_audiofacet(original_audiofacet[0])
            copied_audiofacet.story = partner_story
            copied_audiofacet.owner = user
            copied_audiofacet.organization = organization
            copied_audiofacet.save()
            partner_audiofacet = copied_audiofacet
            audiofacet_copy_record = AudioFacetCopyDetail.objects.create_audiofacet_copy_record(
                original_org=original_org,
                partner=partner,
                original_audiofacet=original_audiofacet,
                partner_audiofacet=partner_audiofacet
            )
            print "Audiofacet Copied"

        if original_videofacet:
            print original_videofacet[0]
            copied_videofacet = VideoFacet.copy_videofacet(original_videofacet[0])
            copied_videofacet.story = partner_story
            copied_videofacet.owner = user
            copied_videofacet.organization = organization
            copied_videofacet.save()
            partner_videofacet = copied_videofacet
            videofacet_copy_record = VideoFacetCopyDetail.objects.create_videofacet_copy_record(
                original_org=original_org,
                partner=partner,
                original_videofacet=original_videofacet,
                partner_videofacet=partner_videofacet
            )
            print "Videofacet Copied"

    return redirect('network_stories')


def network_notes(request, pk):
    """ Display all of the notes for a network. """

    network = get_object_or_404(Network, pk=pk)
    networknotes = NetworkNote.objects.filter(network_id=network.id)
    return render(request, 'editorial/networknotes.html', {
        'networknotes': networknotes,
    })


def create_network_note(request):
    """ Post a note to a network."""

    if request.method == "POST":
        form = NetworkNoteForm(request.POST or None)
        if form.is_valid():
            nw_id = request.POST.get('network')
            network = get_object_or_404(Network, pk=nw_id)
            networknote = form.save(commit=False)
            networknote.owner = request.user
            networknote.network = network
            networknote.save()
            return redirect('network_detail', pk=network.pk)
