""" Series views for editorial app.

    editorial/views/seriesviews.py
"""

# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponse
from django.core.urlresolvers import reverse_lazy, reverse
from django.utils import timezone
from django.views.generic import TemplateView , UpdateView, DetailView, ListView, CreateView, DeleteView
from django.views.decorators.csrf import csrf_exempt
import datetime
import json
from actstream import action

from editorial.forms import (
    SeriesForm,
    CommentForm,
    NoteForm,
    TaskForm,
    EventForm,
    )

from editorial.models import (
    Series,
    Note,
    ImageAsset,
    Comment,
    Discussion,
    Task,
    Event,
    )

#----------------------------------------------------------------------#
#   Series Views
#----------------------------------------------------------------------#

class SeriesListView(ListView):
    """ Displays a filterable table of series.

    Initial display organizes content by series name.
    """

    context_object_name = 'series'

    def get_queryset(self):
        """Return series belonging to the organization."""

        org = self.request.user.organization
        return org.series_organization.all()


class SeriesCreateView(CreateView):
    """ A logged in user can create a series.

    Series serve as a linking mechanism to connect related stories and to share
    assets between them. Series allow users to create planning notes at a series level
    have planning discussions and upload assets. Assets are always associated with a series
    so they are easily accessible to stories and all facets. This means that even single
    stories technically have a series, but in that case the user does not interact with any
    series interface.
    """

    model = Series
    form_class = SeriesForm

    def get_form_kwargs(self):
        """Pass current user organization to the series form."""

        kw = super(SeriesCreateView, self).get_form_kwargs()
        kw.update({'organization': self.request.user.organization})
        return kw

    def form_valid(self, form):
        """Save -- but first adding owner and organization."""

        self.object = series = form.save(commit=False)

        discussion = Discussion.objects.create_discussion("SER")
        series.discussion = discussion

        series.owner = self.request.user
        series.organization = self.request.user.organization

        series.save()
        form.save_m2m()

        action.send(self.request.user, verb="created", action_object=self.object)

        return redirect(self.get_success_url())


class SeriesDetailView(DetailView):
    """ The detail page for a series.

    Displays the series' planning notes, discussion, assets, share and collaboration status
    and sensivity status.
    """

    model = Series

    def get_form_kwargs(self):
        """Pass organization to forms."""

        kw = super(SeriesDetailView, self).get_form_kwargs()
        kw.update({'organization': self.request.user.organization})
        return kw

    def stories(self):
        """Get all stories associated with a series."""

        self.object = self.get_object()
        return self.object.story_set.all()

    def series_discussion(self):
        """Get discussion, comments and comment form for a series."""

        self.object = self.get_object()
        discussion = self.object.discussion
        comments = discussion.comment_set.all()
        form = CommentForm()
        return {'discussion': discussion, 'comments': comments, 'form': form}

    def series_notes(self):
        """Get notes and note form for a series."""

        self.object = self.get_object()
        notes = self.object.notes.all()
        form = NoteForm()
        return {'notes': notes, 'form': form}

    # FIXME Currently causing error because org is not getting passed to TaskForm
    # Commented out task form and version of return statement that uses it.
    def series_tasks(self):
        """Get tasks and task form for a series."""

        self.object = self.get_object()
        tasks = self.object.task_set.all()
        # form = TaskForm()
        # return {'tasks': tasks, 'form': form}
        return {'tasks': tasks}


    # FIXME Currently causing error because org is not getting passed to EventForm
    # Commented out task form and version of return statement that uses it.
    def story_events(self):
        """Get events and event form for a series."""

        self.object = self.get_object()
        events = self.object.event_set.all()
        # form = EventForm()
        # return {'events': events, 'form': form}
        return {'events': events}


class SeriesUpdateView(UpdateView):
    """Update a series."""

    model = Series
    form_class = SeriesForm

    def get_form_kwargs(self):
        """Pass current user organization to the series form."""

        kw = super(SeriesUpdateView, self).get_form_kwargs()
        kw.update({'organization': self.request.user.organization})
        return kw

    def get_success_url(self):
        """Record action for activity stream."""

        action.send(self.request.user, verb="edited", action_object=self.object)
        return super(SeriesUpdateView, self).get_success_url()


# class SeriesDeleteView(DeleteView, FormMessagesMixin):
class SeriesDeleteView(DeleteView):
    """Delete a series and its associated items.

    In this project, we expect deletion to be done via a JS pop-up UI; we don't expect to
    actually use the "do you want to delete this?" Django-generated page. However, this is
    available if useful.
    """

    # FIXME: this would be a great place to use braces' messages; usage commented out for now

    model = Series
    template_name = "editorial/series_delete.html'"

    # form_valid_message = "Deleted."
    # form_invalid_message = "Please check form."

    def get_success_url(self):
        """Post-deletion, return to the series list."""

        return reverse('series_list')


def series_json(request):
    """Displays JSON of series that a story can be a part of."""

    series_list = Series.objects.filter(organization=request.user.organization)
    series = {}
    for item in series_list:
        series[item.id]=item.name
    print series
    return HttpResponse(json.dumps(series), content_type = "application/json")
