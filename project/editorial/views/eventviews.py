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
from django.views.generic import TemplateView , UpdateView, DetailView
from django.views.decorators.csrf import csrf_exempt
import datetime
import json
from actstream import action

from editorial.forms import (
    TaskForm,
    EventForm,
    )

from editorial.models import (
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

# class EventCreateView(generic.CreateView):
#     """Create a new event."""
#
#     model = Event
#     form_class = EventForm
#
#     def form_valid(self, form):
#         form.instance.owner = self.request.user
#         return super(EventCreateView, self).form_valid(form)
#
#     def get_success_url(self):
#
#         self.request.user.organization = self.object
#         self.request.user.save()
#         return reverse('event', kwargs={'pk': self.object.pk})


# function based view version
def event_new(request):
    """A logged in user can create a event.

    Events are used to manage information about events.
    Events can either manage events that an organization are hosting
    or events that an organization is reporting on.
    Ex: Hosting = A townhall discussion hosted by an organization
    Ex: Reporting = A press conference at city hall covered for a story.
    Events have a connection to either a Project, Series, Story or Event.
    """

    form = EventForm(request=request)
    if request.method == "POST":
        form = EventForm(request.POST, request=request)
    if form.is_valid():
        event = form.save(commit=False)
        event.owner = request.user
        event.organization = request.user.organization
        event.creation_date = timezone.now()
        event.save()
        form.save_m2m()

        # record action for activity stream
        action.send(request.user, verb="created", action_object=event)

        return redirect('event_detail', pk=event.pk)
    else:
        form = EventForm(request=request)
    return render(request, 'editorial/event_detail.html', {'form': form})


def event_detail(request, pk):
    """ The detail page for a event.

    Displays the event information.
    """

    try:
        print "IN EVENT TRY"
        event = get_object_or_404(Event, pk=pk)
        form = EventForm(request=request, instance=event)
        print "GOT EVENT F=ORM"
        print form
        # discussion = ...
        # comments = ...

        if request.method == "POST":
            print "IN EVENT TRY POST"
            if 'form' in request.POST:
                form = EventForm(data=request.POST, instance=event, request=request)
                if form.is_valid():
                    form.save()
                    # record action for activity stream
                    action.send(request.user, verb="updated", action_object=event)
                    return redirect('event_detail', pk=pk)

    except:
        print "IN EVENT EXCEPT"
        # except Event.DoesNotExist:
        #display form a save a new event
        if request.method == "POST":
            "IN EVENT EXCEPT POST"
            if 'form' in request.POST:
                form=EventForm(data=request.POST, request=request)
                if form.is_valid():
                    event = form.save(commit=False)
                    event.owner = request.user
                    event.organization = request.user.organization
                    event.creation_date = timezone.now()
                    event.save()
                    form.save_m2m()
                    # record action for activity stream
                    action.send(request.user, verb="created", action_object=event)
                    return redirect('event_detail', pk=event.pk)

    return render(request, 'editorial/event_detail.html', {
        'event': event,
        'form': form,
    })


def org_host_events():
    """ Retrieve all events associated with an organization that are being hosted.
    """

    events = Event.objects.filter(organization=request.user.organization, status="Hosted")
    return render(request, 'editorial/host_event_list.html', {
            'events': events,
        })


def org_report_events():
    """ Retrieve all events associated with an organization that are being reported
    on for a story.
    """

    events = Event.objects.filter(organization=request.user.organization, status="Reporting")
    return render(request, 'editorial/host_event_list.html', {
            'events': events,
        })





# reduce duplication if possible
def org_event_list(request, pk):
    """Display all the events associated with an organization.

    """

    events = Event.objects.filter(organization=request.user.organization)
    return render(request, 'editorial/event_list.html', {
        'org_events': events,
    })


def project_event_list(request, pk):
    """Display all the events associated with a project.

    """

    project = get_object_or_404(Project, pk=pk)
    events = Event.objects.filter(project=pk)
    return render(request, 'editorial/event_list.html', {
        'project': project,
        'project_events': events,
    })


def series_event_list(request, pk):
    """Display all the evnets associated with a series.

    """

    series = get_object_or_404(Series, pk=pk)
    events = Event.objects.filter(series=pk)
    return render(request, 'editorial/event_list.html', {
        'series': series,
        'series_events': events,
    })


def story_event_list(request, pk):
    """Display all the events associated with a story.

    """

    Story = get_object_or_404(Story, pk=pk)
    events = Event.objects.filter(story=pk)
    return render(request, 'editorial/event_list.html', {
        'story': story,
        'story_events': events,
    })


def event_delete(request, pk):
    """Delete a project and its related objects then redirect user to project list."""

    pass
