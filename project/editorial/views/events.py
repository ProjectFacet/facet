""" Event views for editorial app.

    editorial/views/eventviews.py
"""

# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import json

from actstream import action
from braces.views import LoginRequiredMixin, FormMessagesMixin
from django.conf import settings
from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponse

from django.core.urlresolvers import reverse
from django.views.generic import UpdateView, CreateView, DeleteView, View
from editorial.forms import (
    EventForm,
    CommentForm,
    NoteForm,
    SimpleImageForm,
    SimpleDocumentForm,
    SimpleImageLibraryAssociateForm,
    SimpleDocumentLibraryAssociateForm,
)

from editorial.models import (
    Organization,
    Project,
    Story,
    Event,
    Discussion,
)


# ----------------------------------------------------------------------#
#   Events Views
# ----------------------------------------------------------------------#

# ACCESS: Any org user, or user from an organization that is in collaborate_with
# should be able to create an event for P, Sr, St, F.
# Contractors should only be able to create events for P, Sr or St they are
# assigned to.
class EventCreateView(LoginRequiredMixin, FormMessagesMixin, CreateView):
    """A logged in user can create a event.

    Events are used to manage information about events.
    Events can either manage events that an organization are hosting
    or events that an organization is reporting on.
    Ex: Hosting = A townhall discussion hosted by an organization
    Ex: Reporting = A press conference at city hall covered for a story.
    Ex. Administrative = An internal event like an org or team meeting.
    Events have a connection to either a Project, Story or Event.
    """

    model = Event
    form_class = EventForm
    template_name = "editorial/events/event_form.html"

    form_invalid_message = "Check the form."
    form_valid_message = "Event created."

    def get_form_kwargs(self):
        """Pass user organization to the form."""

        kw = super(EventCreateView, self).get_form_kwargs()
        kw.update({'organization': self.request.user.organization})
        return kw

    def form_valid(self, form):
        """Save -- but first adding owner and organization."""

        self.object = event = form.save(commit=False)

        # create and set discussion
        discussion = Discussion.objects.create_discussion("EV")
        event.discussion = discussion

        # set user specific values
        event.owner = self.request.user
        event.organization = self.request.user.organization

        event.save()
        form.save_m2m()

        # record action for activity stream
        action.send(self.request.user, verb="created", action_object=event)

        return redirect(self.get_success_url())


# ACCESS: Any org user, or user from an organization that is in collaborate_with
# should be able to edit an event for P, Sr, St, F.
# Contractors should only be able to edit events for P, Sr or St they are
# assigned to.
class EventUpdateView(LoginRequiredMixin, FormMessagesMixin, UpdateView):
    """ The detail page for a event.

    Displays the event information.
    """

    model = Event
    form_class = EventForm
    template_name = "editorial/events/event_form.html"

    form_invalid_message = "Something went wrong. Check the form."
    form_valid_message = "Changes saved."

    def get_form_kwargs(self):
        """Pass organization to form."""

        kw = super(EventUpdateView, self).get_form_kwargs()
        kw.update({'organization': self.request.user.organization, 'event': self.object})
        return kw

    def event_discussion(self):
        """Get discussion, comments and comment form for the event."""

        self.object = self.get_object()
        discussion = self.object.discussion
        comments = discussion.comment_set.all().order_by('date')
        form = CommentForm()
        return {'discussion': discussion, 'comments': comments, 'form': form, }

    def event_notes(self):
        """Get notes and note form for event."""

        self.object = self.get_object()
        notes = self.object.notes.all().order_by('-creation_date')
        form = NoteForm()
        return {'notes': notes, 'form': form}

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

    def get_success_url(self):
        action.send(self.request.user, verb="edited", action_object=self.object)
        return super(EventUpdateView, self).get_success_url()


# ACCESS: Any org user that is an admin or editor should be able to delete an
# event associated with their org, or an org PSS.
class EventDeleteView(LoginRequiredMixin, FormMessagesMixin, DeleteView):
    """View for handling deletion of an event.

    In this project, we expect deletion to be done via a JS pop-up UI; we don't expect to
    actually use the "do you want to delete this?" Django-generated page. However, this is
    available if useful.
    """

    model = Event
    template_name = "editorial/events/event_delete.html"

    form_valid_message = "Deleted."
    form_invalid_message = "Please check form."

    def get_success_url(self):
        """Post-deletion, return to the task parent URL."""

        if self.object.project:
            project = self.object.project
            return reverse('project_event_list', kwargs={'pk': project.id})
        if self.object.story:
            story = self.object.story
            return reverse('story_event_list', kwargs={'pk': story.id})
        if self.object.evt_organization:
            organization = self.object.evt_organization
            return reverse('organization_event_list', kwargs={'pk': organization.id})


# ----------------------------------------------------------------------#
#   Content Event Views
# ----------------------------------------------------------------------#

# ACCESS: Any org user should be able to create an event associated
# with their organization
class OrganizationEventView(LoginRequiredMixin, CreateView):
    """Display all the events associated with an organization.
    """

    context_object_name = 'events'
    template_name = 'editorial/events/event_list.html'
    form_class = EventForm

    def get_form_kwargs(self):
        """Pass organization to form."""

        kw = super(OrganizationEventView, self).get_form_kwargs()
        kw.update({'organization': self.request.user.organization})
        return kw

    def get_context_data(self, **kwargs):
        """Return events belonging to the organization."""

        context = super(OrganizationEventView, self).get_context_data(**kwargs)
        organization = get_object_or_404(Organization, id=self.kwargs['pk'])
        events = organization.event_set.all()
        reporting_ct = organization.event_set.filter(event_type="Reporting").count()
        hosting_ct = organization.event_set.filter(event_type="Hosting").count()
        administrative_ct = organization.event_set.filter(event_type="Administrative").count()
        other_ct = organization.event_set.filter(event_type="Other").count()
        context['organization'] = organization
        context['events'] = events
        context['reporting_ct'] = reporting_ct
        context['hosting_ct'] = hosting_ct
        context['administrative_ct'] = administrative_ct
        context['other_ct'] = other_ct
        return context


# TODO
# class OrganizationEventSchedule(View):
#     """Return JSON of organization event schedule."""
#
#     def get(self, request, *args, **kwargs):
#         org_id = self.kwargs['pk']
#         org = Organization.objects.get(id=org_id)
#         org_event_cal = org.get_org_event_schedule()
#
#         return HttpResponse(json.dumps(org_event_cal), content_type='application/json')


# ACCESS: Any org user should be able to view/create an event associated a project owned
# by their organization
# A user from an organization that is in collaborate_with on a project
# should be able to view/create an event for a project they have access to.
class ProjectEventView(LoginRequiredMixin, CreateView):
    """Display all the events associated with a project.
    """

    context_object_name = 'events'
    template_name = 'editorial/events/event_list.html'
    form_class = EventForm

    def get_form_kwargs(self):
        """Pass organization to form."""

        kw = super(ProjectEventView, self).get_form_kwargs()
        kw.update({'organization': self.request.user.organization})
        return kw

    def get_context_data(self, **kwargs):
        """Return events belonging to the project."""

        context = super(ProjectEventView, self).get_context_data(**kwargs)
        project = get_object_or_404(Project, id=self.kwargs['pk'])
        events = project.event_set.all()
        reporting_ct = project.event_set.filter(event_type="Reporting").count()
        hosting_ct = project.event_set.filter(event_type="Hosting").count()
        administrative_ct = project.event_set.filter(event_type="Administrative").count()
        other_ct = project.event_set.filter(event_type="Other").count()
        context['project'] = project
        context['events'] = events
        context['reporting_ct'] = reporting_ct
        context['hosting_ct'] = hosting_ct
        context['administrative_ct'] = administrative_ct
        context['other_ct'] = other_ct
        return context


class ProjectEventSchedule(View):
    """Return JSON of project event schedule.

    displayed at /project/pk/events/
    """

    def get(self, request, *args, **kwargs):
        project_id = self.kwargs['pk']
        project = Project.objects.get(id=project_id)
        project_event_cal = project.get_project_event_schedule()

        return HttpResponse(json.dumps(project_event_cal), content_type='application/json')


# ACCESS: Any org user should be able to view/create an event associated a story owned
# by their organization
# A user from an organization that is in collaborate_with on a story
# should be able to view/create an event for a story they have access to.
class StoryEventView(LoginRequiredMixin, CreateView):
    """Display all the events associated with a story."""

    context_object_name = 'events'
    template_name = 'editorial/events/event_list.html'
    form_class = EventForm

    def get_form_kwargs(self):
        """Pass organization to form."""

        kw = super(StoryEventView, self).get_form_kwargs()
        kw.update({'organization': self.request.user.organization})
        return kw

    def get_context_data(self, **kwargs):
        """Return events belonging to the project."""

        context = super(StoryEventView, self).get_context_data(**kwargs)
        story = get_object_or_404(Story, id=self.kwargs['pk'])
        events = story.event_set.all()
        reporting_ct = story.event_set.filter(event_type="Reporting").count()
        hosting_ct = story.event_set.filter(event_type="Hosting").count()
        administrative_ct = story.event_set.filter(event_type="Administrative").count()
        other_ct = story.event_set.filter(event_type="Other").count()
        context['story'] = story
        context['events'] = events
        context['reporting_ct'] = reporting_ct
        context['hosting_ct'] = hosting_ct
        context['administrative_ct'] = administrative_ct
        context['other_ct'] = other_ct
        return context


class StoryEventSchedule(View):
    """Return JSON of story event schedule.

    displayed at /story/pk/events/
    """

    def get(self, request, *args, **kwargs):
        story_id = self.kwargs['pk']
        story = Story.objects.get(id=story_id)
        story_event_cal = story.get_story_event_schedule()

        return HttpResponse(json.dumps(story_event_cal), content_type='application/json')
