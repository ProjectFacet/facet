from django.contrib.postgres.fields import ArrayField
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.encoding import python_2_unicode_compatible
from simple_history.models import HistoricalRecords

from . import User, Organization, Story
from .discussion import Discussion


#-----------------------------------------------------------------------#
#   FACET
#-----------------------------------------------------------------------#


@python_2_unicode_compatible
class FacetTemplate(models.Model):
    """Template for facets.

    A template is a collection of fields so that when adding/editing a facet,
    only appropriate fields are shown.
    """

    name = models.CharField(
        max_length=50,
    )

    # A template without an organization is a "site-wide" template;
    # when listing templates for an organization, list the site-wide and
    # ones that match the organization.
    organization = models.ForeignKey(
        "Organization",
        blank=True,
        null=True,
    )

    owner = models.ForeignKey(
        "User",
        blank=True,
        null=True,
    )

    description = models.CharField(
        max_length=100,
        blank=True,
    )

    fields_used = ArrayField(
        models.CharField(max_length=50),
        default=list,
        help_text='Fields used by this template.',
        blank=True,
    )

    creation_date = models.DateTimeField(
        auto_now_add=True,
        help_text='When template was created.',
        blank=True,
    )

    is_active = models.BooleanField(
        default=True,
    )

    class Meta:
        ordering = ['id']
        unique_together = ['name', 'organization']

    def __str__(self):
        return self.name

    @property
    def search_title(self):
        return self.name

    @property
    def type(self):
        return "Facet Template"

    def get_absolute_url(self):
        return reverse('facet_template_edit', kwargs={'pk': self.id})


# field which will appear on all facet-editing forms -- and therefore do not
# need to be in the "fields_used" for a template.

COMMON_FIELDS = {
    "name",
    "headline",
    "description",
    "editor",
    "credit",
    # "team",
    "content",
    "status",
    "due_edit",
    "run_date",
    "keywords",
    # "template",
    # "story",
}

FACETTEMPLATE_FIELD_CHOICES = {
    "excerpt",
    "update_note",
    "share_note",
    "edit_note",
    "dateline",
    "topic_code",
    "internal_code",
    "content_license",
    "length",
    "wordcount",
    "related_links",
    "github_link",
    "embeds",
    "sources",
    "pronounciations",
    "sponsors",
    "pull_quotes",
    "sidebar_content",
    "producer",
    "series_title",
    "episode_number",
    "usage_rights",
    "tape_datetime",
    "locations",
    "custom_one",
    "custom_two",
    "custom_three",
    "custom_four",
    "custom_five",
}

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

    template = models.ForeignKey(
        FacetTemplate,
    )

    story = models.ForeignKey(
        Story,
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

    discussion = models.ForeignKey(
        'Discussion',
        help_text='Id of discussion for the facet.',
        blank=True,
        null=True,
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

    update_note  = models.TextField(
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
        null=True,
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

    sources = models.TextField(
        help_text='List of sources in the facet.',
        blank=True,
    )

    edit_note = models.TextField(
        help_text='Information regarding allowable extent of editing and suggestions for specific kinds of edits.',
        blank=True,
    )

    pronounciations = models.TextField(
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
    # pushed_to_wp = models.BooleanField(
    #     default=False,
    #     help_text='Whether the facet has been pushed to the organization WordPress site.',
    # )

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
        null=True,
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
        return reverse('facet_edit', kwargs={'pk': self.id, 'story': self.story_id})

    def copy(self):
        """ Create a copy of a facet for a partner organization in a network."""

        self.id = None
        self.original=False
        self.code = ''
        self.status= 'NR'
        self.due_edit = None
        self.run_date = None
        self.discussion = Discussion.objects.create_discussion("F")
        self.edit_history = None
        self.save()
        return self

    def get_facet_images(self):
        """Retrieve all images objects associated with a facet."""

        return self.image_assets.all()

    def get_facet_documents(self):
        """Retrieve all documents objects associated with a facet."""
        return self.document_assets.all()

    def get_facet_audio(self):
        """Retrieve all audio objects associated with a facet."""
        return self.audio_assets.all()

    def get_facet_video(self):
        """Retrieve all video objects associated with a facet."""
        return self.video_assets.all()

    def get_facet_download(self):
        """ Return rst formatted string for downloading facet and its meta."""

        # loop over m2m and get the values as string
        credits = self.credit.all()
        credits = [ user.credit_name for user in credits]
        credits = ",".join(credits)

        editors = self.editor.all()
        editors = [ user.credit_name for user in editors]
        editors = ",".join(editors)

        # loop over m2m and get the values as string
        images = self.image_assets.all()
        images = [image.title for image in images]
        images = ",".join(images)

        # loop over m2m and get the values as string
        documents = self.document_assets.all()
        documents = [document.title for document in documents]
        documents = ",".join(documents)

        # loop over m2m and get the values as string
        audiofiles = self.audio_assets.all()
        audiofiles = [audiofile.title for audiofile in audiofiles]
        audiofiles = ",".join(audiofiles)

        # verify the text area fields have correct encoding
        name = self.name.encode('utf-8')
        description = self.description.encode('utf-8')
        excerpt = self.excerpt.encode('utf-8')
        share_note = self.share_note.encode('utf-8')
        content = self.content.encode('utf-8')

        facet_download = """
        Facet
        ========
        {name}
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
        Documents: {documents}\n
        AudioFiles: {audiofiles}\n
        \n
        Content\n
        -------
        {content}
        """.format(name=name, desc=description, story=self.story, owner=self.owner,
        organization=self.organization.name, original=self.original, editor=editors,
        credit=credits, code=self.internal_code, excerpt=excerpt,
        keywords=self.keywords, status=self.status, dueedit=self.due_edit, rundate=self.run_date,
        sharenote=share_note, images=images, documents=documents, audiofiles=audiofiles, content=content)

        return facet_download

    @property
    def search_title(self):
        return self.name

    @property
    def type(self):
        return "Facet"

    def is_editable_by_org(self, org):
        """Can this facet be edited by this org?"""

        # FIXME: add contractor access?

        story = self.organization

        return (org == story.organization or
                (story.collaborate and org in story.collaborate_with.all()))


@receiver(post_save, sender=Facet)
def add_discussion(sender, instance, **kwargs):
    if not instance.discussion:
        instance.discussion = Discussion.objects.create_discussion("F")
        instance.save()



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
    includes the 7 established variations of the Creative Commons license;
    these have a blank Organization field.

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
        verbose_name = 'Content License'
        verbose_name_plural = 'Content Licenses'
        ordering = ['name']

    def __str__(self):
        return self.name
