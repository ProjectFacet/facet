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
from . import Facet, WebFacet, PrintFacet, AudioFacet, VideoFacet   # XXX
from . import DocumentAsset, ImageAsset, AudioAsset, VideoAsset

#-----------------------------------------------------------------------#
#   CopyDetails:
#   SeriesCopyDetail, StoryCopyDetail, WebFacetCopyDetail,
#   PrintFacetCopyDetail, AudioFacetCopyDetail, VideoFacetCopyDetail,
#   ImageAssetCopyDetail, DocumentAssetCopyDetail, AudioFacetCopyDetail
#-----------------------------------------------------------------------#

class SeriesCopyDetailManager(models.Manager):
    """Custom manager to create copy records for series. """

    def create_story_copy_record(self, original_org, partner, original_series, partner_series):
        """Method for quick creation of a copy record."""
        story_copy_detail=self.create(original_org=original_org, partner=partner, original_series=original_series, partner_series=partner_series)
        return story_copy_detail


@python_2_unicode_compatible
class SeriesCopyDetail(models.Model):
    """ The details of each copy of a series.

    Each time an organization elects to copy a shared facet, query to see if the
    series has already been copied over. If not copy the series and the story to the
    new organization.
    """

    original_org = models.ForeignKey(
        Organization,
        help_text='Organization that originally created the content.',
        related_name='original_series_organization',
    )

    original_series = models.ForeignKey(
        Series,
        help_text='Original copy of the series.',
        related_name='original_series_detail'
    )

    partner = models.ForeignKey(
        Organization,
        help_text='Organization that made the copy.',
        related_name='series_copying_organization',
    )

    partner_series = models.ForeignKey(
        Series,
        help_text='The new version of the series saved by the partner organization.',
        related_name='series_copy',
    )

    copy_date = models.DateTimeField(
        auto_now_add=True,
        help_text='Datetime when copy was made.'
    )

    objects = SeriesCopyDetailManager()

    def __str__(self):
        return "Copyinfo for {copyorg} \'s copy of series: {series}".format(
                                copyorg=self.partner.name,
                                series=self.original_series,
                                )


class StoryCopyDetailManager(models.Manager):
    """Custom manager to create copy records for stories. """

    def create_story_copy_record(self, original_org, partner, original_story, partner_story):
        """Method for quick creation of a copy record."""
        story_copy_detail=self.create(original_org=original_org, partner=partner, original_story=original_story, partner_story=partner_story)
        return story_copy_detail


@python_2_unicode_compatible
class StoryCopyDetail(models.Model):
    """ The details of each copy of a story.

    Each time an organization elects to copy a shared facet, query to see if the
    story has already been copied over. If not, copy the story to the new organization.
    """

    original_org = models.ForeignKey(
        Organization,
        help_text='Organization that originally created the content.',
        related_name='original_story_organization',
    )

    original_story = models.ForeignKey(
        Story,
        help_text='Original copy of the story.',
        related_name='original_story_detail',
    )

    partner = models.ForeignKey(
        Organization,
        help_text='Organization that made the copy.',
        related_name='story_copying_organization',
    )

    partner_story = models.ForeignKey(
        Story,
        help_text='The new version of the story saved by the partner organization.',
        related_name='story_copy',
    )

    copy_date = models.DateTimeField(
        auto_now_add=True,
        help_text='Datetime when copy was made.'
    )

    objects = StoryCopyDetailManager()

    def __str__(self):
        return "Copyinfo for {copyorg} \'s copy of story: {story}".format(
                                copyorg=self.partner.name,
                                story=self.original_story,
                                )


class WebFacetCopyDetailManager(models.Manager):
    """Custom manager for WebFacet Copy Details."""

    def create_webfacet_copy_record(self, original_org, partner, original_webfacet, partner_webfacet):
        """Method for quick creation of webfacet copy detail record."""
        webfacet_copy_detail=self.create(original_org=original_org, partner=partner, original_webfacet=original_webfacet, partner_webfacet=partner_webfacet)
        return webfacet_copy_detail


@python_2_unicode_compatible
class WebFacetCopyDetail(models.Model):
    """ The details of a each copy of a webfacet. """

    original_org = models.ForeignKey(
        Organization,
        help_text='Organization that originally created the content.',
        related_name='original_webfacet_organization',
    )

    original_webfacet = models.ForeignKey(
        WebFacet,
        help_text='Original copy of the webfacet.',
        related_name='original_webfacet_detail',
    )

    partner = models.ForeignKey(
        Organization,
        help_text='Organization that made the copy.',
        related_name='webfacet_copying_organization',
    )

    partner_webfacet = models.ForeignKey(
        WebFacet,
        help_text='The new version of the webfacet saved by the partner organization.',
        related_name='webfacet_copy',
    )

    copy_date = models.DateTimeField(
        auto_now_add=True,
        help_text='Datetime when copy was made.'
    )

    objects = WebFacetCopyDetailManager()

    def __str__(self):
        return "Copyinfo for {copyorg} \'s copy of webfacet: {webfacet}".format(
                                copyorg=self.partner.name,
                                webfacet=self.original_webfacet,
                                )


class PrintFacetCopyDetailManager(models.Manager):
    """Custom manager for PrintFacet Copy Details."""

    def create_printfacet_copy_record(self, original_org, partner, original_printfacet, partner_printfacet):
        """Method for quick creation of printfacet copy detail record."""
        printfacet_copy_detail=self.create(original_org=original_org, partner=partner, original_printfacet=original_printfacet, partner_printfacet=partner_printfacet)
        return printfacet_copy_detail


@python_2_unicode_compatible
class PrintFacetCopyDetail(models.Model):
    """ The details of a each copy of a printfacet. """

    original_org = models.ForeignKey(
        Organization,
        help_text='Organization that originally created the content.',
        related_name='original_printfacet_organization',
    )

    original_printfacet = models.ForeignKey(
        PrintFacet,
        help_text='Original copy of the printfacet.',
        related_name='original_printfacet_detail',
    )

    partner = models.ForeignKey(
        Organization,
        help_text='Organization that made the copy.',
        related_name='printfacet_copying_organization',
    )

    partner_printfacet = models.ForeignKey(
        PrintFacet,
        help_text='The new version of the printfacet saved by the partner organization.',
        related_name='printfacet_copy',
    )

    copy_date = models.DateTimeField(
        auto_now_add=True,
        help_text='Datetime when copy was made.'
    )

    objects = PrintFacetCopyDetailManager()

    def __str__(self):
        return "Copyinfo for {copyorg} \'s copy of printfacet: {printfacet}".format(
                                copyorg=self.partner.name,
                                printfacet=self.original_printfacet,
                                )


class AudioFacetCopyDetailManager(models.Manager):
    """Custom manager for AudioFacet Copy Details."""

    def create_audiofacet_copy_record(self, original_org, partner, original_audiofacet, partner_audiofacet):
        """Method for quick creation of audiofacet copy detail record."""
        audiofacet_copy_detail=self.create(original_org=original_org, partner=partner, original_audiofacet=original_audiofacet, partner_audiofacet=partner_audiofacet)
        return audiofacet_copy_detail


@python_2_unicode_compatible
class AudioFacetCopyDetail(models.Model):
    """ The details of a each copy of a audiofacet. """

    original_org = models.ForeignKey(
        Organization,
        help_text='Organization that originally created the content.',
        related_name='original_audiofacet_organization',
    )

    original_audiofacet = models.ForeignKey(
        AudioFacet,
        help_text='Original copy of the audiofacet.',
        related_name='original_audiofacet_detail',
    )

    partner = models.ForeignKey(
        Organization,
        help_text='Organization that made the copy.',
        related_name='audiofacet_copying_organization',
    )

    partner_audiofacet = models.ForeignKey(
        AudioFacet,
        help_text='The new version of the audiofacet saved by the partner organization.',
        related_name='audiofacet_copy',
    )

    copy_date = models.DateTimeField(
        auto_now_add=True,
        help_text='Datetime when copy was made.'
    )

    objects = AudioFacetCopyDetailManager()

    def __str__(self):
        return "Copyinfo for {copyorg} \'s copy of audiofacet: {audiofacet}".format(
                                copyorg=self.partner.name,
                                audiofacet=self.original_audiofacet,
                                )


class VideoFacetCopyDetailManager(models.Manager):
    """Custom manager for VideoFacet Copy Details."""

    def create_videofacet_copy_record(self, original_org, partner, original_videofacet, partner_videofacet):
        """Method for quick creation of videofacet copy detail record."""
        videofacet_copy_detail=self.create(original_org=original_org, partner=partner, original_videofacet=original_videofacet, partner_videofacet=partner_videofacet)
        return videofacet_copy_detail


@python_2_unicode_compatible
class VideoFacetCopyDetail(models.Model):
    """ The details of a each copy of a videofacet. """

    original_org = models.ForeignKey(
        Organization,
        help_text='Organization that originally created the content.',
        related_name='original_videofacet_organization',
    )

    original_videofacet = models.ForeignKey(
        VideoFacet,
        help_text='Original copy of the videofacet.',
        related_name='original_videofacet_detail',
    )

    partner = models.ForeignKey(
        Organization,
        help_text='Organization that made the copy.',
        related_name='videofacet_copying_organization',
    )

    partner_videofacet = models.ForeignKey(
        VideoFacet,
        help_text='The new version of the videofacet saved by the partner organization.',
        related_name='videofacet_copy',
    )

    copy_date = models.DateTimeField(
        auto_now_add=True,
        help_text='Datetime when copy was made.',
    )

    objects = VideoFacetCopyDetailManager()

    def __str__(self):
        return "Copyinfo for {copyorg} \'s copy of videofacet: {videofacet}".format(
                                copyorg=self.partner.name,
                                videofacet=self.original_videofacet,
                                )


class ImageAssetCopyDetailManager(models.Manager):
    """Custom manager for ImageAsset Copy Details."""

    def create_imageasset_copy_record(self, original_org, original_imageasset, partner, partner_imageasset):
        """Method for quick creation of image copy detail recod."""
        imageasset_copy_detail=self.create(
                                        original_org=original_org,
                                        original_imageasset=original_imageasset,
                                        partner=partner,
                                        partner_imageasset=partner_imageasset)
        return imageasset_copy_detail


@python_2_unicode_compatible
class ImageAssetCopyDetail(models.Model):
    """ The details of each copy of an ImageAsset."""

    original_org = models.ForeignKey(
        Organization,
        help_text='Organization that originally created the content',
        related_name='original_imageasset_organization',
    )

    original_imageasset = models.ForeignKey(
        ImageAsset,
        help_text='Original copy of the imageasset',
        related_name='original_imageasset_detail',
    )

    partner = models.ForeignKey(
        Organization,
        help_text='Organization that made the copy.',
        related_name='imageasset_copying_organization',
    )

    partner_imageasset = models.ForeignKey(
        ImageAsset,
        help_text='The copied version of the imageasset saved by the partner organization.',
        related_name='imageasset_copy',
    )

    copy_date = models.DateTimeField(
        auto_now_add=True,
        help_text='Datetime when copy was made.',
    )

    objects = ImageAssetCopyDetailManager()

    def __str__(self):
        return "Copyinfo for {copyorg} \'s copy of imageasset: {imageasset}".format(
                                copyorg=self.partner.name,
                                imageasset=self.original_imageasset,
        )


class DocumentAssetCopyDetailManager(models.Manager):
    """Custom manager for DocumentAsset Copy Details."""

    def create_documentasset_copy_record(self, original_org, original_documentasset, partner, partner_documentasset):
        """Method for quick creation of document copy detail recod."""
        documentasset_copy_detail=self.create(
                                        original_org=original_org,
                                        original_documentasset=original_documentasset,
                                        partner=partner,
                                        partner_documentasset=partner_documentasset)
        return documentasset_copy_detail


@python_2_unicode_compatible
class DocumentAssetCopyDetail(models.Model):
    """ The details of each copy of an DocumentAsset."""

    original_org = models.ForeignKey(
        Organization,
        help_text='Organization that originally created the content',
        related_name='original_documentasset_organization',
    )

    original_documentasset = models.ForeignKey(
        DocumentAsset,
        help_text='Original copy of the documentasset',
        related_name='original_documentasset_detail',
    )

    partner = models.ForeignKey(
        Organization,
        help_text='Organization that made the copy.',
        related_name='documentasset_copying_organization',
    )

    partner_documentasset = models.ForeignKey(
        DocumentAsset,
        help_text='The copied version of the documentasset saved by the partner organization.',
        related_name='documentasset_copy',
    )

    copy_date = models.DateTimeField(
        auto_now_add=True,
        help_text='Datetime when copy was made.',
    )

    objects = DocumentAssetCopyDetailManager()

    def __str__(self):
        return "Copyinfo for {copyorg} \'s copy of documentasset: {documentasset}".format(
                                copyorg=self.partner.name,
                                documentasset=self.original_documentasset,
        )


class AudioAssetCopyDetailManager(models.Manager):
    """Custom manager for AudioAsset Copy Details."""

    def create_audioasset_copy_record(self, original_org, original_audioasset, partner, partner_audioasset):
        """Method for quick creation of audio copy detail recod."""
        audioasset_copy_detail=self.create(
                                        original_org=original_org,
                                        original_audioasset=original_audioasset,
                                        partner=partner,
                                        partner_audioasset=partner_audioasset)
        return audioasset_copy_detail


@python_2_unicode_compatible
class AudioAssetCopyDetail(models.Model):
    """ The details of each copy of an AudioAsset."""

    original_org = models.ForeignKey(
        Organization,
        help_text='Organization that originally created the content',
        related_name='original_audioasset_organization',
    )

    original_audioasset = models.ForeignKey(
        AudioAsset,
        help_text='Original copy of the audioasset',
        related_name='original_audioasset_detail',
    )

    partner = models.ForeignKey(
        Organization,
        help_text='Organization that made the copy.',
        related_name='audioasset_copying_organization',
    )

    partner_audioasset = models.ForeignKey(
        AudioAsset,
        help_text='The copied version of the audioasset saved by the partner organization.',
        related_name='audioasset_copy',
    )

    copy_date = models.DateTimeField(
        auto_now_add=True,
        help_text='Datetime when copy was made.',
    )

    objects = AudioAssetCopyDetailManager()

    def __str__(self):
        return "Copyinfo for {copyorg} \'s copy of audioasset: {audioasset}".format(
                                copyorg=self.partner.name,
                                audioasset=self.original_audioasset,
        )


class VideoAssetCopyDetailManager(models.Manager):
    """Custom manager for VideoAsset Copy Details."""

    def create_videoasset_copy_record(self, original_org, original_videoasset, partner, partner_videoasset):
        """Method for quick creation of video copy detail recod."""
        videoasset_copy_detail=self.create(
                                        original_org=original_org,
                                        original_videoasset=original_videoasset,
                                        partner=partner,
                                        partner_videoasset=partner_videoasset)
        return videoasset_copy_detail


@python_2_unicode_compatible
class VideoAssetCopyDetail(models.Model):
    """ The details of each copy of an VideoAsset."""

    original_org = models.ForeignKey(
        Organization,
        help_text='Organization that originally created the content',
        related_name='original_videoasset_organization',
    )

    original_videoasset = models.ForeignKey(
        VideoAsset,
        help_text='Original copy of the videoasset',
        related_name='original_videoasset_detail',
    )

    partner = models.ForeignKey(
        Organization,
        help_text='Organization that made the copy.',
        related_name='videoasset_copying_organization',
    )

    partner_videoasset = models.ForeignKey(
        VideoAsset,
        help_text='The copied version of the videoasset saved by the partner organization.',
        related_name='videoasset_copy',
    )

    copy_date = models.DateTimeField(
        auto_now_add=True,
        help_text='Datetime when copy was made.',
    )

    objects = VideoAssetCopyDetailManager()

    def __str__(self):
        return "Copyinfo for {copyorg} \'s copy of videoasset: {videoasset}".format(
                                copyorg=self.partner.name,
                                videoasset=self.original_videoasset,
        )
