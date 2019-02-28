""" Private Message and Comment views for editorial app.

    editorial/views/communicationviews.py
"""

# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.views.generic import TemplateView , UpdateView, DetailView, CreateView, View
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import datetime
import json
from actstream import action
from braces.views import LoginRequiredMixin, FormMessagesMixin

from editorial.forms import (
    PrivateMessageForm,
    CommentForm,
    )

from editorial.models import (
    User,
    Organization,
    Network,
    Project,
    Story,
    Facet,
    Task,
    Event,
    Assignment,
    Comment,
    PrivateMessage,
    Discussion,)


#----------------------------------------------------------------------#
#   AJAX Mixin
#----------------------------------------------------------------------#

# TODO implementation on comments in discussion
class AjaxCommentFormMixin(object):
    """Mixin for using Ajax on comment forms."""

    def form_invalid(self, form):
        response = super(AjaxCommentFormMixin, self).form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        response = super(AjaxCommentFormMixin, self).form_valid(form)
        if self.request.is_ajax():
            data = {
                'pk': self.object.pk,
            }
            return JsonResponse(data)
        else:
            return response





#----------------------------------------------------------------------#
#   Create Comment View
#----------------------------------------------------------------------#

# ACCESS Any org user should be able to comment on their own organization, on a network
# their organization is a member/owner of, on any PSSF, Task, Event that their org is owner of
# or is accessible through collaborate_with
# Contractors should only be able to comment on PSSFTE that they have access to.
class CommentCreateView(LoginRequiredMixin, CreateView):
    """Post a comment."""

    # handle users that are not logged in
    login_url = settings.LOGIN_URL

    model = Comment
    form_class = CommentForm

    def form_valid(self, form):
        """Save -- but first add some information and associate it
        with the correct object."""

        self.object = comment = form.save(commit=False)
        # set request based attributes
        comment.user = self.request.user
        # get thing that the document is being associated with
        associated_object = self.request.POST.get('association')
        if associated_object == 'organization':
            org_id = self.request.POST.get('organization')
            organization = get_object_or_404(Organization, id=org_id)
            discussion = get_object_or_404(Discussion, id=organization.discussion.id)
            comment_text = self.request.POST.get('text')
            comment = Comment.objects.create_comment(user=self.request.user, discussion=discussion, text=comment_text)
            # save comment
            comment.save()
            # record action for activity stream
            action_target = organization
            action.send(self.request.user, verb="posted", action_object=comment, target=action_target)
            # redirect to the associated object
            return HttpResponseRedirect(reverse('org_detail', args=(organization.id,)))
        elif associated_object == 'network':
            network_id = self.request.POST.get('network')
            network = get_object_or_404(Network, id=network_id)
            discussion = get_object_or_404(Discussion, id=network.discussion.id)
            comment_text = self.request.POST.get('text')
            comment = Comment.objects.create_comment(user=self.request.user, discussion=discussion, text=comment_text)
            # save comment
            comment.save()
            # record action for activity stream
            action_target = network
            action.send(self.request.user, verb="posted", action_object=comment, target=action_target)
            # redirect to the associated object
            return HttpResponseRedirect(reverse('network_detail', args=(network.id,)))
        elif associated_object == 'project':
            project_id = self.request.POST.get('project')
            project = get_object_or_404(Project, id=project_id)
            discussion = get_object_or_404(Discussion, id=project.discussion.id)
            comment_text = self.request.POST.get('text')
            comment = Comment.objects.create_comment(user=self.request.user, discussion=discussion, text=comment_text)
            # save comment
            comment.save()
            # record action for activity stream
            action_target = project
            action.send(self.request.user, verb="posted", action_object=comment, target=action_target)
            # redirect to the associated object
            return HttpResponseRedirect(reverse('project_detail', args=(project.id,)))
        elif associated_object == 'story':
            story_id = self.request.POST.get('story')
            story = get_object_or_404(Story, id=story_id)
            discussion = get_object_or_404(Discussion, id=story.discussion.id)
            comment_text = self.request.POST.get('text')
            comment = Comment.objects.create_comment(user=self.request.user, discussion=discussion, text=comment_text)
            # save comment
            comment.save()
            # record action for activity stream
            action_target = story
            action.send(self.request.user, verb="posted", action_object=comment, target=action_target)
            # redirect to the associated object
            return HttpResponseRedirect(reverse('story_detail', args=(story.id,)))
        elif associated_object == 'facet':
            facet_id = self.request.POST.get('facet')
            facet = get_object_or_404(Facet, id=facet_id)
            discussion = get_object_or_404(Discussion, id=facet.discussion.id)
            comment_text = self.request.POST.get('text')
            comment = Comment.objects.create_comment(user=self.request.user, discussion=discussion, text=comment_text)
            # save comment
            comment.save()
            # record action for activity stream
            action_target = facet
            action.send(self.request.user, verb="posted", action_object=comment, target=action_target)
            # redirect to the associated object
            return HttpResponseRedirect(reverse('facet_edit', args=(facet.story.id, facet.id)))
        elif associated_object == 'task':
            task_id = self.request.POST.get('task')
            task = get_object_or_404(Task, id=task_id)
            discussion = get_object_or_404(Discussion, id=task.discussion.id)
            comment_text = self.request.POST.get('text')
            comment = Comment.objects.create_comment(user=self.request.user, discussion=discussion, text=comment_text)
            # save comment
            comment.save()
            # record action for activity stream
            action_target = task
            action.send(self.request.user, verb="posted", action_object=comment, target=action_target)
            # redirect to the associated object
            return HttpResponseRedirect(reverse('task_detail', args=(task.id,)))
        elif associated_object == 'event':
            event_id = self.request.POST.get('event')
            event = get_object_or_404(Event, id=event_id)
            discussion = get_object_or_404(Discussion, id=event.discussion.id)
            comment_text = self.request.POST.get('text')
            comment = Comment.objects.create_comment(user=self.request.user, discussion=discussion, text=comment_text)
            # save comment
            comment.save()
            # record action for activity stream
            action_target = event
            action.send(self.request.user, verb="posted", action_object=comment, target=action_target)
            # redirect to the associated object
            return HttpResponseRedirect(reverse('event_detail', args=(event.id,)))
        elif associated_object == 'assignment':
            assignment_id = self.request.POST.get('assignment')
            assignment = get_object_or_404(Assignment, id=assignment_id)
            discussion = get_object_or_404(Discussion, id=assignment.discussion.id)
            comment_text = self.request.POST.get('text')
            comment = Comment.objects.create_comment(user=self.request.user, discussion=discussion, text=comment_text)
            # save comment
            comment.save()
            # record action for activity stream
            action_target = assignment
            action.send(self.request.user, verb="posted", action_object=comment, target=action_target)
            # redirect to the associated object
            return HttpResponseRedirect(reverse('assignment_detail', args=(assignment.id,)))



# XXX Comments are not currently editable or deletable, but any user should
# be able to edit or delete their own comments.
# Admins should be able to remove any comments on anything their org "owns"

# class CommentUpdateView(UpdateView):
#     """FUTURE ability to edit a comment"""
#     pass

# class CommentDeleteView(DeleteView):
#     """FUTURE ability to delete a comment."""
#     pass



#----------------------------------------------------------------------#
#   Organization Comment Views
#----------------------------------------------------------------------#

# def org_comments(request):
#     """ Return JSON of all organization discussion comments."""
#
#     organization = request.user.organization
#     org_comments = {}
#     org_comments[organization.name] = Comment.objects.filter(discussion=organization.discussion).order_by('-date')
#     print org_comments
#     return HttpResponse(json.dumps(org_comments), content_type = "application/json")
