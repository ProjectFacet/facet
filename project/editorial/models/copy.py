from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from . import DocumentAsset, ImageAsset, AudioAsset, VideoAsset
from . import Facet
from . import Organization, Story


#-----------------------------------------------------------------------#
#   Copy Details:
#   SeriesCopyDetail, StoryCopyDetail
#   FacetCopyDetail
#   ImageAssetCopyDetail, DocumentAssetCopyDetail, AudioFacetCopyDetail, VideoAssetCopyDetail
#-----------------------------------------------------------------------#


# #-----------------------------------------------------------------------#
# #    SERIES
# #-----------------------------------------------------------------------#
#
# class SeriesCopyDetailManager(models.Manager):
#     """Custom manager to create copy records for series. """
#
#     def create_story_copy_record(self, original_org, partner, original_series, partner_series):
#         """Method for quick creation of a copy record."""
#         story_copy_detail=self.create(original_org=original_org, partner=partner, original_series=original_series, partner_series=partner_series)
#         return story_copy_detail
#
#
# @python_2_unicode_compatible
# class SeriesCopyDetail(models.Model):
#     """ The details of each copy of a series.
#
#     Each time an organization elects to copy a shared facet, query to see if the
#     series has already been copied over. If not copy the series and the story to the
#     new organization.
#     """
#
#     original_org = models.ForeignKey(
#         Organization,
#         help_text='Organization that originally created the content.',
#         related_name='original_series_organization',
#     )
#
#     original_series = models.ForeignKey(
#         Series,
#         help_text='Original copy of the series.',
#         related_name='original_series_detail'
#     )
#
#     partner = models.ForeignKey(
#         Organization,
#         help_text='Organization that made the copy.',
#         related_name='series_copying_organization',
#     )
#
#     partner_series = models.ForeignKey(
#         Series,
#         help_text='The new version of the series saved by the partner organization.',
#         related_name='series_copy',
#     )
#
#     copy_date = models.DateTimeField(
#         auto_now_add=True,
#         help_text='Datetime when copy was made.'
#     )
#
#     objects = SeriesCopyDetailManager()
#
#     def __str__(self):
#         return "Copyinfo for {copyorg} \'s copy of series: {series}".format(
#                                 copyorg=self.partner.name,
#                                 series=self.original_series,
#                                 )


#-----------------------------------------------------------------------#
#    STORY
#-----------------------------------------------------------------------#

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


#-----------------------------------------------------------------------#
#    FACET
#-----------------------------------------------------------------------#

class FacetCopyDetailManager(models.Manager):
    """Custom manager for Facet Copy Details."""

    def create_facet_copy_record(self, original_org, partner, original_facet, partner_facet):
        """Method for quick creation of facet copy detail record."""
        facet_copy_detail=self.create(original_org=original_org, partner=partner, original_facet=original_facet, partner_facet=partner_facet)
        return facet_copy_detail


@python_2_unicode_compatible
class FacetCopyDetail(models.Model):
    """ The details of a each copy of a facet. """

    original_org = models.ForeignKey(
        Organization,
        help_text='Organization that originally created the content.',
        related_name='original_facet_organization',
    )

    original_facet = models.ForeignKey(
        Facet,
        help_text='Original copy of the facet.',
        related_name='original_facet_detail',
    )

    partner = models.ForeignKey(
        Organization,
        help_text='Organization that made the copy.',
        related_name='facet_copying_organization',
    )

    partner_facet = models.ForeignKey(
        Facet,
        help_text='The new version of the facet saved by the partner organization.',
        related_name='facet_copy',
    )

    copy_date = models.DateTimeField(
        auto_now_add=True,
        help_text='Datetime when copy was made.'
    )

    objects = FacetCopyDetailManager()

    def __str__(self):
        return "Copyinfo for {copyorg} \'s copy of facet: {facet}".format(
                                copyorg=self.partner.name,
                                facet=self.original_facet,
                                )


#-----------------------------------------------------------------------#
#    ASSETS
#-----------------------------------------------------------------------#

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
