""" Story views for editorial app.

    editorial/views/storyviews.py
"""

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from actstream import action
from braces.views import LoginRequiredMixin, FormMessagesMixin
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import UpdateView, DetailView, CreateView, ListView, \
    DeleteView, View

from editorial.forms import (
    StoryForm,
    CommentForm,
    NoteForm,
    TaskForm,
    EventForm,
)

from editorial.models import (
    Series,
    Story,
    Discussion,
    User)

from editorial.views import CustomUserTest


# ----------------------------------------------------------------------#
#   Story Views
# ----------------------------------------------------------------------#

# ACCESS: Any user should be able to see their org's stories
class StoryListView(CustomUserTest, ListView):
    """ Displays a filterable table of stories.

    Initial display organizes content by story>facet>est. run date
    Filterable by story name, facet type, facet name, due for edit, est. run date, credit,
    editor, status.
    """

    # TODO from Joel: it can be finicky to have views like this that show "your stuff";
    # often better is to get that in the URL -- so, /orgs/1/stories, rather than
    # /stores. Then, Django admins can visit the URL to see stories for that user, rather
    # than only for themselves.

    context_object_name = 'stories'

    def test_user(self, user):
        """User must be member of an org."""

        if user.organization:
            return True

        raise PermissionDenied()

    def get_queryset(self):
        """Return stories belonging to the organization."""
        org = self.request.user.organization
        # print "STORY STORY STORY: ", stories
        return org.story_set.all()


# ACCESS: Any org user should be able to create a story for their org.
# Any user of an org that's part of collaborate_with on a project or series should
# be able to create a story for that project or series.
# Future: A contractor with access to a project or series should be able to create
# a story for that project or series.
class StoryCreateView(CustomUserTest, FormMessagesMixin, CreateView):
    """Create a story."""

    # TODO From Joel: see note above; make this /orgs/1/stories/new, so the URL is bound
    # to the org, rather than being "your" organization.

    model = Story
    form_class = StoryForm
    form_invalid_message = "Check the form."
    form_valid_message = "Story created."

    def test_user(self, user):
        """User must be member of an org."""

        if user.organization:
            return True

        raise PermissionDenied()

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


# ACCESS: Any org user should be able to update a story belonging to their org
# Any user of an org that's part of collaborate_with for a story should be able to
# update the story details.
class StoryUpdateView(CustomUserTest, FormMessagesMixin, UpdateView):
    """Update a story."""

    model = Story
    form_class = StoryForm
    form_invalid_message = "Something went wrong. Check the form."
    form_valid_message = "Changes saved."

    def test_user(self, user):
        """User must be member of the story's org or a collaborating org."""

        # FIXME : needs to handle contractors

        story = self.object = self.get_object()
        org = user.organization

        if story.is_editable_by_org(org) and user.user_type in [User.ADMIN, User.EDITOR]:
            return True

        raise PermissionDenied()

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


# ACCESS: Any org user should be able to view a story for their org unless the story is marked sensitive.
# Any user of an org that's part of collaborate_with on a project or series or story should
# be able to view the stories of the project, series or a collaborative story.
# Future: A contractor with access to a project or series or story should be able to view the
# stories of that project or series or the specific story.
class StoryDetailView(CustomUserTest, DetailView):
    """Show all the details and related items for a story."""

    model = Story

    def test_user(self, user):
        """User must be member of the story's org or a collaborating org."""

        # FIXME : needs to handle contractors

        story = self.object = self.get_object()
        org = user.organization

        if story.is_editable_by_org(org) and user.user_type in [User.ADMIN, User.EDITOR]:
            return True

        raise PermissionDenied()

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

    def story_tasks(self):
        """Get tasks and task form for the story."""

        tasks = self.object.task_set.all()
        identified = self.object.task_set.filter(status="Identified")
        inprogress = self.object.task_set.filter(status="In Progress")
        complete = self.object.task_set.filter(status="Complete")
        identified_ct = identified.count()
        inprogress_ct = inprogress.count()
        complete_ct = complete.count()
        form = TaskForm(organization=self.object.organization)

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

    def story_events(self):
        """Get events and event form for the story."""

        events = self.object.event_set.all()
        form = EventForm(organization = self.object.organization)
        return {'events': events, 'form': form}

    def story_assets(self):
        """Return all the assets associated with a story."""

        images = self.object.get_story_images()
        documents = self.object.get_story_documents()
        audio = self.object.get_story_audio()
        video = self.object.get_story_video()
        return {'images': images, 'documents': documents, 'audio': audio, 'video': video}


# ACCESS: Only an org admin or editor can delete a story belonging to their organization.
class StoryDeleteView(CustomUserTest, FormMessagesMixin, DeleteView):
    """Delete a story and it's associated items.

    In this project, we expect deletion to be done via a JS pop-up UI; we don't expect to
    actually use the "do you want to delete this?" Django-generated page. However, this is
    available if useful.
    """

    model = Story
    template_name = "editorial/story_delete.html'"

    form_valid_message = "Deleted."
    form_invalid_message = "Please check form."

    def test_user(self, user):
        """User must be member of the story's org or a collaborating org."""

        # FIXME : needs to handle contractors

        story = self.object = self.get_object()
        org = user.organization

        if story.is_editable_by_org(org) and user.user_type in [User.ADMIN, User.EDITOR]:
            return True

        raise PermissionDenied()

    def get_success_url(self):
        """Post-deletion, return to the story list."""

        return reverse('story_list')


class StorySchedule(View):
    """Return JSON of story schedule information."""

    def get(self, request, *args, **kwargs):
        story_id = self.kwargs['pk']
        story = Story.objects.get(id=story_id)
        story_calendar = story.get_story_schedule()

        return HttpResponse(json.dumps(story_calendar), content_type='application/json')


# def story_team_options_json(request, pk):
#     """Returns JSON of team members that can be assigned to a story."""
#
#     story = get_object_or_404(Story, pk=pk)
#     print story
#
#     team = Story.get_story_team(story)
#     story_team = {}
#     for item in team:
#         story_team[item.id] = item.credit_name
#     print story_team
#     return HttpResponse(json.dumps(story_team), content_type="application/json")
