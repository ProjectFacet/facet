from django.db import models
from django.db.models import Q
from model_utils.models import TimeStampedModel
import time as timemk
from datetime import datetime, timedelta, time
from imagekit.models import ProcessedImageField, ImageSpecField
from django.utils.encoding import python_2_unicode_compatible
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError

from .people import User

#-----------------------------------------------------------------------#
#   Discussion:
#   Discussion, PrivateDiscussion, PrivateMessage, Comment, CommentReadStatus
#-----------------------------------------------------------------------#

class DiscussionManager(models.Manager):
    """ Custom manager for discussions."""

    def create_discussion(self, discussion_type):
        """ Method for quick creation of a discussion."""
        discussion = self.create(discussion_type=discussion_type)
        return discussion


@python_2_unicode_compatible
class Discussion(models.Model):
    """ Class for  for related comments. """

    # Choices for Discussion type
    ORGANIZATION = 'ORG'
    NETWORK = 'NET'
    PRIVATE = 'PRI'
    PROJECT = 'PRO'
    SERIES = 'SER'
    STORY = 'STO'
    FACET = 'F'
    TASK = 'TSK'
    EVENT = 'EV'
    WEBFACET = 'WF'
    PRINTFACET = 'PF'
    AUDIOFACET = 'AF'
    VIDEOFACET = 'VF'

    DISCUSSION_TYPE_CHOICES = (
        (ORGANIZATION, 'Organization Conversation'),
        (NETWORK, 'Network Conversation'),
        (PRIVATE, 'Private Conversation'),
        (PROJECT, 'Project Conversation'),
        (SERIES, 'Series Conversation'),
        (STORY, 'Story Conversation'),
        (FACET, 'Facet Conversation'),
        (TASK, 'Task Conversation'),
        (EVENT, 'Event Conversation'),
        (WEBFACET, 'WebFacet Conversation'),
        (PRINTFACET, 'PrintFacet Conversation'),
        (AUDIOFACET, 'AudioFacet Conversation'),
        (VIDEOFACET, 'VideoFacet Conversation'),
    )

    discussion_type = models.CharField(
        max_length=25,
        choices=DISCUSSION_TYPE_CHOICES,
        help_text='What kind of discussion is it.'
    )

    objects = DiscussionManager()

    def __str__(self):
        return "Discussion:{discussion} from {discussion_type}".format(
                                discussion=self.id,
                                discussion_type=self.discussion_type
                                )


@python_2_unicode_compatible
class PrivateDiscussion(models.Model):
    """ Signifier of private conversations.

    Private conversations can occur between two or more individuals and only exist in their
    own inboxes and are not attached to any content types.
    """

    discussion = models.ForeignKey(
        Discussion,
    )

    users = models.ManyToManyField(
        User,
        related_name='private_discussion_user',
    )

    def __str__(self):
        return "Private discussion:{discussion}.".format(
                                discussion=self.id,
                                )


class PrivateMessageManager(models.Manager):
    """ Customer manager for private messaging."""

    def create_private_message(self, user, recipient, discussion, subject, text):
        """ Method for quick creation of a private discussion."""

        message = self.create(user=user, recipient=recipient, discussion=discussion, subject=subject, text=text)
        return message


@python_2_unicode_compatible
class PrivateMessage(models.Model):
    """ A private message to a specific user.

    Private messages can be sent to a specific user and will only be
    visible to those users in their inbox.
    """

    user = models.ForeignKey(
        User,
        related_name='private_message_sender',
        help_text='The sender of the private message.',
    )

    recipient = models.ForeignKey(
        User,
        related_name='private_message_recipient',
        help_text='The recipient of the private message.'
    )

    discussion = models.ForeignKey(
        Discussion,
    )

    subject = models.TextField(
        help_text='The topic of the message.',
        blank=True,
    )

    text = models.TextField(
        help_text='The content of the message.'
    )

    date = models.DateTimeField(
        auto_now_add=True,
    )

    objects = PrivateMessageManager()

    class Meta:
        verbose_name = 'Private Message'
        verbose_name_plural = "Private Messages"
        ordering = ['date']

    def __str__(self):
        return self.subject

    @property
    def type(self):
        return "Private Message"


class CommentManager(models.Manager):
    """ Custom manager for comments."""

    def create_comment(self, user, discussion, text):
        """ Method for quick creation of a discussion."""
        comment = self.create(user=user, discussion=discussion, text=text)
        return comment


@python_2_unicode_compatible
class Comment(models.Model):
    """An individual comment.

    Comments can be made on a seriesplan, storyplan, webfacet,
    audiofacet, videofacet, or between one or more people privately.
    """

    user = models.ForeignKey(
        User,
    )

    discussion = models.ForeignKey(
        Discussion,
    )

    text = models.TextField(
        help_text='The content of the comment.'
    )

    date = models.DateTimeField(
        auto_now_add=True,
    )

    objects = CommentManager()

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return "Comment:{comment} from discussion:{discussion}".format(
                                comment=self.id,
                                discussion=self.discussion.id,
                                )

    @property
    def type(self):
        return "Comment"


@python_2_unicode_compatible
class CommentReadStatus(models.Model):
    """ Tracking if a user involved in a discussion has read the most recent
    comment in order to surface unread comments first.
    """

    comment = models.ForeignKey(
        Comment,
    )

    user = models.ForeignKey(
        User,
    )

    datetime_read = models.DateTimeField(
        auto_now_add=True,
    )

    has_read = models.BooleanField(
        default=True,
    )

    def __str__(self):
        return "Comment:{comment} has {status} read status.".format(
                                comment=self.comment.id,
                                status=self.has_read,
                                )
