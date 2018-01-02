""" Task views for editorial app.

    editorial/views/taskviews.py
"""

# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponse
from django.utils import timezone
from django.views.generic import TemplateView , UpdateView, DetailView, CreateView, ListView, View, DeleteView
from django.views.decorators.csrf import csrf_exempt
import datetime
import json
from actstream import action
from django.core.urlresolvers import reverse
from braces.views import LoginRequiredMixin, FormMessagesMixin

from editorial.forms import (
    TaskForm,
    CommentForm,
    NoteForm,
    )

from editorial.models import (
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
#   General Task Views
#----------------------------------------------------------------------#

# ACCESS: Any org user, or user from an organization that is in collaborate_with
# should be able to create an event for P, Sr, St, F.
# Contractors should only be able to create events for P, Sr or St they are
# assigned to.
class TaskCreateView(LoginRequiredMixin, CreateView):
    """Create a new task."""

    # handle users that are not logged in
    login_url = settings.LOGIN_URL

    model = Task
    form_class = TaskForm

    def get_form_kwargs(self):
        """Pass user organization to the form."""

        kw = super(TaskCreateView, self).get_form_kwargs()
        kw.update({'organization': self.request.user.organization})
        return kw

    def form_valid(self, form):
        """Save -- but first adding owner and organization."""

        self.object = task = form.save(commit=False)

        # create and set discussion
        discussion = Discussion.objects.create_discussion("TSK")
        task.discussion = discussion

        # set user specific values
        task.owner = self.request.user
        task.organization = self.request.user.organization

        task.save()
        form.save_m2m()

        # record action for activity stream
        action.send(self.request.user, verb="created", action_object=task)

        return redirect(self.get_success_url())


# ACCESS: Any org user, or user from an organization that is in collaborate_with
# should be able to edit an event for P, Sr, St, F.
# Contractors should only be able to edit events for P, Sr or St they are
# assigned to.
class TaskUpdateView(LoginRequiredMixin, UpdateView):
    """The detail page for a task.
    Displays the task information."""

    # handle users that are not logged in
    login_url = settings.LOGIN_URL

    model = Task
    form_class = TaskForm

    def get_form_kwargs(self):
        """Pass organization to form."""

        kw = super(TaskUpdateView, self).get_form_kwargs()
        kw.update({'organization': self.request.user.organization})
        return kw

    def task_notes(self):
        """Get notes and note form for tasks."""

        self.object = self.get_object()
        notes = self.object.notes.all().order_by('-creation_date')
        form = NoteForm()
        return {'notes': notes, 'form': form}

    def task_discussion(self):
        """Get discussion, comments and comment form for the task."""

        self.object = self.get_object()
        discussion = self.object.discussion
        comments = discussion.comment_set.all()
        form = CommentForm()
        return {'discussion': discussion, 'comments': comments, 'form': form,}

    def get_success_url(self):

        action.send(self.request.user, verb="edited", action_object=self.object)
        return super(TaskUpdateView, self).get_success_url()


# ACCESS: Any org user that is an admin or editor should be able to delete an
# event associated with their org, or an org PSS.
# class TaskDeleteView(DeleteView, FormMessagesMixin):
class TaskDeleteView(LoginRequiredMixin, DeleteView):
    """View for handling deletion of a task.

    In this project, we expect deletion to be done via a JS pop-up UI; we don't expect to
    actually use the "do you want to delete this?" Django-generated page. However, this is
    available if useful.
    """

    # handle users that are not logged in
    login_url = settings.LOGIN_URL

    # FIXME: this would be a great place to use braces' messages; usage commented out for now

    model = Task
    template_name = "editorial/task_delete.html"

    # form_valid_message = "Deleted."
    # form_invalid_message = "Please check form."

    def get_success_url(self):
        """Post-deletion, return to the task parent URL."""

        if self.object.project:
            project = self.object.project
            return reverse('project_task_list', kwargs={'pk': project.id})
        if self.object.series:
            series = self.object.series
            return reverse('series_task_list', kwargs={'pk': series.id})
        if self.object.story:
            story = self.object.story
            return reverse('story_task_list', kwargs={'pk': story.id})
        if self.object.event:
            event = self.object.event
            return reverse('event_task_list', kwargs={'pk': event.id})

#----------------------------------------------------------------------#
#   Content Task Views
#----------------------------------------------------------------------#

# ACCESS: Any org user should be able to view/create a task associated a project owned
# by their organization
# A user from an organization that is in collaborate_with on a project
# should be able to view/create a task for a project they have access to.
class ProjectTaskView(LoginRequiredMixin, CreateView):
    """Create a project task."""

    # handle users that are not logged in
    login_url = settings.LOGIN_URL

    context_object_name = 'tasks'
    template_name = 'editorial/task_list.html'
    form_class = TaskForm

    def get_form_kwargs(self):
        """Pass organization to form."""

        kw = super(ProjectTaskView, self).get_form_kwargs()
        kw.update({'organization': self.request.user.organization})
        return kw

    def get_context_data(self, **kwargs):
        """Return tasks belonging to the story."""

        context = super(ProjectTaskView, self).get_context_data(**kwargs)
        project = get_object_or_404(Project, id=self.kwargs['pk'])
        tasks = project.task_set.all()
        count = tasks.count()
        identified_ct = project.task_set.filter(status="Identified").count()
        inprogress_ct = project.task_set.filter(status="In Progress").count()
        complete_ct = project.task_set.filter(status="Complete").count()
        # ratio of complete to total number of tasks
        if complete_ct>0:
            progress = 100 * float(complete_ct)/float(count)
        else:
            progress = 0
        context['project'] = project
        context['tasks'] = tasks
        context['progress'] = progress
        context['identified_ct'] = identified_ct
        context['inprogress_ct'] = inprogress_ct
        context['complete_ct'] = complete_ct
        return context


# ACCESS: Any org user should be able to view/create a task associated a series owned
# by their organization
# A user from an organization that is in collaborate_with on a series
# should be able to view/create a task for a series they have access to.
class SeriesTaskView(LoginRequiredMixin, CreateView):
    """Create a series task."""

    # handle users that are not logged in
    login_url = settings.LOGIN_URL

    context_object_name = 'tasks'
    template_name = 'editorial/task_list.html'
    form_class = TaskForm

    def get_form_kwargs(self):
        """Pass organization to form."""

        kw = super(SeriesTaskView, self).get_form_kwargs()
        kw.update({'organization': self.request.user.organization})
        return kw

    def get_context_data(self, **kwargs):
        """Return tasks belonging to the story."""

        context = super(SeriesTaskView, self).get_context_data(**kwargs)
        series = get_object_or_404(Series, id=self.kwargs['pk'])
        tasks = series.task_set.all()
        count = tasks.count()
        identified_ct = series.task_set.filter(status="Identified").count()
        inprogress_ct = series.task_set.filter(status="In Progress").count()
        complete_ct = series.task_set.filter(status="Complete").count()
        # ratio of complete to total number of tasks
        if complete_ct>0:
            progress = 100 * float(complete_ct)/float(count)
        else:
            progress = 0
        context['series'] = series
        context['tasks'] = tasks
        context['progress'] = progress
        context['identified_ct'] = identified_ct
        context['inprogress_ct'] = inprogress_ct
        context['complete_ct'] = complete_ct
        return context


# ACCESS: Any org user should be able to view/create a task associated a story owned
# by their organization
# A user from an organization that is in collaborate_with on a story
# should be able to view/create a task for a story they have access to.
class StoryTaskView(LoginRequiredMixin, CreateView):
    """Create a story task."""

    # handle users that are not logged in
    login_url = settings.LOGIN_URL

    context_object_name = 'tasks'
    template_name = 'editorial/task_list.html'
    form_class = TaskForm

    def get_form_kwargs(self):
        """Pass organization to form."""

        kw = super(StoryTaskView, self).get_form_kwargs()
        kw.update({'organization': self.request.user.organization})
        return kw

    def get_context_data(self, **kwargs):
        """Return tasks belonging to the story."""

        context = super(StoryTaskView, self).get_context_data(**kwargs)
        story = get_object_or_404(Story, id=self.kwargs['pk'])
        tasks = story.task_set.all()
        count = tasks.count()
        identified_ct = story.task_set.filter(status="Identified").count()
        inprogress_ct = story.task_set.filter(status="In Progress").count()
        complete_ct = story.task_set.filter(status="Complete").count()
        # ratio of complete to total number of tasks
        if complete_ct>0:
            progress = 100 * float(complete_ct)/float(count)
        else:
            progress = 0
        context['story'] = story
        context['tasks'] = tasks
        context['progress'] = progress
        context['identified_ct'] = identified_ct
        context['inprogress_ct'] = inprogress_ct
        context['complete_ct'] = complete_ct
        return context



class EventTaskView(LoginRequiredMixin, CreateView):
    """Create event task."""

    # handle users that are not logged in
    login_url = settings.LOGIN_URL

    context_object_name = 'tasks'
    template_name = 'editorial/task_list.html'
    form_class = TaskForm

    def get_form_kwargs(self):
        """Pass organization to form."""

        kw = super(EventTaskView, self).get_form_kwargs()
        kw.update({'organization': self.request.user.organization})
        return kw

    def get_context_data(self, **kwargs):
        """Return tasks belonging to the story."""

        context = super(EventTaskView, self).get_context_data(**kwargs)
        event = get_object_or_404(Event, id=self.kwargs['pk'])
        tasks = event.task_set.all()
        count = tasks.count()
        identified_ct = event.task_set.filter(status="Identified").count()
        inprogress_ct = event.task_set.filter(status="In Progress").count()
        complete_ct = event.task_set.filter(status="Complete").count()
        # ratio of complete to total number of tasks
        if complete_ct>0:
            progress = 100 * float(complete_ct)/float(count)
        else:
            progress = 0
        context['event'] = event
        context['tasks'] = tasks
        context['progress'] = progress
        context['identified_ct'] = identified_ct
        context['inprogress_ct'] = inprogress_ct
        context['complete_ct'] = complete_ct
        return context
