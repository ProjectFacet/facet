""" Project views for editorial app.

    editorial/views/projectviews.py
"""

# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import json

from actstream import action
from braces.views import LoginRequiredMixin, FormMessagesMixin
from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import TemplateView, UpdateView, DetailView, ListView, CreateView, DeleteView, FormView, View

from editorial.forms import (
    ProjectForm,
    ProjectTeamForm,
    CommentForm,
    NoteForm,
    TaskForm,
    EventForm,
    SimpleImageForm,
    SimpleDocumentForm,
    SimpleImageLibraryAssociateForm,
    SimpleDocumentLibraryAssociateForm,
)

from editorial.models import (
    Project,
    Discussion,
    # ProjectNote,
)


# ----------------------------------------------------------------------#
#   Project Views
# ----------------------------------------------------------------------#

# Project Notes are created and edited in noteviews

# ACCESS: Any org user should be able to see a list of projects for their org
class ProjectListView(LoginRequiredMixin, ListView):
    """ Displays a filterable table of projects.

    Initial display organizes content by project name.
    """

    context_object_name = 'projects'
    template_name = 'editorial/projects/project_list.html'

    def get_queryset(self):
        """Return projects belonging to the organization."""

        # FIXME exclude sensitive unless user is owner or a member of the team
        org = self.request.user.organization

        return org.project_organization.all()


# ACCESS: Any org user should be able to create a project for their org.
class ProjectCreateView(LoginRequiredMixin, FormMessagesMixin, CreateView):
    """A logged in user with an organization can create a project.

    Projects are a large-scale organizational component made up of multiple project and or
    stories. The primary use is as an organization mechanism for large scale complex
    collaborative projects. Projects can have project, stories, assets, notes, discussions,
    governing documents, calendars and meta information.
    """

    model = Project
    form_class = ProjectForm
    template_name = 'editorial/projects/project_form.html'

    form_invalid_message = "Check the form."
    form_valid_message = "Project created."

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


# ACCESS: Any org user should be able to update details for a project belonging to their org
class ProjectUpdateView(LoginRequiredMixin, FormMessagesMixin, UpdateView):
    """Update a project."""

    model = Project
    form_class = ProjectForm

    template_name = 'editorial/projects/project_form.html'

    form_invalid_message = "Something went wrong. Check the form."
    form_valid_message = "Changes saved."

    def get_form_kwargs(self):
        """Pass user organization to the form."""

        kw = super(ProjectUpdateView, self).get_form_kwargs()
        kw.update({'organization': self.request.user.organization, 'project': self.object})
        return kw

    def get_success_url(self):
        """Record action for activity stream."""

        action.send(self.request.user, verb="edited", action_object=self.object)
        return super(ProjectUpdateView, self).get_success_url()


# ACCESS: Any org user, or user from an organization that is in collaborate_with
# for a project should be able to view the project detail.
# Contractors should only be able to do so for projects that they have access to
# That should be handled by limiting which project they have access to.
class ProjectDetailView(LoginRequiredMixin, DetailView):
    """ The detail page for a project.

    Displays the projects planning notes, discussion, assets, share and collaboration status
    and sensitivity status.
    """

    model = Project

    template_name = 'editorial/projects/project_detail.html'

    def get_form_kwargs(self):
        """Pass organization to form."""

        kw = super(ProjectDetailView, self).get_form_kwargs()
        kw.update({'organization': self.request.user.organization})
        return kw

    def stories(self):
        """Get all project stories."""
        return self.object.get_project_stories()

    def project_assets(self):
        """Get all the assets associated with a project through story facets."""

        images = self.object.get_project_images()
        documents = self.object.get_project_documents()
        audio = self.object.get_project_audio()
        video = self.object.get_project_video()

        return {'images': images, 'documents': documents, 'audio': audio, 'video': video}

    def project_discussion(self):
        """Get discussion, comments and comment form for the project."""

        discussion = self.object.discussion
        comments = discussion.comment_set.all().order_by('date')
        form = CommentForm()

        return {'discussion': discussion, 'comments': comments, 'form': form}

    def project_notes(self):
        """Get notes and note form for the project."""

        notes = self.object.notes.all().order_by('-creation_date')
        form = NoteForm()

        return {'notes': notes, 'form': form}

    def project_tasks(self):
        """Get tasks and task form for the project."""

        tasks = self.object.task_set.all()
        identified = self.object.task_set.filter(status="Identified")
        inprogress = self.object.task_set.filter(status="In Progress")
        complete = self.object.task_set.filter(status="Complete")
        identified_ct = identified.count()
        inprogress_ct = inprogress.count()
        complete_ct = complete.count()
        form = TaskForm(organization=self.request.user.organization)

        return {
            'tasks': tasks,
            'identified': identified,
            'inprogress': inprogress,
            'complete': complete,
            'identified_ct': identified_ct,
            'inprogress_ct': inprogress_ct,
            'complete_ct': complete_ct,
            'form': form,
        }

    def project_events(self):
        """Get events and event form for the project."""

        events = self.object.event_set.all().order_by('-event_date')
        form = EventForm(organization=self.request.user.organization)

        return {'events': events, 'form': form}

    def simple_images(self):
        """Return simple images."""

        images = self.object.simple_image_assets.all()
        form = SimpleImageForm()
        addform = SimpleImageLibraryAssociateForm(organization=self.request.user.organization)
        return {'images': images, 'form': form, 'addform': addform,}

    def simple_documents(self):
        """Return simple documents."""

        documents = self.object.simple_document_assets.all()
        form = SimpleDocumentForm()
        addform = SimpleDocumentLibraryAssociateForm(organization=self.request.user.organization)
        return {'documents': documents, 'form': form, 'addform': addform,}


class ProjectTeamUpdateView(LoginRequiredMixin, FormMessagesMixin, UpdateView):
    """Process project team form."""

    model = Project
    template_name = 'editorial/projects/projectteam_form.html'
    form_class = ProjectTeamForm
    form_valid_message = "Project team updated."
    form_invalid_message = "Something went wrong. Please check the form."

    def get_form_kwargs(self):
        kw = super(ProjectTeamUpdateView, self).get_form_kwargs()
        project = Project.objects.get(id=self.kwargs['pk'])
        kw.update({'organization': self.request.user.organization, 'project': project})
        return kw

    def project_details(self):
        """Get project object to display information."""

        project = Project.objects.get(id=self.kwargs['pk'])
        return project

    def form_valid(self, form):
        """Handle submission of form."""

        project = Project.objects.get(id=self.kwargs['pk'])
        team_list = form.cleaned_data['team']
        print team_list
        project.team = team_list
        project.save()

        return redirect('project_detail', pk=project.id)


# ACCESS: Any org user, or user from an organization that is in collaborate_with
# for a project should be able to view the project asset library.
# Contractors should only be able to do so for project that they have access to
# That should be handled by limiting which project they have access to.
class ProjectAssetTemplateView(LoginRequiredMixin, TemplateView):
    """Display media associated with a project."""

    template_name = 'editorial/projects/project_assets.html'

    def get_context_data(self, pk):
        """Return all the (complex) assets associated with a project."""

        project = get_object_or_404(Project, id=pk)
        images = project.get_project_images()
        documents = project.get_project_documents()
        audio = project.get_project_audio()
        video = project.get_project_video()

        return {
            'project': project,
            'images': images,
            'documents': documents,
            'audio': audio,
            'video': video,
        }


# ACCESS: Any org user, or user from an organization that is in collaborate_with
# for a project should be able to view the project stories.
# Contractors should only be able to do so for project that they have access to
# That should be handled by limiting which project they have access to.
class ProjectStoryTemplateView(LoginRequiredMixin, TemplateView):
    """Return and display all the stories associated with a project."""

    template_name = 'editorial/projects/project_stories.html'

    def get_context_data(self, pk):
        """Return all the stories."""

        project = get_object_or_404(Project, id=pk)
        stories = project.get_project_stories()

        # For each story, use the first image (if any) as the "featured image"

        for story in stories:
            images = story.get_story_images()
            if images:
                story.featured_image = images[0]

        return {'project': project, 'stories': stories}


# ACCESS: Only an org admin should be able to delete a project owned by that org
class ProjectDeleteView(LoginRequiredMixin, FormMessagesMixin, DeleteView):
    """Delete a project and it's associated notes.

    Stories and media should not be deleted.

    In this project, we expect deletion to be done via a JS pop-up UI; we don't expect to
    actually use the "do you want to delete this?" Django-generated page. However, this is
    available if useful.
    """

    model = Project
    template_name = "editorial/projects/project_delete.html'"

    form_valid_message = "Deleted."
    form_invalid_message = "Please check form."

    def get_success_url(self):
        """Post-deletion, return to the project list."""

        return reverse('project_list')


class ProjectSchedule(View):
    """Return JSON of project schedule information."""

    def get(self, request, *args, **kwargs):
        project_id = self.kwargs['pk']
        project = Project.objects.get(id=project_id)
        project_calendar = project.get_project_schedule()

        return HttpResponse(json.dumps(project_calendar), content_type='application/json')
