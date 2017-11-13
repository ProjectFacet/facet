from django.db import models
from django.db.models import Q
from django.contrib.postgres.fields import ArrayField
from imagekit.models import ProcessedImageField, ImageSpecField
from django.utils.encoding import python_2_unicode_compatible
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404

from .people import User, Organization

#-----------------------------------------------------------------------#
#   Assets:
#   BaseAsset, BaseAssetMetadata, BaseImage, BaseDocument, BaseAudio, BaseVideo
#   ImageAsset, DocumentAsset, AudioAsset, VideoAsset,
#-----------------------------------------------------------------------#

@python_2_unicode_compatible
class BaseAsset(models.Model):
    """Base class for assets (some metadata)."""

    owner = models.ForeignKey(
        User,
    )

    organization = models.ForeignKey(
        Organization,
    )

    title = models.CharField(
        max_length=200,
        help_text='Text for file name. Name it intuitively.',
        blank=True,
    )

    description = models.TextField(
        max_length=300,
        help_text='What is the asset. (If a photo or graphic, it should be the caption.)',
        blank=True,
    )

    creation_date = models.DateTimeField(
        auto_now_add=True,
        help_text='When the asset was created.'
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.title

    @property
    def search_title(self):
        return self.title


class BaseAssetMetadata(models.Model):
    """Base class for facet-attaching asset metadata.

    Used for asset types that are attached to facets.
    """

    original = models.BooleanField(
        default=True,
        help_text='This content originally belonged to this organization.'
    )

    attribution = models.TextField(
        max_length=200,
        help_text='The appropriate information for crediting the asset.',
        blank=True,
    )

    keywords = ArrayField(
        models.CharField(max_length=100),
        default=list,
        help_text='List of keywords for search.',
        blank=True,
    )

    class Meta:
        abstract = True

    def copy_image(self):
        """ Create a copy of an asset for a partner organization in a network.

        Copied assets keep all associated information. Organization is set to
        the copier's organization and the original flag is set to false.
        Triggering a copy also triggers the creation of an asset copy detail record."""

        # FIXME Q for J:
        # Unclear how to generalize this for base when there are still 4 asset types

        image_copy = get_object_or_404(ImageAsset, id=self.id)
        #set the id = None to create the copy of the image instance
        image_copy.id = None
        image_copy.save()
        image_copy.original = False
        image_copy.save()
        return image_copy

    def get_asset_download_info(self):
        """Return rst of asset information for download."""

        title = self.title.encode('utf-8')
        description = self.description.encode('utf-8')
        attribution = self.attribution.encode('utf-8')

        asset_info="""
        {type}
        =======
        {title}.jpg
        Description: {description}
        Attribution: {attribution}
        Creation Date: {date}
        Owner: {owner}
        Organization: {organization}
        Original: {original}
        Keywords: {keywords}
        """.format(title=title, description=description, attribution=attribution,
        type=asset_type, date=self.creation_date, owner=self.owner,
        organization=self.organization.name, original=self.original,
        keywords=self.keywords)

        return image_info

#-----------------------------------------------------------------------#
#   Image Asset
#-----------------------------------------------------------------------#


class BaseImage(BaseAsset):
    """Base class for image assets (an image with some metadata).

    Used for ImageAssets (attached to facets) as well as SimpleAssets
    (attached for tasks, notes, etc).
    """

    # type name for search system
    type = "Image"

    photo = models.ImageField(
        upload_to='photos',
        blank=True,
    )

    display_photo = ImageSpecField(
        source='photo',
        format='JPEG',
    )

    class Meta:
        abstract = True


class ImageAssetManager(models.Manager):
    """Custom manager for ImageAsset."""

    def create_imageasset(self, owner, organization, title, description, attribution, photo, asset_type, keywords):
        """Method for quick creation of an image asset."""

        imageasset=self.create(owner=owner, organization=organization, title=title, description=description, attribution=attribution, photo=photo, asset_type=asset_type, keywords=keywords)
        return imageasset


class ImageAsset(BaseImage, BaseAssetMetadata):
    """ Uploaded Image Asset for a facet. """

    #Choices for Asset type
    PHOTO = 'PIC'
    GRAPHIC = 'GRAPH'

    ASSET_TYPE_CHOICES = (
        (PHOTO, 'Photograph'),
        (GRAPHIC, 'Graphic or Illustration'),
    )

    asset_type = models.CharField(
        max_length=20,
        choices = ASSET_TYPE_CHOICES,
        help_text='The kind of image.'
    )

    objects = ImageAssetManager()

    def get_image_usage(self):
        """Return facets an image is associated with."""

        # After Facet refactor
        # image_usage = Facet.objects.filter(Q(image_assets=self))

        image_usage = []
        image_webfacets = WebFacet.objects.filter(Q(image_assets=self))
        image_printfacets = PrintFacet.objects.filter(Q(image_assets=self))
        image_audiofacets = AudioFacet.objects.filter(Q(image_assets=self))
        image_videofacets = VideoFacet.objects.filter(Q(image_assets=self))
        image_usage.extend(image_webfacets)
        image_usage.extend(image_printfacets)
        image_usage.extend(image_audiofacets)
        image_usage.extend(image_videofacets)
        return image_usage

    def get_absolute_url(self):
        return reverse('image_asset_detail', kwargs={'pk': self.id})


class SimpleImage(BaseImage):
    """Simple image (with some metadata) for attaching to tasks, events, etc."""


#-----------------------------------------------------------------------#
# DocumentAsset
#-----------------------------------------------------------------------#

class BaseDocumentAsset(BaseAsset):
    """Base documents.

    There are subclasses of this for DocumentAssets (attached to facets with lots of
    metadata) and SimpleDocuments (attached to tasks, events, etc).
    """

    # type name for search system
    type = "Document"

    document = models.FileField(
        upload_to='documents',
        blank=True,
    )

    class Meta:
        abstract = True


class DocumentAssetManager(models.Manager):
    """Custom manager for DocumentAsset."""

    def create_documentasset(self, owner, organization, title, description, attribution, document, asset_type, keywords):
        """Method for quick creation of a document asset."""
        documentasset=self.create(owner=owner, organization=organization, title=title, description=description, attribution=attribution, document=document, asset_type=asset_type, keywords=keywords)
        return documentasset


class DocumentAsset(BaseDocumentAsset, BaseAssetMetadata):
    """Document Assets (attached to facets)"""

    #Choices for Asset type
    PDF = 'PDF'
    WORD = 'WORD DOC'
    TXT =  'TEXT'
    CSV = 'COMMA SEPARATED'
    XLS = 'EXCEL'
    OTHER = 'OTHER'

    ASSET_TYPE_CHOICES = (
        (PDF, 'Adobe PDF'),
        (WORD, 'Word Doc'),
        (TXT, 'Text File'),
        (CSV, 'Comma Separated'),
        (XLS, 'Excel File'),
        (OTHER, 'Other'),
    )

    asset_type = models.CharField(
        max_length=20,
        choices = ASSET_TYPE_CHOICES,
        help_text='The kind of document.'
    )

    objects = DocumentAssetManager()

    def get_document_usage(self):
        """Return facets a document is associated with."""

        # After Facet refactor
        # document_usage = Facet.objects.filter(Q(document_assets=self))

        document_usage = []
        document_webfacets = WebFacet.objects.filter(Q(document_assets=self))
        document_printfacets = PrintFacet.objects.filter(Q(document_assets=self))
        document_audiofacets = AudioFacet.objects.filter(Q(document_assets=self))
        document_videofacets = VideoFacet.objects.filter(Q(document_assets=self))
        document_usage.extend(document_webfacets)
        document_usage.extend(document_printfacets)
        document_usage.extend(document_audiofacets)
        document_usage.extend(document_videofacets)
        return document_usage

    # def get_absolute_url(self):
    #     return reverse('document_asset_detail', kwargs={'pk': self.id})


class SimpleDocument(BaseDocumentAsset):
    """Simple Document (file upload, attached to events, tasks, etc.)"""


#-----------------------------------------------------------------------#
# AudioAsset
#-----------------------------------------------------------------------#

class BaseAudio(BaseAsset):
    """Base type for audio files.

    Subclassed by AudioAsset and SimpleAudio.
    """

    # metadata for search system
    type = "Audio"

    audio = models.FileField(
        upload_to='audio',
        blank=True,
    )

    link = models.URLField(
        max_length=400,
        help_text='Link to audio file on SoundCloud',
        blank=True,
    )

    class Meta:
        abstract = True


class AudioAssetManager(models.Manager):
    """Custom manager for AudioAsset."""

    def create_audioasset(self, owner, organization, title, description, attribution, audio, asset_type, keywords):
        """Method for quick creation of a audio asset."""
        audioasset=self.create(owner=owner, organization=organization, title=title, description=description, attribution=attribution, audio=audio, asset_type=asset_type, keywords=keywords)
        return audioasset


class AudioAsset(BaseAudio, BaseAssetMetadata):
    """Audio asset (attaches to a facet)"""

    #Choices for Asset type
    MP3 = 'MP3'
    WAV = 'WAV'
    SOUNDCLOUD = 'SC'

    ASSET_TYPE_CHOICES = (
        (MP3, 'mp3'),
        (WAV, 'wav'),
        (SOUNDCLOUD, 'SoundCloud')
    )

    asset_type = models.CharField(
        max_length=20,
        choices = ASSET_TYPE_CHOICES,
        help_text='The kind of audio.'
    )

    objects = AudioAssetManager()

    def get_audio_usage(self):
        """Return facets an audio file is associated with."""

        # After Facet refactor
        # audio_usage = Facet.objects.filter(Q(audio_assets=self))

        audio_usage = []
        audio_webfacets = WebFacet.objects.filter(Q(audio_assets=self))
        audio_printfacets = PrintFacet.objects.filter(Q(audio_assets=self))
        audio_audiofacets = AudioFacet.objects.filter(Q(audio_assets=self))
        audio_videofacets = VideoFacet.objects.filter(Q(audio_assets=self))
        audio_usage.extend(audio_webfacets)
        audio_usage.extend(audio_printfacets)
        audio_usage.extend(audio_audiofacets)
        audio_usage.extend(audio_videofacets)
        return audio_usage

    # def get_absolute_url(self):
    #     return reverse('asset_detail', kwargs={'pk': self.id})


class SimpleAudio(BaseAudio):
    """Simple Audio (attaches to an event, task, etc.)"""


#-----------------------------------------------------------------------#
#VideoAsset
#-----------------------------------------------------------------------#

class BaseVideo(BaseAsset):
    """Base class for videos.

    Subclassed by VideoAsset and SimpleVideo.
    """

    # metadata for search system
    type = "Video"

    video = models.FileField(
        upload_to='videos',
        blank=True,
    )

    # poster = models.FileField(
    #     upload_to='videos',
    #     blank=True,
    # )

    link = models.URLField(
        max_length=400,
        help_text='Link to video file on YouTube or Vimeo',
        blank=True,
    )

    class Meta:
        abstract = True


class VideoAssetManager(models.Manager):
    """Custom manager for VideoAsset."""

    def create_videoasset(self, owner, organization, title, description, attribution, video, asset_type, keywords):
        """Method for quick creation of a video asset."""
        videoasset=self.create(owner=owner, organization=organization, title=title, description=description, attribution=attribution, video=video, asset_type=asset_type, keywords=keywords)
        return videoasset


class VideoAsset(BaseVideo, BaseAssetMetadata):
    """ Uploaded Video Asset. """

    #Choices for Asset type
    MP4 = 'MP4'
    YT = 'YOUTUBE'
    VIM = 'VIMEO'

    ASSET_TYPE_CHOICES = (
        (MP4, 'mp4'),
        (YT, 'YouTube'),
        (VIM, 'Vimeo')
    )

    asset_type = models.CharField(
        max_length=20,
        choices = ASSET_TYPE_CHOICES,
        help_text='The kind of video.'
    )

    objects = VideoAssetManager()

    def get_video_usage(self):
        """Return facets an video file is associated with."""

        # After Facet refactor
        # video_usage = Facet.objects.filter(Q(video_assets=self))

        video_usage = []
        video_webfacets = WebFacet.objects.filter(Q(video_assets=self))
        video_printfacets = PrintFacet.objects.filter(Q(video_assets=self))
        video_videofacets = VideoFacet.objects.filter(Q(video_assets=self))
        video_usage.extend(video_webfacets)
        video_usage.extend(video_printfacets)
        video_usage.extend(video_videofacets)
        video_usage.extend(video_videofacets)
        return video_usage


class SimpleVideo(BaseVideo):
    """Uploaded video (attaches to tasks, events, etc)"""
