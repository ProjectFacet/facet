"""Inbox views for editorial app. """

# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, reverse
from django.template.loader import render_to_string
from django.views.generic import TemplateView, View, FormView
from braces.views import LoginRequiredMixin, FormMessagesMixin, CsrfExemptMixin


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
    """

    template_name = 'editorial/inbox/inbox.html'

    def get_context_data(self):
        """Return all the assorted items associated with a team user inbox."""

        private_messages_received = self.request.user.private_messages_received()

        return {
            'messages': private_messages_received,
    }


class SentMessages(TemplateView):
    """Return sent messages."""

    template_name = 'editorial/inbox/sent-messages.html'

    def get_context_data(self):
        """Return all the assorted items associated with a team user inbox."""

        sent_messages = self.request.user.private_messages_sent()

        return {
            'messages': sent_messages,
    }


class CommentList(TemplateView):
    """Return comment feeds."""

    template_name = 'editorial/inbox/inbox-comments.html'

    def get_context_data(self, comment_type):
        """Return all the assorted items associated with a team user inbox."""

        organization = self.request.user.organization
        # returns all comments involving any user of an Organization
        # all_comments = organization.get_org_user_comments()

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
        # elif comment_type=="series":
        # returns all comments for any series of an Organization
            # comments = organization.get_series_comments()
        elif comment_type=="facet":
        # returns all comments for any facets of stories of an Organization
            comments = organization.get_facet_comments()

        return {
            'comments': comments,
            'comment_type': comment_type,
        }


class MessageContent(TemplateView):
    """Return html for displaying a specific message."""

    template_name = "editorial/inbox/private-message-content.html"

    def get_context_data(self, pk):
        message = get_object_or_404(PrivateMessage, id=pk)
        return {'message': message}

# ACCESS Any org user should be able to message any other same org user
# Any org user should be able to message org users from organizations in shared networks
# Contractors should be able to message any user with a talenteditor profile & public is true
# Any user with a talenteditor profile should be able to message any user with a contractorprofile and public is true


class PrivateMessageCompose(FormMessagesMixin, CsrfExemptMixin, FormView):
    """Compose private messages (form & form handling)."""

    template_name = "editorial/inbox/privatemessage_compose_form.html"
    form_class = PrivateMessageForm
    form_valid_message = "Message sent."
    form_invalid_message = "Please correct the errors below."

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


class PrivateMessageComposeModal(PrivateMessageCompose):
    template_name = "editorial/inbox/privatemessage_compose_form_modal.html"

    def get_success_url(self):
        return reverse("privatemessage_compose_modal_success")


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
