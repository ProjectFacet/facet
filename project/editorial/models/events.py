from django.db import models
from django.db.models import Q
# from django.contrib.postgres.fields import ArrayField
# from simple_history.models import HistoricalRecords
from model_utils.models import TimeStampedModel
import time as timemk
from datetime import datetime, timedelta, time
from imagekit.models import ProcessedImageField, ImageSpecField
# from pilkit.processors import ResizeToFit, SmartResize
# from django.contrib.auth.models import AbstractUser
from django.utils.encoding import python_2_unicode_compatible
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.shortcuts import get_object_or_404
# from itertools import chain
# from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
# from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
# from django.db.models.signals import post_save
# from django.dispatch import receiver

from . import User, Organization, Network, Project, Series, Story

#-----------------------------------------------------------------------#
#  EVENT
#-----------------------------------------------------------------------#

class Event(models.Model):
    """An event.

    An event can be assigned to an Organization, Project, Series or Story.
    """

    organization = models.ForeignKey(
        Organization,
        blank=True,
        null=True,
    )

    owner = models.ForeignKey(
      User,
      related_name='eventowner'
    )

    name = models.TextField(
        help_text='Name of the event.'
    )

    text = models.TextField(
        help_text='Description of the event.',
        blank=True,
    )

    # Choices for event type.
    # Hosting: An event that is managed by an organization.
    # Example: Live studio taping open to the public
    # Reporting: An external event that is being covered for a story.
    # Example: Press conference at the police department
    HOSTING = 'Hosting'
    REPORTING = 'Reporting'
    OTHER = 'Other'
    EVENT_TYPE_CHOICES = (
        (HOSTING, 'Hosting'),
        (REPORTING, 'Reporting'),
        (OTHER, 'Other'),
    )

    event_type = models.CharField(
        max_length=50,
        choices=EVENT_TYPE_CHOICES,
        help_text='Kind of event.'
    )

    team = models.ManyToManyField(
        # There can be multiple users assigned to an event.
        User,
        related_name='eventteam',
        help_text='The users assigned to an event.',
        blank=True,
    )

    creation_date = models.DateTimeField(
        auto_now_add=True,
        help_text='Date and time event is created.',
        blank=True,
    )

    event_date = models.DateTimeField(
        help_text='Date and time of the event.',
        blank=True,
    )

    venue = models.TextField(
        help_text = 'The location of the event.',
        blank=True,
    )

    # Notes
    #TODO Add Notes to note class to be attached to Events

    # an event can be associated with an organization, project, series or story.
    evt_organization = models.ForeignKey(
        Organization,
        related_name='evt_organization',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    series = models.ForeignKey(
        Series,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    story = models.ForeignKey(
        Story,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = 'Event'
        verbose_name_plural = "Events"
        ordering = ['name']

    def __str__(self):
        return self.name

    @property
    def search_title(self):
        return self.name

    @property
    def description(self):
        return self.description.encode('utf-8')

    @property
    def type(self):
        return "Event"

    def clean(self):
        """Enforce that there is one relationship."""

        super(Event, self).clean()

        count = (
            (1 if self.organization else 0) +
            (1 if self.project else 0) +
            (1 if self.series else 0) +
            (1 if self.story else 0)
        )

        if count != 1:
            raise ValidationError("Events can only relate to one thing.")
