""" Event views for editorial app.

    editorial/views/eventviews.py
"""

# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponse
from django.utils import timezone
from django.views.generic import TemplateView , UpdateView, DetailView, CreateView, ListView, DeleteView
from django.views.decorators.csrf import csrf_exempt
import datetime
import json
from actstream import action
from braces.views import LoginRequiredMixin, FormMessagesMixin

from editorial.forms import (
    EventForm,
    CommentForm,
    NoteForm,
    )


from editorial.models import (
    Organization,
    Project,
    Series,
    Story,
    Task,
    Event,
    Comment,
    Discussion,
    Note,
    )


#----------------------------------------------------------------------#
#   Events Views
#----------------------------------------------------------------------#

# ACCESS: Any org user, or user from an organization that is in collaborate_with
# should be able to create an event for P, Sr, St, F.
# Contractors should only be able to create events for P, Sr or St they are
# assigned to.
class EventCreateView(LoginRequiredMixin, CreateView):
    """A logged in user can create a event.

    Events are used to manage information about events.
    Events can either manage events that an organization are hosting
    or events that an organization is reporting on.
    Ex: Hosting = A townhall discussion hosted by an organization
    Ex: Reporting = A press conference at city hall covered for a story.
    Ex. Administrative = An internal event like an org or team meeting.
    Events have a connection to either a Project, Series, Story or Event.
    """

    # handle users that are not logged in
    login_url = settings.LOGIN_URL

    model = Event
    form_class = EventForm

    def get_form_kwargs(self):
        """Pass user organization to the form."""

        kw = super(EventCreateView, self).get_form_kwargs()
        kw.update({'organization': self.request.user.organization})
        return kw

    def form_valid(self, form):
        """Save -- but first adding owner and organization."""

        self.object = event = form.save(commit=False)

        # create and set discussion
        discussion = Discussion.objects.create_discussion("EV")
        event.discussion = discussion

        # set user specific values
        event.owner = self.request.user
        event.organization = self.request.user.organization

        event.save()
        form.save_m2m()

        # record action for activity stream
        action.send(self.request.user, verb="created", action_object=event)

        return redirect(self.get_success_url())


# ACCESS: Any org user, or user from an organization that is in collaborate_with
# should be able to edit an event for P, Sr, St, F.
# Contractors should only be able to edit events for P, Sr or St they are
# assigned to.
class EventUpdateView(LoginRequiredMixin, UpdateView):
    """ The detail page for a event.

    Displays the event information.
    """

    # handle users that are not logged in
    login_url = settings.LOGIN_URL

    model = Event
    form_class = EventForm

    def get_form_kwargs(self):
        """Pass organization to form."""

        kw = super(EventUpdateView, self).get_form_kwargs()
        kw.update({'organization': self.request.user.organization})
        return kw

    def event_discussion(self):
        """Get discussion, comments and comment form for the event."""

        self.object = self.get_object()
        discussion = self.object.discussion
        comments = discussion.comment_set.all()
        form = CommentForm()
        return {'discussion': discussion, 'comments': comments, 'form': form,}

    def event_notes(self):
        """Get notes and note form for event."""

        self.object = self.get_object()
        notes = self.object.notes.all().order_by('-creation_date')
        form = NoteForm()
        return {'notes': notes, 'form': form}

    def get_success_url(self):

        action.send(self.request.user, verb="edited", action_object=self.object)
        return super(EventUpdateView, self).get_success_url()


# ACCESS: Any org user that is an admin or editor should be able to delete an
# event associated with their org, or an org PSS.
# class EventDeleteView(DeleteView, FormMessagesMixin):
class EventDeleteView(LoginRequiredMixin, DeleteView):
    """View for handling deletion of an event.

    In this project, we expect deletion to be done via a JS pop-up UI; we don't expect to
    actually use the "do you want to delete this?" Django-generated page. However, this is
    available if useful.
    """

    # handle users that are not logged in
    login_url = settings.LOGIN_URL

    # FIXME: this would be a great place to use braces' messages; usage commented out for now

    model = Event
    template_name = "editorial/event_delete.html"

    # form_valid_message = "Deleted."
    # form_invalid_message = "Please check form."

    def get_success_url(self):
        """Post-deletion, return to the task parent URL."""

        if self.object.project:
            project = self.object.project
            return reverse('project_event_list', kwargs={'pk': project.id})
        if self.object.series:
            series = self.object.series
            return reverse('series_event_list', kwargs={'pk': series.id})
        if self.object.story:
            story = self.object.story
            return reverse('story_event_list', kwargs={'pk': story.id})
        if self.object.evt_organization:
            organization = self.object.evt_organization
            return reverse('organization_event_list', kwargs={'pk': organization.id})

#----------------------------------------------------------------------#
#   Content Event Views
#----------------------------------------------------------------------#

# ACCESS: Any org user should be able to create an event associated
# with their organization
class OrganizationEventView(LoginRequiredMixin, CreateView):
    """Display all the events associated with an organization.
    """

    # handle users that are not logged in
    login_url = settings.LOGIN_URL

    context_object_name = 'events'
    template_name = 'editorial/event_list.html'
    form_class = EventForm

    def get_form_kwargs(self):
        """Pass organization to form."""

        kw = super(OrganizationEventView, self).get_form_kwargs()
        kw.update({'organization': self.request.user.organization})
        return kw

    def get_context_data(self, **kwargs):
        """Return events belonging to the organization."""

        context = super(OrganizationEventView, self).get_context_data(**kwargs)
        organization = get_object_or_404(Organization, id=self.kwargs['pk'])
        events = organization.event_set.all()
        reporting_ct = organization.event_set.filter(event_type="Reporting").count()
        hosting_ct = organization.event_set.filter(event_type="Hosting").count()
        context['organization'] = organization
        context['events'] = events
        context['reporting_ct'] = reporting_ct
        context['hosting_ct'] = hosting_ct
        return context


# ACCESS: Any org user should be able to view/create an event associated a project owned
# by their organization
# A user from an organization that is in collaborate_with on a project
# should be able to view/create an event for a project they have access to.
class ProjectEventView(LoginRequiredMixin, CreateView):
    """Display all the events associated with a project.
    """

    # handle users that are not logged in
    login_url = settings.LOGIN_URL

    context_object_name = 'events'
    template_name = 'editorial/event_list.html'
    form_class = EventForm

    def get_form_kwargs(self):
        """Pass organization to form."""

        kw = super(ProjectEventView, self).get_form_kwargs()
        kw.update({'organization': self.request.user.organization})
        return kw

    def get_context_data(self, **kwargs):
        """Return events belonging to the project."""

        context = super(ProjectEventView, self).get_context_data(**kwargs)
        project = get_object_or_404(Project, id=self.kwargs['pk'])
        events = project.event_set.all()
        reporting_ct = project.event_set.filter(event_type="Reporting").count()
        hosting_ct = project.event_set.filter(event_type="Hosting").count()
        context['project'] = project
        context['events'] = events
        context['reporting_ct'] = reporting_ct
        context['hosting_ct'] = hosting_ct
        return context


# ACCESS: Any org user should be able to view/create an event associated a series owned
# by their organization
class SeriesEventView(LoginRequiredMixin, CreateView):
    """Display all the events associated with a series.
    """

    # handle users that are not logged in
    login_url = settings.LOGIN_URL

    context_object_name = 'events'
    template_name = 'editorial/event_list.html'
    form_class = EventForm

    def get_form_kwargs(self):
        """Pass organization to form."""

        kw = super(SeriesEventView, self).get_form_kwargs()
        kw.update({'organization': self.request.user.organization})
        return kw

    def get_context_data(self, **kwargs):
        """Return events belonging to the series."""

        context = super(SeriesEventView, self).get_context_data(**kwargs)
        series = get_object_or_404(Series, id=self.kwargs['pk'])
        events = series.event_set.all()
        reporting_ct = series.event_set.filter(event_type="Reporting").count()
        hosting_ct = series.event_set.filter(event_type="Hosting").count()
        context['series'] = series
        context['events'] = events
        context['reporting_ct'] = reporting_ct
        context['hosting_ct'] = hosting_ct
        return context


# ACCESS: Any org user should be able to view/create an event associated a story owned
# by their organization
# A user from an organization that is in collaborate_with on a story
# should be able to view/create an event for a story they have access to.
class StoryEventView(LoginRequiredMixin, CreateView):
    """Display all the events associated with a story."""

    # handle users that are not logged in
    login_url = settings.LOGIN_URL

    context_object_name = 'events'
    template_name = 'editorial/event_list.html'
    form_class = EventForm

    def get_form_kwargs(self):
        """Pass organization to form."""

        kw = super(StoryEventView, self).get_form_kwargs()
        kw.update({'organization': self.request.user.organization})
        return kw

    def get_context_data(self, **kwargs):
        """Return events belonging to the project."""

        context = super(StoryEventView, self).get_context_data(**kwargs)
        story = get_object_or_404(Story, id=self.kwargs['pk'])
        events = story.event_set.all()
        reporting_ct = story.event_set.filter(event_type="Reporting").count()
        hosting_ct = story.event_set.filter(event_type="Hosting").count()
        context['story'] = story
        context['events'] = events
        context['reporting_ct'] = reporting_ct
        context['hosting_ct'] = hosting_ct
        return context
