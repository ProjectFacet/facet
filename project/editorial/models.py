""" Model for editorial application. """

from django.db import models

from model_utils.models import TimeStampedModel

from datetime import timedelta

from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from imagekit.processors import ResizeToFit
from imagekit.models import ProcessedImageField


# from django.core.exceptions import ValidationError
# from django.core.urlresolvers import reverse
# from django.core.validators import RegexValidator

# from django.utils import timezone
# from postgres.fields import ArrayField

#----------------------------------------------------#
#   People
#----------------------------------------------------#


class User(models.Model):
    """ Site User.

    A user can either be an admin or a general user. Most users
    can do most things. An admin user can be a site owner, add new
    users, create and manage networks and shift users from active
    to inactive. A general user creates and collaborates on content.
    """

    user_id = models.SlugField(
        max_length=15,
        primary_key=True,
        help_text='Unique code for a user.'
        )

    user_organization_id = models.ForeignKey(Organization)

    user_admin_privilege = models.BooleanField(
        initial = false
        help_text='Is a user able to manage an organization/network and make/remove users.'
        )

    user_fname = models.CharField(
        max_length=45,
        db_index=True,
        )

    user_lname = models.CharField(
        max_length=45,
        db_index=True,
        )

    user_credit_name = models.CharField(
        max_length=75,
        help_text='Full name of user as listed as a credit on content.'
    )

    username = models.CharField(
        max_length=30,
        unique=True,
        help_text='Username as needed for login purposes.'
        )

    user_title = models.CharField(
        max_length=100,
        unique=True,
        help_text='Professional title'
    )

    user_date_joined = models.DateTimeField(
        auto_now_add=True
        )

    user_last_login = models.DateTimeField(
        auto_now = True
        )

    user_is_active = models.BooleanField(
        initial = True
        )

    email = models.EmailField(
        blank=True,
        )

    phone = models.CharField(
        max_length=20,
        blank=True,
        )

    bio = models.TextField(
        help_text="Short bio.",
        blank=True
        )

    profile_photo = models.ImageField(
        upload_to="users",
        blank=True,
        )

    photo_display = ImageSpecField(
        source='photo',
        processors=[ResizeToFit(200, 200)],
        format='JPEG',
        )

    #Links to user's professional social media accounts
    user_facebook = models.CharField(
        max_length=150
        )

    user_twitter = models.CharField(
        max_length=150
    )

    user_linkedin = models.CharField(
        max_length=150
    )

    user_instagram = models.CharField(
        max_length=150
    )

    user_snapchat = models.CharField(
        max_length=150
    )

    user_vine = models.CharField(
        max_length=150
    )

    class Meta:
        verbose_name= = 'Team member'
        verbose_name_plural = "Team members"
        ordering = ['user_credit_name']

    def __str__(self):
        return self.user_credit_name

    @property
    def description(self):
        return "{user}, {title}".format(
                                        user=self.user_credit_name,
                                        title=self.user_title
                                        )


class Organization(models.Model)
    """ Media Organization.

    An organization is a media or publishing entity. Organization's are created
    and owned by one admin user. They can be managed by multiple admin users.
    Organizations have many users and serve as the owner of story content. Organizations
    can create and manage Networks. Ownership of an organization can be transferred
    from one admin user to another.
    """

    organization_id = models.SlugField(
        max_length=15,
        primary_key=True,
        help_text='Unique code for an organization.'
        )

    organization_name = models.CharField(
        max_length=75,
        db_index=True,
        )

    organization_owner = models.ForeignKey(
        User,
        )

    organization_description = models.TextField(
        help_text="Short profile of organization.",
        blank=True
        )

    organization_creation_date = models.DateTimeField(
        auto_now_add=True
        )

    organization_logo = models.ImageField(
        upload_to="organizations",
        blank=True
        )

    logo_display = ImageSpecField(
        source='photo',
        processors=[ResizeToFit(200, 200)],
        format='JPEG',
    )

    class Meta:
        verbose_name= = 'Organization'
        verbose_name_plural = "Organizations"
        ordering = ['organization_name']

    def __str__(self):
        return self.organization_name

    @property
    def description(self):
        return "{organization}, {description}".format(
                                                    organization=self.organization_name,
                                                    description=self.organization_description
                                                    )


class Network(models.Model)
    """ A group of organizations.

    A network is a collection of two or more organizations seeking to create a sharing
    or collaborating relationship. Sharing means the organization can add content that has been
    marked for sharing to that network. Collaborating means that any user from the guest network
    organization(s) can participate in the editorial process on the host organization's content that has been
    selected as collaborative. At the conclusion of the editorial process, the guest can add the final
    version of the content to their own account.
    """

    network_id = models.SlugField(
        max_length=15,
        primary_key=True,
        help_text='Unique identifier for a network'
        )

    network_owner_organization = models.ForeignKey(
        Organization,
        )

    network_name = models.CharField(
        max_length=75,
        db_index=True,
        help_text="The name by which members identify the network."
        )

    network_creation_date = models.DateTimeField(
        auto_now_add=True
        )

    network_description = TextField(
        help_text="Short description of a network.",
        blank=True
        )

    network_logo = models.ImageField(
        upload_to="organizations",
        blank=True
        )

    logo_display = ImageSpecField(
        source='photo',
        processors=[ResizeToFit(200, 200)],
        format='JPEG',
    )

    class Meta:
        verbose_name= = 'Network'
        verbose_name_plural = "Networks"
        ordering = ['network_name']

    def __str__(self):
        return self.network_name

    @property
    def description(self):
        return "{network}, {description}".format(
                                                network=self.network_name,
                                                description=self.network_description
                                                )


class NetworkOrganizaton(models.Model):
    """ The connection between Organizations and Networks. """

    network_organization_id = models.SlugField(
        max_length=15,
        primary_key=True,
        help_text='Unique identifier for a network/organization connection.'
        )

    network_id = models.ForeignKey(
        Network,
        )

    organization_id = models.ForeignKey(
        Organization,
        )

    class Meta:
        unique_together = [['organization_name','network_name']]

    def __str__(self):
        return "{network}, {organization}".format(
                                                network=self.network.network_name,
                                                organization=self.organization.organization_name
                                                )

# #----------------------------------------------------#
# # Content
# #----------------------------------------------------#

# # A series has multiple stories.
# # Stories can have multiple forms.

# class Series(models.Model)
# """ A specific series """
#
#     series_id = models.SlugField(
#         max_length=15,
#         primary_key=True,
#         help_text='unique identifier for a series'
#         )
#
#     series_name = models.CharField(
#         max_length=75,
#         db_index=True,
#     )
#
#     description = TextField(
#         help_text="Short description of a series.",
#         blank=True
#     )


# class Story(models.Model)
# """ The unit of a story """
#
#     story_id = models.SlugField(
#         max_length=15,
#         primary_key=True,
#         help_text='unique identifier for a story'
#         )
#
#     series_id = models.CharField(
#         max_length=75,
#         db_index=True,
#     )
#
#     description = TextField(
#         help_text="Short description of a story.",
#         blank=True
#     )


# # Tracking notes and documents and plans for a story
# class StoryPlans(models.Model)
# """ Planning for a story. """
# pass


# # Assets associated with a story
# class StoryAssets(models.Model)
# """ Assets for a story. """
# pass


# # Notes for the planning of a story
# class StoryNotes(models.Model)
# """ Notes for a story. """
# pass


# # Meta details associated with a story
# # Perhaps place on main story class?
# class StoryMeta(models.Model)
# """ Meta details for a story. """
# pass


# class WebFacet(Story)
# """ Regularly published web content.
# Ex: Daily news, articles, videos, photo galleries
# """
# pass


# class PrintFacet(Story)
# """ The print version of a story.
# Ex: Daily news article, column, story.
# """
# pass


# class AudioFacet(Story)
# """ Scheduled radio programming.
# Ex: A single segment on Morning Edition.
# """
# pass


# class VideoFacet(Story)
# """ Scheduled television programming.
# Ex: An episode of a television program.
# """
# pass
