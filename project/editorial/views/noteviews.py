""" Note views for editorial app.

    editorial/views/noteviews.py
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponse
from django.utils import timezone
from django.views.generic import TemplateView , UpdateView, DetailView
from django.views.decorators.csrf import csrf_exempt
import datetime
import json

from editorial.forms import (
    NetworkNoteForm,
    OrganizationNoteForm,
    UserNoteForm,
    SeriesNoteForm,
    StoryNoteForm,)

from editorial.models import (
    User,
    Organization,
    Network,
    Series,
    Story,
    SeriesNote,
    StoryNote,
    NetworkNote,
    OrganizationNote,
    UserNote,
    SeriesNote,
    StoryNote,)


#----------------------------------------------------------------------#
#   Organization Note Views
#----------------------------------------------------------------------#

def org_notes(request, pk):
    """ Display all of the notes for an organization. """

    organization = get_object_or_404(Organization, pk=pk)
    organizationnotes = OrganizationNote.objects.filter(organization_id=organization.id)
    organizationnoteform = OrganizationNoteForm()

    return render(request, 'editorial/organizationnotes.html', {
        'organization': organization,
        'organizationnoteform': organizationnoteform,
        'organizationnotes': organizationnotes,
    })


def create_org_note(request):
    """ Post a note to an organization."""

    organization = request.user.organization
    print organization
    print organization.id
    if request.method == "POST":
        form = OrganizationNoteForm(request.POST or None)
        if form.is_valid():
            organizationnote = form.save(commit=False)
            organizationnote.owner = request.user
            organizationnote.organization = organization
            organizationnote.save()
            return redirect('org_detail', pk=organization.id)


#----------------------------------------------------------------------#
#   User Note Views
#----------------------------------------------------------------------#

def user_notes(request,pk):
    """ Display all of the notes for a user. """

    user = request.user
    usernoteform = UserNoteForm()
    usernotes = UserNote.objects.filter(owner_id=request.user)
    return render(request, 'editorial/usernotes.html', {
        'user': user,
        'usernotes': usernotes,
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
#   Series Note Views
#----------------------------------------------------------------------#

def series_notes(request, pk):
    """ Display all of the notes for an series. """

    series = get_object_or_404(Series, pk=pk)
    seriesnoteform = SeriesNoteForm()
    seriesnotes = SeriesNote.objects.filter(series_id=series.id)

    return render(request, 'editorial/seriesnotes.html', {
        'series': series,
        'seriesnoteform': seriesnoteform,
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
#   Story Note Views
#----------------------------------------------------------------------#

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
#   Network Note Views
#----------------------------------------------------------------------#

def network_notes(request, pk):
    """ Display all of the notes for a network. """

    network = get_object_or_404(Network, pk=pk)
    networknotes = NetworkNote.objects.filter(network_id=network.id)
    networknoteform = NetworkNoteForm()
    return render(request, 'editorial/networknotes.html', {
        'network': network,
        'networknotes': networknotes,
        'networknoteform': networknoteform,
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
