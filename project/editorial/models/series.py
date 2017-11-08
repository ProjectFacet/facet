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

from . import User, Organization, Network, Discussion

#-----------------------------------------------------------------------#
#  SERIES
#-----------------------------------------------------------------------#


@python_2_unicode_compatible
class Series(models.Model):
    """ A specific series.

    Series are an organizational component for one or more stories. The primary use is
    to connect multiple stories on a particular topic. Series are also the method for keeping
    assets easily available to all stories/facets.
    """

    name = models.CharField(
        max_length=75,
        help_text='The name identifying the series.'
    )

    series_description = models.TextField(
        blank=True,
        help_text='Short description of a series.',
    )

    owner = models.ForeignKey(
        User,
        related_name='series_owner',
        help_text='The user that created the series.'
    )

    organization = models.ForeignKey(
        Organization,
        related_name='series_organization',
        help_text='The org'
    )

    team = models.ManyToManyField(
        User,
        related_name='series_team_member',
        help_text='User contributing to the series.',
        blank=True,
    )

    creation_date = models.DateTimeField(
        auto_now_add=True,
    )

    sensitive = models.BooleanField(
        default=False,
        help_text='Is a series sensitive, for limited viewing?'
    )

    share = models.BooleanField(
        default=False,
        help_text='The series is being shared with a network.'
    )

    share_with = models.ManyToManyField(
        Network,
        related_name='series_shared_with_network',
        help_text='Network ids that a series is shared with.',
        blank=True,
    )

    share_with_date = models.DateTimeField(
        help_text="Estimated date the series will be available",
        blank=True,
        null=True,
    )

    collaborate = models.BooleanField(
        default=False,
        help_text='The series is being collaborated on with a network.'
    )

    collaborate_with = models.ManyToManyField(
        Organization,
        related_name='series_collaborated_with_organization',
        help_text='Organization ids that a series is open to collaboration with.',
        blank=True,
    )

    archived = models.BooleanField(
        default=False,
        help_text='Is the content no longer active and needed?'
    )

    discussion = models.ForeignKey(
        'Discussion',
        help_text='Id of planning discussion for a series.',
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = 'Series'
        verbose_name_plural = "Series"
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('series_detail', kwargs={'pk': self.id})

    def get_series_team(self):
        """Return queryset with org users and users from collaboration orgs for a series."""

        collaborators = self.collaborate_with.all()
        series_team = User.objects.filter(Q(Q(organization=self.organization) | Q(organization__in=collaborators)))
        return series_team

    @property
    def description(self):
        return "{description}".format(description=self.series_description)

    @property
    def search_title(self):
        return self.name

    @property
    def type(self):
        return "Series"
