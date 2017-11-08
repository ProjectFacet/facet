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
#  TASK
#-----------------------------------------------------------------------#

class Task(models.Model):
    """A Task.

    A task is an action item assigned to a project, series,
    story or an event. A task has an assigned team of users.
    """

    organization = models.ForeignKey(
        Organization,
    )

    owner = models.ForeignKey(
      User,
      related_name='taskowner'
    )

    name = models.TextField(
        help_text='Name of the task.'
    )

    text = models.TextField(
        help_text='Content of the task.',
        blank=True,
    )

    assigned_to = models.ManyToManyField(
        # There can be multiple users listed as assigned to the task.
        User,
        related_name='taskassigneduser',
        help_text='The users assigned to the task.',
        blank=True,
    )

    # Choices for Task status.
    IDENTIFIED = 'Identified'
    IN_PROGRESS = 'In Progress'
    COMPLETE = 'Complete'
    TASK_STATUS_CHOICES = (
        (IDENTIFIED, 'Identified'),
        (IN_PROGRESS, 'In Progress'),
        (COMPLETE, 'Complete'),
    )

    status = models.CharField(
        max_length=50,
        choices=TASK_STATUS_CHOICES,
        help_text='Task status.'
    )

    important = models.BooleanField(
        default=False,
        help_text='Whether a task is important.'
    )

    creation_date = models.DateTimeField(
        auto_now_add=True,
        help_text='Date and time task is created.',
        blank=True,
    )

    due_date = models.DateTimeField(
        help_text='Date and time task is to be completed.',
        blank=True,
    )

    inprogress_date = models.DateTimeField(
        help_text='Date and time task status is changed to in progress.',
        blank=True,
        null=True,
    )

    completion_date = models.DateTimeField(
        auto_now_add=True,
        help_text='Date and time task status is changed to complete.',
        blank=True,
        null=True,
    )

    # a task can be associated with a project, series, story or an event.
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

    event = models.ForeignKey(
        'Event',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    upload = models.FileField(
        upload_to="task/%Y/%m/%d/",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = 'Task'
        verbose_name_plural = "Tasks"
        ordering = ['name']

    def __str__(self):
        return self.name

    @property
    def search_title(self):
        return self.name

    @property
    def description(self):
        return self.text.encode('utf-8')

    @property
    def type(self):
        return "Task"

    def clean(self):
        """Enforce that there is one relationship."""

        super(Task, self).clean()

        count = (
            (1 if self.project else 0) +
            (1 if self.series else 0) +
            (1 if self.story else 0) +
            (1 if self.event else 0)
        )

        if count != 1:
            raise ValidationError("Tasks can only relate to one thing.")
