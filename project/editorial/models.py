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
from django.shortcuts import get_object_or_404

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

    location = models.CharField(
        max_length='255',
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

    def get_user_content(self):
        """Return list of all content user is associated with as
        owner, editor, team or credit."""

        user_content = []
        series = Series.object.filter(Q(Q(owner=self) | Q(team=self)))
        stories = Story.objects.filter(Q(Q(owner=self) | Q(team=self)))
        webfacets = WebFacet.objects.filter(Q(Q(owner=self) | Q(editor=self) | Q(credit=self)))
        printfacets = PrintFacet.objects.filter(Q(Q(owner=self) | Q(editor=self) | Q(credit=self)))
        audiofacets = AudioFacet.objects.filter(Q(Q(owner=self) | Q(editor=self) | Q(credit=self)))
        videofacets = VideoFacet.objects.filter(Q(Q(owner=self) | Q(editor=self) | Q(credit=self)))
        user_content.append(series, stories, webfacets, printfacets, audiofacets, videofacets)

        return user_content

    def inbox_comments(self):
        """ Return list of comments from discussions the user is a participant in."""

        discussion_ids = {cd['discussion_id'] for cd in Comment.objects.filter(user_id=self.id).values('discussion_id')}
        inbox_comments = Comment.objects.filter(discussion_id__in=discussion_ids)

        return inbox_comments

    def recent_comments(self):
        """Return list of comments from discussions the user is a participant in
        since the user's last login."""

        discussion_ids = {cd['discussion_id'] for cd in Comment.objects.filter(user_id=self.id).values('discussion_id')}
        recent_comments = Comment.objects.filter(discussion_id__in=discussion_ids, date__gte=self.last_login)

        return recent_comments

    def private_messages_received(self):
        """ Return all private messages a user is a recipient of."""

        messages_received = PrivateMessage.objects.filter(recipient=self)
        return messages_received

    def private_messages_sent(self):
        """ Return all private messages a user is a recipient of."""

        messages_sent = PrivateMessage.objects.filter(user=self)
        return messages_sent

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

    location = models.CharField(
        max_length='255',
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

    discussion = models.ForeignKey(
        'Discussion',
        related_name='organization_discussion',
        help_text='Id of discussion for an organization.',
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = 'Organization'
        verbose_name_plural = "Organizations"
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_org_users(self):
        """ Return dictionary of all users in an organization."""

        organization_users = {}
        organization_users['organization'] = self
        organization_users['users'] = User.objects.filter(organization=self)

        return organization_users

    def get_org_networks(self):
        """ Return list of all the networks that an organization is owner of or member of."""

        # organization_networks = {}
        # organization_networks['organization'] = self
        # organization_networks['network_owner'] = Network.objects.filter(owner_organization=self)
        # organization_networks['network_member'] = []
        # network_orgs = NetworkOrganization.objects.filter(organization = self)
        # for item in network_orgs:
        #     network = item.network
        #     organization_networks['network_member'].append(network)

        organization_networks = []
        owned_networks = Network.objects.filter(owner_organization=self)
        organization_networks.extend(owned_networks)
        network_orgs = NetworkOrganization.objects.filter(organization = self)
        for item in network_orgs:
            network = item.network
            if network not in organization_networks:
                organization_networks.append(network)

        return organization_networks

    @property
    def description(self):
        return "{organization}, {description}".format(
                                                    organization=self.name,
                                                    description=self.org_description
                                                    )

    @property
    def type(self):
        return "Organization"


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

    discussion = models.ForeignKey(
        'Discussion',
        related_name='network_discussion',
        help_text='Id of discussion for a network.',
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = 'Network'
        verbose_name_plural = "Networks"
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_network_organizations(self):
        """ Return list of all organizations that are part of a network. """

        network_organizations = NetworkOrganization.objects.filter(network=self)
        print "NETWORK ORGANIZATIONS: ", network_organizations
        return network_organizations


    def get_network_shared_stories(self):
        """ Return list of stories shared with a network. """

        network_orgs = get_network_organizations(self)

        network_stories = []
        for network in network_orgs:
            shared_stories = Story.objects.filter(share_with = self.id)
            print "SHARED STORIES: ", shared_stories
            network_stories.extend(shared_stories)

        return network_stories

    @property
    def description(self):
        return "{network}, {description}".format(
                                                network=self.name,
                                                description=self.network_description
                                                )

    @property
    def type(self):
        return "Network"

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

    organization = models.ForeignKey(
        Organization,
        related_name='series_organization',
        help_text='The org'
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

    share_with_date = models.DateTimeField(
        help_text="Estimated date the series will be available",
        blank=True,
        null=True,
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

    @property
    def type(self):
        return "Series"



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

    organization = models.ForeignKey(
        Organization,
        help_text="Organization that owns this story."
    )

    original_story = models.BooleanField(
        default=True,
        help_text='Was this story originally created by a user from this organization?'
        #If story is not original, set to false and use StoryCopyDetail for additional info.
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

    share_with_date = models.DateTimeField(
        help_text="Estimated date the story will be available",
        blank=True,
        null=True,
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
        null=True,
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
        null=True,
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


    def copy_story(self):
        """ Create a copy of a story for a partner organization in a network.

        Copied stories keep name, story_description, embargo, embargo, datetime,
        creation_date, team. All other attributes are cleared or set to False.
        Organization is set to the copier's organization and the original_content
        flag is set to false. Triggering a copy also triggers the creation of a
        story copy detail record.
        """

        story_copy = get_object_or_404(Story, id=self.id)
        # Set the id = None to create the copy the story instance
        story_copy.id = None
        story_copy.save()
        # clear relationships if they exist
        if story_copy.series:
            story_copy.series.clear()
        if story_copy.share_with:
            story_copy.share_with.clear()
        if story_copy.collaborate_with:
            story_copy.collaborate_with.clear()
        # clear attributes for the copying organization
        story_copy.original_story = False
        story_copy.sensitive = False
        story_copy.share = False
        story_copy.ready_to_share = False
        story_copy.collaborate = False
        story_copy.archived = False
        story_copy.discussion = Discussion.objects.create_discussion("STO")
        story_copy.save()

        return story_copy


    @property
    def description(self):
        return "{story}, {description}".format(
                                                story=self.name,
                                                description=self.story_description
                                                )

    @property
    def type(self):
        return "Story"


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

    def copy_webfacet(self):
        """ Create a copy of a webfacet for a partner organization in a network."""

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

    @property
    def description(self):
        return "Webfacet: {webfacet} by {credit}".format(
                                webfacet=self.id,
                                credit=self.credit,
                                )

    @property
    def type(self):
        return "WebFacet"


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

    def copy_printfacet(self):
        """ Create a copy of a printfacet for a partner organization in a network."""

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


    @property
    def description(self):
        return "Printfacet: {printfacet} by {credit}".format(
                                printfacet=self.id,
                                credit=self.credit,
                                )

    @property
    def type(self):
        return "PrintFacet"


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

    length = models.IntegerField(
        help_text='Runtime of the audiofacet.',
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

    def copy_audiofacet(self):
        """ Create a copy of a audiofacet for a partner organization in a network."""

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

    @property
    def description(self):
        return "Audiofacet: {audiofacet} by {credit}".format(
                                audiofacet=self.id,
                                credit=self.credit,
                                )

    @property
    def type(self):
        return "AudioFacet"


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

    length = models.IntegerField(
        help_text='Runtime of the videofacet.',
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

    def copy_videofacet(self):
        """ Create a copy of a videofacet for a partner organization in a network."""

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

    @property
    def description(self):
        return "Videofacet: {videofacet} by {credit}".format(
                                videofacet=self.id,
                                credit=self.credit,
                                )

    @property
    def type(self):
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


class SeriesCopyDetailManager(models.Manager):
    """Custom manager to create copy records for series. """

    def create_story_copy_record(self, original_org, partner, original_series, partner_series):
        """Method for quick creation of a copy record."""
        story_copy_detail=self.create(original_org=original_org, partner=partner, original_series=original_series, partner_series=partner_series)
        return story_copy_detail


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
        return create_webfacet_copy_record


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
        return create_printfacet_copy_record


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
        return create_audiofacet_copy_record


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
        return create_videofacet_copy_record


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

    @property
    def type(self):
        return "{asset_type} Asset". format(asset_type=self.asset_type)


class Note(models.Model):
    """ Abstract base class for notes."""

    title = models.CharField(
        max_length=255,
    )

    text = models.TextField(
        help_text='Content of the note',
        blank=True,
    )

    creation_date = models.DateTimeField(
        auto_now_add=True,
        help_text='When the note was created.'
    )

    important = models.BooleanField(
        default=False,
        help_text='Mark as important for pinning to top of notes',
        blank=True,
    )

    keywords = ArrayField(
        models.CharField(max_length=100),
        default=list,
        help_text='List of keywords for note search.',
        blank=True,
    )

    class Meta:
        abstract = True


class NetworkNote(Note):
    """ General purpose notes for a network."""

    owner=models.ForeignKey(
        User,
        related_name='networknote_owner'
    )

    network=models.ForeignKey(
        Network,
        related_name='networknote_network'
    )

    @property
    def type(self):
        return "Network Note"


class OrganizationNote(Note):
    """ General purpose notes for an organization."""

    owner=models.ForeignKey(
        User,
        related_name='organizationnote_owner'
    )

    organization=models.ForeignKey(
        Organization,
        related_name="orgnote_org"
    )

    @property
    def type(self):
        return "Organization Note"


class UserNote(Note):
    """ General purpose notes from a user. """

    owner = models.ForeignKey(
        User,
        related_name='usernote_owner'
    )

    @property
    def type(self):
        return "User Note"


class SeriesNote(Note):
    """ A note attached to a series."""

    owner = models.ForeignKey(
        User,
        related_name='seriesnote_owner'
    )

    series = models.ForeignKey(
        Series,
        related_name="seriesnote",
    )

    def __str__(self):
        return "SeriesNote: {seriesnote} for Series: {series}".format(
                                seriesnote=self.id,
                                series=self.series.id,
                                )

    @property
    def type(self):
        return "Series Note"


class StoryNote(Note):
    """ Planning notes and conversation for a story. """

    owner = models.ForeignKey(
        User,
        related_name='storynote_owner'
    )

    story = models.ForeignKey(
        Story,
    )

    def __str__(self):
        return "StoryNote: {storynote} for Story: {story}".format(
                                storynote=self.id,
                                story=self.story.id,
                                )

    @property
    def type(self):
        return "Story Note"


class DiscussionManager(models.Manager):
    """ Custom manager for discussions."""

    def create_discussion(self, discussion_type):
        """ Method for quick creation of a discussion."""
        discussion = self.create(discussion_type=discussion_type)
        return discussion


class Discussion(models.Model):
    """ Class for  for related comments. """

    # Choices for Discussion type
    ORGANIZATION = 'ORG'
    NETWORK = 'NET'
    PRIVATE = 'PRI'
    SERIESPLAN = 'SER'
    STORYPLAN = 'STO'
    WEBFACET = 'WF'
    PRINTFACET = 'PF'
    AUDIOFACET = 'AF'
    VIDEOFACET = 'VF'

    DISCUSSION_TYPE_CHOICES = (
        (ORGANIZATION, 'Organization Conversation'),
        (NETWORK, 'Network Conversation'),
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


class PrivateMessageManager(models.Manager):
    """ Customer manager for private messaging."""

    def create_private_message(self, user, recipient, discussion, subject, text):
        """ Method for quick creation of a private discussion."""

        message = self.create(user=user, recipient=recipient, discussion=discussion, subject=subject, text=text)
        return message


class PrivateMessage(models.Model):
    """ A private message to a specific user.

    Private messages can be sent to a specific user and will only be
    visible to those users in their inbox.
    """

    user = models.ForeignKey(
        User,
        related_name='private_message_sender',
        help_text='The sender of the private message.',
    )

    recipient = models.ForeignKey(
        User,
        related_name='private_message_recipient',
        help_text='The recipient of the private message.'
    )

    discussion = models.ForeignKey(
        Discussion,
    )

    subject = models.TextField(
        help_text='The topic of the message.',
        blank=True,
    )

    text = models.TextField(
        help_text='The content of the message.'
    )

    date = models.DateTimeField(
        auto_now_add=True,
    )

    objects = PrivateMessageManager()

    @property
    def type(self):
        return "Private Message"


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
        ordering = ['-date']

    def __str__(self):
        return "Comment:{comment} from discussion:{discussion}".format(
                                comment=self.id,
                                discussion=self.discussion.id,
                                )

    @property
    def type(self):
        return "Comment"


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
