from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.db import models

from . import SimpleImage, SimpleDocument, SimpleAudio, SimpleVideo
from . import User, Organization, Project, Series, Story


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

    # Choices for event type:
    # Hosting: An event that is managed by an organization.
    # Ex - Live studio taping open to the public
    # Reporting: An external event that is being covered for a story.
    # Ex - Press conference at the police department
    # Administrative: An internal event such as a team meeting or conference call
    HOSTING = 'Hosting'
    REPORTING = 'Reporting'
    ADMINISTRATIVE = 'Administrative'
    OTHER = 'Other'
    EVENT_TYPE_CHOICES = (
        (HOSTING, 'Hosting'),
        (REPORTING, 'Reporting'),
        (ADMINISTRATIVE, 'Administrative'),
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

    discussion = models.ForeignKey(
        'Discussion',
        help_text='Id of discussion for the event.',
        blank=True,
        null=True,
    )

    notes = models.ManyToManyField(
        'Note',
        blank=True,
    )


    # an event can be associated with an organization, project, series or story.
    # this can be different than organization that makes the event in the db
    # ex. a user from an org partnering with other orgs is the one to make the event
    # that's being hosted by another organization for the collaborative project.
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

    # assets
    simple_image_assets = models.ManyToManyField(
        SimpleImage,
        blank=True,
    )

    simple_document_assets = models.ManyToManyField(
        SimpleDocument,
        blank=True,
    )

    simple_audio_assets = models.ManyToManyField(
        SimpleAudio,
        blank=True,
    )

    simple_video_assets = models.ManyToManyField(
        SimpleVideo,
        blank=True,
    )

    class Meta:
        verbose_name = 'Event'
        verbose_name_plural = "Events"
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('event_detail', kwargs={'pk': self.id})

    @property
    def search_title(self):
        return self.name

    @property
    def type(self):
        return "Event"

    @property
    def description(self):
        return self.text

    def clean(self):
        """Enforce that there is one relationship."""

        super(Event, self).clean()

        count = (
            (1 if self.evt_organization else 0) +
            (1 if self.project else 0) +
            (1 if self.series else 0) +
            (1 if self.story else 0)
        )

        if count != 1:
            raise ValidationError("Events can only relate to one thing.")
