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
from django.views.generic import TemplateView , UpdateView, DetailView
from django.views.decorators.csrf import csrf_exempt
import datetime
import json
from actstream import action

from editorial.forms import (
    TaskForm,
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

# class TaskCreateView(generic.CreateView):
#     """Create a new task."""
#
#     model = Task
#     form_class = TaskForm
#
#     def form_valid(self, form):
#         form.instance.owner = self.request.user
#         return super(OrganizationCreateView, self).form_valid(form)
#
#     def get_success_url(self):
#
#         self.request.user.organization = self.object
#         self.request.user.save()
#         return reverse('task', kwargs={'pk': self.object.pk})

# function based view version
def task_new(request):
    """A logged in user can create a task.

    Tasks are actionable items containing information about something to be done.
    Tasks have a title, text, an assigned team and a connection to either a Project,
    Series, Story or Event.
    """

    form = TaskForm(request=request)
    if request.method == "POST":
        form = TaskForm(request.POST, request=request)
    if form.is_valid():
        task = form.save(commit=False)
        task.owner = request.user
        task.organization = request.user.organization
        task.creation_date = timezone.now()
        task.save()
        form.save_m2m()

        # record action for activity stream
        action.send(request.user, verb="created", action_object=task)

        return redirect('task_detail', pk=task.pk)
    else:
        form = TaskForm(request=request)
    return render(request, 'editorial/task_detail.html', {'form': form})


def task_detail(request, pk):
    """ The detail page for a task.

    Displays the tasks information.
    """

    # FIXME q for J: Having a hard time figuring out how to translate this try except view to cbv

    try:
        task = get_object_or_404(Task, pk=pk)
        form = TaskForm(request=request, instance=task)
        # discussion = ...
        # comments = ...

        if request.method == "POST":
            if 'form' in request.POST:
                form = TaskForm(data=request.POST, instance=task, request=request)
                if form.is_valid():
                    form.save()
                    # record action for activity stream
                    action.send(request.user, verb="updated", action_object=task)
                    return redirect('task_detail', pk=pk)

    except:
        # except Task.DoesNotExist:
        #display form a save a new task
        if request.method == "POST":
            if 'form' in request.POST:
                form=TaskForm(data=request.POST, request=request)
                if form.is_valid():
                    task = form.save(commit=False)
                    task.owner = request.user
                    task.organization = request.user.organization
                    task.creation_date = timezone.now()
                    task.save()
                    form.save_m2m()
                    # record action for activity stream
                    action.send(request.user, verb="created", action_object=task)
                    return redirect('task_detail', pk=task.pk)

    return render(request, 'editorial/task_detail.html', {
        'task': task,
        'form': form,
    })


# reduce duplication if possible
def project_task_list(request, pk):
    """Display all the tasks associated with a project.

    """

    project = get_object_or_404(Project, pk=pk)
    tasks = Task.objects.filter(project=pk)
    count = tasks.count()
    # FIXME how to get count for each status without doing three filters
    identified_ct = Task.objects.filter(project=pk, status="Identified").count()
    inprogress_ct = Task.objects.filter(project=pk, status="In Progress").count()
    complete_ct = Task.objects.filter(project=pk, status="Complete").count()
    # ratio of complete to total number of tasks
    progress = 100 * float(complete_ct)/float(count)
    return render(request, 'editorial/task_list.html', {
        'project': project,
        'project_tasks': tasks,
        'progress': progress,
        'identified_ct': identified_ct,
        'inprogress_ct': inprogress_ct,
        'complete_ct': complete_ct,
    })

def series_task_list(request, pk):
    """Display all the tasks associated with a story.

    """

    series = get_object_or_404(Series, pk=pk)
    tasks = Task.objects.filter(series=pk)
    count = tasks.count()
    # FIXME how to get count for each status without doing three of the following
    identified_ct = Task.objects.filter(series=pk, status="Identified").count()
    inprogress_ct = Task.objects.filter(series=pk, status="In Progress").count()
    complete_ct = Task.objects.filter(series=pk, status="Complete").count()
    # ratio of complete to total number of tasks
    progress = 100 * float(complete_ct)/float(count)
    return render(request, 'editorial/task_list.html', {
        'series': series,
        'series_tasks': tasks,
        'progress': progress,
        'identified_ct': identified_ct,
        'inprogress_ct': inprogress_ct,
        'complete_ct': complete_ct,
    })

def story_task_list(request, pk):
    """Display all the tasks associated with a series.

    """

    story = get_object_or_404(Story, pk=pk)
    tasks = Task.objects.filter(story=pk)
    count = tasks.count()
    # FIXME how to get count for each status without doing three of the following
    identified_ct = Task.objects.filter(story=pk, status="Identified").count()
    inprogress_ct = Task.objects.filter(story=pk, status="In Progress").count()
    complete_ct = Task.objects.filter(story=pk, status="Complete").count()
    # ratio of complete to total number of tasks
    progress = 100 * float(complete_ct)/float(count)
    return render(request, 'editorial/task_list.html', {
        'story': story,
        'story_tasks': tasks,
        'progress': progress,
        'identified_ct': identified_ct,
        'inprogress_ct': inprogress_ct,
        'complete_ct': complete_ct,
    })

def event_task_list(request, pk):
    """Display all the tasks associated with an event.

    """

    event = get_object_or_404(Event, pk=pk)
    tasks = Task.objects.filter(event=pk)
    count = tasks.count()
    # FIXME how to get count for each status without doing three of the following
    identified_ct = Task.objects.filter(event=pk, status="Identified").count()
    inprogress_ct = Task.objects.filter(event=pk, status="In Progress").count()
    complete_ct = Task.objects.filter(event=pk, status="Complete").count()
    # ratio of complete to total number of tasks
    progress = 100 * float(complete_ct)/float(count)
    return render(request, 'editorial/task_list.html', {
        'event': event,
        'event_tasks': tasks,
        'progress': progress,
        'identified_ct': identified_ct,
        'inprogress_ct': inprogress_ct,
        'complete_ct': complete_ct,
    })


def task_delete(request, pk):
    """Delete a project and its related objects then redirect user to project list."""

    pass
