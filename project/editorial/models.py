""" Model for editorial application.

    Tables
    ---------
    People:
    - Main Tables: User, Organization, Network
    - Associations: NetworkOrganization

    Content:
    - Main Tables: Series, Story, WebFacet, PrintFacet, AudioFacet, VideoFacet
    - Associations: WebFacetContributors, PrintFacetContributors, AudioFacetContributors, VideoFacetContributors
                StoryCopyDetails, SeriesCopyDetails, WebFacetCopyDetails, PrintFacetCopyDetails, AudioFacetCopyDetails, VideoFacetCopyDetails

    MetaMaterials:
    - Main Tables: SeriesPlan, StoryPlan, Asset, Comment, CommentReadStatus, Discussion, PrivateDiscussion
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
# from django.utils import timezone


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

    # id = django automatic id

    code = models.SlugField(
        max_length=15,
        db_index=True,
        help_text='Unique code for a user.',
        blank=True,
    )

    # could make ManyToMany to accomodate freelance users contributing
    # to multiple organizations
    # or make optional for users not pushing content to an org
    organization_id = models.ForeignKey(
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

    profile_photo = models.ImageField(
        upload_to="users",
        blank=True,
    )

    #Links to user's professional social media accounts
    facebook = models.CharField(
        max_length=150,
        blank=True,
    )

    twitter = models.CharField(
        max_length=150,
        blank=True,
    )

    linkedin = models.CharField(
        max_length=150,
        blank=True,
    )

    instagram = models.CharField(
        max_length=150,
        blank=True,
    )

    snapchat = models.CharField(
        max_length=150,
        blank=True,
    )

    vine = models.CharField(
        max_length=150,
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

    # id = django automatic id

    name = models.CharField(
        max_length=75,
        db_index=True,
    )

    owner = models.ForeignKey(
        User,
    )

    org_description = models.TextField(
        help_text="Short profile of organization.",
        blank=True,

    )

    creation_date = models.DateTimeField(
        auto_now_add=True
    )

    organization_logo = models.ImageField(
        upload_to="organizations",
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

    # id = django automatic id

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
        blank=True,    )

    member = models.ManyToManyField(
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

    # id = django automatic id

    network_id = models.ForeignKey(
        Network,
    )

    organization_id = models.ForeignKey(
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

    # id = django automatic id

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

    # connection to users participating in a series
    team = models.ManyToManyField(
        User,
        related_name='series_team_member',
        help_text='User contributing to the series.',
        blank=True,
    )

    creation_date = models.DateTimeField(
        auto_now_add=True,
    )

    share = models.BooleanField(
        default=False,
        help_text='The series is being shared with a network.'
    )

    # For now a boolean for sensitive or not. May have levels of sensitivity later.
    sensitivity = models.BooleanField(
        default=False,
        help_text='Is a series sensitive, for limited viewing?'
    )

    collaborate = models.BooleanField(
        default=False,
        help_text='The series is being collaborated on with a network.'
    )

    share_with = models.ManyToManyField(
        Network,
        related_name='series_shared_with_network',
        help_text='Network ids that a series is shared with.',
        blank=True,
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

    # id = django automatic id

    series_id = models.ForeignKey(
        Series,
        blank=True,
        null=True
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

    share = models.BooleanField(
        default=False,
        help_text='The story is being shared with a network.'
    )

    ready_to_share = models.BooleanField(
        default=False,
        help_text='The story is finished and ready to be copied.'
    )

    # For now a boolean for sensitive or not. May have levels of sensitivity later.
    sensitivity = models.BooleanField(
        default=False,
        help_text='Is a story sensitive, for limited viewing?'
    )

    collaborate = models.BooleanField(
        default=False,
        help_text='The story is being collaborated on with a network.'
    )

    share_with = models.ManyToManyField(
        Network,
        related_name='story_shared_with_network',
        help_text='Network ids that a story is shared with.',
        blank=True,
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

    # id = django automatic id

    story_id = models.ForeignKey(
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
        help_text='Users that contributed to a facet. Used to associate multiple users to a facet.'
    )

    credit = models.ManyToManyField(
        # There can be multiple users listed as the credit.
        User,
        related_name='webfacetcredit',
        help_text='The full user name(s) to be listed as the credit for the facet.'
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

    content = models.TextField(
        help_text='Content of the webFacet.',
        blank=True,
    )

    length = models.IntegerField(
        help_text='Wordcount of the WebFacet.',
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
    )

    run_date = models.DateTimeField(
        help_text='Planned run date.',
        blank=True
    )

    creation_date = models.DateTimeField(
        auto_now_add=True,
        help_text='Day WebFacet was created.'
    )

    discussion_id = models.ForeignKey(
        'Discussion',
        help_text='Id of edit discussion for the webfacet.'
    )

    edit_history = HistoricalRecords()

    share_note = models.TextField(
        help_text='Information for organizations making a copy of the webfacet.',
        blank=True,
    )

    assets = models.ManyToManyField(
        'Asset',
    )

    class Meta:
        verbose_name = 'Webfacet'
        verbose_name_plural = 'Webfacets'
        ordering = ['creation_date']

    def __str__(self):
        return self.webfacet_title

    @property
    def description(self):
        return "Webfacet: {webfacet} by {credit}".format(
                                webfacet=self.id,
                                credit=self.credit,
                                )


class PrintFacet(models.Model):
    """ The print version of a story.

    Ex: Daily news article, column, story.
    """

    # id = django automatic id

    story_id = models.ForeignKey(
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

    content = models.TextField(
        help_text='Content of the printfacet.',
        blank=True,
    )

    length = models.IntegerField(
        help_text='Wordcount of the printfacet.',
        blank=True,
    )

    keywords = ArrayField(
        models.CharField(max_length=100),
        default=list,
        help_text='List of keywords for search.',
        blank=True,
    )

    due_edit = models.DateTimeField(
        help_text='Due for edit.',
        blank=True,
    )

    run_date = models.DateTimeField(
        help_text='Planned run date.',
        blank=True,
    )

    creation_date = models.DateTimeField(
        auto_now_add=True,
        help_text='Day printfacet was created.',
        blank=True,
    )

    discussion_id = models.ForeignKey(
        'Discussion',
        help_text='Id of edit discussion for the printfacet.'
    )

    edit_history = HistoricalRecords()

    share_note = models.TextField(
        help_text='Information for organizations making a copy of the printfacet.'
    )

    assets = models.ManyToManyField(
        'Asset',
    )

    class Meta:
        verbose_name = 'Printfacet'
        verbose_name_plural = 'Printfacets'
        ordering = ['creation_date']

    def __str__(self):
        return self.printfacet_title

    @property
    def description(self):
        return "Printfacet: {printfacet} by {credit}".format(
                                printfacet=self.id,
                                credit=self.credit,
                                )


class AudioFacet(models.Model):
    """ Scheduled radio programming.

    Ex: A single segment on Morning Edition.
    """

    # id = django automatic id

    story_id = models.ForeignKey(
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

    content = models.TextField(
        help_text='Content of the audiofacet.',
        blank=True,
    )

    length = models.IntegerField(
        help_text='Wordcount of the audiofacet.',
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
    )

    run_date = models.DateTimeField(
        help_text='Planned run date.',
        blank=True,
    )

    creation_date = models.DateTimeField(
        auto_now_add=True,
        help_text='Day audiofacet was created.',
        blank=True,
    )

    discussion_id = models.ForeignKey(
        'Discussion',
        help_text='Id of edit discussion for the audiofacet.'
    )

    edit_history = HistoricalRecords()

    share_note = models.TextField(
        help_text='Information for organizations making a copy of the audiofacet.',
        blank=True,

    )

    assets = models.ManyToManyField(
        'Asset',
    )

    class Meta:
        verbose_name = 'Audiofacet'
        verbose_name_plural = 'Audiofacets'
        ordering = ['creation_date']

    def __str__(self):
        return self.audiofacet_title

    @property
    def description(self):
        return "Audiofacet: {audiofacet} by {credit}".format(
                                audiofacet=self.id,
                                credit=self.credit,
                                )


class VideoFacet(models.Model):
    """ Scheduled television programming.

    Ex: An episode of a television program.
    """

    # id = django automatic id

    story_id = models.ForeignKey(
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

    content = models.TextField(
        help_text='Content of the videofacet.',
        blank=True,
    )

    length = models.IntegerField(
        help_text='Wordcount of the videofacet.',
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
    )

    run_date = models.DateTimeField(
        help_text='Planned run date.',
        blank=True,
    )

    creation_date = models.DateTimeField(
        auto_now_add=True,
        help_text='Day videofacet was created.',
        blank=True,
    )

    discussion_id = models.ForeignKey(
        'Discussion',
        help_text='ID of edit discussion for the videofacet.'
    )

    edit_history = HistoricalRecords()

    share_note = models.TextField(
        help_text='Information for organizations making a copy of the videofacet.',
        blank=True,
    )

    assets = models.ManyToManyField(
        'Asset',
    )

    class Meta:
        verbose_name = 'Videofacet'
        verbose_name_plural = 'Videofacets'
        ordering = ['creation_date']

    def __str__(self):
        return self.videofacet_title

    @property
    def description(self):
        return "Videofacet: {videofacet} by {credit}".format(
                                videofacet=self.id,
                                credit=self.credit,
                                )


#   Associations
#   ------------


class WebFacetContributor(models.Model):
    """ Which users are participating in creating the WebFacet. """

    # id = django automatic id

    webfacet_id = models.ForeignKey(
        WebFacet,
    )

    user_id = models.ForeignKey(
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

    # id = django automatic id

    printfacet_id = models.ForeignKey(
        PrintFacet,
    )

    user_id = models.ForeignKey(
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

    # id = django automatic id

    audiofacet_id = models.ForeignKey(
        AudioFacet,
    )

    user_id = models.ForeignKey(
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

    # id = django automatic id

    videofacet_id = models.ForeignKey(
        VideoFacet,
    )

    user_id = models.ForeignKey(
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

    # id = django automatic id

    organization_id = models.ForeignKey(
        Organization,
        help_text='Id of the organization that made the copy.'
    )

    original_series_id = models.ForeignKey(
        Series,
        help_text='Original id of the series.'
    )

    new_series_id = models.SlugField(
        max_length = 15,
        help_text='Id of the series on the copying organization\'s site.'
    )

    copy_date = models.DateTimeField(
        auto_now_add=True,
        help_text='Datetime when copy was made.'
    )

    def __str__(self):
        return "Copyinfo for {copyorg} \'s copy of series: {series}".format(
                                copyorg=self.organization_id.name,
                                series=self.original_series_id,
                                )


class StoryCopyDetail(models.Model):
    """ The details of each copy of a story.

    Each time an organization elects to copy a shared facet, query to see if the
    story has already been copied over. If not, copy the story to the new organization.
    """

    # id = django automatic id

    organization_id = models.ForeignKey(
        Organization,
        help_text='Id of the organization that made the copy.'
    )

    original_story_id = models.ForeignKey(
        Story,
        help_text='Original id of the story.'
    )

    new_story_id = models.SlugField(
        max_length = 15,
        help_text='Id of the story on the copying organization\'s site.'
    )

    copy_date = models.DateTimeField(
        auto_now_add=True,
        help_text='Datetime when copy was made.'
    )

    def __str__(self):
        return "Copyinfo for {copyorg} \'s copy of story: {story}".format(
                                copyorg=self.organization_id.name,
                                story=self.original_story_id,
                                )


class WebFacetCopyDetail(models.Model):
    """ The details of a each copy of a webfacet. """

    # id = django automatic id

    organization_id = models.ForeignKey(
        Organization,
        help_text='Id of the organization that made the copy.'
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
                                copyorg=self.organization_id.name,
                                webfacet=self.original_webfacet_id,
                                )


class PrintFacetCopyDetail(models.Model):
    """ The details of a each copy of a printfacet. """

    # id = django automatic id

    organization_id = models.ForeignKey(
        Organization,
        help_text='Id of the organization that made the copy.'
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
                                copyorg=self.organization_id.name,
                                printfacet=self.original_printfacet_id,
                                )


class AudioFacetCopyDetail(models.Model):
    """ The details of a each copy of a audiofacet. """

    # id = django automatic id

    organization_id = models.ForeignKey(
        Organization,
        help_text='Id of the organization that made the copy.'
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
                                copyorg=self.organization_id.name,
                                audiofacet=self.original_audiofacet_id,
                                )


class VideoFacetCopyDetail(models.Model):
    """ The details of a each copy of a videofacet. """

    # id = django automatic id

    organization_id = models.ForeignKey(
        Organization,
        help_text='Id of the organization that made the copy.'
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
                                copyorg=self.organization_id.name,
                                videofacet=self.original_videofacet_id,
                                )


#----------------------------------------------------------------------#
#   MetaMaterials:
#   - Main Tables:  SeriesPlan, StoryPlan, Asset, Comment
#                   CommentReadStatus, Discussion, PrivateDiscussion
#   - Associations: None
#----------------------------------------------------------------------#


class SeriesPlan(models.Model):
    """ Planning notes and conversation for a series. """

    # id = django automatic id

    series_id = models.ForeignKey(
        Series,
    )

    note = models.TextField(
        help_text='Notes for planning a series. Can be any details needed to be tracked while a series is planned/reported.'
    )

    note_owner = models.ForeignKey(
        User,
    )

    series_discussion_id = models.ForeignKey(
        'Discussion',
    )

    def __str__(self):
        return "SeriesPlan: {seriesplan} for Series: {series}".format(
                                seriesplan=self.id,
                                series=self.series_id.id,
                                )


class StoryPlan(models.Model):
    """ Planning notes and conversation for a story. """

    # id = django automatic id

    story_id = models.ForeignKey(
        Story,
    )

    note = models.TextField(
        help_text='Notes for planning a story. Can be any details needed to be tracked while a story is planned/reported.'
    )

    note_owner = models.ForeignKey(
        User,
    )

    story_discussion_id = models.ForeignKey(
        'Discussion',
    )

    def __str__(self):
        return "StoryPlan: {storyplan} for Story: {story}".format(
                                storyplan=self.id,
                                story=self.story_id.id,
                                )


class Asset(models.Model):
    """ Assets for all the content contained in a series.

    Because series are an organizational container for all content, whether
    there is one or more stories, making the asset associated with the series,
    makes it easily available to all content associated with it, rather than the
    assets either be attached to a story or to a series.
    """

    # id = django automatic id

    series_id = models.ForeignKey(
        Series,
    )

    owner = models.ForeignKey(
        User,
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

    def __str__(self):
        return "Asset: {asset_id} is a {asset_type}".format(
                                asset_id=self.id,
                                asset_type=self.asset_type,
                                )


class Discussion(models.Model):
    """ Class for  for related comments. """

    # id = django automatic id

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

    # id = django automatic id

    discussion_id = models.ForeignKey(
        Discussion,
    )

    users = models.ManyToManyField(
        User,
    )

    def __str__(self):
        return "Private discussion:{discussion}.".format(
                                discussion=self.id,
                                )

class Comment(models.Model):
    """An individual comment.

    Comments can be made on a seriesplan, storyplan, webfacet,
    audiofacet, videfacet, or between one or more people privately.
    """

    # id = django automatic id

    user_id = models.ForeignKey(
        User,
    )

    discussion_id = models.ForeignKey(
        Discussion,
    )

    text = models.TextField(
        help_text='The comment of the comment.'
    )

    date = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return "Comment:{comment} from discussion:{discussion}".format(
                                comment=self.id,
                                discussion=self.discussion_id.id,
                                )


class CommentReadStatus(models.Model):
    """ Tracking if a user involved in a discussion has read the most recent
    comment in order to surface unread comments first.
    """

    # id = django automatic id

    comment_id = models.ForeignKey(
        Comment,
    )

    user_id = models.ForeignKey(
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
                                comment=self.comment_id.id,
                                status=self.has_read,
                                )


#   Associations
#   ------------

# None
