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
from django.views.generic import TemplateView , UpdateView, DetailView, CreateView, ListView
from django.views.decorators.csrf import csrf_exempt
import datetime
import json
from actstream import action

from editorial.forms import (
    TaskForm,
    CommentForm,
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
#   Task Views
#----------------------------------------------------------------------#

class TaskCreateView(CreateView):
    """Create a new task."""

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


class TaskUpdateView(UpdateView):
    """The detail page for a task.
    Displays the task information."""

    model = Task
    form_class = TaskForm

    def get_form_kwargs(self):
        """Pass organization to form."""

        kw = super(TaskUpdateView, self).get_form_kwargs()
        kw.update({'organization': self.request.user.organization})
        return kw

    def task_discussion(self):
        """Get discussion, comments and comment form for the task."""

        self.object = self.get_object()
        discussion = self.object.discussion
        comments = discussion.comment_set.all()
        form = TaskCommentForm()
        return {'discussion': discussion, 'comments': comments, 'form': form,}

    def get_success_url(self):

        action.send(self.request.user, verb="edited", action_object=self.object)
        return super(TaskUpdateView, self).get_success_url()


def task_delete(request, pk):
    """Delete a task and its related objects."""
    pass


# FIXME form challenges
class ProjectTaskTemplateView(TemplateView):

    context_object_name = 'tasks'
    template_name = 'editorial/task_list.html'
    # form_class = TaskForm
    #
    # def get_form_kwargs(self):
    #     """Pass organization to form."""
    #
    #     kw = super(ProjectTaskTemplateView, self).get_form_kwargs()
    #     kw.update({'organization': self.request.user.organization})
    #     return kw


    def get_context_data(self, pk):
        """Return tasks belonging to the project."""

        project = get_object_or_404(Project, id=pk)
        # form = TaskForm()
        tasks = project.task_set.all()
        count = tasks.count()
        identified_ct=0
        inprogress_ct=0
        complete_ct=0
        for task in tasks:
            if task.status=='Identified':
                identified_ct = identified_ct + 1
            elif task.status=='In Progress':
                inprogress_ct = inprogress_ct + 1
            elif task.status=='Complete':
                complete_ct = complete_ct + 1

        # ratio of complete to total number of tasks
        if complete_ct>0:
            progress = 100 * float(complete_ct)/float(count)
        else:
            progress = 0
        return {
            'project': project,
            'tasks': tasks,
            # 'form': form,
            'progress': progress,
            'identified_ct': identified_ct,
            'inprogress_ct' : inprogress_ct,
            'complete_ct': complete_ct,
        }


# FIXME form challenges
class SeriesTaskTemplateView(TemplateView):

    context_object_name = 'tasks'
    template_name = 'editorial/task_list.html'
    # form_class = TaskForm
    #
    # def get_form_kwargs(self):
    #     """Pass organization to form."""
    #
    #     kw = super(SeriesTaskTemplateView, self).get_form_kwargs()
    #     kw.update({'organization': self.request.user.organization})
    #     return kw


    def get_context_data(self, pk):
        """Return tasks belonging to the series."""

        series = get_object_or_404(Series, id=pk)
        # form = TaskForm()
        tasks = series.task_set.all()
        count = tasks.count()
        identified_ct=0
        inprogress_ct=0
        complete_ct=0
        for task in tasks:
            if task.status=='Identified':
                identified_ct = identified_ct + 1
            elif task.status=='In Progress':
                inprogress_ct = inprogress_ct + 1
            elif task.status=='Complete':
                complete_ct = complete_ct + 1
        # ratio of complete to total number of tasks
        if complete_ct>0:
            progress = 100 * float(complete_ct)/float(count)
        else:
            progress = 0
        return {
            'series': series,
            'tasks': tasks,
            # 'form': form,
            'progress': progress,
            'identified_ct': identified_ct,
            'inprogress_ct' : inprogress_ct,
            'complete_ct': complete_ct,
        }


# FIXME form challenges
class StoryTaskTemplateView(TemplateView):

    context_object_name = 'tasks'
    template_name = 'editorial/task_list.html'
    # form_class = TaskForm
    #
    # def get_form_kwargs(self):
    #     """Pass organization to form."""
    #
    #     kw = super(StoryTaskTemplateView, self).get_form_kwargs()
    #     kw.update({'organization': self.request.user.organization})
    #     return kw


    def get_context_data(self, pk):
        """Return tasks belonging to the story."""

        story = get_object_or_404(Story, id=pk)
        tasks = story.task_set.all()
        count = tasks.count()
        identified_ct=0
        inprogress_ct=0
        complete_ct=0
        for task in tasks:
            if task.status=='Identified':
                identified_ct = identified_ct + 1
            elif task.status=='In Progress':
                inprogress_ct = inprogress_ct + 1
            elif task.status=='Complete':
                complete_ct = complete_ct + 1
        # ratio of complete to total number of tasks
        if complete_ct>0:
            progress = 100 * float(complete_ct)/float(count)
        else:
            progress = 0
        return {
            'story': story,
            'tasks': tasks,
            'progress': progress,
            'identified_ct': identified_ct,
            'inprogress_ct' : inprogress_ct,
            'complete_ct': complete_ct,
        }


# FIXME form challenges
class EventTaskTemplateView(TemplateView):

    context_object_name = 'tasks'
    template_name = 'editorial/task_list.html'
    # form_class = TaskForm
    #
    # def get_form_kwargs(self):
    #     """Pass organization to form."""
    #
    #     kw = super(EventTaskTemplateView, self).get_form_kwargs()
    #     kw.update({'organization': self.request.user.organization})
    #     return kw


    def get_context_data(self, pk):
        """Return tasks belonging to the event."""

        event = get_object_or_404(Event, id=pk)
        # form = TaskForm()
        tasks = event.task_set.all()
        count = tasks.count()
        identified_ct=0
        inprogress_ct=0
        complete_ct=0
        for task in tasks:
            if task.status=='Identified':
                identified_ct = identified_ct + 1
            elif task.status=='In Progress':
                inprogress_ct = inprogress_ct + 1
            elif task.status=='Complete':
                complete_ct = complete_ct + 1
        # ratio of complete to total number of tasks
        if complete_ct>0:
            progress = 100 * float(complete_ct)/float(count)
        else:
            progress = 0
        return {
            'event': event,
            'tasks': tasks,
            # 'form': form,
            'progress': progress,
            'identified_ct': identified_ct,
            'inprogress_ct' : inprogress_ct,
            'complete_ct': complete_ct,
        }
