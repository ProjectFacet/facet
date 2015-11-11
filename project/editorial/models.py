""" Model for editorial application. """

from django.db import models
from datetime import timedelta
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from imagekit.processors import ResizeToFit
from imagekit.models import ProcessedImageField


# from django.core.exceptions import ValidationError
# from django.core.urlresolvers import reverse
# from django.core.validators import RegexValidator
# from django.db import models
# from django.utils import timezone
# from postgres.fields import ArrayField

# Models

#----------------------------------------------------#
# Users and permissions
#----------------------------------------------------#


class User(models.Model):
    """ Site User """

    # STATUS = (
    #     ('ft', 'Full-time'),
    #     ('pt', 'Part-time'),
    #     ('fr', 'Freelance'),
    #     ('co', 'Contract'),
    # )
    #
    # PERMISSIONS = (
    #     ('noncontent', 'Noncontent'),
    #     ('affiliate', 'Affiliate'),
    #     ('contributor', 'Contributor'),
    #     ('staff', 'Staff'),
    #     ('editor', 'Editor'),
    #     ('administrator', 'Administrator'),
    # )

    user_id = models.SlugField(
        max_length=15,
        primary_key=True,
        help_text='Unique code for a user.'
        )

    first_name = models.CharField(
        max_length=45,
        db_index=True,
        )

    last_name = models.CharField(
        max_length=45,
        db_index=True,
        )

    username = models.CharField(
        max_length=30
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

    # status = models.CharField(
    #     max_length=1,
    #     choice=STATUS
    #     )

    # permissions = models.CharField(
    #     max_length=1,
    #     choice=PERMISSIONS
    #     )

    profile_photo = models.ImageField(
        upload_to="users",
        blank=True,
        )

    photo_display = ImageSpecField(
        source='photo',
        processors=[ResizeToFit(200, 200)],
        format='JPEG',
        )

    facebook_un = models.CharField(
        max_length=75
        )

    twitter_un = models.CharField(
        max_length=75
    )

    linkedin_un = models.CharField(
        max_length=75
    )


# class Organization(models.Model)
# """ Media Organization """
#
#     org_id = models.SlugField(
#         max_length=15,
#         primary_key=True,
#         help_text='Unique code for a user.'
#         )
#
#     org_name = models.CharField(
#         max_length=75,
#         db_index=True,
#         )
#
#     description = TextField(
#         help_text="Short profile of organization.",
#         blank=True
#         )
#
#     org_logo = models.ImageField(
#         upload_to="organizations",
#         blank=True
#         )
#
#     photo_display = ImageSpecField(
#         source='photo',
#         processors=[ResizeToFit(200, 200)],
#         format='JPEG',
#     )
#
#
# class Network(models.Model)
# """ A group of organizations. """
#
#     network_id = models.SlugField(
#         max_length=15,
#         primary_key=True,
#         help_text='unique identifier for a network'
#         )
#
#     network_name = models.CharField(
#         max_length=75,
#         db_index=True,
#         )
#
#     description = TextField(
#         help_text="Short description of a network.",
#         blank=True
#         )
#
# #----------------------------------------------------#
# # Content
# #----------------------------------------------------#
#
# # A series has multiple stories.
# # Stories can have multiple forms.
#
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
#
#
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
#
#
# # Tracking notes and documents and plans for a story
# class StoryPlans(models.Model)
# """ Planning for a story. """
# pass
#
#
# # Assets associated with a story
# class StoryAssets(models.Model)
# """ Assets for a story. """
# pass
#
#
# # Notes for the planning of a story
# class StoryNotes(models.Model)
# """ Notes for a story. """
# pass
#
#
# # Meta details associated with a story
# # Perhaps place on main story class?
# class StoryMeta(models.Model)
# """ Meta details for a story. """
# pass
#
#
# class WebForms(Story)
# """ Regularly published web content.
# Ex: Daily news, articles, videos, photo galleries
# """
# pass
#
#
# class PrintForm(Story)
# """ The print version of a story.
# Ex: Daily news article, column, story.
# """
# pass
#
#
# class RadioForm(Story)
# """ Scheduled radio programming.
# Ex: A single segment on Morning Edition.
# """
# pass
#
#
# class TvForm(Story)
# """ Scheduled television programming.
# Ex: An episode of a television program.
# """
# pass
