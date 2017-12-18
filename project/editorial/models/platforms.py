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

from . import User, Organization, Network, Project, Series

#--------------------------------------------------------------------------#
#   Platforms and PlatformAccounts
#   Social accounts connected to Users, Organizations, Projects and Series.
#   Ex. Users can have social media accounts, Organizations will often
#   have multiple accounts on any single platform, a special project or series
#   may have a unique social presence.
#--------------------------------------------------------------------------#

class Platform(models.Model):
    """A platform.

    Lookup table with details for each major platform. Instances populate
    options in PlatformAccount.
    Ex. Facebook, Twitter, YouTube, Vimeo, Snapchat, LinkedIn, Github, Reddit
    Instagram, Pinterest, Flickr, Behance, Tumblr
    """

    name = models.CharField(
       max_length=250,
       help_text='Name of the platform.'
    )

    # code for font awesome icon for the platform
    # ex. 'fa-facebook' is the Font Awesome icon for Facebook
    icon_code = models.CharField(
        max_length=50,
        blank=True,
        help_text='text for font-awesome icon for the platform'
    )

    class Meta:
        verbose_name = 'Platform'
        verbose_name_plural = "Platforms"
        ordering = ['name']

    def __str__(self):
        return self.name


class PlatformAccount(models.Model):
    """ A Platform Account.

    Platform accounts are the types and urls of different social media
    and platform accounts. Platform accounts can be connected to a user,
    organization, project or series. The attributes should always be the same
    regardless of model it's associated with.
    """

    name = models.CharField(
       max_length=250,
       db_index=True,
       help_text='Short name to identify the social account.'
    )

    platform = models.ForeignKey(
       Platform
    )

    url = models.URLField(
        max_length=250,
        blank=True,
    )

    description = models.TextField(
        blank=True,
        help_text='Short description of the purpose of the account.',
    )

    # if a social account is associated with an Organization, Project or Series.
    # UI not available to do this on platform accounts associated with a User.
    team = models.ManyToManyField(
        User,
        related_name='platform_team_member',
        help_text='User that contributes to this account.',
        blank=True,
    )

    # a platform account can be connected to a User, Organization or Project
    # a platform account must be true for one of these.

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    project = models.ForeignKey(
        'Project',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = 'Platform Account'
        verbose_name_plural = "Platform Accounts"
        ordering = ['name']

        # The same user/org/project cannot use the same name/URL twice
        unique_together = [
            ('user', 'url'), ('organization', 'url'), ('project', 'url'),
            ('user', 'name'), ('organization', 'name'), ('project', 'name'),
        ]

    def __str__(self):
        return self.name

    @property
    def type(self):
        return "Platform Account"
