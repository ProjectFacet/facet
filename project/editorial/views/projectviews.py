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
from django.views.generic import TemplateView , UpdateView, DetailView, ListView, CreateView
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

# Project Notes are created and edited in noteviews


class ProjectListView(ListView):
    """ Displays a filterable table of projects.

    Initial display organizes content by project name.
    """

    context_object_name = 'projects'

    def get_queryset(self):
        """Return projects belonging to the organization."""

        org = self.request.user.organization

        return org.project_organization.all()


class ProjectCreateView(CreateView):
    """ A logged in user with an organization can create a project.

    Projects are a large-scale organizational component made up of multiple project and or stories. The primary use
    is as an organization mechanism for large scale complex collaborative projects. Projects can have project, stories,
    assets, notes, discussions, governing documents, calendars and meta information.
    """

    model = Project
    form_class = ProjectForm

    def get_form_kwargs(self):
        """Pass user organization to the form."""

        kw = super(ProjectCreateView, self).get_form_kwargs()
        kw.update({'organization': self.request.user.organization})
        return kw

    def form_valid(self, form):
        """Save -- but first adding owner and organization."""

        self.object = project = form.save(commit=False)

        # create and set discussion
        discussion = Discussion.objects.create_discussion("PRO")
        project.discussion = discussion

        # set user specific values
        project.owner = self.request.user
        project.organization = self.request.user.organization

        project.save()
        form.save_m2m()

        # record action for activity stream
        action.send(self.request.user, verb="created", action_object=project)

        return redirect(self.get_success_url())


class ProjectUpdateView(UpdateView):
    """Update a project."""

    model = Project
    form_class = ProjectForm

    def get_form_kwargs(self):
        """Pass user organization to the form."""

        kw = super(ProjectUpdateView, self).get_form_kwargs()
        kw.update({'organization': self.request.user.organization})
        return kw

    def get_success_url(self):
        """Record action for activity stream."""

        action.send(self.request.user, verb="edited", action_object=self.object)
        return super(ProjectUpdateView, self).get_success_url()


class ProjectDetailView(DetailView):
    """ The detail page for a project.

    Displays the projects planning notes, discussion, assets, share and collaboration status
    and sensivity status.
    """

    model = Project

    def get_form_kwargs(self):
        """Pass organization to form."""

        kw = super(ProjectDetailView, self).get_form_kwargs()
        kw.update({'organization': self.request.user.organization})
        return kw


    def stories(self):
        """Get all project stories."""

        self.object = self.get_object()
        return self.get_project_stories()


    def project_assets(self):
        """Get all the assets associated with a project through story facets."""

        self.object = self.get_object()
        images = self.object.get_project_images()
        documents = self.object.get_project_documents()
        audio = self.object.get_project_audio()
        video = self.object.get_project_video()
        return {'images': images, 'documents': documents, 'audio': audio, 'video': video,}


    def project_discussion(self):
        """Get discussion, comments and comment form for the project."""

        self.object = self.get_object()
        discussion = self.object.discussion
        comments = discussion.comment_set.all()
        form = ProjectCommentForm()
        return {'discussion': discussion, 'comments': comments, 'form': form}


    # FIXME Currently causing error because org is not getting passed to EventForm
    # Commented out task form and version of return statement that uses it.
    def project_notes(self):
        """Get notes and note form for the project."""

        self.object = self.get_object()
        notes = self.object.projectnote.all()
        form = ProjectNoteForm()
        return {'notes': notes, 'form': form,}


    # FIXME Currently causing error because org is not getting passed to EventForm
    # Commented out task form and version of return statement that uses it.
    def project_tasks(self):
        """Get tasks and task form for the project."""

        self.object = self.get_object()
        tasks = self.object.task_set.all()
        # form = TaskForm()
        # return {'tasks': tasks, 'form': form}
        return {'tasks': tasks}


    def project_events(self):
        """Get events and event form for the project."""

        self.object = self.get_object()
        events = self.object.event_set.all()
        # form = EventForm()
        # return {'events': events, 'form': form}
        return {'events': events}


class ProjectAssetTemplateView(TemplateView):
    """Display media associated with a project."""

    template_name = 'editorial/project_assets.html'

    def get_context_data(self, pk):
        """Return all the (complex) assets associated with a project."""

        project = get_object_or_404(Project, id=pk)
        images = project.get_project_images()
        documents = project.get_project_documents()
        audio = project.get_project_audio()
        video = project.get_project_video()
        return {'project':project, 'images': images, 'documents': documents, 'audio': audio, 'video': video,}


class ProjectStoryTemplateView(TemplateView):
    """Return and display all the stories associated with a project."""

    template_name = 'editorial/project_stories.html'

    def get_context_data(self, pk):
        """Return all the stories."""

        project = get_object_or_404(Project, id=pk)
        stories = project.get_project_stories()
        for story in stories:
            if story.get_story_images():
                story.featured_image = story.get_story_images()[0]
        return {'project': project, 'stories': stories,}


def project_schedule(request, pk):
    """Generate a JSON object containing entries to display on project calendar."""

    project = get_object_or_404(Project, pk=pk)
    project_calendar = Project.get_project_story_events(project)

    return HttpResponse(json.dumps(project_calendar), content_type='application/json')


def project_delete(request, pk):
    """Delete a project and its related objects then redirect user to project list."""

    if request.method == "POST":
        project = get_object_or_404(Project, pk=pk)
        project.delete()

    return redirect('project_list')
