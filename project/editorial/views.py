from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import StoryForm, EditUserProfile, SeriesForm, CreateOrganization
from django.utils import timezone
# from django.utils.timezone import now
import datetime
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
    SeriesPlan,
    StoryPlan,
    Asset,
    Comment,
    Discussion)

#----------------------------------------------------------------------#
#   Initial Views
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
    # queries for new comments since last_login from any discussions the user has participated
    # queries for any new content created since last_login
    # queries for other user activity since last_login

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

    return render(request, 'editorial/team.html')

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

def organization_new(request):
    """ A user can create an organization after signing up.

    Ex. A member of a news organization creates an organization account for the newsroom.
    Ex. A freelancer can create their own organization to form a network with any newsroom
    they regularly contribute to.
    """

    form = CreateOrganization()
    if request.method == "POST":
        # form = CreateOrganization(request.POST or None)
        if form.is_valid():
            organization = form.save(commit=False)
            organization.owner = request.user
            organization.save()
            return redirect('index')
    else:
        form = CreateOrganization()
    return render(request, 'editorial/createorg.html', {'form': form})


def org_detail(request):
    """ The public profile of an organization.

    Visible to users/organizations in the same networks.
    Displays the organization's name, logo, description, team members, most recent
    shared content, admin email addresses.
    """

    return render(request, 'editorial/org_detail.html')


def org_edit(request):
    """ Edit organization page."""

    return HttpResponse("Could edit an organization here.")

#----------------------------------------------------------------------#
#   User Views
#----------------------------------------------------------------------#

def user_detail(request):
    """ The public profile of a user.

    Displays the user's organization, title, credit name, email, phone,
    bio, expertise, profile photo, social media links and most recent content.
    """

    return render(request, 'editorial/user.html')


def user_edit(request, pk):
    # return user profile page with profile forms
    user = get_object_or_404(POST, pk=pk)

    if request.method == "POST":
        form = EditUserProfile(request.POST, instance=user)
    if form.is_valid():
        user = form.save(commit=False)
        user.save()
        return redirect('user_detail')
    else:
        form = EditUserProfile(instance=user)
    return render(request, 'editorial/user_profile_settings.html', {'form': form})

#----------------------------------------------------------------------#
#   Series Views
#----------------------------------------------------------------------#

def series_list(request):
    """ Displays a filterable table of series.

    Initial display organizes content by series name.
    """
    pass


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
        print "SERIES OWNER: ", series.owner
        series.creation_date = timezone.now()
        series.save()
        return redirect('series_detail')
    else:
        form = SeriesForm()
    return render(request, 'editorial/series.html', {'form': form})


def series_detail(request):
    """ The detail page for a series.

    Displays the series' planning notes, discussion, assets, share and collaboration status
    and sensivity status.
    """

    return HttpResponse("I think it worked for a series.")


def series_edit(request, pk):
    """ Edit series page."""

    return HttpResponse("Could edit a series here.")

#----------------------------------------------------------------------#
#   Story Views
#----------------------------------------------------------------------#

def story_list(request):
    """ Displays a filterable table of stories.

    Initial display organizes content by story>facet>est. run date
    Filterable by story name, facet type, facet name, due for edit, est. run date, credit,
    editor, status.
    """

    stories = Story.objects.filter(creation_date=timezone.now()).order_by('creation_date')

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
        return redirect('story_detail', pk=post.pk)
    else:
        form = StoryForm()
    return render(request, 'editorial/story.html', {'form': form})


def story_detail(request):
    """ The detail page for a story.

    Displays the story's planning notes, discussion, assets, share and collaboration status
    and sensivity status. From here the user can also see any facets, edit them and add new ones.
    """

    return HttpResponse("I think it worked for a story.")


def story_edit(request, pk):
    """ Edit story page. """

    return HttpResponse("Could edit a story here.")



#----------------------------------------------------------------------#
#   Facet Views
#----------------------------------------------------------------------#






#----------------------------------------------------------------------#
#   Network Views
#----------------------------------------------------------------------#

# def network_new(request):
#     """ Create a new network. """
#
#     pass


# def network_detail(request):
#     """ Public profile of a network. """
#
#     pass


# def network_edit(request, pk):
#     """ Edit network page. """
#
#     pass


# def network_member(request):
#     """ Table of networks your org is member of."""
#
#     pass


# def network_stories(request):
#     """ Displays a filterable table of stories marked as shared/ready to share by any
#     organizations that a user's organization is a part of.
#
#     Initial display organizes content by story>facet>est. run date
#     Filterable by story name, facet type, facet name, due for edit, est. run date, credit,
#     editor, status.
#
#     Stories marked as share appear but are greyed out/inaccessible until the owner marks
#     them as Ready to Share. (This is so partners know it will exist and can plan to incorporate
#     it once it becomes available.)
#     """
#
#     pass
