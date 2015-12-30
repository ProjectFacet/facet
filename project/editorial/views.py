from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.utils import timezone
from django.views.generic import TemplateView , UpdateView, DetailView
import datetime

from .forms import (
    UserForm,
    CreateOrganization,
    NetworkForm,
    SeriesForm,
    StoryForm,
    WebFacetForm,
    PrintFacetForm,
    AudioFacetForm,
    VideoFacetForm,
    AddToNetworkForm,
    CommentForm)

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
    # query for new comments since last_login from any discussions the user has participated
    # query for any new content created since last_login
    # query for other user activity since last_login

    # return dashboard view for logged in user.
    return render(request, 'editorial/dashboard.html')

#----------------------------------------------------------------------#
#   Team Views
#----------------------------------------------------------------------#

def team_list(request):
    """ Return teams list.

    Displays team members from the user's own organization.
    Displays team members from any network that the user's organization is part of.
    """

    org_team = User.objects.filter(organization=request.user.organization)
    print "ORG TEAM: ", org_team

    return render(request, 'editorial/team.html', {
        'org_team': org_team
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
    for discussion in discussions:
      recent_comment = Comment.objects.filter(discussion = discussion, date__gte=request.user.last_login)
      recent_comments.extend(recent_comment)

    print recent_comments

    return render(request, 'editorial/discussion.html', {
        'recent_comments': recent_comments,
    })

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

    form = UserForm()
    if request.method == "POST":
        form = UserForm(request.POST or None)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            return redirect('user_detail', pk=user.pk)
    else:
        form=UserForm()
    return render(request, 'editorial/usernew.html', {'form': form})


def user_detail(request, pk):
    """ The public profile of a user.

    Displays the user's organization, title, credit name, email, phone,
    bio, expertise, profile photo, social media links and most recent content.
    """

    user = get_object_or_404(User, pk=pk)
    user_stories = Story.objects.filter(owner=user)

    return render(request, 'editorial/userdetail.html', {
        'user': user,
        'user_stories': user_stories
        })


def user_edit(request, pk):
    """ Edit the user's profile."""

    user = get_object_or_404(User, pk=pk)

    if request.method == "POST":
        form = UserForm(data=request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_detail', pk = user.id)
    else:
        form = UserForm(instance=user)

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

    return render(request, 'editorial/seriesdetail.html', {'series': series})


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

    stories = Story.objects.all()

    return render(request, 'editorial/storylist.html', {'stories': stories})


def story_new(request):
    """ Create story page. """

    series = Series.objects.all()
    print series
    form = StoryForm()
    if request.method == "POST":
        form = StoryForm(request.POST or None)
    if form.is_valid():
        story = form.save(commit=False)
        story.owner = request.user
        story.creation_date = timezone.now()
        discussion = Discussion.objects.create_discussion("STO")
        print discussion
        story.discussion = discussion
        print story.discussion
        story.save()
        return redirect('story_detail', pk=story.pk)
    else:
        form = StoryForm()
    return render(request, 'editorial/storynew.html', {
        'form': form,
        'series': series
        })


def story_detail(request, pk):
    """ The detail page for a story.

    Displays the story's planning notes, discussion, assets, share and collaboration status
    and sensivity status. From here the user can also see any facets, edit them and add new ones.
    """

    story = get_object_or_404(Story, pk=pk)
    team = story.team.all()
    notes = StoryNote.objects.filter(story=story)

# ------------------------------ #
#           webfacet             #
# ------------------------------ #

    try:
        webfacet = get_object_or_404(WebFacet, story=story)
        # retrieve discussion and comments
        webfacetdiscussion = get_object_or_404(Discussion, id=webfacet.discussion.id)
        webcomments = Comment.objects.filter(discussion=webfacetdiscussion).order_by('-date')
        # update an existing webfacet
        if request.method == "POST":
            print "IF POST"
            if 'webform' in request.POST:
                print "IF WEBFORM"
                webform = WebFacetForm(data=request.POST, instance=webfacet)
                if webform.is_valid():
                    print webform.errors
                    webfacet.save()
                    return redirect('story_detail', pk=story.pk)
        else:
            print "Try Else"
            webform = WebFacetForm(instance=webfacet)
    except:
        # display form and save a new webfacet
        if request.method == "POST":
            if 'webform' in request.POST:
                webform = WebFacetForm(request.POST or None)
                if webform.is_valid():
                    print webform.errors
                    webfacet = webform.save(commit=False)
                    webfacet.story = story
                    webfacet.owner = request.user
                    webfacet.original_org = request.user.organization
                    webfacet.creation_date = timezone.now()
                    discussion = Discussion.objects.create_discussion("WF")
                    print discussion
                    webfacet.discussion = discussion
                    print webfacet.discussion
                    webfacet.save()
                    # create history of the webfacet
                    webhistory = webfacet.edit_history.all()
                    return redirect('story_detail', pk=story.pk)
        else:
            print "Except Else"
            webform = WebFacetForm()
            print "WEBFORM ASSIGNED"

# ------------------------------ #
#           printfacet           #
# ------------------------------ #

    try:
        printfacet = get_object_or_404(PrintFacet, story=story)
        # retrieve discussion and comments
        printfacetdiscussion = get_object_or_404(Discussion, id=printfacet.discussion.id)
        printcomments = Comment.objects.filter(discussion=printfacetdiscussion).order_by('-date')
        print "p1"
        # update an existing printfacet
        if request.method == "POST":
            if 'printform' in request.POST:
                print "p2"
                printform = PrintFacetForm(data=request.POST, instance=printfacet)
                if printform.is_valid():
                    print "p3"
                    printfacet.save()
                    print "p4"
                    return redirect('story_detail', pk=story.pk)
        else:
            print "p5"
            printform = PrintFacetForm(instance=printfacet)
    except:
        print "p6"
        # display form and save a new printfacet
        if request.method == "POST":
            print "p7"
            if 'printform' in request.POST:
                print "p8"
                printform = PrintFacetForm(request.POST or None)
                print "p9"
                if printform.is_valid():
                    print "p10"
                    printfacet = printform.save(commit=False)
                    printfacet.story = story
                    printfacet.owner = request.user
                    printfacet.original_org = request.user.organization
                    printfacet.editor = request.user
                    printfacet.creation_date = timezone.now()
                    discussion = Discussion.objects.create_discussion("PF")
                    print discussion
                    printfacet.discussion = discussion
                    print printfacet.discussion
                    printfacet.save()
                    # create history of the printfacet
                    printhistory = printfacet.edit_history.all()
                    return redirect('story_detail', pk=story.pk)
        else:
            print "p11"
            printform = PrintFacetForm()
            print "PRINTFORM ASSIGNED"

# ------------------------------ #
#           audiofacet           #
# ------------------------------ #

    try:
        audiofacet = get_object_or_404(AudioFacet, story=story)
        # retrieve discussion and comments
        audiofacetdiscussion = get_object_or_404(Discussion, id=audiofacet.discussion.id)
        audiocomments = Comment.objects.filter(discussion=audiofacetdiscussion).order_by('-date')
        print "a1"
        # update an existing webfacet
        if request.method == "POST":
            if 'audioform' in request.POST:
                print "a2"
                audioform = AudioFacetForm(data=request.POST, instance=audiofacet)
                if audioform.is_valid():
                    print "a3"
                    audiofacet.save()
                    print "a4"
                    return redirect('story_detail', pk=story.pk)
        else:
            print "a5"
            audioform = AudioFacetForm(instance=audiofacet)
    except:
        print "a6"
        # display form and save a new webfacet
        if request.method == "POST":
            print "a7"
            if 'audioform' in request.POST:
                print "a8"
                audioform = AudioFacetForm(request.POST or None)
                print "a9"
                if audioform.is_valid():
                    print "a10"
                    audiofacet = audioform.save(commit=False)
                    audiofacet.story = story
                    audiofacet.owner = request.user
                    audiofacet.original_org = request.user.organization
                    audiofacet.editor = request.user
                    audiofacet.creation_date = timezone.now()
                    discussion = Discussion.objects.create_discussion("AF")
                    print discussion
                    audiofacet.discussion = discussion
                    print audiofacet.discussion
                    audiofacet.save()
                    # create history of the audiofacet
                    audiohistory = audiofacet.edit_history.all()
                    return redirect('story_detail', pk=story.pk)
        else:
            print "a11"
            audioform = AudioFacetForm()
            print "AUDIOFORM ASSIGNED"

# ------------------------------ #
#           videofacet           #
# ------------------------------ #

    try:
        videofacet = get_object_or_404(VideoFacet, story=story)
        # retrieve discussion and comments
        videofacetdiscussion = get_object_or_404(Discussion, id=videofacet.discussion.id)
        videocomments = Comment.objects.filter(discussion=videofacetdiscussion).order_by('-date')
        print "v1"
        # update an existing printfacet
        if request.method == "POST":
            if 'videoform' in request.POST:
                print "v2"
                videoform = VideoFacetForm(data=request.POST, instance=videofacet)
                if videoform.is_valid():
                    print "v3"
                    videofacet.save()
                    print "v4"
                    return redirect('story_detail', pk=story.pk)
        else:
            print "v5"
            videoform = VideoFacetForm(instance=videofacet)
    except:
        print "v6"
        # display form and save a new printfacet
        if request.method == "POST":
            print "v7"
            if 'videoform' in request.POST:
                print "v8"
                videoform = VideoFacetForm(request.POST or None)
                print "v9"
                if videoform.is_valid():
                    print "v10"
                    videofacet = videoform.save(commit=False)
                    videofacet.story = story
                    videofacet.owner = request.user
                    videofacet.original_org = request.user.organization
                    videofacet.editor = request.user
                    videofacet.creation_date = timezone.now()
                    discussion = Discussion.objects.create_discussion("VF")
                    print discussion
                    videofacet.discussion = discussion
                    print videofacet.discussion
                    videofacet.save()
                    # create history of the videofacet
                    videohistory = videofacet.edit_history.all()
                    return redirect('story_detail', pk=story.pk)
        else:
            print "v11"
            videoform = VideoFacetForm()
            print "VIDEOFORM ASSIGNED"

    return render(request, 'editorial/storydetail.html', {
        'story': story,
        'team': team,
        'webform': webform,
        'webcomments': webcomments,
        'printform': printform,
        'printcomments': printcomments,
        'audioform': audioform,
        'audiocomments': audiocomments,
        'videoform': videoform,
        'videocomments': videocomments,
        # 'webhistory': webhistory,
        # 'printhistory': printhistory,
        # 'audiohistory': audiohistory,
        # 'videohistory': videohistory,
        })


def story_edit(request, pk):
    """ Edit story page. """

    print "SOMETHING"
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
    print network

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

    networkstories = [ ]
    print "networkstories list: ", networkstories

    org_id = request.user.organization_id
    print "org id: ", org_id

    networks = NetworkOrganization.objects.filter(organization_id=org_id)
    print "NETWORKS: ", networks

    for network in networks:
        print "Network: ", network
        shared_stories = Story.objects.filter(share_with = network.id)
        print "SHARED STORIES: ", shared_stories
        for story in shared_stories:
            print "STORY: ", story
            story = Story.objects.filter(id = story.id)
            networkstories.extend(story)

    networkstories = set(networkstories)

    # networkstoriesdict={}
    # for story in networkstories:
    #     webfacet = WebFacet.objects.filter(story_id=story.id)
    #     printfacet = PrintFacet.objects.filter(story_id=story.id)
    #     audiofacet = AudioFacet.objects.filter(story_id=story.id)
    #     videofacet = VideoFacet.objects.filter(story_id=story.id)
    #     networkstoriesdict[story] = {"webfacet": webfacet,
    #                             "printfacet": printfacet,
    #                             "audiofacet": audiofacet,
    #                             "videofacet": videofacet}

    networkstoryfacets = []
    for story in networkstories:
        webfacet = WebFacet.objects.filter(story_id=story.id)
        printfacet = PrintFacet.objects.filter(story_id=story.id)
        audiofacet = AudioFacet.objects.filter(story_id=story.id)
        videofacet = VideoFacet.objects.filter(story_id=story.id)
        networkstoryfacets.extend(webfacet)
        networkstoryfacets.extend(printfacet)
        networkstoryfacets.extend(audiofacet)
        networkstoryfacets.extend(videofacet)
    print "ERRM, Maybe? ", networkstoryfacets

    return render(request, 'editorial/networkstories.html', {
        'networkstories': networkstories,
        'networkstoryfacets': networkstoryfacets,
        })
