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
#   Project Views
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
        taskform.save_m2m()

        # record action for activity stream
        action.send(request.user, verb="created", action_object=task)

        return redirect('task_detail', pk=project.pk)
    else:
        form = TaskForm(request=request)
    return render(request, 'editorial/task_form.html', {'form': form})


def task_detail(request, pk):
    """ The detail page for a task.

    Displays the tasks information.
    """

    task = get_object_or_404(Task, pk=pk)

    return render(request, 'editorial/task_form.html', {
        'task': task,
    })


def task_edit(request, pk):
    """ Edit project page."""

    pass
    # project = get_object_or_404(Project, pk=pk)
    #
    # if request.method =="POST":
    #     projectform = ProjectForm(data=request.POST, instance=project, request=request)
    #     if projectform.is_valid():
    #         projectform.save()
    #
    #         # record action for activity stream
    #         action.send(request.user, verb="edited", action_object=project)
    #
    #         return redirect('project_detail', pk=project.id)
    # else:
    #     projectform = ProjectForm(instance=project, request=request)
    #
    # return render(request, 'editorial/projectedit.html', {
    #     'project': project,
    #     'projectform': projectform,
    #     })


def task_delete(request, pk):
    """Delete a project and its related objects then redirect user to project list."""

    pass
