from datetime import datetime, timedelta, time

from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import Q
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from imagekit.models import ImageSpecField
from pilkit.processors import SmartResize

from .organization import Organization


@python_2_unicode_compatible
class Network(models.Model):
    """A group of organizations.

    A network is a collection of two or more organizations seeking to create a sharing
    or collaborating relationship.

    Sharing means the source organization has made the content available to other
    members of the network.

    An organization can opt to collaborate with one of more members of a Network.
    Collaboration means that a user from a collaborating organization can participate
    in the editorial process on the host organization's content. They can edit, upload
    assets and participate in any relevant discussions.
    """

    owner_organization = models.ForeignKey(
        Organization,
        help_text='Organization that owns the network.'
    )

    name = models.CharField(
        max_length=75,
        db_index=True,
        help_text="The name by which members identify the network."
    )

    creation_date = models.DateTimeField(
        auto_now_add=True
    )

    network_description = models.TextField(
        help_text="Short description of a network.",
        blank=True,
    )

    logo = models.ImageField(
        upload_to='networks',
        blank=True,
    )

    display_logo = ImageSpecField(
        source='logo',
        processors=[SmartResize(500, 500)],
        format='JPEG',
    )

    organizations = models.ManyToManyField(
        Organization,
        related_name='network_organization',
    )

    discussion = models.ForeignKey(
        'Discussion',
        related_name='network_discussion',
        help_text='Id of discussion for a network.',
        blank=True,
        null=True,
    )

    notes = models.ManyToManyField(
        'Note',
        blank=True,
    )

    # simple assets
    simple_image_assets = models.ManyToManyField(
        'SimpleImage',
        blank=True,
    )

    simple_document_assets = models.ManyToManyField(
        'SimpleDocument',
        blank=True,
    )

    simple_audio_assets = models.ManyToManyField(
        'SimpleAudio',
        blank=True,
    )

    simple_video_assets = models.ManyToManyField(
        'SimpleVideo',
        blank=True,
    )

    class Meta:
        verbose_name = 'Network'
        verbose_name_plural = "Networks"
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('network_detail', kwargs={'pk': self.id})

    def get_network_shared_stories(self):
        """ Return list of stories shared with a network.

        This is used to populate the network content dashboard.
        """

        from .story import Story

        network_stories = Story.objects.filter(Q(share_with=self))
        return network_stories

    @property
    def description(self):
        return "{description}".format(description=self.network_description)

    @property
    def search_title(self):
        return self.name

    @property
    def type(self):
        return "Network"
