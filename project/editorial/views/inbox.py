"""Inbox views for editorial app. """

# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, reverse
from django.template.loader import render_to_string
from django.views.generic import TemplateView, View, FormView


from editorial.forms import (
    PrivateMessageForm,
)
from editorial.models import (
    User,
    PrivateMessage,
    Discussion,
)


#----------------------------------------------------------------------#
#   Inbox Views
#----------------------------------------------------------------------#

# ACCESS: All users have access to their inbox.
class Inbox(TemplateView):
    """ Return discussion inbox.

    Displays inbox and sent messages.

    Displays comments from Project Discussions involving user.
    Displays comments from Series Discussions involving user.
    Displays comments from Story Discussions involving user.
    Displays comments from any Facet Discussion involving user.
    Displays comments from any PrivateDiscussion involving user.
    """

    template_name = 'editorial/inbox.html'

    def get_context_data(self):
        """Return all the assorted items associated with a team user inbox."""

        private_messages_received = self.request.user.private_messages_received()

        return {
            'private_messages_received': private_messages_received,
    }


class SentMessages(View):
    """Return sent messages."""

    def get(self, request):

        sent_messages = self.request.user.private_messages_sent()

        sent_messages_html = render_to_string('sent-messages.html', {'sent_messages': sent_messages})

        return HttpResponse(sent_messages_html)


class CommentList(View):
    """Return comment feeds."""

    def get(self, request, comment_type):

        organization = request.user.organization
        # returns all comments involving any user of an Organization
        all_comments = organization.get_org_user_comments()

        if comment_type=="organization":
        # returns all comments made for an Organization
            comments = organization.get_org_comments()
        elif comment_type=="network":
        # returns all comments for any networks an Organization is part of
            comments = organization.get_network_comments()
        elif comment_type=="project":
        # returns all comments for all projects an Organization owns.
            comments = organization.get_project_comments()
        elif comment_type=="story":
        # returns all comments for any story of an Organization
            comments = organization.get_story_comments()
        elif comment_type=="series":
        # returns all comments for any series of an Organization
            comments = organization.get_series_comments()
        elif comment_type=="facet":
        # returns all comments for any facets of stories of an Organization
            comments = organization.get_facet_comments()

        comments_html = render_to_string('inbox-comments.html', {
                                'comments': comments,
                                'comment_type': comment_type,
        })

        return HttpResponse(comments_html)


class MessageContent(TemplateView):
    """Return html for displaying a specific message."""

    template_name = "editorial/private-message-content.html"

    def get_context_data(self, pk):
        message = get_object_or_404(PrivateMessage, id=pk)
        return {'message': message}

# ACCESS Any org user should be able to message any other same org user
# Any org user should be able to message org users from organizations in shared networks
# Contractors should be able to message any user with a talenteditor profile & public is true
# Any user with a talenteditor profile should be able to message any user with a contractorprofile and public is true


class PrivateMessageCompose(FormView):
    """Compose private messages (form & form handling)."""

    template_name = "editorial/compose-message.html"
    form_class = PrivateMessageForm

    def get_form_kwargs(self):
        kwargs = super(PrivateMessageCompose, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        message_subject = form.cleaned_data['subject']
        message_text = form.cleaned_data['text']
        recipient = form.cleaned_data['recipient']
        discussion = Discussion.objects.create_discussion('PRI')
        sender = self.request.user
        message = PrivateMessage.objects.create_private_message(
                user=sender,
                recipient=recipient,
                discussion=discussion,
                subject=message_subject,
                text=message_text)
        # message.save()
        return super(PrivateMessageCompose, self).form_valid(form)

    def get_success_url(self):
        # TODO: pass through "where i should return to"
        return reverse("inbox")


# def inbox_important(request):
#     """Return important messages."""
#
#     return render(request, 'editorial/inbox.html')
#
#
# def inbox_trash(request):
#     """Return trashed messages."""
#
#     return render(request, 'editorial/inbox.html')
