""" Note views for editorial app.

    editorial/views/noteviews.py
"""

# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from actstream import action
from braces.views import LoginRequiredMixin, FormMessagesMixin
from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.views.generic import TemplateView, CreateView, DeleteView, View
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
    Event,
    Task,
    Note,
)


#----------------------------------------------------------------------#
#   General Note Views
#----------------------------------------------------------------------#

# ACCESS: Any org user, or user from an organization that is in collaborate_with
# should be able to view the notes for the object they have access to
# Contractors should only be able to do so for PSSF that they have access to
# That should be handled by limiting which PSSF they have access to.
class NoteContent(LoginRequiredMixin, View):
    """Return note content as html for display on <object>notes.html pages."""

    def get(self, request, *args, **kwargs):

        note_id = self.kwargs['note']
        note = get_object_or_404(Note, pk=note_id)
        note_html = render_to_string('note-content.html', {
                        'note': note,
        })

        return HttpResponse(note_html)


# ACCESS: Any org user, or user from an organization that is in collaborate_with
# should be able to create a note for P, Sr, St, F, T or E they have access to.
# Contractors should only be able to do so for PSSFTE that they have access to
# That should be handled by limiting which PSSF they have access to.
class NoteCreateView(LoginRequiredMixin, FormMessagesMixin, CreateView):
    """Create a note."""

    model = Note
    form_class = NoteForm
    form_invalid_message = "Something went wrong. Check the form."
    form_valid_message = "Note created."

    def form_valid(self, form):
        """Save -- but first add some information and association
        with the correct object."""

        self.object = note = form.save(commit=False)
        # identify what the note is being associated with
        associated_object = self.request.POST.get('association')
        if associated_object == 'network':
            # retrieve the object to connect with the note
            network_id = self.request.POST.get('network')
            network = get_object_or_404(Network, id=network_id)
            # retrieve or set values for note attributes
            title = self.request.POST.get('title')
            text = self.request.POST.get('text')
            important = form.cleaned_data['important']
            note_type = "NET"
            # create and save note
            note = Note.objects.create_note(owner=self.request.user, title=title, text=text, note_type=note_type, important=important)
            note.save()
            # associate note with object
            network.notes.add(note)
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
            important = form.cleaned_data['important']
            note_type = "ORG"
            # create and save note
            note = Note.objects.create_note(owner=self.request.user, title=title, text=text, note_type=note_type, important=important)
            note.save()
            # associate note with object
            organization.notes.add(note)
            # record action
            action_target = organization
            action.send(self.request.user, verb="created", action_object=note, target=action_target)
            # redirect to the associated object
            return HttpResponseRedirect(reverse('org_detail', args=(organization.id,)))
        elif associated_object == 'user':
            # retrieve the object to connect with the note
            user_id = self.request.POST.get('user')
            user = get_object_or_404(User, id=user_id)
            # retrieve or set values for note attributes
            title = self.request.POST.get('title')
            text = self.request.POST.get('text')
            important = form.cleaned_data['important']
            note_type = "USER"
            # create and save note
            note = Note.objects.create_note(owner=self.request.user, title=title, text=text, note_type=note_type, important=important)
            note.save()
            # associate note with object
            user.notes.add(note)
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
            important = form.cleaned_data['important']
            note_type = "PRO"
            # create and save note
            note = Note.objects.create_note(owner=self.request.user, title=title, text=text, note_type=note_type, important=important)
            note.save()
            # associate note with object
            project.notes.add(note)
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
            important = form.cleaned_data['important']
            note_type = "SER"
            # create and save note
            note = Note.objects.create_note(owner=self.request.user, title=title, text=text, note_type=note_type, important=important)
            note.save()
            # associate note with object
            series.notes.add(note)
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
            important = form.cleaned_data['important']
            note_type = "STO"
            # create and save note
            note = Note.objects.create_note(owner=self.request.user, title=title, text=text, note_type=note_type, important=important)
            note.save()
            # associate note with object
            story.notes.add(note)
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
            important = form.cleaned_data['important']
            note_type = "TSK"
            # create and save note
            note = Note.objects.create_note(owner=self.request.user, title=title, text=text, note_type=note_type, important=important)
            note.save()
            # associate note with object
            task.notes.add(note)
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
            important = form.cleaned_data['important']
            note_type = "EV"
            # create and save note
            note = Note.objects.create_note(owner=self.request.user, title=title, text=text, note_type=note_type, important=important)
            note.save()
            # associate note with object
            event.notes.add(note)
            # record action
            action_target = event
            action.send(self.request.user, verb="created", action_object=note, target=action_target)
            # redirect to the associated object
            return HttpResponseRedirect(reverse('event_detail', args=(event.id,)))


# ACCESS: Any org user, or user from an organization that is in collaborate_with
# should be able to delete a note for P, Sr, St, F, T or E that they have access to
class NoteDelete(LoginRequiredMixin, FormMessagesMixin, DeleteView):
    """View for handling deletion of a note.

    In this project, we expect deletion to be done via a JS pop-up UI; we don't expect to
    actually use the "do you want to delete this?" Django-generated page. However, this is
    available if useful.
    """

    model = Note
    template_name = "editorial/note_delete.html"

    form_valid_message = "Deleted."
    form_invalid_message = "Please check form."

    def get_success_url(self):
        """Post-deletion, return to the parent object detail url."""

        print "THING: ", self.object
        print self.object.pk
        if self.object.organization_set.first():
            organization = self.object.organization_set.first()
            print "organization: ", organization
            return reverse('org_detail', kwargs={'pk': organization.id})
        if self.object.user_set.first():
            user = self.object.user_set.first()
            print "user: ", user
            return reverse('user_detail', kwargs={'pk': user.id})
        if self.object.network_set.first():
            network = self.object.network_set.first()
            print "NETWORK: ", network
            return reverse('network_detail', kwargs={'pk': network.id})
        if self.object.project_set.first():
            project = self.object.project_set.first()
            print "PROJECT: ", project
            return reverse('project_detail', kwargs={'pk': project.id})
        if self.object.series_set.first():
            series = self.object.series_set.first()
            print "SERIES: ", series
            return reverse('series_detail', kwargs={'pk': series.id})
        if self.object.story_set.first():
            story = self.object.story_set.first()
            print "STORY: ", story
            return reverse('story_detail', kwargs={'pk': story.id})
        if self.object.event_set.first():
            event = self.object.event_set.first()
            print "EVENT: ", event
            return reverse('event_detail', kwargs={'pk': event.id})
        if self.object.task_set.first():
            task = self.object.task_set.first()
            print "TASK: ", task
            return reverse('task_detail', kwargs={'pk': task.id})


#----------------------------------------------------------------------#
#   Template Note Views
#----------------------------------------------------------------------#

# ACCESS: Any org user, user from an organization that is part of the network
# should be able to view/create notes for the network
class NetworkNoteView(LoginRequiredMixin, TemplateView):
    """Display all of the notes for a network."""

    template_name = 'editorial/network/networknotes.html'

    def get_context_data(self, pk):
        network = get_object_or_404(Network, pk=pk)
        form = NoteForm()
        notes = network.notes.all().order_by('-creation_date')
        return {
            'network': network,
            'form': form,
            'notes': notes,
        }


# ACCESS: Any org user should be able to view/create notes for the organization
class OrganizationNoteView(LoginRequiredMixin, TemplateView):
    """Display all of the notes for an organization."""

    template_name = 'editorial/organization/organizationnotes.html'

    def get_context_data(self, pk):
        organization = get_object_or_404(Organization, pk=pk)
        form = NoteForm()
        notes = organization.notes.all().order_by('-creation_date')
        all_notes = organization.notes.all()
        return {
            'organization': organization,
            'form': form,
            'notes': notes,
        }


# ACCESS: Any should be able to view/create notes for theirself
class UserNoteView(LoginRequiredMixin, TemplateView):
    """Display all of the notes for a user."""

    template_name = 'editorial/usernotes.html'

    def get_context_data(self, pk):
        user = get_object_or_404(User, pk=pk)
        form = NoteForm()
        notes = user.notes.all().order_by('-creation_date')
        return {
            'user': user,
            'form': form,
            'notes': notes,
        }


# ACCESS: Any org user, user from an organization that is part collaborate_with
# for a project should be able to view/create notes for the project
# A contractor with access to the project should be able to view/create a note for it.
class ProjectNoteView(LoginRequiredMixin, TemplateView):
    """Display all of the notes for a project."""

    template_name = 'editorial/projectnotes.html'

    def get_context_data(self, pk):
        project = get_object_or_404(Project, pk=pk)
        form = NoteForm()
        notes = project.notes.all().order_by('-creation_date')
        return {
            'project': project,
            'form': form,
            'notes': notes,
        }


# ACCESS: Any org user, user from an organization that is part collaborate_with
# for a series should be able to view/create notes for the series
# A contractor with access to the series should be able to viewcreate a note for it.
class SeriesNoteView(LoginRequiredMixin, TemplateView):
    """Display all of the notes for a project."""

    template_name = 'editorial/seriesnotes.html'

    def get_context_data(self, pk):
        series = get_object_or_404(Series, pk=pk)
        form = NoteForm()
        notes = series.notes.all().order_by('-creation_date')
        return {
            'series': series,
            'form': form,
            'notes': notes,
        }


# ACCESS: Any org user, user from an organization that is part collaborate_with
# for a story should be able to view/create notes for the story
# A contractor with access to the story should be able to view/create a note for it.
class StoryNoteView(LoginRequiredMixin, TemplateView):
    """Display all of the notes for a story."""

    template_name = 'editorial/storynotes.html'

    def get_context_data(self, pk):
        story = get_object_or_404(Story, pk=pk)
        form = NoteForm()
        notes = story.notes.all().order_by('-creation_date')
        return {
            'story': story,
            'form': form,
            'notes': notes,
        }


# ACCESS: Any org user, user from organization that is part of a collaborate_with
# for an object related to the task can view and create notes for a task.
class TaskNoteView(LoginRequiredMixin, TemplateView):
    """Display all of the notes for a task."""

    template_name = 'editorial/tasknotes.html'

    def get_context_data(self, pk):
        task = get_object_or_404(Task, pk=pk)
        form = NoteForm()
        notes = task.notes.all().order_by('-creation_date')
        return {
            'task': task,
            'form': form,
            'notes': notes,
        }


# ACCESS: Any org user, user from organization that is part of a collaborate_with
# for an object related to the event can view and create notes for an event.
class EventNoteView(LoginRequiredMixin, TemplateView):
    """Display all of the notes for an event."""

    template_name = 'editorial/eventnotes.html'

    def get_context_data(self, pk):
        event = get_object_or_404(Event, pk=pk)
        form = NoteForm()
        notes = event.notes.all().order_by('-creation_date')
        return {
            'event': event,
            'form': form,
            'notes': notes,
        }
