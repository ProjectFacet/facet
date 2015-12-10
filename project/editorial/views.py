from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import StoryForm, EditUserProfile, SeriesForm, CreateOrganization
# from django.util import timezone
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
#   Story Views
#----------------------------------------------------------------------#


def storylist(request):
    """ Returns story list. """

    return render(request, 'editorial/storylist.html')


def story_new(request):
    """ Return edit story page. """

    form = StoryForm()
    if request.method == "POST":
        form = StoryForm(request.POST or None)
    if form.is_valid():
        story = form.save(commit=False)
        story.owner = request.user
        story.creation_date = datetime.datetime.now()
        story.save()
        return redirect('story_detail', pk=post.pk)
    else:
        form = StoryForm()
    return render(request, 'editorial/story.html', {'form': form})

def story_detail(request):
    return HttpResponse("I think it worked for a story.")


#----------------------------------------------------------------------#
#   Series Views
#----------------------------------------------------------------------#


def series_new(request):
    """ Return edit series page. """

    form = SeriesForm()
    if request.method == "POST":
        form = SeriesForm(request.POST or None)
    if form.is_valid():
        series = form.save(commit=False)
        series.owner = request.user
        series.creation_date = datetime.datetime.now()
        series.save()
        return redirect()
    else:
        form = SeriesForm()
    return render(request, 'editorial/series/html', {'form': form})


def series_detail(request):
    """ Return series detail page. """

    return HttpResponse("I think it worked for a series.")


#----------------------------------------------------------------------#
#   Facet Views
#----------------------------------------------------------------------#




#----------------------------------------------------------------------#
#   User Views
#----------------------------------------------------------------------#

def edit_user(request):
    # return user profile page with profile forms
    form = EditUserProfile()
    if request.method == "POST":
        form = EditUserProfile(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        user.save()
        return redirect('index')
    else:
        form = EditUserProfile()
    return render(request, 'editorial/user_profile_settings.html', {'form': form})


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


#----------------------------------------------------------------------#
#   Network Views
#----------------------------------------------------------------------#