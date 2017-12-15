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
from django.views.generic import TemplateView , UpdateView, DetailView, CreateView, ListView
from django.views.decorators.csrf import csrf_exempt
import datetime
import json
from actstream import action

from editorial.forms import (
    EventForm,
    CommentForm,
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
    )


#----------------------------------------------------------------------#
#   Events Views
#----------------------------------------------------------------------#

class EventCreateView(CreateView):
    """A logged in user can create a event.

    Events are used to manage information about events.
    Events can either manage events that an organization are hosting
    or events that an organization is reporting on.
    Ex: Hosting = A townhall discussion hosted by an organization
    Ex: Reporting = A press conference at city hall covered for a story.
    Events have a connection to either a Project, Series, Story or Event.
    """

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


class EventUpdateView(UpdateView):
    """ The detail page for a event.

    Displays the event information.
    """

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
        form = EventCommentForm()
        return {'discussion': discussion, 'comments': comments, 'form': form,}

    def get_success_url(self):

        action.send(self.request.user, verb="edited", action_object=self.object)
        return super(EventUpdateView, self).get_success_url()


def event_delete(request, pk):
    """Delete a project and its related objects then redirect user to project list."""

    pass


# FIXME form challenges
class OrganizationEventTemplateView(TemplateView):
    """Display all the events associated with an organization.

    """

    context_object_name = 'events'
    template_name = 'editorial/event_list.html'

    # form_class = EventForm
    #
    # def get_form_kwargs(self):
    #     """Pass organization to form."""
    #
    #     kw = super(ProjectEventTemplateView, self).get_form_kwargs()
    #     kw.update({'organization': self.request.user.organization})
    #     return kw

    def get_context_data(self, pk):
        """Return events belonging to the project."""

        organization = get_object_or_404(Organization, id=pk)
        # form = TaskForm()
        events = organization.event_set.all()
        return {
            'organization': organization,
            'events': events,
            # 'form': form,
        }


# FIXME form challenges
class ProjectEventTemplateView(TemplateView):
    """Display all the events associated with a project.

    """

    context_object_name = 'events'
    template_name = 'editorial/event_list.html'

    # form_class = EventForm
    #
    # def get_form_kwargs(self):
    #     """Pass organization to form."""
    #
    #     kw = super(ProjectEventTemplateView, self).get_form_kwargs()
    #     kw.update({'organization': self.request.user.organization})
    #     return kw

    def get_context_data(self, pk):
        """Return events belonging to the project."""

        project = get_object_or_404(Project, id=pk)
        # form = TaskForm()
        events = project.event_set.all()
        return {
            'project': project,
            'events': events,
            # 'form': form,
        }


# FIXME form challenges
class SeriesEventTemplateView(TemplateView):
    """Display all the events associated with a series.

    """

    context_object_name = 'events'
    template_name = 'editorial/event_list.html'

    # form_class = EventForm
    #
    # def get_form_kwargs(self):
    #     """Pass organization to form."""
    #
    #     kw = super(SeriesEventTemplateView, self).get_form_kwargs()
    #     kw.update({'organization': self.request.user.organization})
    #     return kw

    def get_context_data(self, pk):
        """Return events belonging to the series."""

        series = get_object_or_404(Series, id=pk)
        # form = TaskForm()
        events = series.event_set.all()
        return {
            'series': series,
            'events': events,
            # 'form': form,
        }


# FIXME form challenges
class StoryEventTemplateView(TemplateView):
    """Display all the events associated with a story."""

    context_object_name = 'events'
    template_name = 'editorial/event_list.html'

    # form_class = EventForm
    #
    # def get_form_kwargs(self):
    #     """Pass organization to form."""
    #
    #     kw = super(StoryEventTemplateView, self).get_form_kwargs()
    #     kw.update({'organization': self.request.user.organization})
    #     return kw

    def get_context_data(self, pk):
        """Return events belonging to the story."""

        story = get_object_or_404(Story, id=pk)
        # form = TaskForm()
        events = story.event_set.all()
        return {
            'story': story,
            'events': events,
            # 'form': form,
        }
