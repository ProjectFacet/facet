""" Model for editorial application.

    Tables
    ---------
    People:
    - Main Tables: User, Organization, Network
    - Associations: NetworkOrganization

    Content:
    - Main Tables: Series, Story, WebFacet, PrintFacet, AudioFacet, VideoFacet
    - Associations: WebFacetContributors, PrintFacetContributors, AudioFacetContributors,
                    VideoFacetContributors, StoryCopyDetails, SeriesCopyDetails,
                    WebFacetCopyDetails, PrintFacetCopyDetails, AudioFacetCopyDetails,
                    VideoFacetCopyDetails

    MetaMaterials:
    - Main Tables: SeriesPlan, StoryPlan, Asset, Comment, CommentReadStatus,
                   Discussion, PrivateDiscussion
    - Associations:
"""

from django.db import models
from django.contrib.postgres.fields import ArrayField
from simple_history.models import HistoricalRecords
from model_utils.models import TimeStampedModel
from datetime import timedelta
from imagekit.models import ProcessedImageField
from django.contrib.auth.models import AbstractUser
from django.utils.encoding import python_2_unicode_compatible
from django.core.urlresolvers import reverse
from django.utils import timezone

#----------------------------------------------------------------------#
#   People:
#   - Main Tables: User, Organization, Network
#   - Associations: NetworkOrganization, UserSeries, UserStory
#----------------------------------------------------------------------#

@python_2_unicode_compatible
class User(AbstractUser):
    """ Site User.

    A user can either be an admin or a general user. Most users
    can do most things. An admin user can be a site owner, add new
    users, create and manage networks and shift users from active
    to inactive. A general user creates and collaborates on content.
    """

    # Made optional for users not pushing content to an org (freelancers)
    organization = models.ForeignKey(
        'Organization',
        blank=True,
        null=True,
    )

    credit_name = models.CharField(
        max_length=75,
        help_text='Full name of user as listed as a credit on content.',
        blank=True,
    )

    title = models.CharField(
        max_length=100,
        help_text='Professional title',
        blank=True,
    )

    phone = models.CharField(
        max_length=20,
        blank=True,
    )

    bio = models.TextField(
        help_text="Short bio.",
        blank=True,
    )

    expertise = ArrayField(
        models.CharField(max_length=100),
        default=list,
        help_text='Array of user skills and beats to filter/search by.',
        blank=True,
    )

    notes = models.ManyToManyField(
        'UserNote',
        related_name='user_note',
        blank=True,
    )

    # FK to an asset?
    profile_photo = models.ImageField(
        upload_to="users",
        blank=True,
    )

    facebook = models.CharField(
        max_length=250,
        blank=True,
    )

    twitter = models.CharField(
        max_length=250,
        blank=True,
    )

    linkedin = models.CharField(
        max_length=250,
        blank=True,
    )

    instagram = models.CharField(
        max_length=250,
        blank=True,
    )

    snapchat = models.CharField(
        max_length=250,
        blank=True,
    )

    vine = models.CharField(
        max_length=250,
        blank=True,
    )

    website = models.CharField(
        max_length=250,
        blank=True,
    )

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = "Users"
        ordering = ['credit_name']

    def __str__(self):
        return self.credit_name

    @property
    def description(self):
        return "{user}, {title}".format(
                                        user=self.credit_name,
                                        title=self.title
                                        )


class Organization(models.Model):
    """ Media Organization.

    An organization is a media or publishing entity. Organization's are created
    and owned by one admin user. They can be managed by multiple admin users.
    Organizations have many users and serve as the owner of story content. Organizations
    can create and manage Networks. Ownership of an organization can be transferred
    from one admin user to another.
    """

    name = models.CharField(
        max_length=75,
        db_index=True,
    )

    owner = models.ForeignKey(
        User,
        related_name='organization_owner',
    )

    org_description = models.TextField(
        help_text="Short profile of organization.",
        blank=True,
    )

    creation_date = models.DateTimeField(
        auto_now_add=True
    )

    logo = models.ImageField(
        upload_to="organizations",
        blank=True,
    )

    facebook = models.CharField(
        max_length=250,
        blank=True,
    )

    twitter = models.CharField(
        max_length=250,
        blank=True,
    )

    website = models.CharField(
        max_length=250,
        blank=True,
    )


    class Meta:
        verbose_name = 'Organization'
        verbose_name_plural = "Organizations"
        ordering = ['name']

    def __str__(self):
        return self.name

    @property
    def description(self):
        return "{organization}, {description}".format(
                                                    organization=self.name,
                                                    description=self.org_description
                                                    )


class Network(models.Model):
    """ A group of organizations.

    A network is a collection of two or more organizations seeking to create a sharing
    or collaborating relationship. Sharing means the organization can add content that has been
    marked for sharing to that network. Collaborating means that any user from the guest network
    organization(s) can participate in the editorial process on the host organization's content that has been
    selected as collaborative. At the conclusion of the editorial process, the guest can add the final
    version of the content to their own account.
    """

    owner_organization = models.ForeignKey(
        Organization,
        help_text='Organization that owns the network.'
    )

    name = models.CharField(
        max_length=75,
        db_index=True,
        help_text="The name by which members identify the network."
    )

    creation_date = models.DateTimeField(
        auto_now_add=True
    )

    network_description = models.TextField(
        help_text="Short description of a network.",
        blank=True,
    )

    logo = models.ImageField(
        upload_to="organizations",
        blank=True,
    )

    members = models.ManyToManyField(
        Organization,
        through='NetworkOrganization',
        related_name='network_organization',
    )

    class Meta:
        verbose_name = 'Network'
        verbose_name_plural = "Networks"
        ordering = ['name']

    def __str__(self):
        return self.name

    @property
    def description(self):
        return "{network}, {description}".format(
                                                network=self.name,
                                                description=self.network_description
                                                )

#   Associations
#   ------------

class NetworkOrganization(models.Model):
    """ The connection between Organizations and Networks. """

    network = models.ForeignKey(
        Network,
    )

    organization = models.ForeignKey(
        Organization,
    )

    def __str__(self):
        return "{network}, {organization}".format(
                                                network=self.network.name,
                                                organization=self.organization.name
                                                )

#----------------------------------------------------------------------#
#   Content:
#   - Main Tables:  Series, Story, WebFacet, PrintFacet, AudioFacet, VideoFacet
#   - Associations: WebFacetContributors, PrintFacetContributors,
#                   AudioFacetContributors, VideoFacetContributors
#                   StoryCopyDetails, SeriesCopyDetails, WebFacetCopyDetails,
#                   PrintFacetCopyDetails, AudioFacetCopyDetails, VideoFacetCopyDetails
#----------------------------------------------------------------------#

# A Facet is always part of a story, even if there is only one facet.
# A story is always part of a Series, even if it's a series of one.
# (This helps maintain organization of assets as a series level for maximum flexibility.)


class Series(models.Model):
    """ A specific series.

    Series are an organizational component for one or more stories. The primary use is
    to connect multiple stories on a particular topic. Series are also the method for keeping
    assets easily available to all stories/facets.
    """

    name = models.CharField(
        max_length=75,
        help_text='The name identifying the series.'
    )

    series_description = models.TextField(
        blank=True,
        help_text='Short description of a series.',
    )

    owner = models.ForeignKey(
        User,
        related_name='series_owner',
        help_text='The user that created the series.'
    )

    team = models.ManyToManyField(
        User,
        related_name='series_team_member',
        help_text='User contributing to the series.',
        blank=True,
    )

    creation_date = models.DateTimeField(
        auto_now_add=True,
    )

    # For now a boolean for sensitive or not. May have levels of sensitivity later.
    sensitivity = models.BooleanField(
        default=False,
        help_text='Is a series sensitive, for limited viewing?'
    )

    share = models.BooleanField(
        default=False,
        help_text='The series is being shared with a network.'
    )

    share_with = models.ManyToManyField(
        Network,
        related_name='series_shared_with_network',
        help_text='Network ids that a series is shared with.',
        blank=True,
    )

    collaborate = models.BooleanField(
        default=False,
        help_text='The series is being collaborated on with a network.'
    )

    collaborate_with = models.ManyToManyField(
        Network,
        related_name='series_collaborated_with_network',
        help_text='Network ids that a series is open to collaboration with.',
        blank=True,
    )

    archived = models.BooleanField(
        default=False,
        help_text='Is the content no longer active and needed?'
    )

    discussion = models.ForeignKey(
        'Discussion',
        help_text='Id of planning discussion for a series.',
        blank=True,
        null=True,
    )

    assets = models.ManyToManyField(
        'Asset',
        blank=True,
        help_text='',
    )

    class Meta:
        verbose_name = 'Series'
        verbose_name_plural = "Series"
        ordering = ['name']

    def __str__(self):
        return self.name

    @property
    def description(self):
        return "{series}, {description}".format(
                                                series=self.name,
                                                description=self.series_description
                                                )



class Story(models.Model):
    """ The unit of a story.

    A story is the one or more facets that make up a particular story.
    Sharing and collaboration is controlled at the story level.
    The story also controls the sensivity and embargo status of the content.
    """

    series = models.ForeignKey(
        Series,
        blank=True,
        null=True,
    )

    owner = models.ForeignKey(
        User,
        related_name='story_owner',
        help_text='User who created the story'
    )

    name = models.CharField(
        max_length=250,
        help_text='The name by which the story is identified'
    )

    story_description = models.TextField(
        help_text="Short description of a story.",
        blank=True,
    )

    embargo = models.BooleanField(
        default=False,
        help_text='Is a story embargoed?'
        )

    embargo_datetime = models.DateTimeField(
        help_text='When is the story no longer under embargo.',
        blank=True,
        null=True,
    )

    creation_date = models.DateTimeField(
        auto_now_add=True,
        help_text='When was the story created.'
    )

    # connection to users participating in a story
    team = models.ManyToManyField(
        User,
        related_name='story_team_member',
        help_text='User contributing to the story.',
        blank=True,
    )

    sensitive = models.BooleanField(
        default=False,
        help_text='Is a story sensitive and viewing it limited only to the team working on it?'
    )

    share = models.BooleanField(
        default=False,
        help_text='The story is being shared with a network.'
    )

    ready_to_share = models.BooleanField(
        default=False,
        help_text='The story is finished and ready to be copied.'
    )

    share_with = models.ManyToManyField(
        Network,
        related_name='story_shared_with_network',
        help_text='Network ids that a story is shared with.',
        blank=True,
    )

    collaborate = models.BooleanField(
        default=False,
        help_text='The story is being collaborated on with a network.'
    )

    collaborate_with = models.ManyToManyField(
        Network,
        related_name='story_collaborated_with_network',
        help_text='Network ids that a story is open to collaboration with.',
        blank=True,
    )

    archived = models.BooleanField(
        default=False,
        help_text='Is the content no longer active and needed?'
    )

    discussion = models.ForeignKey(
        'Discussion',
        help_text='Id of planning discussion for a story.',
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = 'Story'
        verbose_name_plural = "Stories"
        ordering = ['name']

    def __str__(self):
        return self.name

    @property
    def description(self):
        return "{story}, {description}".format(
                                                story=self.name,
                                                description=self.story_description
                                                )


class WebFacet(models.Model):
    """ Regularly published web content.

    Ex: Daily news, articles, videos, photo galleries
    """

    story = models.ForeignKey(
        Story,
    )

    owner = models.ForeignKey(
        User,
        related_name='webfacetowner'
    )

    original_org = models.ForeignKey(
        Organization,
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

    length = models.IntegerField(
        help_text='Length of the webfacet.',
        blank=True,
    )

    keywords = ArrayField(
        models.CharField(max_length=100),
        default=list,
        help_text='List of keywords for search.',
        blank=True,
    )

    # Choices for WebFacet status.
    DRAFT = 'DRFT'
    PITCH = 'PT'
    IN_PROGRESS = 'IP'
    EDIT = 'EDT'
    REVISION = 'RVN'
    READY = 'RDY'

    WEBFACET_STATUS_CHOICES = (
        (DRAFT, 'Draft'),
        (PITCH, 'Pitch'),
        (IN_PROGRESS, 'In Progress'),
        (EDIT, 'Edit'),
        (REVISION, 'Revision'),
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

    assets = models.ManyToManyField(
        'Asset',
        blank=True,
    )

    captions = models.TextField(
        help_text='Captions and credits for any assets in use.',
        blank=True,
    )

    class Meta:
        verbose_name = 'Webfacet'
        verbose_name_plural = 'Webfacets'
        ordering = ['creation_date']

    def __str__(self):
        return self.title

    @property
    def description(self):
        return "Webfacet: {webfacet} by {credit}".format(
                                webfacet=self.id,
                                credit=self.credit,
                                )

    @property
    def facet_type(self):
        return "WebFacet"


class PrintFacet(models.Model):
    """ The print version of a story.

    Ex: Daily news article, column, story.
    """

    story = models.ForeignKey(
        Story,
    )

    owner = models.ForeignKey(
        User,
        related_name='printfacetowner'
    )

    original_org = models.ForeignKey(
        Organization,
    )

    editor = models.ForeignKey(
        User,
        related_name='printfaceteditor'
    )

    contributors = models.ManyToManyField(
        User,
        through='PrintFacetContributor',
        help_text='Users that contributed to a facet. Used to associate multiple users to a facet.'
    )

    credit = models.ManyToManyField(
        # There can be multiple users listed as the credit.
        User,
        related_name='printfacetcredit',
        help_text='The full user name(s) to be listed as the credit for the facet.'
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

    length = models.IntegerField(
        help_text='Length of the printfacet.',
        blank=True,
    )

    keywords = ArrayField(
        models.CharField(max_length=100),
        default=list,
        help_text='List of keywords for search.',
        blank=True,
    )

    # Choices for WebFacet status.
    DRAFT = 'DRFT'
    PITCH = 'PT'
    IN_PROGRESS = 'IP'
    EDIT = 'EDT'
    REVISION = 'RVN'
    READY = 'RDY'

    PRINTFACET_STATUS_CHOICES = (
        (DRAFT, 'Draft'),
        (PITCH, 'Pitch'),
        (IN_PROGRESS, 'In Progress'),
        (EDIT, 'Edit'),
        (REVISION, 'Revision'),
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
        blank=True,
    )

    discussion = models.ForeignKey(
        'Discussion',
        help_text='Id of edit discussion for the printfacet.',
        blank=True,
        null=True,
    )

    edit_history = HistoricalRecords()

    share_note = models.TextField(
        help_text='Information for organizations making a copy of the printfacet.'
    )

    assets = models.ManyToManyField(
        'Asset',
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

    @property
    def description(self):
        return "Printfacet: {printfacet} by {credit}".format(
                                printfacet=self.id,
                                credit=self.credit,
                                )

    @property
    def facet_type(self):
        return "PrintFacet"


class AudioFacet(models.Model):
    """ Scheduled radio programming.

    Ex: A single segment on Morning Edition.
    """

    story = models.ForeignKey(
        Story,
    )

    owner = models.ForeignKey(
        User,
        related_name='audiofacetowner'
    )

    original_org = models.ForeignKey(
        Organization,
    )

    editor = models.ForeignKey(
        User,
        related_name='audiofaceteditor'
    )

    contributors = models.ManyToManyField(
        User,
        through='AudioFacetContributor',
        help_text='Users that contributed to a facet. Used to associate multiple users to a facet.'
    )

    credit = models.ManyToManyField(
        # There can be multiple users listed as the credit.
        User,
        related_name='audiofacetcredit',
        help_text='The full user name(s) to be listed as the credit for the facet.'
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

    length = models.IntegerField(
        help_text='Runtime of the audiofacet.',
        blank=True,
    )

    keywords = ArrayField(
        models.CharField(max_length=100),
        default=list,
        help_text='List of keywords for search.'
    )

    # Choices for WebFacet status.
    DRAFT = 'DRFT'
    PITCH = 'PT'
    IN_PROGRESS = 'IP'
    EDIT = 'EDT'
    REVISION = 'RVN'
    READY = 'RDY'

    AUDIOFACET_STATUS_CHOICES = (
        (DRAFT, 'Draft'),
        (PITCH, 'Pitch'),
        (IN_PROGRESS, 'In Progress'),
        (EDIT, 'Edit'),
        (REVISION, 'Revision'),
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

    assets = models.ManyToManyField(
        'Asset',
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

    @property
    def description(self):
        return "Audiofacet: {audiofacet} by {credit}".format(
                                audiofacet=self.id,
                                credit=self.credit,
                                )

    @property
    def facet_type(self):
        return "AudioFacet"


class VideoFacet(models.Model):
    """ Scheduled television programming.

    Ex: An episode of a television program.
    """

    story = models.ForeignKey(
        Story,
    )

    owner = models.ForeignKey(
        User,
        related_name='videofacetowner'
    )

    original_org = models.ForeignKey(
        Organization,
    )

    editor = models.ForeignKey(
        User,
        related_name='videofaceteditor'
    )

    contributors = models.ManyToManyField(
        User,
        through='VideoFacetContributor',
        help_text='Users that contributed to a facet. Used to associate multiple users to a facet.'
    )

    credit = models.ManyToManyField(
        # There can be multiple users listed as the credit.
        User,
        related_name='videofacetcredit',
        help_text='The full user name(s) to be listed as the credit for the facet.'
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

    length = models.IntegerField(
        help_text='Runtime of the videofacet.',
        blank=True,
    )

    keywords = ArrayField(
        models.CharField(max_length=100),
        default=list,
        help_text='List of keywords for search.'
    )

    # Choices for WebFacet status.
    DRAFT = 'DRFT'
    PITCH = 'PT'
    IN_PROGRESS = 'IP'
    EDIT = 'EDT'
    REVISION = 'RVN'
    READY = 'RDY'

    VIDEOFACET_STATUS_CHOICES = (
        (DRAFT, 'Draft'),
        (PITCH, 'Pitch'),
        (IN_PROGRESS, 'In Progress'),
        (EDIT, 'Edit'),
        (REVISION, 'Revision'),
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

    assets = models.ManyToManyField(
        'Asset',
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

    @property
    def description(self):
        return "Videofacet: {videofacet} by {credit}".format(
                                videofacet=self.id,
                                credit=self.credit,
                                )

    @property
    def facet_type(self):
        return "VideoFacet"


#   Associations
#   ------------

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


class SeriesCopyDetail(models.Model):
    """ The details of each copy of a series.

    Each time an organization elects to copy a shared facet, query to see if the
    series has already been copied over. If not copy the series and the story to the
    new organization.
    """

    partner = models.ForeignKey(
        Organization,
        help_text='Organization that made the copy.'
    )

    original_series_id = models.ForeignKey(
        Series,
        help_text='Original id of the series.'
    )

    partner_series_id = models.SlugField(
        max_length = 15,
        help_text='Id of the series on the copying organization\'s site.'
    )

    copy_date = models.DateTimeField(
        auto_now_add=True,
        help_text='Datetime when copy was made.'
    )

    def __str__(self):
        return "Copyinfo for {copyorg} \'s copy of series: {series}".format(
                                copyorg=self.partner.name,
                                series=self.original_series_id
                                )


class StoryCopyDetail(models.Model):
    """ The details of each copy of a story.

    Each time an organization elects to copy a shared facet, query to see if the
    story has already been copied over. If not, copy the story to the new organization.
    """

    partner = models.ForeignKey(
        Organization,
        help_text='Organization that made the copy.'
    )

    original_story_id = models.ForeignKey(
        Story,
        help_text='Original id of the story.'
    )

    partner_story_id = models.SlugField(
        max_length = 15,
        help_text='Id of the story on the copying organization\'s site.'
    )

    copy_date = models.DateTimeField(
        auto_now_add=True,
        help_text='Datetime when copy was made.'
    )

    def __str__(self):
        return "Copyinfo for {copyorg} \'s copy of story: {story}".format(
                                copyorg=self.partner.name,
                                story=self.original_story_id,
                                )


class WebFacetCopyDetail(models.Model):
    """ The details of a each copy of a webfacet. """

    partner = models.ForeignKey(
        Organization,
        help_text='Organization that made the copy.'
    )

    original_webfacet_id = models.ForeignKey(
        WebFacet,
        help_text='Original id of the story.'
    )

    new_webfacet_id = models.SlugField(
        max_length = 15,
        help_text='Id of the story on the copying organization\'s site.'
    )

    copy_date = models.DateTimeField(
        auto_now_add=True,
        help_text='Datetime when copy was made.'
    )

    def __str__(self):
        return "Copyinfo for {copyorg} \'s copy of webfacet: {webfacet}".format(
                                copyorg=self.partner.name,
                                webfacet=self.original_webfacet_id,
                                )


class PrintFacetCopyDetail(models.Model):
    """ The details of a each copy of a printfacet. """

    partner = models.ForeignKey(
        Organization,
        help_text='Organization that made the copy.'
    )

    original_printfacet_id = models.ForeignKey(
        PrintFacet,
        help_text='Original id of the story.'
    )

    new_printfacet_id = models.SlugField(
        max_length = 15,
        help_text='Id of the story on the copying organization\'s site.'
    )

    copy_date = models.DateTimeField(
        auto_now_add=True,
        help_text='Datetime when copy was made.'
    )

    def __str__(self):
        return "Copyinfo for {copyorg} \'s copy of printfacet: {printfacet}".format(
                                copyorg=self.partner.name,
                                printfacet=self.original_printfacet_id,
                                )


class AudioFacetCopyDetail(models.Model):
    """ The details of a each copy of a audiofacet. """

    partner = models.ForeignKey(
        Organization,
        help_text='Organization that made the copy.'
    )

    original_audiofacet_id = models.ForeignKey(
        AudioFacet,
        help_text='Original id of the story.'
    )

    new_audiofacet_id = models.SlugField(
        max_length = 15,
        help_text='Id of the story on the copying organization\'s site.'
    )

    copy_date = models.DateTimeField(
        auto_now_add=True,
        help_text='Datetime when copy was made.'
    )

    def __str__(self):
        return "Copyinfo for {copyorg} \'s copy of audiofacet: {audiofacet}".format(
                                copyorg=self.partner.name,
                                audiofacet=self.original_audiofacet_id,
                                )


class VideoFacetCopyDetail(models.Model):
    """ The details of a each copy of a videofacet. """

    partner = models.ForeignKey(
        Organization,
        help_text='Organization that made the copy.'
    )

    original_videofacet_id = models.ForeignKey(
        VideoFacet,
        help_text='Original id of the story.'
    )

    new_videofacet_id = models.SlugField(
        max_length = 15,
        help_text='Id of the story on the copying organization\'s site.'
    )

    copy_date = models.DateTimeField(
        auto_now_add=True,
        help_text='Datetime when copy was made.'
    )

    def __str__(self):
        return "Copyinfo for {copyorg} \'s copy of videofacet: {videofacet}".format(
                                copyorg=self.partner.name,
                                videofacet=self.original_videofacet_id,
                                )

#----------------------------------------------------------------------#
#   MetaMaterials:
#   - Main Tables:  Asset, Note, UserNote, SeriesNote, StoryNote, Comment
#                   CommentReadStatus, Discussion, PrivateDiscussion,
#   - Associations: None
#----------------------------------------------------------------------#

class Asset(models.Model):
    """ Assets for all the content contained in a series.

    Because series are an organizational container for all content, whether
    there is one or more stories, making the asset associated with the series,
    makes it easily available to all content associated with it, rather than the
    assets either be attached to a story or to a series.
    """

    owner = models.ForeignKey(
        User,
        related_name='asset_owner',
    )

    asset_description = models.TextField(
        max_length=300,
        help_text='What is the asset. (If a photo or graphic, it should be the caption.)',
        blank=True,
    )

    attribution = models.TextField(
        max_length=200,
        help_text='The appropriate information for crediting the asset.',
        blank=True,
    )

    s3_link = models.URLField(
        max_length=300,
        help_text='The item on S3.'
    )

    #Choices for Asset type
    PHOTO = 'PIC'
    GRAPHIC = 'GRAPH'
    AUDIO = 'AUD'
    VIDEO = 'VID'
    DOCUMENT = 'DOC'

    ASSET_TYPE_CHOICES = (
        (PHOTO, 'Photograph'),
        (GRAPHIC, 'Graphic'),
        (AUDIO, 'Audio'),
        (VIDEO, 'Video'),
        (DOCUMENT, 'Document'),
    )

    asset_type = models.CharField(
        max_length=20,
        choices = ASSET_TYPE_CHOICES,
        help_text='What kind is the asset.'
    )

    creation_date = models.DateTimeField(
        auto_now_add=True,
        help_text='When the asset was created.'
    )

    keywords = ArrayField(
        models.CharField(max_length=100),
        default=list,
        help_text='List of keywords for search.'
    )

    def __str__(self):
        return "Asset: {asset} is a {asset_type}".format(
                                asset=self.id,
                                asset_type=self.asset_type,
                                )


class Note(models.Model):
    """ Abstract base class for notes."""

    text = models.TextField(
        help_text='Content of the note',
        blank=True,
    )

    creation_date = models.DateTimeField(
        auto_now_add=True,
        help_text='When the note was created.'
    )

    class Meta:
        abstract = True


class UserNote(Note):
    """ General purpose notes from a user. """

    owner = models.ForeignKey(
        User,
        related_name='usernote_owner'
    )

    title = models.CharField(
        max_length=255,
    )

    keywords = ArrayField(
        models.CharField(max_length=100),
        default=list,
        help_text='List of keywords for search.'
    )


class SeriesNote(Note):
    """ A note attached to a series."""

    owner = models.ForeignKey(
        User,
        related_name='seriesnote_owner'
    )

    title = models.CharField(
        max_length=255,
    )

    series = models.ForeignKey(
        Series,
        related_name='Se',
    )

    def __str__(self):
        return "SeriesNote: {seriesnote} for Series: {series}".format(
                                seriesnote=self.id,
                                series=self.series.id,
                                )


class StoryNote(Note):
    """ Planning notes and conversation for a story. """

    owner = models.ForeignKey(
        User,
        related_name='storynote_owner'
    )

    title = models.CharField(
        max_length=255,
    )

    story = models.ForeignKey(
        Story,
    )

    def __str__(self):
        return "StoryNote: {storynote} for Story: {story}".format(
                                storynote=self.id,
                                story=self.story.id,
                                )


class DiscussionManager(models.Manager):
    """ Custom manager for discussions."""

    def create_discussion(self, discussion_type):
        """ Method for quick creation of a discussion."""
        discussion = self.create(discussion_type=discussion_type)
        return discussion


class Discussion(models.Model):
    """ Class for  for related comments. """

    # Choices for Discussion type
    PRIVATE = 'PRI'
    SERIESPLAN = 'SER'
    STORYPLAN = 'STO'
    WEBFACET = 'WF'
    PRINTFACET = 'PF'
    AUDIOFACET = 'AF'
    VIDEOFACET = 'VF'

    DISCUSSION_TYPE_CHOICES = (
        (PRIVATE, 'Private Conversation'),
        (SERIESPLAN, 'Series Conversation'),
        (STORYPLAN, 'Story Conversation'),
        (WEBFACET, 'WebFacet Conversation'),
        (PRINTFACET, 'PrintFacet Conversation'),
        (AUDIOFACET, 'AudioFacet Conversation'),
        (VIDEOFACET, 'VideoFacet Conversation'),
    )

    discussion_type = models.CharField(
        max_length=25,
        choices=DISCUSSION_TYPE_CHOICES,
        help_text='What kind of discussion is it.'
    )

    objects = DiscussionManager()

    def __str__(self):
        return "Discussion:{discussion} from {discussion_type}".format(
                                discussion=self.id,
                                discussion_type=self.discussion_type
                                )


class PrivateDiscussion(models.Model):
    """ Signifier of private conversations.

    Private conversations can occur between two or more individuals and only exist in their
    own inboxes and are not attached to any content types.
    """

    discussion = models.ForeignKey(
        Discussion,
    )

    users = models.ManyToManyField(
        User,
        related_name='private_discussion_user',
    )

    def __str__(self):
        return "Private discussion:{discussion}.".format(
                                discussion=self.id,
                                )

class CommentManager(models.Manager):
    """ Custom manager for comments."""

    def create_comment(self, user, discussion, text):
        """ Method for quick creation of a discussion."""
        comment = self.create(user=user, discussion=discussion, text=text)
        return comment


class Comment(models.Model):
    """An individual comment.

    Comments can be made on a seriesplan, storyplan, webfacet,
    audiofacet, videfacet, or between one or more people privately.
    """

    user = models.ForeignKey(
        User,
    )

    discussion = models.ForeignKey(
        Discussion,
    )

    text = models.TextField(
        help_text='The content of the comment.'
    )

    date = models.DateTimeField(
        auto_now_add=True,
    )

    objects = CommentManager()

    class Meta:
        ordering = ['date']

    def __str__(self):
        return "Comment:{comment} from discussion:{discussion}".format(
                                comment=self.id,
                                discussion=self.discussion.id,
                                )


class CommentReadStatus(models.Model):
    """ Tracking if a user involved in a discussion has read the most recent
    comment in order to surface unread comments first.
    """

    comment = models.ForeignKey(
        Comment,
    )

    user = models.ForeignKey(
        User,
    )

    datetime_read = models.DateTimeField(
        auto_now_add=True,
    )

    has_read = models.BooleanField(
        default=True,
    )

    def __str__(self):
        return "Comment:{comment} has {status} read status.".format(
                                comment=self.comment.id,
                                status=self.has_read,
                                )

#   Associations
#   ------------

# None
