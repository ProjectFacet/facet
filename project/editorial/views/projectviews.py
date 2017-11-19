""" Project views for editorial app.

    editorial/views/projectviews.py
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
    ProjectForm,
    ProjectCommentForm,
    ProjectNoteForm,
    TaskForm,)

from editorial.models import (
    Project,
    Series,
    Story,
    Task,
    Event,
    Comment,
    Discussion,
    ProjectNote,)

#----------------------------------------------------------------------#
#   Project Views
#----------------------------------------------------------------------#

def project_list(request):
    """ Displays a filterable table of projects.

    Initial display organizes content by project name.
    """

    projects = Project.objects.filter(organization=request.user.organization)

    return render(request, 'editorial/projectlist.html', {'projects': projects})


def project_new(request):
    """ A logged in user can create a project.

    Projects are a large-scale organizational component made up of multiple project and or stories. The primary use
    is as an organization mechanism for large scale complex collaborative projects. Projects can have project, stories,
    assets, notes, discussions, governing documents, calendars and meta information.
    """

    projectform = ProjectForm(request=request)
    if request.method == "POST":
        projectform = ProjectForm(request.POST, request=request)
    if projectform.is_valid():
        project = projectform.save(commit=False)
        project.owner = request.user
        project.organization = request.user.organization
        project.creation_date = timezone.now()
        discussion = Discussion.objects.create_discussion("PRO")
        project.discussion = discussion
        project.save()
        projectform.save_m2m()

        # record action for activity stream
        action.send(request.user, verb="created", action_object=project)

        return redirect('project_detail', pk=project.pk)
    else:
        projectform = ProjectForm(request=request)
    return render(request, 'editorial/projectnew.html', {'projectform': projectform})


def project_detail(request, pk):
    """ The detail page for a project.

    Displays the projects planning notes, discussion, assets, share and collaboration status
    and sensivity status.
    """

    project = get_object_or_404(Project, pk=pk)
    projectnoteform = ProjectNoteForm()
    # taskform = TaskForm(request=request)
    projectnotes = ProjectNote.objects.filter(project=project)[:10]
    projectcommentform = ProjectCommentForm()
    projectcomments = Comment.objects.filter(discussion=project.discussion).order_by('-date')
    project_images = project.get_project_images()
    project_documents = project.get_project_documents()
    project_audio = project.get_project_audio()
    project_video = project.get_project_video()
    project_tasks = project.get_project_tasks()
    project_events = Event.objects.filter(project=project)

    return render(request, 'editorial/projectdetail.html', {
        'project': project,
        'projectnoteform': projectnoteform,
        'projectnotes': projectnotes,
        'projectcomments': projectcomments,
        'projectcommentform': projectcommentform,
        'projectevents': project_events,
        'project_images': project_images,
        'project_documents': project_documents,
        'project_audio': project_audio,
        'project_video': project_video,
        'project_tasks': project_tasks,
        # 'taskform': taskform,
    })


def project_schedule(request, pk):
    """Generate a JSON object containing entries to display on project calendar."""

    project = get_object_or_404(Project, pk=pk)
    project_calendar = Project.get_project_story_events(project)

    return HttpResponse(json.dumps(project_calendar), content_type='application/json')


def project_assets(request, pk):
    """ Return all the assets associated with a project.
    """
    project = get_object_or_404(Project, pk=pk)
    project_images = Project.get_project_images(project)
    project_documents = Project.get_project_documents(project)
    project_audio = Project.get_project_audio(project)
    project_video = Project.get_project_video(project)

    return render(request, 'editorial/project_assets.html', {
        'project': project,
        'images': project_images,
        'documents': project_documents,
        'audio': project_audio,
        'video': project_video,
})


def project_stories(request,pk):
    """Return all stories associated with a project."""

    project = get_object_or_404(Project, pk=pk)

    return render(request, 'editorial/project_stories.html', {
        'project': project,
    })

def project_events(request,pk):
    """Return all events all types associated with a project."""


    project = get_object_or_404(Project, pk=pk)
    events = Events.objects.filter(project=project)

    return render(request, 'editorial/project_events.html', {
        'project': project,
        'events': events,
    })



def project_edit(request, pk):
    """ Edit project page."""

    project = get_object_or_404(Project, pk=pk)

    if request.method =="POST":
        projectform = ProjectForm(data=request.POST, instance=project, request=request)
        if projectform.is_valid():
            projectform.save()

            # record action for activity stream
            action.send(request.user, verb="edited", action_object=project)

            return redirect('project_detail', pk=project.id)
    else:
        projectform = ProjectForm(instance=project, request=request)

    return render(request, 'editorial/projectedit.html', {
        'project': project,
        'projectform': projectform,
        })


def project_delete(request, pk):
    """Delete a project and its related objects then redirect user to project list."""

    if request.method == "POST":
        project = get_object_or_404(Project, pk=pk)
        project.delete()

    return redirect('project_list')
