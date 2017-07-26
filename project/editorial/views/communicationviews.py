""" Private Message and Comment views for editorial app.

    editorial/views/communicationviews.py
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
    PrivateMessageForm,)

from editorial.models import (
    User,
    Network,
    Series,
    Story,
    WebFacet,
    PrintFacet,
    AudioFacet,
    VideoFacet,
    Comment,
    PrivateMessage,
    Discussion,)


#----------------------------------------------------------------------#
#   Private Message Views
#----------------------------------------------------------------------#

#TODO: Refactor to reduce repetitiveness/use AJAX for submission

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
#   Organization Comment Views
#----------------------------------------------------------------------#

def create_orgcomment(request):
    """ Regular form posting method."""

    if request.method == 'POST':
        comment_text = request.POST.get('text')
        organization = request.user.organization
        discussion = get_object_or_404(Discussion, id=organization.discussion.id)
        comment = Comment.objects.create_comment(user=request.user, discussion=discussion, text=comment_text)
        comment.save()

        # record action for activity stream
        action.send(request.user, verb="commented on", action_object=organization)

        return redirect('org_detail', pk=organization.id)

def org_comments(request):
    """ Return JSON of all organization discussion comments."""

    organization = request.user.organization
    org_comments = {}
    org_comments[organization.name] = Comment.objects.filter(discussion=organization.discussion).order_by('-date')
    print org_comments
    return HttpResponse(json.dumps(org_comments), content_type = "application/json")

#----------------------------------------------------------------------#
#   Create Comment Views
#----------------------------------------------------------------------#

def create_networkcomment(request):
    """ Regular form posting method."""

    if request.method == 'POST':
        comment_text = request.POST.get('text')
        network_id = request.POST.get('network')
        network = get_object_or_404(Network, id=network_id)
        discussion = get_object_or_404(Discussion, id=network.discussion.id)
        comment = Comment.objects.create_comment(user=request.user, discussion=discussion, text=comment_text)
        comment.save()

        # record action for activity stream
        action.send(request.user, verb="commented on", action_object=network)

        return redirect('network_detail', pk=network.id)


def create_projectcomment(request):
    """ Regular form posting method."""

    if request.method == 'POST':
        comment_text = request.POST.get('text')
        project_id = request.POST.get('project')
        project = get_object_or_404(Project, id=project_id)
        discussion = get_object_or_404(Discussion, id=project.discussion.id)
        comment = Comment.objects.create_comment(user=request.user, discussion=discussion, text=comment_text)
        comment.save()

        # record action for activity stream
        action.send(request.user, verb="commented on", action_object=project)

        return redirect('project_detail', pk=project.id)


def create_seriescomment(request):
    """ Regular form posting method."""

    if request.method == 'POST':
        comment_text = request.POST.get('text')
        series_id = request.POST.get('series')
        series = get_object_or_404(Series, id=series_id)
        discussion = get_object_or_404(Discussion, id=series.discussion.id)
        comment = Comment.objects.create_comment(user=request.user, discussion=discussion, text=comment_text)
        comment.save()

        # record action for activity stream
        action.send(request.user, verb="commented on", action_object=series)

        return redirect('series_detail', pk=series.id)


def create_storycomment(request):
    """ Regular form posting method."""

    if request.method == 'POST':
        comment_text = request.POST.get('text')
        story_id = request.POST.get('story')
        story = get_object_or_404(Story, id=story_id)
        discussion = get_object_or_404(Discussion, id=story.discussion.id)
        comment = Comment.objects.create_comment(user=request.user, discussion=discussion, text=comment_text)
        comment.save()

        # record action for activity stream
        action.send(request.user, verb="commented on", action_object=story)

        return redirect('story_detail', pk=story.id)

def create_webcomment(request):
    """ Regular form posting method."""

    if request.method == 'POST':
        comment_text = request.POST.get('text')
        story_id = request.POST.get('story')
        story = get_object_or_404(Story, id=story_id)
        webfacet = get_object_or_404(WebFacet, story=story)
        discussion = get_object_or_404(Discussion, id=webfacet.discussion.id)
        comment = Comment.objects.create_comment(user=request.user, discussion=discussion, text=comment_text)
        comment.save()

        # record action for activity stream
        action.send(request.user, verb="commented on", action_object=webfacet)

        return redirect('story_detail', pk=story.id)


def create_printcomment(request):
    """ Regular form posting method."""

    if request.method == 'POST':
        comment_text = request.POST.get('text')
        story_id = request.POST.get('story')
        story = get_object_or_404(Story, id=story_id)
        printfacet = get_object_or_404(PrintFacet, story=story)
        discussion = get_object_or_404(Discussion, id=printfacet.discussion.id)
        comment = Comment.objects.create_comment(user=request.user, discussion=discussion, text=comment_text)
        comment.save()

        # record action for activity stream
        action.send(request.user, verb="commented on", action_object=printfacet)

        return redirect('story_detail', pk=story.id)


def create_audiocomment(request):
    """ Regular form posting method."""

    if request.method == 'POST':
        comment_text = request.POST.get('text')
        story_id = request.POST.get('story')
        story = get_object_or_404(Story, id=story_id)
        audiofacet = get_object_or_404(AudioFacet, story=story)
        discussion = get_object_or_404(Discussion, id=audiofacet.discussion.id)
        comment = Comment.objects.create_comment(user=request.user, discussion=discussion, text=comment_text)
        comment.save()

        # record action for activity stream
        action.send(request.user, verb="commented on", action_object=audiofacet)

        return redirect('story_detail', pk=story.id)


def create_videocomment(request):
    """ Regular form posting method."""

    if request.method == 'POST':
        comment_text = request.POST.get('text')
        story_id = request.POST.get('story')
        story = get_object_or_404(Story, id=story_id)
        videofacet = get_object_or_404(VideoFacet, story=story)
        discussion = get_object_or_404(Discussion, id=videofacet.discussion.id)
        comment = Comment.objects.create_comment(user=request.user, discussion=discussion, text=comment_text)
        comment.save()

        # record action for activity stream
        action.send(request.user, verb="commented on", action_object=videofacet)

        return redirect('story_detail', pk=story.id)


# FIXME: Needs further debugging before replacing above sections
# def create_webcomment(request):
#     """ Receive AJAX Post for creating a comment on a webfacet. """
#
#     if request.method == 'POST':
#         comment_text = request.POST.get('text')
#         story = request.POST.get('story')
#         webfacet = get_object_or_404(WebFacet, story=story)
#         discussion = get_object_or_404(Discussion, id=webfacet.discussion.id)
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
