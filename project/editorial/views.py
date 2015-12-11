from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import StoryForm, EditUserProfile, SeriesForm, CreateOrganization
from django.utils import timezone
# from django.utils.timezone import now
import datetime


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
    """ Returns dashboard. """

    # return dashboard view for logged in user.
    return render(request, 'editorial/dashboard.html')

#----------------------------------------------------------------------#
#   Team Views
#----------------------------------------------------------------------#

def team_list(request):
    """ Return teams list."""

    return render(request, 'editorial/team.html')


#----------------------------------------------------------------------#
#   Discussion Views
#----------------------------------------------------------------------#

def discussion(request):
    """ Return discussion inbox."""

    return render(request, 'editorial/discussion.html')


#----------------------------------------------------------------------#
#   Organization Views
#----------------------------------------------------------------------#

def new_organization(request):
    form = CreateOrganization()
    if request.method == "POST":
        form = CreateOrganization(request.POST or None)
    if form.is_valid():
        organization = form.save(commit=False)
        organization.owner = request.user
        organization.save()
        return redirect('index')
    else:
        form = CreateOrganization()
    return render(request, 'editorial/createorg.html', {'form': form})


def org_detail(request):
    """ The public profile of an organization. """

    return render(request, 'editorial/org_detail.html')


def org_edit(request):
    """ Edit the profile of an organization. """

    pass

#----------------------------------------------------------------------#
#   User Views
#----------------------------------------------------------------------#

def user_detail(request):
    """ The public profile of a user. """

    return render(request, 'editorial/user_detail.html')


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
    """ Table of active series. """
    pass


def series_new(request):
    """ Create series page. """

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
    """ Return series detail page. """

    return HttpResponse("I think it worked for a series.")


def series_edit(request, pk):
    """ Edit series page."""
    
    return HttpResponse("Could edit a series here.")

#----------------------------------------------------------------------#
#   Story Views
#----------------------------------------------------------------------#

def story_list(request):
    """ Table of active stories and their facets. """

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
    """ Return story detail page."""

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

def network_new(request):
    """ Create a new network. """

    pass


def network_detail(request):
    """ Public profile of a network. """

    pass


def network_edit(request, pk):
    """ Edit network page. """
    
    pass


def network_member(request):
    """ Table of networks your org is member of."""

    pass


def network_stories(request):
    """ Return story detail page."""

    pass

