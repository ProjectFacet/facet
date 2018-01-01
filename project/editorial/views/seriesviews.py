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
from braces.views import LoginRequiredMixin

from editorial.forms import (
    SeriesForm,
    CommentForm,
    NoteForm,
    TaskForm,
    EventForm,
    SimpleImageForm,
    SimpleDocumentForm,
    )

from editorial.models import (
    Series,
    Note,
    ImageAsset,
    Comment,
    Discussion,
    Task,
    Event,
    SimpleImage,
    SimpleDocument,
    )

#----------------------------------------------------------------------#
#   Series Views
#----------------------------------------------------------------------#

class SeriesListView(LoginRequiredMixin, ListView):
    """ Displays a filterable table of series.

    Initial display organizes content by series name.
    """

    # handle users that are not logged in
    login_url = settings.LOGIN_URL

    context_object_name = 'series'

    def get_queryset(self):
        """Return series belonging to the organization."""

        org = self.request.user.organization
        return org.series_organization.all()


class SeriesCreateView(LoginRequiredMixin, CreateView):
    """ A logged in user can create a series.

    Series serve as a linking mechanism to connect related stories and to share
    assets between them. Series allow users to create planning notes at a series level
    have planning discussions and upload assets. Assets are always associated with a series
    so they are easily accessible to stories and all facets. This means that even single
    stories technically have a series, but in that case the user does not interact with any
    series interface.
    """

    # handle users that are not logged in
    login_url = settings.LOGIN_URL

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


class SeriesDetailView(LoginRequiredMixin, DetailView):
    """ The detail page for a series.

    Displays the series' planning notes, discussion, assets, share and collaboration status
    and sensivity status.
    """

    # handle users that are not logged in
    login_url = settings.LOGIN_URL

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
        notes = self.object.notes.all().order_by('-creation_date')
        form = NoteForm()
        return {'notes': notes, 'form': form}

    # FIXME Currently causing error because org is not getting passed to TaskForm
    # Commented out task form and version of return statement that uses it.
    def series_tasks(self):
        """Get tasks and task form for a series."""

        self.object = self.get_object()
        tasks = self.object.task_set.all()
        identified = self.object.task_set.filter(status="Identified")
        inprogress = self.object.task_set.filter(status="In Progress")
        complete = self.object.task_set.filter(status="Complete")
        identified_ct = identified.count()
        inprogress_ct = inprogress.count()
        complete_ct = complete.count()
        # form = TaskForm()
        return {
                'tasks': tasks,
                'identified': identified,
                'inprogress': inprogress,
                'complete': complete,
                'identified_ct': identified_ct,
                'inprogress_ct': inprogress_ct,
                'complete_ct': complete_ct
                # 'form': form,
                }


    # FIXME Currently causing error because org is not getting passed to EventForm
    # Commented out task form and version of return statement that uses it.
    def story_events(self):
        """Get events and event form for a series."""

        self.object = self.get_object()
        events = self.object.event_set.all()
        # form = EventForm()
        # return {'events': events, 'form': form}
        return {'events': events}

    def series_assets(self):
        """Get all the assets associated with facets of stories in a series."""

        self.object = self.get_object()
        images = self.object.get_series_images()
        documents = self.object.get_series_documents()
        audio = self.object.get_series_audio()
        video = self.object.get_series_video()
        return {'images': images, 'documents': documents, 'audio': audio, 'video': video}

    def simple_images(self):
        """Return simple images."""

        self.object = self.get_object()
        images = self.object.simple_image_assets.all()
        print "IMG: ", images
        form = SimpleImageForm()
        return {'images': images, 'form':form,}

    def simple_documents(self):
        """Return simple documents."""

        self.object = self.get_object()
        documents = self.object.simple_document_assets.all()
        print "DOC: ", documents
        form = SimpleDocumentForm()
        return {'documents': documents, 'form':form,}



class SeriesUpdateView(LoginRequiredMixin, UpdateView):
    """Update a series."""

    # handle users that are not logged in
    login_url = settings.LOGIN_URL

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


class SeriesAssetTemplateView(LoginRequiredMixin, TemplateView):
    """Display media associated with a series."""

    # handle users that are not logged in
    login_url = settings.LOGIN_URL

    template_name = 'editorial/series_assets.html'

    def get_context_data(self, pk):
        """Return all the (complex) assets associated with a series."""

        series = get_object_or_404(Series, id=pk)
        images = series.get_series_images()
        documents = series.get_series_documents()
        audio = series.get_series_audio()
        video = series.get_series_video()
        return {'series':series, 'images': images, 'documents': documents, 'audio': audio, 'video': video,}


# class SeriesDeleteView(DeleteView, FormMessagesMixin):
class SeriesDeleteView(LoginRequiredMixin, DeleteView):
    """Delete a series and its associated items.

    In this series, we expect deletion to be done via a JS pop-up UI; we don't expect to
    actually use the "do you want to delete this?" Django-generated page. However, this is
    available if useful.
    """

    # handle users that are not logged in
    login_url = settings.LOGIN_URL

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


def series_schedule(request, pk):
    """Generate a JSON object containing entries to display on series calendar."""

    series = get_object_or_404(Series, pk=pk)
    series_calendar = Series.get_series_story_events(series)

    return HttpResponse(json.dumps(series_calendar), content_type='application/json')
