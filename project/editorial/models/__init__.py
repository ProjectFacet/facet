""" Model for editorial application.

    Tables
    ---------
    People:
    - User, Organization, Network

    Content:
    - Project, Series, Story, WebFacet, PrintFacet, AudioFacet, VideoFacet

    Contributor Associations:
    - WebFacetContributors, PrintFacetContributors, AudioFacetContributors,
      VideoFacetContributors,

    Copy Details:
    - StoryCopyDetails, SeriesCopyDetails, WebFacetCopyDetails,
      PrintFacetCopyDetails, AudioFacetCopyDetails, VideoFacetCopyDetails

    Assets:
    - ImageAsset, DocumentAsset, AudioAsset, VideoAsset

    Notes:
    - Note, NetworkNote, OrganizationNote, UserNote, SeriesNote, StoryNote

    Discussion:
    - Discussion, PrivateDiscussion, PrivateMessage, Comment, CommentReadStatus


"""

from django.db import models
from django.db.models import Q
from django.contrib.postgres.fields import ArrayField
from simple_history.models import HistoricalRecords
from model_utils.models import TimeStampedModel
import time as timemk
from datetime import datetime, timedelta, time
from imagekit.models import ProcessedImageField, ImageSpecField
from pilkit.processors import ResizeToFit, SmartResize
from django.contrib.auth.models import AbstractUser
from django.utils.encoding import python_2_unicode_compatible
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.shortcuts import get_object_or_404
from itertools import chain
from embed_video.fields import EmbedVideoField
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save
from django.dispatch import receiver


from .people import User, Organization, Network
from .assets import ImageAsset, DocumentAsset, AudioAsset, VideoAsset
from .assets import SimpleImage, SimpleDocument, SimpleAudio, SimpleVideo
from .discussion import Discussion, Comment, PrivateMessage
from .projects import Project
from .series import Series
from .story import Story
from .facets import Facet, WebFacet, AudioFacet, VideoFacet, PrintFacet # XXX
from .notes import OrganizationNote, ProjectNote, SeriesNote, StoryNote, UserNote, NetworkNote
from .platforms import Platform, PlatformAccount
from .tasks import Task
from .events import Event
from .copy import *   # XXX

# from .freelancers import FreelancerInfo, OrganizationFreelancerInfo



#-----------------------------------------------------------------------#
#   Content:
#   Project, Series, Story, WebFacet, PrintFacet, AudioFacet, VideoFacet
#   (A Facet is always part of a story, even if there is only one facet.)
#-----------------------------------------------------------------------#




#-----------------------------------------------------------------------#
#   Secondary Content:
#   Tasks, Events, Social Posts
#-----------------------------------------------------------------------#


#-----------------------------------------------------------------------#
#  SOCIAL POST
#-----------------------------------------------------------------------#

# FIXME Leaving this commented out for now to think about how to best
# relate or make use of Platform and PlatformAccount in the options.

# class SocialPost(models.Model):
#     """A social post.
#
#     A social post to promote a project, series, story or event.
#     """
#
#     FACEBOOK = 'Facebook'
#     TWITTER = 'Twitter'
#     INSTAGRAM = 'Instagram'
#     SOCIAL_ACCOUNT_CHOICES = (
#         (FACEBOOK, 'Facebook'),
#         (TWITTER, 'Twitter'),
#         (INSTAGRAM, 'Instagram'),
#     )
#
#     social_platform = models.CharField(
#         max_length=50,
#         choices=SOCIAL_ACCOUNT_CHOICES,
#         help_text='Platform the post is created for.'
#     )
#
#     text = models.TextField(
#         help_text='Content of the post.'
#     )
#
#     # a social post can be associated with a project, series, story or an event.
#     #TODO Add connection to P, Se, St, or E
#
#     #TODO Add Image assets for social posts to Assets section.
#



#-----------------------------------------------------------------------#
# GoverningDocumentAsset
#
# class GoverningDocumentAssetManager(models.Manager):
#     """Custom manager for GoverningDocumentAsset."""
#
#     def create_governingdocumentasset(self, owner, organization, asset_title, asset_description, asset_attribution, document, doc_type, keywords):
#         """Method for quick creation of a document asset."""
#         documentasset=self.create(owner=owner, organization=organization, asset_title=asset_title, asset_description=asset_description, asset_attribution=asset_attribution, document=document, doc_type=doc_type, keywords=keywords)
#         return documentasset
#
#
# @python_2_unicode_compatible
# class GoverningDocumentAsset(models.Model):
#     """ Uploaded Governing Document Asset. """
#
#     owner = models.ForeignKey(
#         User,
#         related_name='governing_document_asset_owner',
#     )
#
#     organization = models.ForeignKey(
#         Organization,
#         related_name='governing_document_asset_organization'
#     )
#
#     original = models.BooleanField(
#         default=True,
#         help_text='This content originally belonged to this organization.'
#     )
#
#     asset_title = models.CharField(
#         max_length=200,
#         help_text='Text for file name. Name it intuitively.',
#         blank=True,
#     )
#
#     asset_description = models.TextField(
#         max_length=300,
#         help_text='What is the asset.',
#         blank=True,
#     )
#
#     attribution = models.TextField(
#         max_length=200,
#         help_text='The appropriate information for crediting the asset.',
#         blank=True,
#     )
#
#     document = models.FileField(
#         upload_to='governing documents',
#         blank=True,
#     )
#
#     #Choices for Asset type
#     PDF = 'PDF'
#     WORD = 'WORD DOC'
#     TXT =  'TEXT'
#     CSV = 'COMMA SEPARATED'
#     XLS = 'EXCEL'
#     OTHER = 'OTHER'
#
#     DOCUMENT_TYPE_CHOICES = (
#         (PDF, 'Adobe PDF'),
#         (WORD, 'Word Doc'),
#         (TXT, 'Text File'),
#         (CSV, 'Comma Separated'),
#         (XLS, 'Excel File'),
#         (OTHER, 'Other'),
#     )
#
#     doc_type = models.CharField(
#         max_length=20,
#         choices = DOCUMENT_TYPE_CHOICES,
#         help_text='The kind of document.'
#     )
#
#     creation_date = models.DateTimeField(
#         auto_now_add=True,
#         help_text='When the asset was created.'
#     )
#
#     keywords = ArrayField(
#         models.CharField(max_length=100),
#         default=list,
#         help_text='List of keywords for search.',
#         blank=True,
#     )
#
#     objects = GoverningDocumentAssetManager()
#
#     class Meta:
#         verbose_name = "Governing Document"
#         verbose_name_plural = "Governing Documents"
#
#     def __str__(self):
#         return self.asset_title
#
#     # def get_absolute_url(self):
#     #     return reverse('document_asset_detail', kwargs={'pk': self.id})
#
#     @property
#     def description(self):
#         return self.asset_description.encode('utf-8')
#
#     @property
#     def search_title(self):
#         return self.asset_title
#
#     @property
#     def type(self):
#         return "Governing Document"
#
#
#
# #-----------------------------------------------------------------------#
# # ProjectDocumentAsset
#
# class ProjectDocumentAssetManager(models.Manager):
#     """Custom manager for ProjectDocumentAsset."""
#
#     def create_projectdocumentasset(self, owner, organization, asset_title, asset_description, asset_attribution, document, doc_type, keywords):
#         """Method for quick creation of a document asset."""
#         documentasset=self.create(owner=owner, organization=organization, asset_title=asset_title, asset_description=asset_description, asset_attribution=asset_attribution, document=document, doc_type=doc_type, keywords=keywords)
#         return documentasset
#
#
# @python_2_unicode_compatible
# class ProjectDocumentAsset(models.Model):
#     """ Uploaded Project Document Asset. """
#
#     owner = models.ForeignKey(
#         User,
#         related_name='project_document_asset_owner',
#     )
#
#     organization = models.ForeignKey(
#         Organization,
#         related_name='project_document_asset_organization'
#     )
#
#     original = models.BooleanField(
#         default=True,
#         help_text='This content originally belonged to this organization.'
#     )
#
#     asset_title = models.CharField(
#         max_length=200,
#         help_text='Text for file name. Name it intuitively.',
#         blank=True,
#     )
#
#     asset_description = models.TextField(
#         max_length=300,
#         help_text='What is the asset.',
#         blank=True,
#     )
#
#     attribution = models.TextField(
#         max_length=200,
#         help_text='The appropriate information for crediting the asset.',
#         blank=True,
#     )
#
#     document = models.FileField(
#         upload_to='project documents',
#         blank=True,
#     )
#
#     #Choices for Asset type
#     PDF = 'PDF'
#     WORD = 'WORD DOC'
#     TXT =  'TEXT'
#     CSV = 'COMMA SEPARATED'
#     XLS = 'EXCEL'
#     OTHER = 'OTHER'
#
#     DOCUMENT_TYPE_CHOICES = (
#         (PDF, 'Adobe PDF'),
#         (WORD, 'Word Doc'),
#         (TXT, 'Text File'),
#         (CSV, 'Comma Separated'),
#         (XLS, 'Excel File'),
#         (OTHER, 'Other'),
#     )
#
#     doc_type = models.CharField(
#         max_length=20,
#         choices = DOCUMENT_TYPE_CHOICES,
#         help_text='The kind of document.'
#     )
#
#     creation_date = models.DateTimeField(
#         auto_now_add=True,
#         help_text='When the asset was created.'
#     )
#
#     keywords = ArrayField(
#         models.CharField(max_length=100),
#         default=list,
#         help_text='List of keywords for search.',
#         blank=True,
#     )
#
#     objects = ProjectDocumentAssetManager()
#
#     class Meta:
#         verbose_name = "Project Document"
#         verbose_name_plural = "Project Documents"
#
#     def __str__(self):
#         return self.asset_title
#
#     # def get_absolute_url(self):
#     #     return reverse('document_asset_detail', kwargs={'pk': self.id})
#
#     @property
#     def description(self):
#         return self.asset_description.encode('utf-8')
#
#     @property
#     def search_title(self):
#         return self.asset_title
#
#     @property
#     def type(self):
#         return "Project Document"
