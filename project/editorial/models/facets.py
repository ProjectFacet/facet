from django.db import models
from django.db.models import Q
from django.contrib.postgres.fields import ArrayField
from simple_history.models import HistoricalRecords
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

#-----------------------------------------------------------------------#
#-----------------------------------------------------------------------#
#   FACET
#-----------------------------------------------------------------------#
#-----------------------------------------------------------------------#


# class FacetTemplate(models.Model):
#     """Template for facets.
#
#     A template is a collection of fields so that when adding/editing a facet,
#     only appropriate fields are shown.
#     """
#
#     name = models.CharField(
#         max_length=50,
#     )

    # Organization  null=system-wide
    # Owner
    # Description
    # Fields [arrayfield]  ["runtime", "editor", etc]
    #   does not contain always-common fields [title, credit, body, etc]

    # creation_date

# TODO: add a few out-of-box templates
#   "Video Facet" = these fields



class Facet(models.Model):
    """A version of a story.

    A facet must belong to a story and can only belong to one story. A facet is a version
    of the story.

    Ex. A story about wildfires could have:
    - a web story facet that is a text article with photos and video
    - a host-wrap facet that is the radio script of a story about the fire
    - a video facet that is a video segment about the fire for distribution via social media.
    """

    # ------------------------#
    # required fields
    # ------------------------#

    # populated during save
    owner = models.ForeignKey(
        User,
        related_name='facetowner'
    )

    organization = models.ForeignKey(
        Organization,
        help_text='Organization that owns this facet.'
    )

    # template = models.ForeignKey(
    #     FacetTemplate,
    # )

    story = models.ForeignKey(
        Story,
        related_name='facetstory',
    )

    original = models.BooleanField(
        default=True,
        help_text='Was this facet originally created by a user from this organization?',
        # If facet is not original, set to false and use FacetCopyDetail for additional info.
    )

    creation_date = models.DateTimeField(
        auto_now_add=True,
        help_text='Day facet was created.',
        blank=True,
    )

    # populated by user
    name = models.TextField(
        # displayed on form as label
        help_text='Internal name for facet.'
    )

    headline = models.TextField(
        help_text='Headline of the facet',
    )

    description = models.TextField(
        help_text='Description of the facet.',
        blank=True,
    )

    editor = models.ManyToManyField(
        User,
        related_name='faceteditor',
        help_text='The full user name(s) to be listed as the editor(s) for the facet.',
        blank=True,
    )

    credit = models.ManyToManyField(
        User,
        related_name='facetcredit',
        help_text='The full user name(s) to be listed as the credit for the facet.',
        blank=True,
    )

    team = models.ManyToManyField(
        User,
        through='FacetContributor',
        help_text='Users that contributed to a facet. Used to associate multiple users to a facet.',
        blank=True,
    )

    content = models.TextField(
        help_text='Content of the facet.',
        blank=True,
    )

    # Choices for facet status.
    DRAFT = 'Draft'
    PITCH = 'Pitch'
    IN_PROGRESS = 'In Progress'
    EDIT = 'Edit'
    REVISION = 'Revision'
    NEEDS_REVIEW = 'Needs Review'
    READY = 'Ready'
    FACET_STATUS_CHOICES = (
        (DRAFT, 'Draft'),
        (PITCH, 'Pitch'),
        (IN_PROGRESS, 'In Progress'),
        (EDIT, 'Edit'),
        (REVISION, 'Revision'),
        (NEEDS_REVIEW, 'Needs Review'),
        (READY, 'Ready'),
    )

    status = models.CharField(
        max_length=25,
        choices=FACET_STATUS_CHOICES,
        help_text='Facet status choice.'
    )

    due_edit = models.DateTimeField(
        help_text='Due for edit.',
        blank=True,
        null=True,
    )

    run_date = models.DateTimeField(
        help_text='Planned run date.',
        blank=True,
        null=True,
    )

    keywords = ArrayField(
        models.CharField(max_length=100),
        default=list,
        help_text='List of keywords for search.',
        blank=True,
    )

    # assets
    image_assets = models.ManyToManyField(
        'ImageAsset',
        blank=True,
    )

    document_assets = models.ManyToManyField(
        'DocumentAsset',
        blank=True,
    )

    audio_assets = models.ManyToManyField(
        'AudioAsset',
        blank=True,
    )

    video_assets = models.ManyToManyField(
        'VideoAsset',
        blank=True,
    )

    # history
    edit_history = HistoricalRecords()

    # ------------------------#
    # optional fields
    # ------------------------#

    update_notes  = models.TextField(
        help_text='Text commenting regarding any updates or corrections made to the facet.',
        blank=True,
    )

    excerpt = models.TextField(
        help_text='Excerpt from the facet.',
        blank=True,
    )

    dateline = models.CharField(
        max_length=150,
        help_text='Where and when the facet was created.',
        blank=True,
    )

    share_note = models.TextField(
        help_text='Information for organizations making a copy of the facet.',
        blank=True,
    )

    topic_code = models.CharField(
        max_length=75,
        help_text='Unique code as needed to designate topic or coverage.',
        blank=True,
    )

    internal_code = models.CharField(
        max_length=75,
        help_text='Unique code as needed for ingest sytems or internal use. Use as needed.',
        blank=True,
    )

    length = models.CharField(
        max_length=75,
        help_text='Length of facet for audio or video.',
        blank=True,
    )

    wordcount = models.CharField(
        max_length=75,
        help_text='Wordcount for text-based facets.',
        blank=True,
    )

    content_license = models.ForeignKey(
        'ContentLicense',
        related_name='facetlicense',
        blank=True,
    )

    related_links = models.TextField(
        help_text='Relevant links that can be included with the facet.',
        blank=True,
    )

    github_link = models.URLField(
        max_length=300,
        help_text='Link to code for any custom feature.',
        blank=True,
    )

    source = models.TextField(
        help_text='List of sources in the facet.',
        blank=True,
    )

    edit_notes = models.TextField(
        help_text='Information regarding allowable extent of editing and suggestions for specific kinds of edits.',
        blank=True,
    )

    pronunciations = models.TextField(
        help_text='Information about pronouncing names or potentially difficult words.',
        blank=True,
    )

    sponsors = models.TextField(
        help_text='Sponsors or underwriters if need to indicate any.',
        blank=True,
    )

    # ------------------------#
    #   web specific fields
    # ------------------------#

    # also relevant for print
    pull_quotes = models.TextField(
        help_text='List of quotes and attributions to be used as pull quotes.',
        blank=True,
    )

    embeds = models.TextField(
        help_text='The necessary information to embed something like a Tweet, FB post, map or video.',
        blank=True,
    )

    # push to CMS history
    pushed_to_wp = models.BooleanField(
        default=False,
        help_text='Whether the facet has been pushed to the organization WordPress site.',
    )

    # ------------------------#
    # print specific fields
    # ------------------------#

    sidebar_content = models.TextField(
        help_text='Content separate from body text meant for sidebar or inset presentation.',
        blank=True,
    )

    # ------------------------#
    # audio specific fields
    # ------------------------#

    # relevant for video
    producer = models.ForeignKey(
        User,
        related_name='facetproducer',
        blank=True,
    )

    # ------------------------#
    # tv and video specific
    # ------------------------#

    series_title = models.TextField(
        help_text='Title of the video series.',
        blank=True,
    )

    episode_number = models.CharField(
        max_length=75,
        help_text='If the video is part of a series, the episode number.',
        blank=True,
    )

    usage_rights = models.TextField(
        help_text='Information regarding the usage of the video if shared.',
        blank=True,
    )

    tape_datetime = models.DateTimeField(
        help_text='Tape date.',
        blank=True,
        null=True,
    )

    locations = models.TextField(
        help_text='Shoot locations.',
        blank=True,
    )

    # ------------------------#
    # user defined fields
    # ------------------------#

    custom_one = models.TextField(
        help_text='User-defined field.',
        blank=True,
    )

    custom_two = models.TextField(
        help_text='User-defined field.',
        blank=True,
    )

    custom_three = models.TextField(
        help_text='User-defined field.',
        blank=True,
    )

    custom_four = models.TextField(
        help_text='User-defined field.',
        blank=True,
    )

    custom_five = models.TextField(
        help_text='User-defined field.',
        blank=True,
    )

    class Meta:
        verbose_name='Facet'
        verbose_name_plural='Facets'
        # ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('story_detail', kwargs={'pk': self.story.id})


    def copy_facet(self):
        """ Create a copy of a facet for a partner organization in a network."""

        # FIXME Copied facet should also carry over credit and editor.

        webfacet_copy = get_object_or_404(WebFacet, id=self.id)
        # set the id=None to create the copy of the webfacet instance
        webfacet_copy.id=None
        webfacet_copy.save()
        # clear attributes for the copying Organization
        webfacet_copy.original_content=False
        webfacet_copy.code = ''
        webfacet_copy.status= 'NR'
        webfacet_copy.due_edit = None
        webfacet_copy.run_date = None
        webfacet_copy.discussion = Discussion.objects.create_discussion("WF")
        webfacet_copy.edit_history = webfacet_copy.edit_history.all()
        webfacet_copy.save()

        return webfacet_copy

    def get_webfacet_images(self):
        """Retrieve all images objects associated with a webfacet."""

        return self.imageasset_set.all()

    def get_webfacet_documents(self):
        """Retrieve all documents objects associated with a webfacet."""

        webfacet_documents = DocumentAsset.objects.filter(webfacet=self)
        return webfacet_documents

    def get_webfacet_audio(self):
        """Retrieve all audio objects associated with a webfacet."""

        webfacet_audio = AudioAsset.objects.filter(webfacet=self)
        return webfacet_audio

    def get_webfacet_video(self):
        """Retrieve all video objects associated with a webfacet."""

        webfacet_video = VideoAsset.objects.filter(webfacet=self)
        return webfacet_video

    def get_webfacet_download(self):
        """ Return rst formatted string for downloading webfacet and its meta."""

        # loop over m2m and get the values as string
        credits = self.credit.all()
        credits = [ user.credit_name for user in credits]
        credits = ",".join(credits)

        # loop over m2m and get the values as string
        images = WebFacet.get_webfacet_images(self)
        images = [image.asset_title for image in images]
        images = ",".join(images)

        # loop over m2m and get the values as string
        documents = WebFacet.get_webfacet_documents(self)
        documents = [document.asset_title for document in documents]
        documents = ",".join(documents)

        # loop over m2m and get the values as string
        audiofiles = WebFacet.get_webfacet_audio(self)
        audiofiles = [audiofile.asset_title for audiofile in audiofiles]
        audiofiles = ",".join(audiofiles)

        # verify the text area fields have correct encoding
        title = self.title.encode('utf-8')
        description = self.wf_description.encode('utf-8')
        excerpt = self.excerpt.encode('utf-8')
        share_note = self.share_note.encode('utf-8')
        content = self.wf_content.encode('utf-8')

        webfacet_download = """
        WebFacet
        ========
        {title}
        --------------
        Description: {desc}\n
        Story: {story}\n
        Owner: {owner}\n
        Organization: {organization}\n
        Original: {original}\n
        Editor: {editor}\n
        Credit: {credit}\n
        Code: {code}\n
        Excerpt: {excerpt}\n
        Keywords: {keywords}\n
        Status: {status}\n
        Due Edit: {dueedit}\n
        Run Date: {rundate}\n
        Share Note: {sharenote}\n
        Images: {images}\n
        Captions: {captions}\n
        Documents: {documents}\n
        AudioFiles: {audiofiles}\n
        \n
        Content\n
        -------
        {content}
        """.format(title=title, desc=description, story=self.story, owner=self.owner,
        organization=self.organization.name, original=self.original_webfacet, editor=self.editor,
        credit=credits, code=self.code, excerpt=excerpt,
        keywords=self.keywords, status=self.status, dueedit=self.due_edit, rundate=self.run_date,
        sharenote=share_note, images=images, captions=self.captions, documents=documents,
        audiofiles=audiofiles, content=content)

        return webfacet_download

    @property
    def description(self):
        return self.wf_description

    @property
    def search_title(self):
        return self.title

    @property
    def type(self):
        return "WebFacet"







#-----------------------------------------------------------------------#
#   FacetContributor
#-----------------------------------------------------------------------#

@python_2_unicode_compatible
class FacetContributor(models.Model):
    """ Which users are participating in creating the facet. """

    facet = models.ForeignKey(
        Facet,
    )

    user = models.ForeignKey(
        User,
    )

    user_role = models.CharField(
        max_length=255,
        help_text='What did the user do?',
    )

    def __str__(self):
        return "{facet}, {contributor}".format(
                                        facet=self.facet.name,
                                        contributor=self.user.credit_name,
                                        )


#-----------------------------------------------------------------------#
#   CONTENT LICENSE
#-----------------------------------------------------------------------#

@python_2_unicode_compatible
class ContentLicense(models.Model):
    """Content License for facets.

    Facets can have a related content license. The data for this model
    includes the 7 7 established variations of the Creative Commons license;
    these have a blank Organziation field.

    Organizations can also create their own content licenses/reuse terms and
    upload documents for the custom license.
    """

    name = models.TextField(
        help_text='Name for the license.',
    )

    organization = models.ForeignKey(
        Organization,
        null=True,
        blank=True,
        help_text='Organization that owns this license.',
    )

    terms = models.TextField(
        help_text='Content of the terms.',
        blank=True,
    )

    upload = models.FileField(
        upload_to="license/%Y/%m/%d/",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name='Content License'
        verbose_name_plural='Content Licenses'
        ordering = ['name']

    def __str__(self):
        return self.name


#-----------------------------------------------------------------------#
#   WEBFACET
#-----------------------------------------------------------------------#

@python_2_unicode_compatible
class WebFacet(models.Model):
    """ Regularly published web content.

    Ex: Daily news, articles, videos, photo galleries
    """

    story = models.ForeignKey(
        Story,
        related_name='webfacetstory',
    )

    owner = models.ForeignKey(
        User,
        related_name='webfacetowner'
    )

    organization = models.ForeignKey(
        Organization,
        help_text='Organization that owns this webfacet.'
    )

    original_webfacet = models.BooleanField(
        default=True,
        help_text='Was this webfacet originally created by a user from this organization?',
        # If webfacet is not original, set to false and use WebFacetCopyDetail for additional info.
    )

    editor = models.ForeignKey(
        User,
        related_name='webfaceteditor'
    )

    contributors = models.ManyToManyField(
        User,
        through='WebFacetContributor',
        help_text='Users that contributed to a facet. Used to associate multiple users to a facet.',
        blank=True,
    )

    credit = models.ManyToManyField(
        User,
        related_name='webfacetcredit',
        help_text='The full user name(s) to be listed as the credit for the facet.',
        blank=True,
    )

    code = models.CharField(
        max_length=75,
        help_text='Unique code as needed for ingest sytems. Use as needed',
        blank=True,
    )

    title = models.TextField(
        help_text='Headline of the Webfacet',
    )

    excerpt = models.TextField(
        help_text='Excerpt from the Webfacet.',
        blank=True,
    )

    wf_description = models.TextField(
        help_text='Description of the WebFacet.',
        blank=True,
    )

    wf_content = models.TextField(
        help_text='Content of the webFacet.',
        blank=True,
    )

    keywords = ArrayField(
        models.CharField(max_length=100),
        default=list,
        help_text='List of keywords for search.',
        blank=True,
    )

    # Choices for WebFacet status.
    DRAFT = 'Draft'
    PITCH = 'Pitch'
    IN_PROGRESS = 'In Progress'
    EDIT = 'Edit'
    REVISION = 'Revision'
    NEEDS_REVIEW = 'Needs Review'
    READY = 'Ready'
    WEBFACET_STATUS_CHOICES = (
        (DRAFT, 'Draft'),
        (PITCH, 'Pitch'),
        (IN_PROGRESS, 'In Progress'),
        (EDIT, 'Edit'),
        (REVISION, 'Revision'),
        (NEEDS_REVIEW, 'Needs Review'),
        (READY, 'Ready'),
    )

    status = models.CharField(
        max_length=25,
        choices=WEBFACET_STATUS_CHOICES,
        help_text='WebFacet status choice.'
    )

    due_edit = models.DateTimeField(
        help_text='Due for edit.',
        blank=True,
        null=True,
    )

    run_date = models.DateTimeField(
        help_text='Planned run date.',
        blank=True,
        null=True,
    )

    creation_date = models.DateTimeField(
        auto_now_add=True,
        help_text='Day WebFacet was created.',
        blank=True,
    )

    discussion = models.ForeignKey(
        'Discussion',
        help_text='Id of edit discussion for the webfacet.',
        blank=True,
        null=True,
    )

    edit_history = HistoricalRecords()

    share_note = models.TextField(
        help_text='Information for organizations making a copy of the webfacet.',
        blank=True,
    )

    github_link = models.URLField(
        max_length=300,
        help_text='Link to code for any custom feature',
        blank=True,
    )

    image_assets = models.ManyToManyField(
        'ImageAsset',
        blank=True,
    )

    document_assets = models.ManyToManyField(
        'DocumentAsset',
        blank=True,
    )

    audio_assets = models.ManyToManyField(
        'AudioAsset',
        blank=True,
    )

    video_assets = models.ManyToManyField(
        'VideoAsset',
        blank=True,
    )

    captions = models.TextField(
        help_text='Captions and credits for any assets in use.',
        blank=True,
    )

    #push to CMS history
    pushed_to_wp = models.BooleanField(
        default=False,
        help_text='Whether the webfacet has been pushed to the organization WordPress site.',
    )

    class Meta:
        verbose_name = 'Webfacet'
        verbose_name_plural = 'Webfacets'
        ordering = ['creation_date']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('story_detail', kwargs={'pk': self.story.id})

    def copy_webfacet(self):
        """ Create a copy of a webfacet for a partner organization in a network."""

        # FIXME Copied facet should also carry over credit and editor.

        webfacet_copy = get_object_or_404(WebFacet, id=self.id)
        # set the id=None to create the copy of the webfacet instance
        webfacet_copy.id=None
        webfacet_copy.save()
        # clear attributes for the copying Organization
        webfacet_copy.original_content=False
        webfacet_copy.code = ''
        webfacet_copy.status= 'NR'
        webfacet_copy.due_edit = None
        webfacet_copy.run_date = None
        webfacet_copy.discussion = Discussion.objects.create_discussion("WF")
        webfacet_copy.edit_history = webfacet_copy.edit_history.all()
        webfacet_copy.save()

        return webfacet_copy

    def get_webfacet_images(self):
        """Retrieve all images objects associated with a webfacet."""

        webfacet_images = ImageAsset.objects.filter(webfacet=self)
        return webfacet_images

    def get_webfacet_documents(self):
        """Retrieve all documents objects associated with a webfacet."""

        webfacet_documents = DocumentAsset.objects.filter(webfacet=self)
        return webfacet_documents

    def get_webfacet_audio(self):
        """Retrieve all audio objects associated with a webfacet."""

        webfacet_audio = AudioAsset.objects.filter(webfacet=self)
        return webfacet_audio

    def get_webfacet_video(self):
        """Retrieve all video objects associated with a webfacet."""

        webfacet_video = VideoAsset.objects.filter(webfacet=self)
        return webfacet_video

    def get_webfacet_download(self):
        """ Return rst formatted string for downloading webfacet and its meta."""

        # loop over m2m and get the values as string
        credits = self.credit.all()
        credits = [ user.credit_name for user in credits]
        credits = ",".join(credits)

        # loop over m2m and get the values as string
        images = WebFacet.get_webfacet_images(self)
        images = [image.asset_title for image in images]
        images = ",".join(images)

        # loop over m2m and get the values as string
        documents = WebFacet.get_webfacet_documents(self)
        documents = [document.asset_title for document in documents]
        documents = ",".join(documents)

        # loop over m2m and get the values as string
        audiofiles = WebFacet.get_webfacet_audio(self)
        audiofiles = [audiofile.asset_title for audiofile in audiofiles]
        audiofiles = ",".join(audiofiles)

        # verify the text area fields have correct encoding
        title = self.title.encode('utf-8')
        description = self.wf_description.encode('utf-8')
        excerpt = self.excerpt.encode('utf-8')
        share_note = self.share_note.encode('utf-8')
        content = self.wf_content.encode('utf-8')

        webfacet_download = """
        WebFacet
        ========
        {title}
        --------------
        Description: {desc}\n
        Story: {story}\n
        Owner: {owner}\n
        Organization: {organization}\n
        Original: {original}\n
        Editor: {editor}\n
        Credit: {credit}\n
        Code: {code}\n
        Excerpt: {excerpt}\n
        Keywords: {keywords}\n
        Status: {status}\n
        Due Edit: {dueedit}\n
        Run Date: {rundate}\n
        Share Note: {sharenote}\n
        Images: {images}\n
        Captions: {captions}\n
        Documents: {documents}\n
        AudioFiles: {audiofiles}\n
        \n
        Content\n
        -------
        {content}
        """.format(title=title, desc=description, story=self.story, owner=self.owner,
        organization=self.organization.name, original=self.original_webfacet, editor=self.editor,
        credit=credits, code=self.code, excerpt=excerpt,
        keywords=self.keywords, status=self.status, dueedit=self.due_edit, rundate=self.run_date,
        sharenote=share_note, images=images, captions=self.captions, documents=documents,
        audiofiles=audiofiles, content=content)

        return webfacet_download


    @property
    def description(self):
        return self.wf_description

    @property
    def search_title(self):
        return self.title

    @property
    def type(self):
        return "WebFacet"

#-----------------------------------------------------------------------#
#   PRINTFACET
#-----------------------------------------------------------------------#

@python_2_unicode_compatible
class PrintFacet(models.Model):
    """ The print version of a story.

    Ex: Daily news article, column, story.
    """

    story = models.ForeignKey(
        Story,
        related_name='printfacetstory',
    )

    owner = models.ForeignKey(
        User,
        related_name='printfacetowner'
    )

    organization = models.ForeignKey(
        Organization,
        help_text='Organization that owns this printfacet.'
    )

    original_printfacet = models.BooleanField(
        default=True,
        help_text='Was this printfacet originally created by a user from this organization?',
        # If printfacet is not original, set to false and use PrintFacetCopyDetail for additional info.
    )

    editor = models.ForeignKey(
        User,
        related_name='printfaceteditor'
    )

    contributors = models.ManyToManyField(
        User,
        through='PrintFacetContributor',
        help_text='Users that contributed to a facet. Used to associate multiple users to a facet.',
        blank=True,
    )

    credit = models.ManyToManyField(
        # There can be multiple users listed as the credit.
        User,
        related_name='printfacetcredit',
        help_text='The full user name(s) to be listed as the credit for the facet.',
        blank=True,
    )

    code = models.CharField(
        max_length=75,
        help_text='Unique code as needed for ingest sytems. Use as needed',
        blank=True,
    )

    title = models.TextField(
        help_text='Headline of the printfacet.'
    )

    excerpt = models.TextField(
        help_text='Excerpt from the printfacet.',
        blank=True,
    )

    pf_description = models.TextField(
        help_text='Description of the printfacet.',
        blank=True,
    )

    pf_content = models.TextField(
        help_text='Content of the printfacet.',
        blank=True,
    )

    keywords = ArrayField(
        models.CharField(max_length=100),
        default=list,
        help_text='List of keywords for search.',
        blank=True,
    )

    # Choices for PrintFacet status.
    DRAFT = 'Draft'
    PITCH = 'Pitch'
    IN_PROGRESS = 'In Progress'
    EDIT = 'Edit'
    REVISION = 'Revision'
    NEEDS_REVIEW = 'Needs Review'
    READY = 'Ready'
    PRINTFACET_STATUS_CHOICES = (
        (DRAFT, 'Draft'),
        (PITCH, 'Pitch'),
        (IN_PROGRESS, 'In Progress'),
        (EDIT, 'Edit'),
        (REVISION, 'Revision'),
        (NEEDS_REVIEW, 'Needs Review'),
        (READY, 'Ready'),
    )

    status = models.CharField(
        max_length=25,
        choices=PRINTFACET_STATUS_CHOICES,
        help_text='Printfacet status choice.'
    )

    due_edit = models.DateTimeField(
        help_text='Due for edit.',
        blank=True,
        null=True,
    )

    run_date = models.DateTimeField(
        help_text='Planned run date.',
        blank=True,
        null=True,
    )

    creation_date = models.DateTimeField(
        auto_now_add=True,
        help_text='Day printfacet was created.',
    )

    discussion = models.ForeignKey(
        'Discussion',
        help_text='Id of edit discussion for the printfacet.',
        blank=True,
        null=True,
    )

    edit_history = HistoricalRecords()

    share_note = models.TextField(
        help_text='Information for organizations making a copy of the printfacet.',
        blank=True,
    )

    github_link = models.TextField(
        max_length=300,
        help_text='Link to code for any custom feature',
        blank=True,
    )

    image_assets = models.ManyToManyField(
        'ImageAsset',
        blank=True,
    )

    document_assets = models.ManyToManyField(
        'DocumentAsset',
        blank=True,
    )

    audio_assets = models.ManyToManyField(
        'AudioAsset',
        blank=True,
    )

    video_assets = models.ManyToManyField(
        'VideoAsset',
        blank=True,
    )

    captions = models.TextField(
        help_text='Captions and credits for any assets in use.',
        blank=True,
    )

    class Meta:
        verbose_name = 'Printfacet'
        verbose_name_plural = 'Printfacets'
        ordering = ['creation_date']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('story_detail', kwargs={'pk': self.story.id})

    def copy_printfacet(self):
        """ Create a copy of a printfacet for a partner organization in a network."""

        # FIXME Copied facet should also carry over credit and editor.

        printfacet_copy = get_object_or_404(PrintFacet, id=self.id)
        # set the id=None to create the copy of the printfacet instance
        printfacet_copy.id=None
        printfacet_copy.save()
        # clear attributes for the copying Organization
        printfacet_copy.original_content=False
        printfacet_copy.code = ''
        printfacet_copy.status= 'NR'
        printfacet_copy.due_edit = None
        printfacet_copy.run_date = None
        printfacet_copy.discussion = Discussion.objects.create_discussion("PF")
        printfacet_copy.edit_history = printfacet_copy.edit_history.all()
        printfacet_copy.save()

        return printfacet_copy

    def get_printfacet_images(self):
        """Retrieve all images objects associated with a printfacet."""

        printfacet_images = ImageAsset.objects.filter(printfacet=self)
        return printfacet_images

    def get_printfacet_documents(self):
        """Retrieve all documents objects associated with a printfacet."""

        printfacet_documents = DocumentAsset.objects.filter(printfacet=self)
        return printfacet_documents

    def get_printfacet_audio(self):
        """Retrieve all audio objects associated with a printfacet."""

        printfacet_audio = AudioAsset.objects.filter(printfacet=self)
        return printfacet_audio

    def get_printfacet_video(self):
        """Retrieve all video objects associated with a printfacet."""

        printfacet_video = VideoAsset.objects.filter(printfacet=self)
        return printfacet_video

    def get_printfacet_download(self):
        """ Return rst formatted string for downloading printfacet and its meta."""

        # loop over m2m and get the values as string
        credits = self.credit.all()
        credits = [ user.credit_name for user in credits]
        credits = ",".join(credits)

        # loop over m2m and get the values as string
        images = PrintFacet.get_printfacet_images(self)
        images = [image.asset_title for image in images]
        images = ",".join(images)

        # loop over m2m and get the values as string
        documents = PrintFacet.get_printfacet_documents(self)
        documents = [document.asset_title for document in documents]
        documents = ",".join(documents)

        # loop over m2m and get the values as string
        audiofiles = PrintFacet.get_printfacet_audio(self)
        audiofiles = [audiofile.asset_title for audiofile in audiofiles]
        audiofiles = ",".join(audiofiles)

        # verify the text area fields have correct encoding
        title = self.title.encode('utf-8')
        description = self.pf_description.encode('utf-8')
        excerpt = self.excerpt.encode('utf-8')
        share_note = self.share_note.encode('utf-8')
        content = self.pf_content.encode('utf-8')

        printfacet_download = """
        PrintFacet
        ========
        {title}
        --------------
        Description: {desc}\n
        Story: {story}\n
        Owner: {owner}\n
        Organization: {organization}\n
        Original: {original}\n
        Editor: {editor}\n
        Credit: {credit}\n
        Code: {code}\n
        Excerpt: {excerpt}\n
        Keywords: {keywords}\n
        Status: {status}\n
        Due Edit: {dueedit}\n
        Run Date: {rundate}\n
        Share Note: {sharenote}\n
        Images: {images}\n
        Captions: {captions}\n
        Documents: {documents}\n
        AudioFiles: {audiofiles}\n
        \n
        Content\n
        -------\n
        {content}
        """.format(title=title, desc=description, story=self.story, owner=self.owner,
        organization=self.organization.name, original=self.original_printfacet, editor=self.editor,
        credit=credits, code=self.code, excerpt=excerpt,
        keywords=self.keywords, status=self.status, dueedit=self.due_edit, rundate=self.run_date,
        sharenote=share_note, images=images, captions=self.captions, documents=documents,
        audiofiles=audiofiles, content=content)

        return printfacet_download

    @property
    def description(self):
        return self.pf_description

    @property
    def search_title(self):
        return self.title

    @property
    def type(self):
        return "PrintFacet"

#-----------------------------------------------------------------------#
#   AUDIOFACET
#-----------------------------------------------------------------------#

@python_2_unicode_compatible
class AudioFacet(models.Model):
    """ Scheduled radio programming.

    Ex: A single segment on Morning Edition.
    """

    story = models.ForeignKey(
        Story,
        related_name='audiofacetstory',
    )

    owner = models.ForeignKey(
        User,
        related_name='audiofacetowner'
    )

    organization = models.ForeignKey(
        Organization,
        help_text='Organization that owns this audiofacet.'
    )

    original_audiofacet = models.BooleanField(
        default=True,
        help_text='Was this audiofacet originally created by a user from this organization?',
        # If audiofacet is not original, set to false and use AudioFacetCopyDetail for additional info.
    )

    editor = models.ForeignKey(
        User,
        related_name='audiofaceteditor'
    )

    contributors = models.ManyToManyField(
        User,
        through='AudioFacetContributor',
        help_text='Users that contributed to a facet. Used to associate multiple users to a facet.',
        blank=True,
    )

    credit = models.ManyToManyField(
        # There can be multiple users listed as the credit.
        User,
        related_name='audiofacetcredit',
        help_text='The full user name(s) to be listed as the credit for the facet.',
        blank=True,
    )

    code = models.CharField(
        max_length=75,
        help_text='Unique code as needed for ingest sytems. Use as needed',
        blank=True,
    )

    title = models.TextField(
        help_text='Headline of the audiofacet.'
    )

    excerpt = models.TextField(
        help_text='Excerpt for the audiofacet.',
        blank=True,
    )

    af_description = models.TextField(
        help_text='Description of the audiofacet.',
        blank=True,
    )

    af_content = models.TextField(
        help_text='Content of the audiofacet.',
        blank=True,
    )

    keywords = ArrayField(
        models.CharField(max_length=100),
        default=list,
        help_text='List of keywords for search.',
        blank=True,
    )

    # Choices for AudioFacet status.
    DRAFT = 'Draft'
    PITCH = 'Pitch'
    IN_PROGRESS = 'In Progress'
    EDIT = 'Edit'
    REVISION = 'Revision'
    NEEDS_REVIEW = 'Needs Review'
    READY = 'Ready'
    AUDIOFACET_STATUS_CHOICES = (
        (DRAFT, 'Draft'),
        (PITCH, 'Pitch'),
        (IN_PROGRESS, 'In Progress'),
        (EDIT, 'Edit'),
        (REVISION, 'Revision'),
        (NEEDS_REVIEW, 'Needs Review'),
        (READY, 'Ready'),
    )

    status = models.CharField(
        max_length=25,
        choices=AUDIOFACET_STATUS_CHOICES,
        help_text='Audiofacet status choice.'
    )

    due_edit = models.DateTimeField(
        help_text='Due for edit.',
        blank=True,
        null=True,
    )

    run_date = models.DateTimeField(
        help_text='Planned run date.',
        blank=True,
        null=True,
    )

    creation_date = models.DateTimeField(
        auto_now_add=True,
        help_text='Day audiofacet was created.',
        blank=True,
    )

    discussion = models.ForeignKey(
        'Discussion',
        help_text='Id of edit discussion for the audiofacet.',
        blank=True,
        null=True,
    )

    edit_history = HistoricalRecords()

    share_note = models.TextField(
        help_text='Information for organizations making a copy of the audiofacet.',
        blank=True,
    )

    github_link = models.URLField(
        max_length=300,
        help_text='Link to code for any custom feature',
        blank=True,
    )

    image_assets = models.ManyToManyField(
        'ImageAsset',
        blank=True,
    )

    document_assets = models.ManyToManyField(
        'DocumentAsset',
        blank=True,
    )

    audio_assets = models.ManyToManyField(
        'AudioAsset',
        blank=True,
    )

    video_assets = models.ManyToManyField(
        'VideoAsset',
        blank=True,
    )

    captions = models.TextField(
        help_text='Captions and credits for any assets in use.',
        blank=True,
    )

    class Meta:
        verbose_name = 'Audiofacet'
        verbose_name_plural = 'Audiofacets'
        ordering = ['creation_date']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('story_detail', kwargs={'pk': self.story.id})

    def copy_audiofacet(self):
        """ Create a copy of a audiofacet for a partner organization in a network."""

        # FIXME Copied facet should also carry over credit and editor.

        audiofacet_copy = get_object_or_404(AudioFacet, id=self.id)
        # set the id=None to create the copy of the audiofacet instance
        audiofacet_copy.id=None
        audiofacet_copy.save()
        # clear attributes for the copying Organization
        audiofacet_copy.original_content=False
        audiofacet_copy.code = ''
        audiofacet_copy.status= 'NR'
        audiofacet_copy.due_edit = None
        audiofacet_copy.run_date = None
        audiofacet_copy.discussion = Discussion.objects.create_discussion("AF")
        audiofacet_copy.edit_history = audiofacet_copy.edit_history.all()
        audiofacet_copy.save()

        return audiofacet_copy

    def get_audiofacet_images(self):
        """Retrieve all images objects associated with a audiofacet."""

        audiofacet_images = ImageAsset.objects.filter(audiofacet=self)
        return audiofacet_images

    def get_audiofacet_documents(self):
        """Retrieve all documents objects associated with an audiofacet."""

        audiofacet_documents = DocumentAsset.objects.filter(audiofacet=self)
        return audiofacet_documents

    def get_audiofacet_audio(self):
        """Retrieve all audio objects associated with a audiofacet."""

        audiofacet_audio = AudioAsset.objects.filter(audiofacet=self)
        return audiofacet_audio

    def get_audiofacet_video(self):
        """Retrieve all video objects associated with a audiofacet."""

        audiofacet_video = VideoAsset.objects.filter(audiofacet=self)
        return audiofacet_video

    def get_audiofacet_download(self):
        """ Return rst formatted string for downloading audiofacet and its meta."""

        # loop over m2m and get the values as string
        credits = self.credit.all()
        credits = [ user.credit_name for user in credits]
        credits = ",".join(credits)

        # loop over m2m and get the values as string
        images = AudioFacet.get_audiofacet_images(self)
        images = [image.asset_title for image in images]
        images = ",".join(images)

        # loop over m2m and get the values as string
        documents = AudioFacet.get_audiofacet_documents(self)
        documents = [document.asset_title for document in documents]
        documents = ",".join(documents)

        # loop over m2m and get the values as string
        audiofiles = AudioFacet.get_audiofacet_audio(self)
        audiofiles = [audiofile.asset_title for audiofile in audiofiles]
        audiofiles = ",".join(audiofiles)

        # verify the text area fields have correct encoding
        title = self.title.encode('utf-8')
        description = self.af_description.encode('utf-8')
        excerpt = self.excerpt.encode('utf-8')
        share_note = self.share_note.encode('utf-8')
        content = self.af_content.encode('utf-8')

        audiofacet_download = """
        AudioFacet
        ========
        {title}\n
        --------------\n
        Description: {desc}\n
        Story: {story}\n
        Owner: {owner}\n
        Organization: {organization}\n
        Original: {original}\n
        Editor: {editor}\n
        Credit: {credit}\n
        Code: {code}\n
        Excerpt: {excerpt}\n
        Keywords: {keywords}\n
        Status: {status}\n
        Due Edit: {dueedit}\n
        Run Date: {rundate}\n
        Share Note: {sharenote}\n
        Images: {images}\n
        Captions: {captions}\n
        Documents: {documents}\n
        AudioFiles: {audiofiles}\n
        \n
        Content\n
        -------\n
        {content}
        """.format(title=title, desc=description, story=self.story, owner=self.owner,
        organization=self.organization.name, original=self.original_audiofacet, editor=self.editor,
        credit=credits, code=self.code, excerpt=excerpt,
        keywords=self.keywords, status=self.status, dueedit=self.due_edit, rundate=self.run_date,
        sharenote=share_note, images=images, captions=self.captions, documents=documents,
        audiofiles=audiofiles, content=content)

        return audiofacet_download


    @property
    def description(self):
        return self.af_description

    @property
    def search_title(self):
        return self.title

    @property
    def type(self):
        return "AudioFacet"

#-----------------------------------------------------------------------#
#   VIDEOFACET
#-----------------------------------------------------------------------#

@python_2_unicode_compatible
class VideoFacet(models.Model):
    """ Scheduled television programming.

    Ex: An episode of a television program.
    """

    story = models.ForeignKey(
        Story,
        related_name='videofacetstory',
    )

    owner = models.ForeignKey(
        User,
        related_name='videofacetowner'
    )

    organization = models.ForeignKey(
        Organization,
        help_text='Organization that owns this videofacet.'
    )

    original_videofacet = models.BooleanField(
        default=True,
        help_text='Was this videofacet originally created by a user from this organization?',
        # If videofacet is not original, set to false and use VideoFacetCopyDetail for additional info.
    )

    editor = models.ForeignKey(
        User,
        related_name='videofaceteditor'
    )

    contributors = models.ManyToManyField(
        User,
        through='VideoFacetContributor',
        help_text='Users that contributed to a facet. Used to associate multiple users to a facet.',
        blank=True,
    )

    credit = models.ManyToManyField(
        # There can be multiple users listed as the credit.
        User,
        related_name='videofacetcredit',
        help_text='The full user name(s) to be listed as the credit for the facet.',
        blank=True,
    )

    code = models.CharField(
        max_length=75,
        help_text='Unique code as needed for ingest sytems. Use as needed',
        blank=True,
    )

    title = models.TextField(
        help_text='Headline of the videofacet.'
    )

    excerpt = models.TextField(
        help_text='Excerpt from the videofacet.',
        blank=True,
    )

    vf_description = models.TextField(
        help_text='Description of the videofacet.',
        blank=True,
    )

    vf_content = models.TextField(
        help_text='Content of the videofacet.',
        blank=True,
    )

    keywords = ArrayField(
        models.CharField(max_length=100),
        default=list,
        help_text='List of keywords for search.',
        blank=True,
    )

    # Choices for VideoFacet status.
    DRAFT = 'Draft'
    PITCH = 'Pitch'
    IN_PROGRESS = 'In Progress'
    EDIT = 'Edit'
    REVISION = 'Revision'
    NEEDS_REVIEW = 'Needs Review'
    READY = 'Ready'
    VIDEOFACET_STATUS_CHOICES = (
        (DRAFT, 'Draft'),
        (PITCH, 'Pitch'),
        (IN_PROGRESS, 'In Progress'),
        (EDIT, 'Edit'),
        (REVISION, 'Revision'),
        (NEEDS_REVIEW, 'Needs Review'),
        (READY, 'Ready'),
    )

    status = models.CharField(
        max_length=25,
        choices=VIDEOFACET_STATUS_CHOICES,
        help_text='Videofacet status choice.'
    )

    due_edit = models.DateTimeField(
        help_text='Due for edit.',
        blank=True,
        null=True,
    )

    run_date = models.DateTimeField(
        help_text='Planned run date.',
        blank=True,
        null=True,
    )

    creation_date = models.DateTimeField(
        auto_now_add=True,
        help_text='Day videofacet was created.',
        blank=True,
    )

    discussion = models.ForeignKey(
        'Discussion',
        help_text='ID of edit discussion for the videofacet.',
        blank=True,
        null=True,
    )

    edit_history = HistoricalRecords()

    share_note = models.TextField(
        help_text='Information for organizations making a copy of the videofacet.',
        blank=True,
    )

    github_link = models.URLField(
        max_length=300,
        help_text='Link to code for any custom feature',
        blank=True,
    )

    image_assets = models.ManyToManyField(
        'ImageAsset',
        blank=True,
    )

    document_assets = models.ManyToManyField(
        'DocumentAsset',
        blank=True,
    )

    audio_assets = models.ManyToManyField(
        'AudioAsset',
        blank=True,
    )

    video_assets = models.ManyToManyField(
        'VideoAsset',
        blank=True,
    )

    captions = models.TextField(
        help_text='Captions and credits for any assets in use.',
        blank=True,
    )

    class Meta:
        verbose_name = 'Videofacet'
        verbose_name_plural = 'Videofacets'
        ordering = ['creation_date']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('story_detail', kwargs={'pk': self.story.id})

    def copy_videofacet(self):
        """ Create a copy of a videofacet for a partner organization in a network."""

        # FIXME Copied facet should also carry over credit and editor.

        videofacet_copy = get_object_or_404(VideoFacet, id=self.id)
        # set the id=None to create the copy of the videofacet instance
        videofacet_copy.id=None
        videofacet_copy.save()
        # clear attributes for the copying Organization
        videofacet_copy.original_content=False
        videofacet_copy.code = ''
        videofacet_copy.status= 'NR'
        videofacet_copy.due_edit = None
        videofacet_copy.run_date = None
        videofacet_copy.discussion = Discussion.objects.create_discussion("VF")
        videofacet_copy.edit_history = videofacet_copy.edit_history.all()
        videofacet_copy.save()

        return videofacet_copy

    def get_videofacet_images(self):
        """Retrieve all images objects associated with a videofacet."""

        videofacet_images = ImageAsset.objects.filter(videofacet=self)
        return videofacet_images

    def get_videofacet_documents(self):
        """Retrieve all documents objects associated with a videofacet."""

        videofacet_documents = DocumentAsset.objects.filter(videofacet=self)
        return videofacet_documents

    def get_videofacet_audio(self):
        """Retrieve all audio objects associated with a videofacet."""

        videofacet_audio = AudioAsset.objects.filter(videofacet=self)
        return videofacet_audio

    def get_videofacet_video(self):
        """Retrieve all video objects associated with a videofacet."""

        videofacet_video = VideoAsset.objects.filter(videofacet=self)
        return videofacet_video

    def get_videofacet_download(self):
        """ Return rst formatted string for downloading videofacet and its meta."""

        # loop over m2m and get the values as string
        credits = self.credit.all()
        credits = [ user.credit_name for user in credits]
        credits = ",".join(credits)

        # loop over m2m and get the values as string
        images = VideoFacet.get_videofacet_images(self)
        images = [image.asset_title for image in images]
        images = ",".join(images)

        # loop over m2m and get the values as string
        documents = VideoFacet.get_videofacet_documents(self)
        documents = [document.asset_title for document in documents]
        documents = ",".join(documents)

        # loop over m2m and get the values as string
        audiofiles = VideoFacet.get_videofacet_audio(self)
        audiofiles = [audiofile.asset_title for audiofile in audiofiles]
        audiofiles = ",".join(audiofiles)

        # verify the text area fields have correct encoding
        title = self.title.encode('utf-8')
        description = self.vf_description.encode('utf-8')
        excerpt = self.excerpt.encode('utf-8')
        share_note = self.share_note.encode('utf-8')
        content = self.vf_content.encode('utf-8')

        videofacet_download = """
        VideoFacet
        ========
        {title}
        --------------
        Description: {desc}\n
        Story: {story}\n
        Owner: {owner}\n
        Organization: {organization}\n
        Original: {original}\n
        Editor: {editor}\n
        Credit: {credit}\n
        Code: {code}\n
        Excerpt: {excerpt}\n
        Keywords: {keywords}\n
        Status: {status}\n
        Due Edit: {dueedit}\n
        Run Date: {rundate}\n
        Share Note: {sharenote}\n
        Images: {images}\n
        Captions: {captions}\n
        Documents: {documents}\n
        AudioFiles: {audiofiles}\n
        \n
        Content\n
        -------\n
        {content}
        """.format(title=title, desc=description, story=self.story, owner=self.owner,
        organization=self.organization.name, original=self.original_videofacet, editor=self.editor,
        credit=credits, code=self.code, excerpt=excerpt,
        keywords=self.keywords, status=self.status, dueedit=self.due_edit, rundate=self.run_date,
        sharenote=share_note, images=images, captions=self.captions, documents=documents,
        audiofiles=audiofiles, content=content)

        return videofacet_download

    @property
    def description(self):
        return self.vf_description

    @property
    def search_title(self):
        return self.title

    @property
    def type(self):
        return "VideoFacet"



#-----------------------------------------------------------------------#
#   Contributor Associations:
#   WebFacetContributor, PrintFacetContributor,
#   AudioFacetContributor, VideoFacetContributor
#-----------------------------------------------------------------------#

@python_2_unicode_compatible
class WebFacetContributor(models.Model):
    """ Which users are participating in creating the WebFacet. """

    webfacet = models.ForeignKey(
        WebFacet,
    )

    user = models.ForeignKey(
        User,
    )

    user_role = models.CharField(
        max_length=255,
        help_text='What did the user do?',
    )

    def __str__(self):
        return "{webfacet}, {contributor}".format(
                                        webfacet=self.webfacet.title,
                                        contributor=self.user.credit_name,
                                        )


@python_2_unicode_compatible
class PrintFacetContributor(models.Model):
    """ Which users are participating in creating the PrintFacet. """

    printfacet = models.ForeignKey(
        PrintFacet,
    )

    user = models.ForeignKey(
        User,
    )

    user_role = models.CharField(
        max_length=255,
        help_text='What did the user do?'
    )

    def __str__(self):
        return "{printfacet}, {contributor}".format(
                                        printfacet=self.webfacet.title,
                                        contributor=self.user.credit_name,
                                        )


@python_2_unicode_compatible
class AudioFacetContributor(models.Model):
    """ Which users are participating in creating the AudioFacet. """

    audiofacet = models.ForeignKey(
        AudioFacet,
    )

    user = models.ForeignKey(
        User,
    )

    user_role = models.CharField(
        max_length=255,
        help_text='What did the user do?'
    )

    def __str__(self):
        return "{audiofacet}, {contributor}".format(
                                        audiofacet=self.webfacet.title,
                                        contributor=self.user.credit_name,
                                        )


@python_2_unicode_compatible
class VideoFacetContributor(models.Model):
    """ Which users are participating in creating the VideoFacet. """

    videofacet = models.ForeignKey(
        VideoFacet,
    )

    user = models.ForeignKey(
        User,
    )

    user_role = models.CharField(
        max_length=255,
        help_text='What did the user do?'
    )

    def __str__(self):
        return "{videofacet}, {contributor}".format(
                                        videofacet=self.webfacet.title,
                                        contributor=self.user.credit_name,
                                        )
