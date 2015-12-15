from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.utils import timezone
import datetime

from .forms import StoryForm, EditUserProfile, SeriesForm, CreateOrganization, NetworkForm

from models import (
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
    Asset,
    Comment,
    Discussion)

#----------------------------------------------------------------------#
#   Initial View
#----------------------------------------------------------------------#

def index(request):
    # return static homepage for now
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

    org_team = User.objects.filter(organization_id_id=request.user.organization_id_id)
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

    return render(request, 'editorial/discussion.html')

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
            # left off trying to automatically connect user to organization
            request.user.organization = organization
            print request.user.organization.id
            request.user.save()
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

def user_detail(request, pk):
    """ The public profile of a user.

    Displays the user's organization, title, credit name, email, phone,
    bio, expertise, profile photo, social media links and most recent content.
    """

    user = get_object_or_404(User, pk=pk)

    return render(request, 'editorial/userdetail.html', {'user': user})


def user_edit(request, pk):
    """ Edit the user's profile."""

    user = get_object_or_404(User, pk=pk)

    if request.method == "POST":
        form = EditUserProfile(data=request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_detail', pk = user.id)
    else:
        form = EditUserProfile(instance=user)

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

    form = StoryForm()
    if request.method == "POST":
        form = StoryForm(request.POST or None)
    if form.is_valid():
        story = form.save(commit=False)
        story.owner = request.user
        story.creation_date = timezone.now()
        story.save()
        return redirect('story_detail', pk=story.pk)
    else:
        form = StoryForm()
    return render(request, 'editorial/storynew.html', {'form': form})


def story_detail(request, pk):
    """ The detail page for a story.

    Displays the story's planning notes, discussion, assets, share and collaboration status
    and sensivity status. From here the user can also see any facets, edit them and add new ones.
    """

    story = get_object_or_404(Story, pk=pk)

    return render(request, 'editorial/storydetail.html', {'story': story})


def story_edit(request, pk):
    """ Edit story page. """

    story = get_object_or_404(Story, pk=pk)
    if request.method == "POST":
        form = StoryForm(data=request.POST, instance=story)
        if form.is_valid():
            form.save()
            return redirect('story_detail', pk=story.id)
    else:
        form = StoryForm(instance=story)

    return render(request, 'editorial/storyedit.html', {
        'story': story,
        'form': form,
    })


#----------------------------------------------------------------------#
#   Facet Views
#----------------------------------------------------------------------#


#----------------------------------------------------------------------#
#   Network Views
#----------------------------------------------------------------------#

def network_new(request):
    """ Create a new network. """

    form = NetworkForm()
    if request.method == "POST":
        form.NetworkForm(request.POST or None)
        if form.is_valid():
            network = form.save(commit=False)
            network.owner_organization = request.user.organization_id_id
            network.creation_date = timezone.now()
            organization.save()
            return redirect('network_detail', pk=network.pk)
    else:
        form = NetworkForm()
    return render(request, 'editorial/networknew.html', {'form': form})


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


def network_member(request):
    """ Table of networks your org is member of."""

    network_membership = Network.objects.filter(member=request.user.organization_id_id)

    return render(request, 'editorial/networklist.html', {'network_membership': network_membership})


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

    network_stories = Story.objects.filter(share=True, share_with=request.user.organization_id_id)
    print "NETWORK STORIES: ", network_stories

    return render(request, 'editorial/networkstories.html', {
        'network_stories': network_stories,
        })
