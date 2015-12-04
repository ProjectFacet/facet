""" Model for editorial application.

    Sections
    ---------
    People: User, Organization, Network
    -Associations: NetworkOrganizaton, UserSeries, UserStory

    Content: Series, Story, WebFacet, PrintFacet, AudioFacet, VideoFacet
    -Associations: WebFacetContributors, PrintFacetContributors, AudioFacetContributors, VideoFacetContributors
                StoryCopyDetails, SeriesCopyDetails, WebFacetCopyDetails, PrintFacetCopyDetails, AudioFacetCopyDetails, VideoFacetCopyDetails

    MetaMaterials: SeriesPlan, StoryPlan, Asset, Comment, CommentReadStatus, Discussion, PrivateDiscussion
    -Associations: WebFacetAsset, PrintFacetAsset, AudioFacetAsset, VideoFacetAsset
"""

from django.db import models
from django.contrib.postgres.fields import ArrayField
from simple_history.models import HistoricalRecords
from model_utils.models import TimeStampedModel
from datetime import timedelta
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from imagekit.processors import ResizeToFit
from imagekit.models import ProcessedImageField
# from django.core.exceptions import ValidationError
# from django.core.urlresolvers import reverse
# from django.core.validators import RegexValidator
# from django.utils import timezone


#----------------------------------------------------------------------#
#   People: 
#   - Main Tables: User, Organization, Network
#   - Associations: NetworkOrganizaton, UserSeries, UserStory
#----------------------------------------------------------------------#


class User(models.Model):
    """ Site User.

    A user can either be an admin or a general user. Most users
    can do most things. An admin user can be a site owner, add new
    users, create and manage networks and shift users from active
    to inactive. A general user creates and collaborates on content.
    """

    user_id = models.SlugField(
        max_length=15,
        primary_key=True,
        help_text='Unique code for a user.'
    )

    user_organization_id = models.ForeignKey('Organization')

    user_admin_privilege = models.BooleanField(
        default=False,
        help_text = 'Is a user able to manage an organization/network and make/remove users.'
    )

    user_fname = models.CharField(
        max_length=45,
        db_index=True,
    )

    user_lname = models.CharField(
        max_length=45,
        db_index=True,
    )

    user_credit_name = models.CharField(
        max_length=75,
        help_text='Full name of user as listed as a credit on content.'
    )

    username = models.CharField(
        max_length=30,
        unique=True,
        help_text='Username as needed for login purposes.'
    )

    user_title = models.CharField(
        max_length=100,
        unique=True,
        help_text='Professional title'
    )

    user_date_joined = models.DateTimeField(
        auto_now_add=True
    )

    user_last_login = models.DateTimeField(
        auto_now = True
    )

    user_is_active = models.BooleanField(
        default = True
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

    user_expertise = ArrayField(
        models.CharField(max_length=100),
        default=list,
        help_text='Array of user skills and beats to filter/search by.'
    )

    profile_photo = models.ImageField(
        upload_to="users",
        blank=True,
    )

    photo_display = ImageSpecField(
        source='photo',
        processors=[ResizeToFit(200, 200)],
        format='JPEG',
    )

    #Links to user's professional social media accounts
    user_facebook = models.CharField(
        max_length=150,
        blank=True,
        null=True,
    )

    user_twitter = models.CharField(
        max_length=150,
        blank=True,
        null=True,
    )

    user_linkedin = models.CharField(
        max_length=150,
        blank=True,
        null=True,
    )

    user_instagram = models.CharField(
        max_length=150,
        blank=True,
        null=True,
    )

    user_snapchat = models.CharField(
        max_length=150,
        blank=True,
        null=True,
    )

    user_vine = models.CharField(
        max_length=150,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = 'Team member'
        verbose_name_plural = "Team members"
        ordering = ['user_credit_name']

    def __str__(self):
        return self.user_credit_name

    @property
    def description(self):
        return "{user}, {title}".format(
                                        user=self.user_credit_name,
                                        title=self.user_title
                                        )


class Organization(models.Model):
    """ Media Organization.

    An organization is a media or publishing entity. Organization's are created
    and owned by one admin user. They can be managed by multiple admin users.
    Organizations have many users and serve as the owner of story content. Organizations
    can create and manage Networks. Ownership of an organization can be transferred
    from one admin user to another.
    """

    organization_id = models.SlugField(
        max_length=15,
        primary_key=True,
        help_text='Unique code for an organization.'
    )

    organization_name = models.CharField(
        max_length=75,
        db_index=True,
    )

    organization_owner = models.ForeignKey(
        User,
    )

    organization_description = models.TextField(
        help_text="Short profile of organization.",
        blank=True
    )

    organization_creation_date = models.DateTimeField(
        auto_now_add=True
    )

    organization_logo = models.ImageField(
        upload_to="organizations",
        blank=True
    )

    logo_display = ImageSpecField(
        source='photo',
        processors=[ResizeToFit(200, 200)],
        format='JPEG',
    )

    class Meta:
        verbose_name = 'Organization'
        verbose_name_plural = "Organizations"
        ordering = ['organization_name']

    def __str__(self):
        return self.organization_name

    @property
    def description(self):
        return "{organization}, {description}".format(
                                                    organization=self.organization_name,
                                                    description=self.organization_description
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

    network_id = models.SlugField(
        max_length=15,
        primary_key=True,
        help_text='Unique identifier for a network'
    )

    network_owner_organization = models.ForeignKey(
        Organization,
    )

    network_name = models.CharField(
        max_length=75,
        db_index=True,
        help_text="The name by which members identify the network."
    )

    network_creation_date = models.DateTimeField(
        auto_now_add=True
    )

    network_description = models.TextField(
        help_text="Short description of a network.",
        blank=True
    )

    network_logo = models.ImageField(
        upload_to="organizations",
        blank=True
    )

    logo_display = ImageSpecField(
        source='photo',
        processors=[ResizeToFit(200, 200)],
        format='JPEG',
    )

    organizations = models.ManyToManyField(
        Organization, through='NetworkOrganizaton'
    )

    class Meta:
        verbose_name = 'Network'
        verbose_name_plural = "Networks"
        ordering = ['network_name']

    def __str__(self):
        return self.network_name

    @property
    def description(self):
        return "{network}, {description}".format(
                                                network=self.network_name,
                                                description=self.network_description
                                                )

#   Associations
#   ------------

class NetworkOrganizaton(models.Model):
    """ The connection between Organizations and Networks. """

    network_organization_id = models.SlugField(
        max_length=15,
        primary_key=True,
        help_text='Unique identifier for a network/organization connection.'
    )

    network_id = models.ForeignKey(
        Network,
    )

    organization_id = models.ForeignKey(
        Organization,
    )

    def __str__(self):
        return "{network}, {organization}".format(
                                                network=self.network.network_name,
                                                organization=self.organization.organization_name
                                                )

# ----------------------------------
# Replaced with ManytoMany Field
# ----------------------------------
# class UserStory(models.Model):
#     """ The connection between a user and a story they contributed to. """

#     user_story_id = models.SlugField(
#         max_length=15,
#         primary_key=True,
#         help_text='Unique identifier for a user/story connection.'
#     )

#     user_id = models.ForeignKey(
#         User,
#     )

#     story_id = models.ForeignKey(
#         'Story',
#     )

#     def __str__(self):
#         return "{user}, {story}".format(
#                                         user=self.user.user_credit_name,
#                                         story=self.story.story_name
#                                         )

# ----------------------------------
# Replaced with ManytoMany Field
# ----------------------------------
# class UserSeries(models.Model):
#     """ The connection between a user and a series they contributed to. """

#     user_series_id = models.SlugField(
#         max_length=15,
#         primary_key=True,
#         help_text='Unique identifier for a user/series connection.'
#     )

#     user_id = models.ForeignKey(
#         User,
#     )

#     series_id = models.ForeignKey(
#         'Series',
#     )

#     def __str__(self):
#         return "{user}, {series}".format(
#                                         user=self.user.user_credit_name,
#                                         series=self.series.series_name
#                                         )

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

    series_id = models.SlugField(
        max_length=15,
        primary_key=True,
        help_text='Unique identifier for a series.'
    )

    series_name = models.CharField(
        max_length=75,
        help_text='The name identifying the series.'
    )

    series_description = models.TextField(
        blank=True,
        help_text='Short description of a series.',
    )

    series_owner = models.ForeignKey(
        User,
        help_text='The user that created the series.'
    )

    # connection to users participating in a series
    series_team = models.ManyToManyField(
        User
    )
    
    series_creation_date = models.DateTimeField(
        auto_now_add=True
    )

    share = models.BooleanField(
        default=False,
        help_text='The series is being shared with a network.'
    )

    collaborate = models.BooleanField(
        default=False,
        help_text='The series is being collaborated on with a network.'
    )

    share_with = models.ManyToManyField(
        Network,
        help_text='Network ids that a series is shared with.'
    )

    collaborate_with = models.ManyToManyField(
        Network,
        help_text='Network ids that a series is open to collaboration with.'
    )

    archived = models.BooleanField(
        default=False,
        help_text='Is the content no longer active and needed?'
    )

    class Meta:
        verbose_name = 'Series'
        verbose_name_plural = "Series"
        ordering = ['series_name']

    def __str__(self):
        return self.series_name

    @property
    def description(self):
        return "{series}, {description}".format(
                                                series=self.series_name,
                                                description=self.series_description
                                                )


class Story(models.Model):
    """ The unit of a story.

    A story is the one or more facets that make up a particular story.
    Sharing and collaboration is controlled at the story level.
    The story also controls the sensivity and embargo status of the content.
    """

    story_id = models.SlugField(
        max_length=15,
        primary_key=True,
        help_text='unique identifier for a story'
    )

    series_id = models.ForeignKey(
        Series,
    )

    story_owner = models.ForeignKey(
        User,
    )

    story_name = models.CharField(
        max_length=250,
        help_text='The name by which the story is identified'
    )

    story_description = models.TextField(
        help_text="Short description of a story.",
        blank=True
    )

    story_embargo = models.BooleanField(
        default=False,
        help_text='Is a story embargoed?'
        )

    story_embargo_datetime = models.DateTimeField(
        help_text='When is the story no longer under embargo.'
    )

    # For now a boolean for sensitive or not. May have levels of sensitivity later.
    story_sensitivity = models.BooleanField(
        default=False,
        help_text='Is a story sensitive, for limited viewing?'
        )

    story_creation_date = models.DateTimeField(
        auto_now_add=True,
        help_text='When was the story created.'
    )

    # connection to users participating in a story
    story_team = models.ManyToManyField(
        User,
    )

    share = models.BooleanField(
        default=False,
        help_text='The story is being shared with a network.'
    )

    collaborate = models.BooleanField(
        default=False,
        help_text='The story is being collaborated on with a network.'
    )

    share_with = models.ManyToManyField(
        Network,
        help_text='Network ids that a story is shared with.'
    )

    collaborate_with = models.ManyToManyField(
        Network,
        help_text='Network ids that a story is open to collaboration with.'
    )

    archived = models.BooleanField(
        default=False,
        help_text='Is the content no longer active and needed?'
    )

    class Meta:
        verbose_name = 'Story'
        verbose_name_plural = "Stories"
        ordering = ['story_name']

    def __str__(self):
        return self.story_name

    @property
    def description(self):
        return "{story}, {description}".format(
                                                story=self.story_name,
                                                description=self.story_description
                                                )


class WebFacet(models.Model):
    """ Regularly published web content.

    Ex: Daily news, articles, videos, photo galleries
    """

    webfacet_id = models.SlugField(
        max_length=25,
        primary_key=True,
        help_text='Unique identifier for webfacet'
    )

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
        help_text='Users that contributed to a facet. Used to associate multiple users to a facet.'
    )

    credit = models.ForeignKey(
        # There can be multiple users listed as the credit.
        # Best way relationship type?
        User,
        related_name='webfacetcredit',
        help_text='The full user name to be listed as the credit for the facet.'
    )

    code = models.CharField(
        max_length=75,
        help_text='Unique code as needed for ingest sytems. Use as needed'
    )

    title = models.TextField(
        help_text='Headline of the Webfacet'
    )

    excerpt = models.TextField(
        help_text='Excerpt from the Webfacet.'
    )

    description = models.TextField(
        help_text='Description of the WebFacet.'
    )

    content = models.TextField(
        help_text='Content of the webFacet.'
    )

    length = models.IntegerField(
        help_text='Wordcount of the WebFacet.'
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
        help_text='Due for edit.'
    )

    run_date = models.DateTimeField(
        help_text='Planned run date.'
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
        help_text='Information for organizations making a copy of the webfacet.'
    )

    assets = ManyToManyField(
        Asset
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
                                webfacet=self.webfacet_id,
                                credit=self.credit,
                                )


class PrintFacet(models.Model):
    """ The print version of a story.

    Ex: Daily news article, column, story.
    """

    printfacet_id = models.SlugField(
        max_length=25,
        primary_key=True,
        help_text='Unique identifier for printfacet'
    )

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
        help_text='Users that contributed to a facet. Used to associate multiple users to a facet.'
    )

    credit = models.ForeignKey(
        # There can be multiple users listed as the credit.
        # Best way relationship type?
        User,
        related_name='printfacetcredit',
        help_text='The full user name to be listed as the credit for the facet.'
    )

    code = models.CharField(
        max_length=75,
        help_text='Unique code as needed for ingest sytems. Use as needed'
    )

    title = models.TextField(
        help_text='Headline of the printfacet.'
    )

    excerpt = models.TextField(
        help_text='Excerpt from the printfacet.'
    )

    description = models.TextField(
        help_text='Description of the printfacet.'
    )

    content = models.TextField(
        help_text='Content of the printfacet.'
    )

    length = models.IntegerField(
        help_text='Wordcount of the printfacet.'
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
        help_text='Due for edit.'
    )

    run_date = models.DateTimeField(
        help_text='Planned run date.'
    )

    creation_date = models.DateTimeField(
        auto_now_add=True,
        help_text='Day printfacet was created.'
    )

    discussion_id = models.ForeignKey(
        'Discussion',
        help_text='Id of edit discussion for the printfacet.'
    )

    edit_history = HistoricalRecords()

    share_note = models.TextField(
        help_text='Information for organizations making a copy of the printfacet.'
    )

    assets = ManyToManyField(
        Asset
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
                                printfacet=self.printfacet_id,
                                credit=self.credit,
                                )


class AudioFacet(models.Model):
    """ Scheduled radio programming.

    Ex: A single segment on Morning Edition.
    """

    audiofacet_id = models.SlugField(
        max_length=25,
        primary_key=True,
        help_text='Unique identifier for audiofacet'
    )

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
        help_text='Users that contributed to a facet. Used to associate multiple users to a facet.'
    )

    credit = models.ForeignKey(
        # There can be multiple users listed as the credit.
        # Best way relationship type?
        User,
        related_name='audiofacetcredit',
        help_text='The full user name to be listed as the credit for the facet.'
    )

    code = models.CharField(
        max_length=75,
        help_text='Unique code as needed for ingest sytems. Use as needed'
    )

    title = models.TextField(
        help_text='Headline of the audiofacet.'
    )

    excerpt = models.TextField(
        help_text='Excerpt for the audiofacet.'
    )

    description = models.TextField(
        help_text='Description of the audiofacet.'
    )

    content = models.TextField(
        help_text='Content of the audiofacet.'
    )

    length = models.IntegerField(
        help_text='Wordcount of the audiofacet.'
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
        help_text='Due for edit.'
    )

    run_date = models.DateTimeField(
        help_text='Planned run date.'
    )

    creation_date = models.DateTimeField(
        auto_now_add=True,
        help_text='Day audiofacet was created.'
    )

    discussion_id = models.ForeignKey(
        'Discussion',
        help_text='Id of edit discussion for the audiofacet.'
    )

    edit_history = HistoricalRecords()

    share_note = models.TextField(
        help_text='Information for organizations making a copy of the audiofacet.'
    )

    assets = ManyToManyField(
        Asset
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
                                audiofacet=self.audiofacet_id,
                                credit=self.credit,
                                )


class VideoFacet(models.Model):
    """ Scheduled television programming.

    Ex: An episode of a television program.
    """

    videofacet_id = models.SlugField(
        max_length=25,
        primary_key=True,
        help_text='Unique identifier for videofacet'
    )

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
        help_text='Users that contributed to a facet. Used to associate multiple users to a facet.'
    )

    credit = models.ForeignKey(
        # There can be multiple users listed as the credit.
        # Best way relationship type?
        User,
        related_name='videofacetcredit',
        help_text='The full user name to be listed as the credit for the facet.'
    )

    code = models.CharField(
        max_length=75,
        help_text='Unique code as needed for ingest sytems. Use as needed'
    )

    title = models.TextField(
        help_text='Headline of the videofacet.'
    )

    excerpt = models.TextField(
        help_text='Excerpt from the videofacet.'
    )

    description = models.TextField(
        help_text='Description of the videofacet.'
    )

    content = models.TextField(
        help_text='Content of the videofacet.'
    )

    length = models.IntegerField(
        help_text='Wordcount of the videofacet.'
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
        help_text='Due for edit.'
    )

    run_date = models.DateTimeField(
        help_text='Planned run date.'
    )

    creation_date = models.DateTimeField(
        auto_now_add=True,
        help_text='Day videofacet was created.'
    )

    discussion_id = models.ForeignKey(
        'Discussion',
        help_text='ID of edit discussion for the videofacet.'
    )

    edit_history = HistoricalRecords()

    share_note = models.TextField(
        help_text='Information for organizations making a copy of the videofacet.'
    )

    assets = ManyToManyField(
        Asset
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
                                videofacet=self.videofacet_id,
                                credit=self.credit,
                                )


#   Associations
#   ------------


class WebFacetContributors(models.Model):
    """ Which users are participating in creating the WebFacet. """

    webfacet_contributor_id = models.SlugField(
        max_length=15,
        primary_key=True,
        help_text='Unique identifier for a webfacet/contributor connection.'
    )

    webfacet_id = models.ForeignKey(
        WebFacet,
    )

    user_id = models.ForeignKey(
        User,
    )

    def __str__(self):
        return "{webfacet}, {contributor}".format(
                                        webfacet=self.webfacet.webfacet_title,
                                        user=self.user.user_credit_name,
                                        )


class PrintFacetContributors(models.Model):
    """ Which users are participating in creating the PrintFacet. """

    printfacet_contributor_id = models.SlugField(
        max_length=15,
        primary_key=True,
        help_text='Unique identifier for a printfacet/contributor connection.'
    )

    printfacet_id = models.ForeignKey(
        PrintFacet,
    )

    user_id = models.ForeignKey(
        User,
    )

    def __str__(self):
        return "{printfacet}, {contributor}".format(
                                        printfacet=self.webfacet.webfacet_title,
                                        user=self.user.user_credit_name,
                                        )


class AudioFacetContributors(models.Model):
    """ Which users are participating in creating the AudioFacet. """

    audiofacet_contributor_id = models.SlugField(
        max_length=15,
        primary_key=True,
        help_text='Unique identifier for a audiofacet/contributor connection.'
    )

    audiofacet_id = models.ForeignKey(
        AudioFacet,
    )

    user_id = models.ForeignKey(
        User,
    )

    def __str__(self):
        return "{audiofacet}, {contributor}".format(
                                        audiofacet=self.webfacet.webfacet_title,
                                        user=self.user.user_credit_name,
                                        )


class VideoFacetContributors(models.Model):
    """ Which users are participating in creating the VideoFacet. """

    videofacet_contributor_id = models.SlugField(
        max_length=15,
        primary_key=True,
        help_text='Unique identifier for a videofacet/contributor connection.'
    )

    videofacet_id = models.ForeignKey(
        VideoFacet,
    )

    user_id = models.ForeignKey(
        User,
    )

    def __str__(self):
        return "{videofacet}, {contributor}".format(
                                        videofacet=self.webfacet.webfacet_title,
                                        user=self.user.user_credit_name,
                                        )


class SeriesCopyDetails(models.Model):
    """ The details of each copy of a series.

    Each time an organization elects to copy a shared facet, query to see if the
    series has already been copied over. If not copy the series and the story to the
    new organization.
    """
    copy_details_id = models.SlugField(
        max_length=15,
        primary_key=True,
        help_text='Unique identifier for a series copy detail object.'
    )

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
                                copyorg=self.organization_id.organization_name,
                                series=self.original_series_id,
                                )


class StoryCopyDetails(models.Model):
    """ The details of each copy of a story.

    Each time an organization elects to copy a shared facet, query to see if the
    story has already been copied over. If not, copy the story to the new organization.
    """
    copy_details_id = models.SlugField(
        max_length=15,
        primary_key=True,
        help_text='Unique identifier for a story copy detail object.'
    )

    organization_id = models.ForeignKey(
        Organization,
        help_text='Id of the organization that made the copy.'
    )

    original_story_id = models.ForeignKey(
        Series,
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
                                copyorg=self.organization_id.organization_name,
                                story=self.original_story_id,
                                )


class WebFacetCopyDetails(models.Model):
    """ The details of a each copy of a webfacet. """

    copy_details_id = models.SlugField(
        max_length=15,
        primary_key=True,
        help_text='Unique identifier for a story copy detail object.'
    )

    organization_id = models.ForeignKey(
        Organization,
        help_text='Id of the organization that made the copy.'
    )

    original_webfacet_id = models.ForeignKey(
        Series,
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
                                copyorg=self.organization_id.organization_name,
                                webfacet=self.original_printfacet_id,
                                )


class PrintFacetCopyDetails(models.Model):
    """ The details of a each copy of a printfacet. """
    copy_details_id = models.SlugField(
        max_length=15,
        primary_key=True,
        help_text='Unique identifier for a story copy detail object.'
    )

    organization_id = models.ForeignKey(
        Organization,
        help_text='Id of the organization that made the copy.'
    )

    original_printfacet_id = models.ForeignKey(
        Series,
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
                                copyorg=self.organization_id.organization_name,
                                printfacet=self.original_printfacet_id,
                                )


class AudioFacetCopyDetails(models.Model):
    """ The details of a each copy of a audiofacet. """
    copy_details_id = models.SlugField(
        max_length=15,
        primary_key=True,
        help_text='Unique identifier for a story copy detail object.'
    )

    organization_id = models.ForeignKey(
        Organization,
        help_text='Id of the organization that made the copy.'
    )

    original_audiofacet_id = models.ForeignKey(
        Series,
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
                                copyorg=self.organization_id.organization_name,
                                audiofacet=self.original_audiofacet_id,
                                )


class VideoFacetCopyDetails(models.Model):
    """ The details of a each copy of a videofacet. """
    copy_details_id = models.SlugField(
        max_length=15,
        primary_key=True,
        help_text='Unique identifier for a story copy detail object.'
    )

    organization_id = models.ForeignKey(
        Organization,
        help_text='Id of the organization that made the copy.'
    )

    original_videofacet_id = models.ForeignKey(
        Series,
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
                                copyorg=self.organization_id.organization_name,
                                videofacet=self.original_videofacet_id,
                                )

#----------------------------------------------------------------------#
#   MetaMaterials:
#   - Main Tables:  SeriesPlan, StoryPlan, Asset, Comment
#                   CommentReadStatus, Discussion, PrivateDiscussion
#   - Associations: WebFacetAsset, PrintFacetAsset, AudioFacetAsset,
#                   VideoFacetAsset
#----------------------------------------------------------------------#


class SeriesPlan(models.Model):
    """ Planning notes and conversation for a series. """

    series_planning_id = models.SlugField(
        max_length = 15,
        primary_key=True,
        help_text='Unique identifier for a series plan.'
    )

    series_id = models.ForeignKey(
        Series,
    )

    series_plan_note = models.TextField(
        help_text='Notes for planning a series. Can be any details needed to be tracked while a series is planned/reported.'
    )

    series_plan_note_owner = models.ForeignKey(
        User,
    )

    series_discussion_id = models.ForeignKey(
        'Discussion',
    )

    def __str__(self):
        return "SeriesPlan: {seriesplan} for Series: {series}".format(
                                seriesplan=self.series_planning_id,
                                series=self.series.series_id,
                                )


class StoryPlan(models.Model):
    """ Planning notes and conversation for a story. """

    story_planning_id = models.SlugField(
        max_length=15,
        primary_key=True,
        help_text='Unique identifier for a story plan.'
    )

    story_id = models.ForeignKey(
        Story,
    )

    story_plan_note = models.TextField(
        help_text='Notes for planning a story. Can be any details needed to be tracked while a story is planned/reported.'
    )

    story_plan_note_owner = models.ForeignKey(
        User,
    )

    story_discussion_id = models.ForeignKey(
        'Discussion',
    )

    def __str__(self):
        return "StoryPlan: {storyplan} for Story: {story}".format(
                                storyplan=self.story_planning_id,
                                story=self.story.story_id,
                                )


class Asset(models.Model):
    """ Assets for all the content contained in a series.

    Because series are an organizational container for all content, whether
    there is one or more stories, making the asset associated with the series,
    makes it easily available to all content associated with it, rather than the
    assets either be attached to a story or to a series.
    """

    asset_id = models.SlugField(
        max_length=15,
        primary_key=True,
        help_text='Unique identifier for an asset.'
    )

    series_id = models.ForeignKey(
        Series,
    )

    asset_owner = models.ForeignKey(
        User,
    )

    asset_description = models.TextField(
        max_length=300,
        help_text='What is the asset. (If a photo or graphic, it should be the caption.)'
    )

    asset_attribution = models.TextField(
        max_length=200,
        help_text='The appropriate information for crediting the asset.'
    )

    asset_s3_link = models.URLField(
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

    asset_creation_date = models.DateTimeField(
        auto_now_add=True,
        help_text='When the asset was created.'
    )

    def __str__(self):
        return "Asset: {asset_id} is a {asset_type}".format(
                                asset_id=self.asset_id,
                                asset_type=self.asset_type,
                                )


class Discussion(models.Model):
    """ Class for  for related comments. """

    discussion_id = models.SlugField(
        max_length=15,
        primary_key=True,
        help_text='Unique identifier for a discussion.'
    )

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
                                discussion=self.discussion_id,
                                discussion_type=self.discussion_type
                                )


class PrivateDiscussion(models.Model):
    """ Signifier of private conversations.

    Private conversations can occur between two or more individuals and only exist in their
    own inboxes and are not attached to any content types.
    """

    private_discussion_id = models.SlugField(
        max_length = 15,
        primary_key=True,
        help_text='Unique identifier of a private discussion'
    )

    discussion_id = models.ForeignKey(
        Discussion,
    )

    users = ManyToManyField(
        User,
    )

    def __str__(self):
        return "Private discussion:{discussion}.".format(
                                discussion=self.private_discussion_id,
                                )

class Comment(models.Model):
    """An individual comment.

    Comments can be made on a seriesplan, storyplan, webfacet,
    audiofacet, videfacet, or between one or more people privately.
    """

    comment_id = models.SlugField(
        max_length=25,
        primary_key=True,
        help_text='Unique identifier for a comment.'
    )

    user_id = models.ForeignKey(
        User,
    )

    discussion_id = models.ForeignKey(
        Discussion,
    )

    text = models.TextField(
        help_text='The comment of the comment.'
    )

    comment_date = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return "Comment:{comment} from discussion:{discussion}".format(
                                comment=self.comment_id,
                                discussion=self.discussion.discussion_id,
                                )


class CommentReadStatus(models.Model):
    """ Tracking if a user involved in a discussion has read the most recent
    comment in order to surface unread comments first.
    """

    read_status_id = models.SlugField(
        max_length=25,
        primary_key=True,
        help_text='Unique identifier for a comment read status.'
    )

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
                                comment=self.comment.comment_id,
                                status=self.has_read,
                                )


#   Associations
#   ------------


# class WebFacetAsset(models.Model):
#     """ An asset connected to a specific webfacet. """

#     webfacet_asset_id = models.SlugField(
#         max_length=15,
#         primary_key=True,
#         help_text='Unique identifier for a webfacet/asset connection.'
#         )

#     webfacet_id = models.ForeignKey(
#         WebFacet,
#         )

#     asset_id = models.ForeignKey(
#         Asset,
#         )

#     def __str__(self):
#         return "{webfacet}: {asset}".format(
#                                         webfacet=self.webfacet.webfacet_title,
#                                         asset=self.asset.asset_description,
#                                         )


# class PrintFacetAsset(models.Model):
#     """ An asset connected to a specific printfacet. """

#     printfacet_asset_id = models.SlugField(
#         max_length=15,
#         primary_key=True,
#         help_text='Unique identifier for a printfacet/asset connection.'
#         )

#     printfacet_id = models.ForeignKey(
#         PrintFacet,
#         )

#     asset_id = models.ForeignKey(
#         Asset,
#         )

#     def __str__(self):
#         return "{printfacet}: {asset}".format(
#                                         printfacet=self.printfacet.printfacet_title,
#                                         asset=self.asset.asset_description,
#                                         )


# class AudioFacetAsset(models.Model):
#     """ An asset connected to a specific audiofacet. """

#     audiofacet_asset_id = models.SlugField(
#         max_length=15,
#         primary_key=True,
#         help_text='Unique identifier for a audiofacet/asset connection.'
#         )

#     audiofacet_id = models.ForeignKey(
#         AudioFacet,
#         )

#     asset_id = models.ForeignKey(
#         Asset,
#         )

#     def __str__(self):
#         return "{audiofacet}: {asset}".format(
#                                         audiofacet=self.audiofacet.audiofacet_title,
#                                         asset=self.asset.asset_description,
#                                         )


# class VideoFacetAsset(models.Model):
#     """ An asset connected to a specific videofacet. """

#     videofacet_asset_id = models.SlugField(
#         max_length=15,
#         primary_key=True,
#         help_text='Unique identifier for a videofacet/asset connection.'
#         )

#     videofacet_id = models.ForeignKey(
#         VideoFacet,
#         )

#     asset_id = models.ForeignKey(
#         Asset,
#         )

#     def __str__(self):
#         return "{videofacet}: {asset}".format(
#                                         videofacet=self.videofacet.videofacet_title,
#                                         asset=self.asset.asset_description,
#                                         )
