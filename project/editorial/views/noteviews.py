""" Note views for editorial app.

    editorial/views/noteviews.py
"""

# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponse
from django.utils import timezone
from django.views.generic import TemplateView , UpdateView, DetailView
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
import datetime
import json
from actstream import action

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
#   General Note Views
#----------------------------------------------------------------------#

def note_content_html(request, note_type, pk):
    """Return note content as html."""

    if note_type=='organization':
        note = get_object_or_404(OrganizationNote, pk=pk)
    elif note_type=='network':
        print "in note_type = network"
        note = get_object_or_404(NetworkNote, pk=pk)
    elif note_type=='user':
        note = get_object_or_404(UserNote, pk=pk)
    elif note_type=='series':
        note = get_object_or_404(SeriesNote, pk=pk)
    elif note_type=='story':
        note = get_object_or_404(StoryNote, pk=pk)

    note_html = render_to_string('note-content.html', {
                        'note': note,
                        'note_type': note_type,
    })

    return HttpResponse(note_html)

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
    if request.method == "POST":
        form = OrganizationNoteForm(request.POST or None)
        if form.is_valid():
            organizationnote = form.save(commit=False)
            organizationnote.owner = request.user
            organizationnote.organization = organization
            organizationnote.save()

            # record action for activity story_team
            action.send(request.user, verb="added note", action_object=organizationnote, target=organization)

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
            seriesnote.organization = request.user.organization
            seriesnote.series = series
            seriesnote.save()

            # record action for activity story_team
            action.send(request.user, verb="added note", action_object=seriesnote, target=series)

            return redirect('series_detail', pk=series.id)

#----------------------------------------------------------------------#
#   Story Note Views
#----------------------------------------------------------------------#

def story_notes(request, pk):
    """ Display all of the notes for an story. """

    story = get_object_or_404(Story, pk=pk)
    storynotes = StoryNote.objects.filter(story_id=story.id)
    storynoteform = StoryNoteForm()

    return render(request, 'editorial/storynotes.html', {
        'story': story,
        'storynotes': storynotes,
        'storynoteform': storynoteform,
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
            storynote.organization = request.user.organization
            storynote.story = story
            storynote.save()

            # record action for activity story_team
            action.send(request.user, verb="added note", action_object=storynote, target=story)

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

            # record action for activity story_team
            action.send(request.user, verb="added note", action_object=networknote, target=network)

            return redirect('network_detail', pk=network.pk)
