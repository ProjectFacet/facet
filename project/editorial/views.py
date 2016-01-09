from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.utils import timezone
from django.views.generic import TemplateView , UpdateView, DetailView
import datetime
import json

from .forms import (
    AddUserForm,
    UserProfileForm,
    CreateOrganization,
    NetworkForm,
    SeriesForm,
    StoryForm,
    WebFacetForm,
    PrintFacetForm,
    AudioFacetForm,
    VideoFacetForm,
    AddToNetworkForm,
    PrivateMessageForm,
    SeriesCommentForm,
    StoryCommentForm,
    WebFacetCommentForm,
    PrintFacetCommentForm,
    AudioFacetCommentForm,
    VideoFacetCommentForm)

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
    Discussion)

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
    comments = Comment.objects.filter(user_id = request.user.id)
    discussions = []
    for comment in comments:
      discussion = Discussion.objects.filter(id = comment.discussion_id)
      discussions.extend(discussion)
    recent_comments = []
    for discussion in set(discussions):
    # --------------------------------------------------------------------------------#
    # actual query needed but not helpful for development
    # recent_comment = Comment.objects.filter(discussion = discussion, date__gte=request.user.last_login)
    # --------------------------------------------------------------------------------#
      recent_comment = Comment.objects.filter(discussion = discussion).order_by('-date')
      recent_comments.extend(recent_comment)

    # query for any new content created since last_login

    # --------------------------------------------------------------------------------#
    # actual query needed but not helpful for development
    # stories = Story.objects.filter(creation_date__gte=request.user.last_login)
    # --------------------------------------------------------------------------------#
    stories = Story.objects.filter(organization = request.user.organization)
    print "DASHBOARD STORIES: ", stories
    # TODO: query for other user activity since last_login

    return render(request, 'editorial/dashboard.html', {
        'recent_comments': recent_comments,
        'stories': stories,
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
    comments = Comment.objects.filter(user_id = request.user.id)
    discussions = []
    for comment in comments:
      discussion = Discussion.objects.filter(id = comment.discussion_id)
      discussions.extend(discussion)
    recent_comments = []
    for discussion in set(discussions):
      recent_comment = Comment.objects.filter(discussion = discussion).order_by('-date')
      recent_comments.extend(recent_comment)

    return render(request, 'editorial/discussion.html', {
        'recent_comments': recent_comments,
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

    form = CreateOrganization()
    if request.method == "POST":
        form = CreateOrganization(request.POST or None)
        if form.is_valid():
            organization = form.save(commit=False)
            organization.owner = request.user
            organization.creation_date = timezone.now()
            organization.save()
            # update user to connect them to the organization
            current_user = get_object_or_404(User, pk=request.user.id)
            current_user.organization = organization
            current_user.save()
            return redirect('org_detail', pk=organization.pk)
    else:
        form = CreateOrganization()
    return render(request, 'editorial/organizationnew.html', {'form': form})


def org_detail(request, pk):
    """ The public profile of an organization.

    Visible to users/organizations in the same networks.
    Displays the organization's name, logo, description, team members, most recent
    shared content, admin email addresses.
    """

    organization = get_object_or_404(Organization, pk=pk)

    users = Organization.get_org_users(organization)

    return render(request, 'editorial/organizationdetail.html', {'organization': organization})


def org_edit(request, pk):
    """ Edit organization page."""

    organization = get_object_or_404(Organization, pk=pk)

    if request.method == "POST":
        form = CreateOrganization(data=request.POST, instance=organization)
        if form.is_valid():
            form.save()
            return redirect('org_detail', pk=organization.id)
    else:
        form = CreateOrganization(instance=organization)

    return render(request, 'editorial/organizationedit.html', {
            'organization': organization,
            'form': form,
    })

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
    user_stories = Story.objects.filter(owner=user)

    content = user.get_user_content()

    return render(request, 'editorial/userdetail.html', {
        'user': user,
        'user_stories': user_stories
        })


def user_edit(request, pk):
    """ Edit the user's profile."""

    user = get_object_or_404(User, pk=pk)

    if request.method == "POST":
        form = UserProfileForm(data=request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_detail', pk = user.id)
    else:
        form = UserProfileForm(instance=user)

    return render(request, 'editorial/useredit.html', {
            'user': user,
            'form': form
    })

#----------------------------------------------------------------------#
#   Series Views
#----------------------------------------------------------------------#

def series_list(request):
    """ Displays a filterable table of series.

    Initial display organizes content by series name.
    """

    series = Series.objects.all()

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

    form = SeriesForm()
    if request.method == "POST":
        form = SeriesForm(request.POST or None)
    if form.is_valid():
        series = form.save(commit=False)
        series.owner = request.user
        series.creation_date = timezone.now()
        discussion = Discussion.objects.create_discussion("SER")
        print discussion
        series.discussion = discussion
        print series.discussion
        series.save()
        return redirect('series_detail', pk=series.pk)
    else:
        form = SeriesForm()
    return render(request, 'editorial/seriesnew.html', {'form': form})


def series_detail(request, pk):
    """ The detail page for a series.

    Displays the series' planning notes, discussion, assets, share and collaboration status
    and sensivity status.
    """

    series = get_object_or_404(Series, pk=pk)
    seriescommentform = SeriesCommentForm()
    seriesdiscussion = get_object_or_404(Discussion, id=series.discussion.id)
    seriescomments = Comment.objects.filter(discussion=seriesdiscussion).order_by('-date')

    return render(request, 'editorial/seriesdetail.html', {
        'series': series,
        'seriescomments': seriescomments,
        'seriescommentform': seriescommentform,
    })


def series_edit(request, pk):
    """ Edit series page."""

    series = get_object_or_404(Series, pk=pk)

    if request.method =="POST":
        form = SeriesForm(data=request.POST, instance=series)
        if form.is_valid():
            form.save()
            return redirect('series_detail', pk=series.id)
    else:
        form = SeriesForm(instance=series)

    return render(request, 'editorial/seriesedit.html', {
        'series': series,
        'form': form,
        })

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
        print "WF Try"
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


#----------------------------------------------------------------------#
#   Comments Views
#----------------------------------------------------------------------#

#TODO: Refactor to reduce repetitiveness/use AJAX for submission

def private_message_new(request):
    """ Private messaging method. """

    print "IN PRIVATE MESSAGE VIEW"
    if request.method == 'POST':
        privatemessageform=PrivateMessageForm(request.POST or None)
        print "IN PM POST"
        if privatemessageform.is_valid():
            message_text = request.POST.get('text')
            send_to = request.POST.get('recipient')
            recipient = get_object_or_404(User, id=send_to)
            discussion = Discussion.objects.create_discussion('PRI')
            message = PrivateMessage.objects.create_private_message(user=request.user, recipient=recipient, discussion=discussion, text=message_text)
            print "MESSAGE: ", message
            message.save()
    return redirect('/discussion')


def create_privatecomment_reply(request):
    """ Reply to a private message."""
    pass


def create_seriescomment(request):
    """ Regular form posting method."""

    if request.method == 'POST':
        comment_text = request.POST.get('text')
        series_id = request.POST.get('series')
        series = get_object_or_404(Story, id=series_id)
        discussion = get_object_or_404(Discussion, id=series.discussion.id)
        comment = Comment.objects.create_comment(user=request.user, discussion=discussion, text=comment_text)
        comment.save()

        return redirect('story_detail', pk=story.id)


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

    form = NetworkForm()
    owner_org = get_object_or_404(Organization, pk=request.user.organization_id)
    if request.method == "POST":
        form = NetworkForm(request.POST or None)
        if form.is_valid():
            network = form.save(commit=False)
            network.owner_organization = owner_org
            network.creation_date = timezone.now()
            network.save()
            # update organization to make it a member of the network
            return redirect('network_detail', pk=network.pk)
    else:
        form = NetworkForm()
    return render(request, 'editorial/networknew.html', {'form': form})


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

    return render(request, 'editorial/networkdetail.html', {'network': network})


def network_edit(request, pk):
    """ Edit network page. """

    network = get_object_or_404(Network, pk=pk)

    if request.method == "POST":
        form = NetworkForm(data=request.POST, instance=network)
        if form.is_valid():
            form.save()
            return redirect('network_detail', pk=network.id)
    else:
        form = NetworkForm(instance=network)

    return render(request, 'editorial/networkedit.html', {
            'network': network,
            'form': form,
        })


def network_list(request):
    """ Table of networks your org is member of."""

    org_id = request.user.organization_id
    print "org id: ", org_id
    network_list = NetworkOrganization.objects.filter(organization_id=org_id)
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

    networks = NetworkOrganization.objects.filter(organization_id=org_id)

    networkstories = []
    for network in networks:
        shared_stories = Story.objects.filter(share_with = network.id).exclude(archived=True)
        for story in shared_stories:
            story = Story.objects.get(id = story.id)
            if story not in networkstories:
                networkstories.append(story)

    return render(request, 'editorial/networkstories.html', {
        'networkstories': networkstories,
        })


def copy_network_story(request, pk):
    """ Copy a story and related facets.

    Currently automatically copies story and all facets.
    """

    #TODO: Query for a story, collect that story and it's facets
    # make a copy of that story and facets for the copying organizations
    # create a record in copy_details_ Tables

    # story fields to keep: organization, name, story_description, embargo, embargo_datetime,
    # creation_date, team,

    # facet fields to keep: story, organization, editor, contributors, credit, title, excerpt, wf_description
    # wf_content, length, keywords, creation_date, share_note, assets, captions

    story = get_object_or_404(Story, pk=pk)

    return redirect('network_stories')
