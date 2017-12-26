""" Note views for editorial app.

    editorial/views/noteviews.py
"""

# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.views.generic import TemplateView , UpdateView, DetailView, CreateView
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
import datetime
import json
from actstream import action

from editorial.forms import (
    NoteForm,
    )


from editorial.models import (
    User,
    Organization,
    Network,
    Project,
    Series,
    Story,
    Facet,
    Event,
    Task,
    Note,
    )


#----------------------------------------------------------------------#
#   General Note Views
#----------------------------------------------------------------------#

def note_content_html(request, note_type, pk):
    """Return note content as html."""

    note = get_object_or_404(Note, pk=pk)

    note_html = render_to_string('note-content.html', {
                        'note': note,
                        'note_type': note_type,
    })

    return HttpResponse(note_html)


class NoteCreateView(CreateView):
    """Create a note."""

    model = Note
    form_class = NoteForm

    def form_valid(self, form):
        """Save -- but first add some information and association
        with the correct object."""

        self.object = note = form.save(commit=False)
        # identify what the note is being associated with
        associated_object = self.request.POST.get('association')
        print "AO: ", associated_object
        if associated_object == 'network':
            # retrieve the object to connect with the note
            network_id = self.request.POST.get('network')
            network = get_object_or_404(Network, id=network_id)
            # retrieve or set values for note attributes
            title = self.request.POST.get('title')
            text = self.request.POST.get('text')
            important = self.request.POST.get('important')
            note_type = "NET"
            # create and save note
            note = Note.objects.create_note(owner=self.request.user, title=title, text=text, note_type=note_type, important=important)
            note.save()
            # record action
            action_target = network
            action.send(self.request.user, verb="created", action_object=note, target=action_target)
            # redirect to the associated object
            return HttpResponseRedirect(reverse('network_detail', args=(network.id,)))
        elif associated_object == 'organization':
            # retrieve the object to connect with the note
            organization_id = self.request.POST.get('organization')
            organization = get_object_or_404(Organization, id=organization_id)
            # retrieve or set values for note attributes
            title = self.request.POST.get('title')
            text = self.request.POST.get('text')
            important = self.request.POST.get('important')
            note_type = "ORG"
            # create and save note
            note = Note.objects.create_note(owner=self.request.user, title=title, text=text, note_type=note_type, important=important)
            note.save()
            # record action
            action_target = organization
            action.send(self.request.user, verb="created", action_object=note, target=action_target)
            # redirect to the associated object
            return HttpResponseRedirect(reverse('organization_detail', args=(organization.id,)))
        elif associated_object == 'user':
            # retrieve the object to connect with the note
            user_id = self.request.POST.get('user')
            print "UI: ", user_id
            user = get_object_or_404(User, id=user_id)
            # retrieve or set values for note attributes
            title = self.request.POST.get('title')
            text = self.request.POST.get('text')
            important = self.request.POST.get('important')
            note_type = "USER"
            # create and save note
            note = Note.objects.create_note(owner=self.request.user, title=title, text=text, note_type=note_type, important=important)
            note.save()
            # record action
            action_target = user
            action.send(self.request.user, verb="created", action_object=note, target=action_target)
            # redirect to the associated object
            return HttpResponseRedirect(reverse('user_detail', args=(user.id,)))
        elif associated_object == 'project':
            # retrieve the object to connect with the note
            project_id = self.request.POST.get('project')
            project = get_object_or_404(Project, id=project_id)
            # retrieve or set values for note attributes
            title = self.request.POST.get('title')
            text = self.request.POST.get('text')
            important = self.request.POST.get('important')
            note_type = "PRO"
            # create and save note
            note = Note.objects.create_note(owner=self.request.user, title=title, text=text, note_type=note_type, important=important)
            note.save()
            # record action
            action_target = project
            action.send(self.request.user, verb="created", action_object=note, target=action_target)
            # redirect to the associated object
            return HttpResponseRedirect(reverse('project_detail', args=(project.id,)))
        elif associated_object == 'series':
            # retrieve the object to connect with the note
            series_id = self.request.POST.get('series')
            series = get_object_or_404(Series, id=series_id)
            # retrieve or set values for note attributes
            title = self.request.POST.get('title')
            text = self.request.POST.get('text')
            important = self.request.POST.get('important')
            note_type = "SER"
            # create and save note
            note = Note.objects.create_note(owner=self.request.user, title=title, text=text, note_type=note_type, important=important)
            note.save()
            # record action
            action_target = series
            action.send(self.request.user, verb="created", action_object=note, target=action_target)
            # redirect to the associated object
            return HttpResponseRedirect(reverse('series_detail', args=(series.id,)))
        elif associated_object == 'story':
            # retrieve the object to connect with the note
            story_id = self.request.POST.get('story')
            story = get_object_or_404(Story, id=story_id)
            # retrieve or set values for note attributes
            title = self.request.POST.get('title')
            text = self.request.POST.get('text')
            important = self.request.POST.get('important')
            note_type = "STO"
            # create and save note
            note = Note.objects.create_note(owner=self.request.user, title=title, text=text, note_type=note_type, important=important)
            note.save()
            # record action
            action_target = story
            action.send(self.request.user, verb="created", action_object=note, target=action_target)
            # redirect to the associated object
            return HttpResponseRedirect(reverse('story_detail', args=(story.id,)))
        elif associated_object == 'task':
            # retrieve the object to connect with the note
            task_id = self.request.POST.get('task')
            task = get_object_or_404(Task, id=task_id)
            # retrieve or set values for note attributes
            title = self.request.POST.get('title')
            text = self.request.POST.get('text')
            important = self.request.POST.get('important')
            note_type = "TSK"
            # create and save note
            note = Note.objects.create_note(owner=self.request.user, title=title, text=text, note_type=note_type, important=important)
            note.save()
            # record action
            action_target = task
            action.send(self.request.user, verb="created", action_object=note, target=action_target)
            # redirect to the associated object
            return HttpResponseRedirect(reverse('task_detail', args=(task.id,)))
        elif associated_object == 'event':
            # retrieve the object to connect with the note
            event_id = self.request.POST.get('event')
            event = get_object_or_404(Event, id=event_id)
            # retrieve or set values for note attributes
            title = self.request.POST.get('title')
            text = self.request.POST.get('text')
            important = self.request.POST.get('important')
            note_type = "EV"
            # create and save note
            note = Note.objects.create_note(owner=self.request.user, title=title, text=text, note_type=note_type, important=important)
            note.save()
            # record action
            action_target = event
            action.send(self.request.user, verb="created", action_object=note, target=action_target)
            # redirect to the associated object
            return HttpResponseRedirect(reverse('event_detail', args=(event.id,)))

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

#----------------------------------------------------------------------#
#   User Note Views
#----------------------------------------------------------------------#

class UserNoteView(TemplateView):
    """Display all of the notes for a user."""

    template_name = 'editorial/usernotes.html'

    def get_context_data(self, pk):
        user = get_object_or_404(User, pk=pk)
        form = NoteForm()
        notes = user.note_set.filter(note_type="USER")
        return {
            'user': user,
            'form': form,
            'notes': notes,
        }

#----------------------------------------------------------------------#
#   Project Note Views
#----------------------------------------------------------------------#

def project_notes(request, pk):
    """ Display all of the notes for an project. """

    project = get_object_or_404(Project, pk=pk)
    projectnoteform = ProjectNoteForm()
    projectnotes = ProjectNote.objects.filter(project_id=project.id)

    return render(request, 'editorial/projectnotes.html', {
        'project': project,
        'projectnoteform': projectnoteform,
        'projectnotes': projectnotes,
    })

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

#----------------------------------------------------------------------#
#   Task Note Views
#----------------------------------------------------------------------#

def task_notes(request, pk):
    """ Display all of the notes for an task. """

    task = get_object_or_404(Task, pk=pk)
    tasknotes = TaskNote.objects.filter(task_id=task.id)
    tasknoteform = TaskNoteForm()

    return render(request, 'editorial/tasknotes.html', {
        'task': task,
        'tasknotes': tasknotes,
        'tasknoteform': tasknoteform,
    })

#----------------------------------------------------------------------#
#   Event Note Views
#----------------------------------------------------------------------#

def event_notes(request, pk):
    """ Display all of the notes for an event. """

    event = get_object_or_404(Event, pk=pk)
    eventnotes = EventNote.objects.filter(event_id=event.id)
    eventnoteform = EventNoteForm()

    return render(request, 'editorial/eventnotes.html', {
        'event': event,
        'eventnotes': eventnotes,
        'eventnoteform': eventnoteform,
    })
