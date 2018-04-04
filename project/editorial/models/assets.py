from django.contrib.postgres.fields import ArrayField
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from imagekit.models import ImageSpecField

from .user import User
from .organization import Organization


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

    # XXX this means that if a user from a partner org uploads an asset to another
    # organization's content, that asset will show up in their own organization's library
    # but not the partner organization's library.
    organization = models.ForeignKey(
        Organization,
        blank=True,
        null=True,
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

    def copy(self):
        """Create a copy of an asset for a partner organization in a network.

        Copied assets keep all associated information. Organization is set to
        the copier's organization and the original flag is set to false.
        Triggering a copy also triggers the creation of an asset copy detail record."""

        #set the id = None to create the copy of the asset instance
        self.id = None
        self.original = False
        self.save()
        return self

    def get_asset_download_info(self):
        """Return rst of asset information for download."""

        title = self.title.encode('utf-8')
        description = self.description.encode('utf-8')
        attribution = self.attribution.encode('utf-8')

        if self.type == "ImageAsset" or self.type == "DocumentAsset":
            link = "NA"
        else:
            link = self.link


        asset_info="""
        {title}\r\n
        =======\r\n
        Description: {description}\r\n
        Attribution: {attribution}\r\n
        Link: {link}\r\n
        Creation Date: {date}\r\n
        Owner: {owner}\r\n
        Organization: {organization}\r\n
        Original: {original}\r\n
        Keywords: {keywords}\r\n
        """.format(title=title,
                description=description,
                attribution=attribution,
                link=link,
                date=self.creation_date,
                owner=self.owner,
                organization=self.organization.name,
                original=self.original,
                keywords=self.keywords,
        )

        return asset_info

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
        return self.facet_set.all()

    def get_absolute_url(self):
        return reverse('image_asset_detail', kwargs={'pk': self.id})

    @property
    def type(self):
        return "ImageAsset"


class SimpleImage(BaseImage):
    """Simple image (with some metadata) for attaching to tasks, events, etc."""

    @property
    def type(self):
        return "SimpleImage"

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
        return self.facet_set.all()

    def get_absolute_url(self):
        return reverse('document_asset_detail', kwargs={'pk': self.id})

    @property
    def type(self):
        return "DocumentAsset"


class SimpleDocument(BaseDocumentAsset):
    """Simple Document (file upload, attached to events, tasks, etc.)"""

    @property
    def type(self):
        return "SimpleDocument"

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
        return self.facet_set.all()

    def get_absolute_url(self):
        return reverse('audio_asset_detail', kwargs={'pk': self.id})

    @property
    def type(self):
        return "AudioAsset"


class SimpleAudio(BaseAudio):
    """Simple Audio (attaches to an event, task, etc.)"""

    @property
    def type(self):
        return "SimpleAudio"

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
        return self.facet_set.all()

    def get_absolute_url(self):
        return reverse('video_asset_detail', kwargs={'pk': self.id})

    @property
    def type(self):
        return "VideoAsset"


class SimpleVideo(BaseVideo):
    """Uploaded video (attaches to tasks, events, etc)"""

    @property
    def type(self):
        return "SimpleVideo"
