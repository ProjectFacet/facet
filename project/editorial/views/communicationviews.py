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
from django.views.generic import TemplateView , UpdateView, DetailView, CreateView
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import datetime
import json
from actstream import action

from editorial.forms import (
    PrivateMessageForm,
    CommentForm,
    )

from editorial.models import (
    User,
    Organization,
    Network,
    Project,
    Series,
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

class AjaxResponseMixin(object):
    """Mixin for using Ajax on comment forms."""

    def form_invalid(self, form):
        response = super(AjaxResponseMixin, self).form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        response = super(AjaxResponseMixin, self).form_valid(form)
        if self.request.is_ajax():
            data = {
                'pk': self.object.pk,
            }
            return JsonResponse(data)
        else:
            return response


#----------------------------------------------------------------------#
#   Private Message Views
#----------------------------------------------------------------------#

# TODO revise so it's not csrf exempt
@csrf_exempt
def private_message_new(request):
    """ Private messaging method. """

    if request.method == 'POST':
        privatemessageform = PrivateMessageForm(request.POST, request=request)
        if privatemessageform.is_valid():
            message_subject = request.POST.get('subject')
            message_text = request.POST.get('text')
            send_to = request.POST.get('recipient')
            recipient = get_object_or_404(User, id=send_to)
            discussion = Discussion.objects.create_discussion('PRI')
            message = PrivateMessage.objects.create_private_message(user=request.user, recipient=recipient, discussion=discussion, subject=message_subject, text=message_text)
            message.save()
    return redirect('/inbox')


def create_privatecomment_reply(request):
    """ Reply to a private message."""
    pass


#----------------------------------------------------------------------#
#   Create Comment View
#----------------------------------------------------------------------#

class CommentCreateView(CreateView):
    """Post a comment."""

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
        elif associated_object == 'series':
            series_id = self.request.POST.get('series')
            series = get_object_or_404(Series, id=series_id)
            discussion = get_object_or_404(Discussion, id=series.discussion.id)
            comment_text = self.request.POST.get('text')
            comment = Comment.objects.create_comment(user=self.request.user, discussion=discussion, text=comment_text)
            # save comment
            comment.save()
            # record action for activity stream
            action_target = series
            action.send(self.request.user, verb="posted", action_object=comment, target=action_target)
            # redirect to the associated object
            return HttpResponseRedirect(reverse('series_detail', args=(series.id,)))
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
            return HttpResponseRedirect(reverse('facet_edit', args=(facet.id,)))
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


#----------------------------------------------------------------------#
#   Organization Comment Views
#----------------------------------------------------------------------#

def org_comments(request):
    """ Return JSON of all organization discussion comments."""

    organization = request.user.organization
    org_comments = {}
    org_comments[organization.name] = Comment.objects.filter(discussion=organization.discussion).order_by('-date')
    print org_comments
    return HttpResponse(json.dumps(org_comments), content_type = "application/json")


# FIXME: Needs further debugging before replacing above sections
# def create_comment(request):
#     """ Receive AJAX Post for creating a comment. """
#
#     if request.method == 'POST':
#         comment_text = request.POST.get('text')
#         story = request.POST.get('story')
#         facet = get_object_or_404(Facet, story=story)
#         discussion = get_object_or_404(Discussion, id=facet.discussion.id)
#
#         response_data = {}
#
#         # comment = Comment(text=comment_text, user=request.user, discussion = discussion)
#         comment = Comment.objects.create_comment(user=request.user, discussion=discussion, text=comment_text)
#         comment.save()
#
#         response_data['result'] = 'Create post successful!'
#         response_data['commentpk'] = comment.pk
#         response_data['text'] = comment.text
#         response_data['user'] = comment.user.credit_name
#
#         return HttpResponse(
#             json.dumps(response_data),
#             content_type="application/json"
#         )
#     else:
#         return HttpResponse(
#             json.dumps({"nothing to see": "this isn't happening"}),
#             content_type="application/json"
#         )
