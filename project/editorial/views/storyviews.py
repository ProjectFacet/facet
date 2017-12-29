""" Story views for editorial app.

    editorial/views/storyviews.py
"""

# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponse
from django.core.urlresolvers import reverse_lazy, reverse
from django.utils import timezone
from django.views.generic import TemplateView , UpdateView, DetailView, CreateView, ListView, DeleteView
from django.views.decorators.csrf import csrf_exempt
import datetime
import json
from actstream import action

from editorial.forms import (
    StoryForm,
    FacetPreCreateForm,
    get_facet_form_for_template,
    ImageAssetForm,
    DocumentAssetForm,
    AudioAssetForm,
    VideoAssetForm,
    TaskForm,
    EventForm,
    CommentForm,
    NoteForm,
    )

from editorial.models import (
    Organization,
    Series,
    Story,
    Facet,
    Task,
    Event,
    ImageAsset,
    DocumentAsset,
    AudioAsset,
    VideoAsset,
    Comment,
    Discussion,
    Note,
    )


#----------------------------------------------------------------------#
#   Story Views
#----------------------------------------------------------------------#

class StoryListView(ListView):
    """ Displays a filterable table of stories.

    Initial display organizes content by story>facet>est. run date
    Filterable by story name, facet type, facet name, due for edit, est. run date, credit,
    editor, status.
    """

    context_object_name = 'stories'

    def get_queryset(self):
        """Return stories belonging to the organization."""
        org = self.request.user.organization
        # print "STORY STORY STORY: ", stories
        return org.story_set.all()


class StoryCreateView(CreateView):
    """Create a story."""

    model = Story
    form_class = StoryForm

    def get_form_kwargs(self):
        """Pass current user organization to the form."""

        kw = super(StoryCreateView, self).get_form_kwargs()
        kw.update({'organization': self.request.user.organization})
        return kw

    def org_partners(self):
        """Get list of networks for the current user."""

        return self.request.user.organization.get_org_networks()

    def series(self):
        return Series.objects.filter(organization=self.request.user.organization)

    def projects(self):
        return self.request.user.organization.get_org_projects()

    def form_valid(self, form):
        """Save -- but first adding owner and organization."""

        self.object = story = form.save(commit=False)

        discussion = Discussion.objects.create_discussion("STO")
        story.discussion = discussion

        story.owner = self.request.user
        story.organization = self.request.user.organization

        story.save()
        form.save_m2m()

        action.send(self.request.user, verb="created", action_object=self.object)

        return redirect(self.get_success_url())


class StoryUpdateView(UpdateView):
    """Update a story."""

    model = Story
    form_class = StoryForm

    def get_form_kwargs(self):
        """Pass current user organization to the form."""

        kw = super(StoryUpdateView, self).get_form_kwargs()
        kw.update({'organization': self.request.user.organization})
        return kw

    def org_partners(self):
        """Get list of networks for the current user."""

        return self.request.user.organization.get_org_networks()

    def get_success_url(self):
        """Record action for activity stream."""

        action.send(self.request.user, verb="edited", action_object=self.object)
        return super(StoryUpdateView, self).get_success_url()


class StoryDetailView(DetailView):
    """Show all the details and related items for a story."""

    model = Story

    def get_form_kwargs(self):
        """Pass organization to forms."""

        kw = super(StoryDetailView, self).get_form_kwargs()
        kw.update({'organization': self.request.user.organization})
        return kw


    def facets(self):
        """Get all story facets"""

        self.object = self.get_object()
        return self.object.get_story_facets()


    def story_discussion(self):
        """Get discussion, comments and comment form for the story."""

        self.object = self.get_object()
        discussion = self.object.discussion
        comments = discussion.comment_set.all()
        form = CommentForm()
        return {'discussion': discussion, 'comments': comments, 'form': form}


    def story_notes(self):
        """Get notes and note form for the story."""

        self.object = self.get_object()
        notes = self.object.notes.all().order_by('-creation_date')
        form = NoteForm()
        return {'notes': notes, 'form': form}


    # FIXME Currently causing error because org is not getting passed to TaskForm
    # Commented out task form and version of return statement that uses it.
    def story_tasks(self):
        """Get tasks and task form for the story."""

        self.object = self.get_object()
        org = self.request.user.organization
        tasks = self.object.task_set.all()
        # form = TaskForm()
        # return {'tasks': tasks, 'form': form}
        return {'tasks': tasks}


    # FIXME Currently causing error because org is not getting passed to EventForm
    # Commented out task form and version of return statement that uses it.
    def story_events(self):
        """Get events and event form for the story."""

        self.object = self.get_object()
        events = self.object.event_set.all()
        # form = EventForm()
        # return {'events': events, 'form': form}
        return {'events': events}


    def story_assets(self):
        """Return all the assets associated with a story."""

        self.object = self.get_object()
        images = self.object.get_story_images()
        documents = self.object.get_story_documents()
        audio = self.object.get_story_audio()
        video = self.object.get_story_video()
        return {'images': images, 'documents': documents, 'audio': audio, 'video': video,}


# class StoryDeleteView(DeleteView, FormMessagesMixin):
class StoryDeleteView(DeleteView):
    """Delete a story and it's associated items.

    In this project, we expect deletion to be done via a JS pop-up UI; we don't expect to
    actually use the "do you want to delete this?" Django-generated page. However, this is
    available if useful.
    """

    # FIXME: this would be a great place to use braces' messages; usage commented out for now

    model = Story
    template_name = "editorial/story_delete.html'"

    # form_valid_message = "Deleted."
    # form_invalid_message = "Please check form."

    def get_success_url(self):
        """Post-deletion, return to the story list."""

        return reverse('story_list')


def story_team_options_json(request, pk):
    """Returns JSON of team members that can be assigned to a story."""

    story = get_object_or_404(Story, pk=pk)
    print story

    team = Story.get_story_team(story)
    story_team = {}
    for item in team:
        story_team[item.id]=item.credit_name
    print story_team
    return HttpResponse(json.dumps(story_team), content_type = "application/json")


def story_schedule(request, pk):
    """Generate a JSON object containing entries to display on project calendar."""

    story = get_object_or_404(Story, pk=pk)
    story_calendar = story.get_story_events()
    # FIXME [<Event: Tour of Lab>] is not JSON serializable

    return HttpResponse(json.dumps(story_calendar), content_type='application/json')
