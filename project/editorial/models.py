""" Model for editorial application.

    Tables
    ---------
    People:
    - User, Organization, Network

    Content:
    - Projects, Series, Story, WebFacet, PrintFacet, AudioFacet, VideoFacet

    Contributor Associations:
    - WebFacetContributors, PrintFacetContributors, AudioFacetContributors,
      VideoFacetContributors,

    Copy Details:
    - StoryCopyDetails, SeriesCopyDetails, WebFacetCopyDetails,
      PrintFacetCopyDetails, AudioFacetCopyDetails, VideoFacetCopyDetails

    Assets:
    - ImageAsset, DocumentAsset, AudioAsset, VideoAsset

    Notes:
    - Note, NetworkNote, OrganizationNote, UserNote, SeriesNote, StoryNote

    Discussion:
    - Discussion, PrivateDiscussion, PrivateMessage, Comment, CommentReadStatus


"""

from django.db import models
from django.db.models import Q
from django.contrib.postgres.fields import ArrayField
from simple_history.models import HistoricalRecords
from model_utils.models import TimeStampedModel
from datetime import datetime, timedelta, time
from imagekit.models import ProcessedImageField, ImageSpecField
from pilkit.processors import ResizeToFit, SmartResize
from django.contrib.auth.models import AbstractUser
from django.utils.encoding import python_2_unicode_compatible
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.shortcuts import get_object_or_404
from itertools import chain
from embed_video.fields import EmbedVideoField
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType

#-----------------------------------------------------------------------#
#   People:
#   User, Organization, Network
#-----------------------------------------------------------------------#

@python_2_unicode_compatible
class User(AbstractUser):
    """ Site User.

    A user can either be an admin or a general user. Most users
    can do most things. An admin user can be a site owner, add new
    users, create and manage networks and shift users from active
    to inactive. A general user creates and collaborates on content.
    """
    # FIXME This structure for a user needs revision in order to
    # account for a user being on a team or being an independent (contractor)
    # See github issue #60 for more detail

    # Made optional for users not pushing content to an org (freelancers)
    organization = models.ForeignKey(
        'Organization',
        blank=True,
        null=True,
    )

    ADMIN = 'Admin'
    EDITOR = 'Editor'
    STAFF = 'Staff'
    USER_TYPE_CHOICES = (
        (ADMIN, 'Admin'),
        (EDITOR, 'Editor'),
        (STAFF, 'Staff'),
    )

    user_type = models.CharField(
        max_length=25,
        choices=USER_TYPE_CHOICES,
        help_text='Type of user.'
    )

    credit_name = models.CharField(
        max_length=75,
        help_text='Full name of user as listed as a credit on content.',
        blank=True,
    )

    title = models.CharField(
        max_length=100,
        help_text='Professional title.',
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
        models.CharField(max_length=255),
        default=list,
        help_text='Array of user skills and beats to filter/search by.',
        blank=True,
    )

    notes = models.ManyToManyField(
        'UserNote',
        related_name='user_note',
        blank=True,
    )

    photo = models.ImageField(
        upload_to='users',
        blank=True,
    )

    display_photo = ImageSpecField(
        source='photo',
        processors=[SmartResize(500, 500)],
        format='JPEG',
    )

    website = models.URLField(
        max_length=250,
        blank=True,
    )

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = "Users"
        ordering = ['credit_name']

    def __str__(self):
        return self.credit_name

    def get_absolute_url(self):
        return reverse('user_detail', kwargs={'pk': self.id})

    def get_user_content(self):
        """Return list of all content user is associated with as
        owner, editor or credit.

        Results are used to display relevant content for a user on
        their dashboard and user profile.
        """

        user_content = []
        series = Series.objects.filter(Q(Q(owner=self) | Q(team=self)))
        stories = Story.objects.filter(Q(Q(owner=self) | Q(team=self)))
        webfacets = WebFacet.objects.filter(Q(Q(owner=self) | Q(editor=self) | Q(credit=self)))
        printfacets = PrintFacet.objects.filter(Q(Q(owner=self) | Q(editor=self) | Q(credit=self)))
        audiofacets = AudioFacet.objects.filter(Q(Q(owner=self) | Q(editor=self) | Q(credit=self)))
        videofacets = VideoFacet.objects.filter(Q(Q(owner=self) | Q(editor=self) | Q(credit=self)))
        user_content.extend(series)
        user_content.extend(stories)
        user_content.extend(webfacets)
        user_content.extend(printfacets)
        user_content.extend(audiofacets)
        user_content.extend(videofacets)
        return user_content


    # This is repetitive of get_user_content.
    # FIXME (for HB) revise get_user_content to include projects and replace get_user_stories in views
    def get_user_stories(self):
        """Return list of stories that a user is associated with."""

        user_stories = Story.objects.filter(Q(Q(owner=self) | Q(team=self)))
        return user_stories

    # TODO complete get_user_assets
    # def get_user_assets(self):
    #     """Return assets that a user is associated with."""
    #     pass

    def inbox_comments(self):
        """ Return list of comments from discussions the user is a participant in.

        Collects all relevant comments for a specific user to show in their
        dashboard and inbox.
        """

        discussion_ids = Comment.objects.filter(user_id=self.id).values('discussion_id')
        user_comments = Comment.objects.filter(user_id=self.id)
        all_comments = Comment.objects.filter(discussion_id__in=discussion_ids)
        inbox_comments = all_comments.exclude(id__in=user_comments)
        return inbox_comments

    def recent_comments(self):
        """Return list of comments from discussions the user is a participant in
        since the user's last login.

        For display on primary dashboard.
        """

        discussion_ids = Comment.objects.filter(user_id=self.id).values('discussion_id')
        user_comments = Comment.objects.filter(user_id=self.id)
        all_comments = Comment.objects.filter(discussion_id__in=discussion_ids, date__gte=self.last_login)
        recent_comments = all_comments.exclude(id__in=user_comments)
        return recent_comments

    # formerly get_user_contact_list
    def get_user_contact_list_vocab(self):
        """ Return queryset containing all users a specific user can contact.
        This includes any user that's a member of an organization in network.

        This vocab list populates the to selection for messaging.
        """

        organization = self.organization
        org_collaborators = Organization.get_org_collaborators_vocab(organization)
        contact_list = User.objects.filter(Q(Q(organization=org_collaborators) | Q(organization=organization)))
        return contact_list

    def private_messages_received(self):
        """ Return all private messages a user is a recipient of.

        Displayed in user inbox under 'inbox'.
        """

        messages_received = PrivateMessage.objects.filter(recipient=self)
        return messages_received

    def private_messages_sent(self):
        """ Return all private messages a user has sent.

        Displayed in user inbox under 'sent'.
        """

        messages_sent = PrivateMessage.objects.filter(user=self)
        return messages_sent

    def get_user_searchable_content(self):
        """ Return queryset of user specific content that is searchable.

        A user can return their own notes in search results.
        """

        usernotes = UserNote.objects.filter(Q(owner=self))

        return usernotes

    @property
    def description(self):
        org = self.organization.name if self.organization else "(No org)"

        return "{user}, {title}, {org}".format(
                                        user=self.credit_name,
                                        title=self.title,
                                        org=org,
                                        )

    @property
    def search_title(self):
        return self.credit_name

    @property
    def type(self):
        return "User"

#-----------------------------------------------------------------------#

@python_2_unicode_compatible
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

    logo = models.ImageField(
        upload_to='organizations',
        blank=True,
    )

    display_logo = ImageSpecField(
        source='logo',
        processors=[SmartResize(500, 500)],
        format='JPEG',
    )

    location = models.CharField(
        max_length='255',
        blank=True,
    )

    creation_date = models.DateTimeField(
        auto_now_add=True
    )

    facebook = models.URLField(
        max_length=250,
        blank=True,
    )

    twitter = models.URLField(
        max_length=250,
        blank=True,
    )

    website = models.URLField(
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

    # Events
    # events = GenericRelation(Event)

    class Meta:
        verbose_name = 'Organization'
        verbose_name_plural = "Organizations"
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('org_detail', kwargs={'pk': self.id})

    def get_org_users(self):
        """ Return queryset of all users in an organization.

        Used for organization dashboards, team views and context processors.
        """

        organization_users = User.objects.filter(organization=self)
        return organization_users

    def get_org_networks(self):
        """ Return list of all the networks that an organization is connected to as
        owner or member of.

        Used for dashboard, network dashboards and network content.
        """

        all_organization_networks = Network.objects.filter(Q(Q(owner_organization=self) | Q(organizations=self)))
        # not necessary but leaving in for now, check to make sure unique list of networks
        organization_networks = all_organization_networks.distinct()
        return organization_networks

    # def get_org_network_content(self):
    #     """Return queryset of content shared with any network an organization is a member of excluding their own content."""
    #
    #     networks = Organization.get_org_networks(self)
    #     content = Network.get_network_shared_stories(network__in=networks)
    #     print "content: ", content
    #     return content

    # formerly get_org_collaborators
    def get_org_collaborators_vocab(self):
        """ Return list of all organizations that are members of the same networks as self.

        Used to for selecting organizations to collaborate with and for displaying partners
        in team dashboard. Also used to create get_user_contact_list_vocab.
        """

        # get list of networks that an org is a member of
        networks = Organization.get_org_networks(self)
        # get list of organizations that are members of any of those networks
        all_organizations = Organization.objects.filter(Q(network_organization=networks))
        # remove user's organization from queryset
        organizations = all_organizations.exclude(id=self.id)
        # get distinct list of organizations
        unique_collaborators = organizations.distinct()
        return unique_collaborators

    def get_org_image_library(self):
        """ Return list of all images associated with an organization.

        Used to display images in media gallery.
        """

        images = ImageAsset.objects.filter(organization=self)
        return images

    def get_org_document_library(self):
        """ Return list of all documents associated with an organization.

        Used to display documents in media gallery.
        """

        documents = DocumentAsset.objects.filter(organization=self)
        return documents

    def get_org_audio_library(self):
        """ Return list of all audio files associated with an organization.

        Used to display audio in media gallery.
        """

        audio = AudioAsset.objects.filter(organization=self)
        return audio

    def get_org_video_library(self):
        """ Return list of all video files associated with an organization.

        Used to display videos in media gallery.
        """

        videos = VideoAsset.objects.filter(organization=self)
        return videos

    def get_org_user_comments(self):
        """Retrieve all the comments associated with users of an organization.

        Effectively 'all' comments for an organization. Used in user inbox
        to display streams of all comments.
        """

        users = Organization.get_org_users(self)
        org_user_comments = Comment.objects.filter(Q(user__in=users))
        return org_user_comments

    def get_org_comments(self):
        """Retrieve all organization comments.

        Used to display all organization comments in dashboard and inbox.
        """

        organization_comments = Comment.objects.filter(discussion__discussion_type='ORG', user__organization=self)
        return organization_comments

    def get_network_comments(self):
        """Retrieve all comments for networks an organization is a member of.

        Used to display all network comments in dashboard and inbox.
        """

        networks = Organization.get_org_networks(self)
        network_discussions = [network.discussion for network in networks]
        network_comments = Comment.objects.filter(discussion__in=network_discussions)
        return network_comments

    def get_story_comments(self):
        """Retrieve all comments for stories belonging to an organization.

        Used to display all story comments in dashboard and inbox.
        """

        org_stories = Story.objects.filter(organization=self)
        story_discussions = [story.discussion for story in org_stories]
        story_comments = Comment.objects.filter(discussion__in=story_discussions)
        return story_comments

    def get_series_comments(self):
        """Retrieve all comments for series belonging to an organization.

        Used to display all series comments in dashboard and inbox.
        """

        org_series = Series.objects.filter(organization=self)
        series_discussions = [series.discussion for series in org_series]
        series_comments = Comment.objects.filter(discussion__in=series_discussions)
        return series_comments

    def get_facet_comments(self):
        """Retrieve all comments for facets belonging to stories of an organization.

        Used to display all facet comments in dashboard and inbox.
        """

        # WJB XXX: this seems inefficient, we should reduce to discussion fields on orig
        # querysets
        # FIXME to be revised after facet refactoring

        org_facets = []
        webfacets = WebFacet.objects.filter(Q(organization=self))
        printfacets = PrintFacet.objects.filter(Q(organization=self))
        audiofacets = AudioFacet.objects.filter(Q(organization=self))
        videofacets = VideoFacet.objects.filter(Q(organization=self))
        org_facets.extend(webfacets)
        org_facets.extend(printfacets)
        org_facets.extend(audiofacets)
        org_facets.extend(videofacets)
        facet_discussions = [facet.discussion for facet in org_facets]
        facet_comments = Comment.objects.filter(discussion__in=facet_discussions)
        return facet_comments

    def get_org_collaborative_content(self):
        """ Return list of all content that an org is a collaborator on.

        All of the collaborative content an organization is participating in
        is displaying in a collaborative content dashboard.
        """

        org_collaborative_content = []
        external_stories = Story.objects.filter(Q(collaborate_with=self))
        internal_stories = Story.objects.filter(organization=self).filter(collaborate=True)
        org_collaborative_content.extend(external_stories)
        org_collaborative_content.extend(internal_stories)

        return org_collaborative_content

    def get_org_stories_running_today(self):
        """Return list of content scheduled to run today.

        Used to display content scheduled to run on any given day
        on the primary dashboard.
        """

        # establish timeliness of content
        today = timezone.now().date()
        tomorrow = today + timedelta(1)
        today_start = datetime.combine(today, time())
        today_end = datetime.combine(tomorrow, time())

        # facets where run_date=today
        # FIXME to be simplified after facet refactoring
        running_today = []
        webfacet_run_today = WebFacet.objects.filter(run_date__range=(today_start, today_end), organization=self)
        printfacet_run_today = PrintFacet.objects.filter(run_date__range=(today_start, today_end), organization=self)
        audiofacet_run_today = AudioFacet.objects.filter(run_date__range=(today_start, today_end), organization=self)
        videofacet_run_today = VideoFacet.objects.filter(run_date__range=(today_start, today_end), organization=self)
        running_today.extend(webfacet_run_today)
        running_today.extend(printfacet_run_today)
        running_today.extend(audiofacet_run_today)
        running_today.extend(videofacet_run_today)

        return running_today

    def get_org_stories_due_for_edit_today(self):
        """Return list of content scheduled for edit today.

        Used to display content scheduled for edit on any given day
        on the primary dashboard.
        """

        # establish timeliness of content
        today = timezone.now().date()
        tomorrow = today + timedelta(1)
        today_start = datetime.combine(today, time())
        today_end = datetime.combine(tomorrow, time())

        edit_today = []
        webfacet_edit_today = WebFacet.objects.filter(due_edit__range=(today_start, today_end), organization=self)
        printfacet_edit_today = PrintFacet.objects.filter(due_edit__range=(today_start, today_end), organization=self)
        audiofacet_edit_today = AudioFacet.objects.filter(due_edit__range=(today_start, today_end), organization=self)
        videofacet_edit_today = VideoFacet.objects.filter(due_edit__range=(today_start, today_end), organization=self)
        edit_today.extend(webfacet_edit_today)
        edit_today.extend(printfacet_edit_today)
        edit_today.extend(audiofacet_edit_today)
        edit_today.extend(videofacet_edit_today)

        return edit_today

    def get_org_searchable_content(self):
        """ Return queryset of all objects that can be searched by a user."""

        #additional required info
        networks = Organization.get_org_networks(self)

        searchable_objects = []

        series = Series.objects.filter(Q(Q(organization=self) | Q(collaborate_with=self)))
        stories = Story.objects.filter(Q(Q(organization=self) | Q(collaborate_with=self)))
        webfacets = WebFacet.objects.filter(Q(organization=self))
        printfacets = PrintFacet.objects.filter(Q(organization=self))
        audiofacets = AudioFacet.objects.filter(Q(organization=self))
        videofacets = VideoFacet.objects.filter(Q(organization=self))
        imageassets = ImageAsset.objects.filter(Q(organization=self))
        networknote = NetworkNote.objects.filter(Q(network__in=networks))
        orgnote = OrganizationNote.objects.filter(Q(organization=self))
        seriesnote = SeriesNote.objects.filter(Q(organization=self))
        storynote = StoryNote.objects.filter(Q(organization=self))
        searchable_objects.append(series)
        searchable_objects.append(stories)
        searchable_objects.append(webfacets)
        searchable_objects.append(printfacets)
        searchable_objects.append(audiofacets)
        searchable_objects.append(videofacets)
        searchable_objects.append(imageassets)
        searchable_objects.append(networknote)
        searchable_objects.append(orgnote)
        searchable_objects.append(seriesnote)
        searchable_objects.append(storynote)

        return searchable_objects

    @property
    def description(self):
        return "{description}".format(description=self.org_description)

    @property
    def search_title(self):
        return self.name

    @property
    def type(self):
        return "Organization"

#-----------------------------------------------------------------------#

@python_2_unicode_compatible
class Network(models.Model):
    """ A group of organizations.

    A network is a collection of two or more organizations seeking to create a sharing
    or collaborating relationship.

    Sharing means the source organization has made the content available to other
    members of the network.

    An organization can opt to collaborate with one of more members of a Network.
    Collaboration means that a user from a collaborating organization can participate
    in the editorial process on the host organization's content. They can edit, upload
    assets and participate in any relevant discussions.
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
        upload_to='networks',
        blank=True,
    )

    display_logo = ImageSpecField(
        source='logo',
        processors=[SmartResize(500, 500)],
        format='JPEG',
    )

    organizations = models.ManyToManyField(
        Organization,
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

    def get_absolute_url(self):
        return reverse('network_detail', kwargs={'pk': self.id})

    def get_network_shared_stories(self):
        """ Return list of stories shared with a network.

        This is used to populate the network content dashboard.
        """

        network_stories = Story.objects.filter(share_with=self.id)
        return network_stories

    @property
    def description(self):
        return "{description}".format(description=self.network_description)

    @property
    def search_title(self):
        return self.name

    @property
    def type(self):
        return "Network"


#--------------------------------------------------------------------------#
#   Platforms and PlatformAccounts
#   Social accounts connected to Users, Organizations, Projects and Series.
#   Ex. Users can have social media accounts, Organizations will often
#   have multiple accounts on any single platform, a special project or series
#   may have a unique social presence.
#--------------------------------------------------------------------------#

class Platform(models.Model):
    """A platform.

    Lookup table with details for each major platform. Instances populate
    options in PlatformAccount.
    Ex. Facebook, Twitter, YouTube, Vimeo, Snapchat, LinkedIn, Github, Reddit
    Instagram, Pinterest, Flickr, Behance, Tumblr
    """

    name = models.CharField(
       max_length=250,
       help_text='Name of the platform.'
    )

    # code for font awesome icon for the platform
    # ex. 'fa-facebook' is the Font Awesome icon for Facebook
    icon_code = models.CharField(
        max_length=50,
        blank=True,
        help_text='text for font-awesome icon for the platform'
    )

    def __str__(self):
        return self.name


class PlatformAccount(models.Model):
    """ A Platform Account.

    Platform accounts are the types and urls of different social media
    and platform accounts. Platform accounts can be connected to a user,
    organization, project or series. The attributes should always be the same
    regardless of model it's associated with.
    """

    name = models.CharField(
       max_length=250,
       db_index=True,
       help_text='Short name to identify the social account.'
    )

    platform = models.ForeignKey(
       Platform
    )

    url = models.URLField(
        max_length=250,
        blank=True,
    )

    description = models.TextField(
        blank=True,
        help_text='Short description of the purpose of the account.',
    )

    # if a social account is associated with an Organization, Project or Series.
    # UI not available to do this on platform accounts associated with a User.
    team = models.ManyToManyField(
        User,
        related_name='platform_team_member',
        help_text='User that contributes to this account.',
        blank=True,
    )

    # a platform account can be connected to a User, Organization or Project
    # using this method to connect platform accounts to another model in order
    # to easily see which models this is connected to without have to search
    # other models to see if there's a GenericForeignKey.
    # Can change later if compelling reason.

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
    )

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        blank=True,
    )

    project = models.ForeignKey(
        'Project',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    @property
    def description(self):
        return self.description

    @property
    def type(self):
        return "Platform Account"

#-----------------------------------------------------------------------#
#   Content:
#   Project, Series, Story, WebFacet, PrintFacet, AudioFacet, VideoFacet
#   (A Facet is always part of a story, even if there is only one facet.)
#-----------------------------------------------------------------------#

#-----------------------------------------------------------------------#
#  PROJECT
#-----------------------------------------------------------------------#

@python_2_unicode_compatible
class Project(models.Model):
    """A project.

    Projects are a large-scale organizational component made up of multiple series and/or
    stories. The primary use is as an organization mechanism for large scale complex
    collaborative projects. Projects can have series, stories, assets, notes, discussions,
    governing documents, events, calendars and meta information.
    """

    name = models.CharField(
        max_length=75,
        help_text='The name identifying the project.'
    )

    project_description = models.TextField(
        blank=True,
        help_text='Short description of a project.',
    )

    project_logo = models.ImageField(
        upload_to='projects',
        blank=True,
    )

    display_logo = ImageSpecField(
        source='project_logo',
        processors=[SmartResize(500, 500)],
        format='JPEG',
    )

    owner = models.ForeignKey(
        User,
        related_name='project_owner',
        help_text='The user that created the project.'
    )

    organization = models.ForeignKey(
        Organization,
        related_name='project_organization',
        help_text='The org'
    )

    team = models.ManyToManyField(
        User,
        related_name='project_team_member',
        help_text='User contributing to the project.',
        blank=True,
    )

    creation_date = models.DateTimeField(
        auto_now_add=True,
    )

    sensitive = models.BooleanField(
        default=False,
        help_text='Is a project sensitive, for limited viewing?'
    )

    share = models.BooleanField(
        default=False,
        help_text='The project is being shared with a network.'
    )

    share_with = models.ManyToManyField(
        Network,
        related_name='project_shared_with_network',
        help_text='Network ids that a project is shared with.',
        blank=True,
    )

    share_with_date = models.DateTimeField(
        help_text="Estimated date the project will be available",
        blank=True,
        null=True,
    )

    collaborate = models.BooleanField(
        default=False,
        help_text='The project is being collaborated on with a network.'
    )

    collaborate_with = models.ManyToManyField(
        Organization,
        related_name='project_collaborated_with_organization',
        help_text='Organization ids that a project is open to collaboration with.',
        blank=True,
    )

    archived = models.BooleanField(
        default=False,
        help_text='Is the content no longer active and needed?'
    )

    discussion = models.ForeignKey(
        'Discussion',
        help_text='Id of planning discussion for a project.',
        blank=True,
        null=True,
    )

    # project site if different than organization
    website = models.URLField(
        max_length=250,
        blank=True,
    )

    #Assets
    governing_document_assets = models.ManyToManyField(
        'GoverningDocumentAsset',
        blank=True,
    )

    project_document_assets = models.ManyToManyField(
        'ProjectDocumentAsset',
        blank=True,
    )

    # Tasks
    # tasks = GenericRelation(Task)

    # Events
    # events = GenericRelation(Event)

    class Meta:
        verbose_name = 'Project'
        verbose_name_plural = "Projects"
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('project_detail', kwargs={'pk': self.id})

    def get_project_team(self):
        """Return queryset with org users and users from collaboration orgs for a project."""

        collaborators = self.collaborate_with.all()
        project_team = User.objects.filter(Q(Q(organization=self.organization) | Q(organization__in=collaborators)))
        return project_team

    @property
    def description(self):
        return "{description}".format(description=self.project_description)

    @property
    def search_title(self):
        return self.name

    @property
    def type(self):
        return "Project"

#-----------------------------------------------------------------------#
#  SERIES
#-----------------------------------------------------------------------#


@python_2_unicode_compatible
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

    sensitive = models.BooleanField(
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
        Organization,
        related_name='series_collaborated_with_organization',
        help_text='Organization ids that a series is open to collaboration with.',
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

    #Tasks
    # tasks = GenericRelation(Task)

    # Events
    # events = GenericRelation(Event)

    class Meta:
        verbose_name = 'Series'
        verbose_name_plural = "Series"
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('series_detail', kwargs={'pk': self.id})

    def get_series_team(self):
        """Return queryset with org users and users from collaboration orgs for a series."""

        collaborators = self.collaborate_with.all()
        series_team = User.objects.filter(Q(Q(organization=self.organization) | Q(organization__in=collaborators)))
        return series_team

    @property
    def description(self):
        return "{description}".format(description=self.series_description)

    @property
    def search_title(self):
        return self.name

    @property
    def type(self):
        return "Series"

#-----------------------------------------------------------------------#
#  STORY
#-----------------------------------------------------------------------#

@python_2_unicode_compatible
class Story(models.Model):
    """The unit of a story.

    A story is the one or more facets that make up a particular story.
    Sharing and collaboration is controlled at the story level.
    The story also controls the sensitivity and embargo status of the content.
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
        help_text='The name by which the story is identified.'
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
        # null=True,
    )

    collaborate = models.BooleanField(
        default=False,
        help_text='The story is being collaborated on with a network.'
    )

    collaborate_with = models.ManyToManyField(
        Organization,
        related_name='story_collaborated_with_organization',
        help_text='Organization ids that a series is open to collaboration with.',
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

    #Tasks
    # tasks = GenericRelation(Task)

    # Events
    # events = GenericRelation(Event)

    class Meta:
        verbose_name = 'Story'
        verbose_name_plural = "Stories"
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('story_detail', kwargs={'pk': self.id})

    def copy_story(self):
        """ Create a copy of a story for a partner organization in a network.

        Copied stories keep name, story_description, embargo, embargo, datetime,
        creation_date, team. All other attributes are cleared or set to False.
        Organization is set to the copier's organization and the original_content
        flag is set to false. Triggering a copy also triggers the creation of a
        story copy detail record.
        """

        # FIXME Copied stories need to maintain attribution of team

        story_copy = get_object_or_404(Story, id=self.id)
        # Set the id = None to create the copy the story instance
        story_copy.id = None
        story_copy.save()
        # clear relationships if they exist
        if story_copy.series:
            story_copy.Series.clear()
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

    def get_story_download(self):
        """ Return rst formatted string for downloading story meta.
        """

        # loop over m2m and get the values as string
        team = self.team.all()
        team = [user.credit_name for user in team]
        team = ",".join(team)

        share_with = self.share_with.all()
        share_with = [org.name for org in share_with]
        share_with = ",".join(share_with)

        collaborate_with = self.share_with.all()
        collaborate_with = [org.name for org in collaborate_with]
        collaborate_with = ",".join(collaborate_with)

        # verify the text area fields have correct encoding
        name = self.name.encode('utf-8')
        # print "NAME: ", name
        description = self.story_description.encode('utf-8')

        series_name = self.series.name if self.series else ""

        story_download = """
        Story
        ========
        {name}
        --------------
        Description: {desc}
        Series: {series}
        Owner: {owner}
        Organization: {organization}
        Original: {original}
        Team: {team}
        Created: {created}
        Sensitive: {sensitive}
        Embargo Status: {embargo}
        Embargo Date/Time: {embargo_dt}
        Share: {share}
        Share Date: {sharedate}
        Shared With: {sharewith}
        Ready for Sharing: {shareready}
        Collaborate: {collaborate}
        Collaborate With: {collaboratewith}
        Archived: {archived}
        """.format(name=name, desc=description, series=series_name, owner=self.owner, organization=self.organization.name,
        original=self.original_story, team=team, created=self.creation_date, sensitive=self.sensitive,
        embargo=self.embargo, embargo_dt=self.embargo_datetime, share=self.share,
        sharedate=self.share_with_date, sharewith=share_with, shareready=self.ready_to_share,
        collaborate=self.collaborate, collaboratewith=collaborate_with, archived=self.archived)
        return story_download

    # formerly get_story_team
    def get_story_team_vocab(self):
        """Return queryset with org users and users from collaboration orgs for a story.
        Used in selecting credit and editors for a facet.
        """

        collaborators = self.collaborate_with.all()
        story_team = User.objects.filter(Q(Q(organization=self.organization) | Q(organization__in=collaborators)))
        return story_team

    def get_story_images(self):
        """Return all the images associated with a story."""

        story_images = []
        webfacet = self.webfacetstory.all()[0]
        webfacet_images = WebFacet.get_webfacet_images(webfacet)
        printfacet = self.printfacetstory.all()[0]
        printfacet_images = PrintFacet.get_printfacet_images(printfacet)
        audiofacet = self.audiofacetstory.all()[0]
        audiofacet_images = AudioFacet.get_audiofacet_images(audiofacet)
        videofacet = self.videofacetstory.all()[0]
        videofacet_images = VideoFacet.get_videofacet_images(videofacet)
        story_images.extend(webfacet_images)
        story_images.extend(printfacet_images)
        story_images.extend(audiofacet_images)
        story_images.extend(videofacet_images)

        return story_images

    def get_story_documents(self):
        """Return all documents associated with a story."""

        story_documents = []
        webfacet = self.webfacetstory.all()[0]
        webfacet_documents = WebFacet.get_webfacet_documents(webfacet)
        printfacet = self.printfacetstory.all()[0]
        printfacet_documents = PrintFacet.get_printfacet_documents(printfacet)
        audiofacet = self.audiofacetstory.all()[0]
        audiofacet_documents = AudioFacet.get_audiofacet_documents(audiofacet)
        videofacet = self.videofacetstory.all()[0]
        videofacet_documents = VideoFacet.get_videofacet_documents(videofacet)
        story_documents.extend(webfacet_documents)
        story_documents.extend(printfacet_documents)
        story_documents.extend(audiofacet_documents)
        story_documents.extend(videofacet_documents)

        return story_documents

    def get_story_audio(self):
        """Return all audio associated with a story."""

        story_audio = []
        webfacet = self.webfacetstory.all()[0]
        webfacet_audio = WebFacet.get_webfacet_audio(webfacet)
        printfacet = self.printfacetstory.all()[0]
        printfacet_audio = PrintFacet.get_printfacet_audio(printfacet)
        audiofacet = self.audiofacetstory.all()[0]
        audiofacet_audio = AudioFacet.get_audiofacet_audio(audiofacet)
        videofacet = self.videofacetstory.all()[0]
        videofacet_audio = VideoFacet.get_videofacet_audio(videofacet)
        story_documents.extend(webfacet_audio)
        story_documents.extend(printfacet_audio)
        story_documents.extend(audiofacet_audio)
        story_documents.extend(videofacet_audio)

        return story_audio

    def get_story_facets(self):
        """Return all existing facets associated with a story."""

        # FIXME to be refactored after refactoring facets

        story_facets = []
        if self.webfacetstory.all():
            webfacet = self.webfacetstory.all()[0]
            story_facets.append(webfacet)
        if self.printfacetstory.all():
            printfacet = self.printfacetstory.all()[0]
            story_facets.append(printfacet)
        if self.audiofacetstory.all():
            audiofacet = self.audiofacetstory.all()[0]
            story_facets.append(audiofacet)
        if self.videofacetstory.all():
            videofacet = self.videofacetstory.all()[0]
            story_facets.append(videofacet)

        return story_facets

    @property
    def description(self):
        return self.story_description

    @property
    def search_title(self):
        return self.name

    @property
    def type(self):
        return "Story"

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
#   Secondary Content:
#   Tasks, Events, Social Posts
#-----------------------------------------------------------------------#

#-----------------------------------------------------------------------#
#  TASK
#-----------------------------------------------------------------------#

# class Task(models.Model):
#     """A Task.
#
#     A task is an action item assigned to a team and to a project, series,
#     story or an event.
#     """
#
#     owner = models.ForeignKey(
#       User,
#       related_name='taskowner'
#     )
#
#     title = models.TextField(
#         help_text='Title of the task.'
#     )
#
#     text = models.TextField(
#         help_text='Content of the task.',
#         blank=True,
#     )
#
#     assigned_to = models.ManyToManyField(
#         # There can be multiple users listed as assigned to the task.
#         User,
#         related_name='taskassigneduser',
#         help_text='The users assigned to the task.',
#         blank=True,
#     )
#
#     # Choices for Task status.
#     IDENTIFIED = 'Identified'
#     IN_PROGRESS = 'In Progress'
#     COMPLETE = 'Complete'
#     TASK_STATUS_CHOICES = (
#         (IDENTIFIED, 'Identified'),
#         (IN_PROGRESS, 'In Progress'),
#         (COMPLETE, 'Complete'),
#     )
#
#     task_status = models.CharField(
#         max_length=50,
#         choices=TASK_STATUS_CHOICES,
#         help_text='Task status.'
#     )
#
#     important = models.BooleanField(
#         default=False,
#         help_text='Whether a task is important.'
#     )
#
#     creation_date = models.DateTimeField(
#         auto_now_add=True,
#         help_text='Date and time task is created.',
#         blank=True,
#     )
#
#     due_date = models.DateTimeField(
#         help_text='Date and time task is to be completed.',
#         blank=True,
#     )
#
#     inprogress_date = models.DateTimeField(
#         help_text='Date and time task status is changed to in progress.',
#         blank=True,
#     )
#
#     completion_date = models.DateTimeField(
#         auto_now_add=True,
#         help_text='Date and time task status is changed to complete.',
#         blank=True,
#     )
#
#     # a task can be associated with a project, series, story or an event.
#     # using contenttypes and generic relations to easily connect to one of
#     # several possible foreign keys and to easily query all the tasks for
#     # one of the associated models (project, series, story, event)
#     content_type = models.ForeignKey(ContentType)
#     object_id = models.PositiveIntegerField()
#     content_object=GenericForeignKey('content_type', 'object_id')
#
#     @property
#     def task_title(self):
#         return self.title



#-----------------------------------------------------------------------#
#  EVENT
#-----------------------------------------------------------------------#

# class Event(models.Model):
#     """An event.
#
#     An event can be assigned to an Organization, Project, Series or Story.
#     """
#
#     title = models.TextField(
#         help_text='Title of the event.'
#     )
#
#     description = models.TextField(
#         help_text='Description of the event.',
#         blank=True,
#     )
#
#     team = models.ManyToManyField(
#         # There can be multiple users assigned to an event.
#         User,
#         related_name='eventteam',
#         help_text='The users assigned to an event.',
#         blank=True,
#     )
#
#     creation_date = models.DateTimeField(
#         auto_now_add=True,
#         help_text='Date and time event is created.',
#         blank=True,
#     )
#
#     event_date = models.DateTimeField(
#         help_text='Date and time of the event.',
#         blank=True,
#     )
#
#     venue = models.TextField(
#         help_text = 'The location of the event.',
#         blank=True,
#     )
#
#     #Tasks
#     tasks = GenericRelation(Task)
#
#     # Notes
#     #TODO Add Notes to note class to be attached to Events
#
#     # Assets
#     #TODO Add Document and Image assets for events to Assets section.
#
#     # an event can be associated with an organization, project, series or story.
#     # using contenttypes and generic relations to connect to one of
#     # several possible foreign keys and to easily query all the tasks for
#     # one of the associated models (organization, project, series or story)
#     content_type = models.ForeignKey(ContentType)
#     object_id = models.PositiveIntegerField()
#     content_object=GenericForeignKey('content_type', 'object_id')
#
#     @property
#     def title(self):
#         return self.title


#-----------------------------------------------------------------------#
#  SOCIAL POST
#-----------------------------------------------------------------------#

# class SocialPost(models.Model):
#     """A social post.
#
#     A social post to promote a project, series, story or event.
#     """
#
#     FACEBOOK = 'Facebook'
#     TWITTER = 'Twitter'
#     INSTAGRAM = 'Instagram'
#     SOCIAL_ACCOUNT_CHOICES = (
#         (FACEBOOK, 'Facebook'),
#         (TWITTER, 'Twitter'),
#         (INSTAGRAM, 'Instagram'),
#     )
#
#     social_platform = models.CharField(
#         max_length=50,
#         choices=SOCIAL_ACCOUNT_CHOICES,
#         help_text='Platform the post is created for.'
#     )
#
#     text = models.TextField(
#         help_text='Content of the post.'
#     )
#
#     # a social post can be associated with a project, series, story or an event.
#     #TODO Add connection to P, Se, St, or E
#
#     #TODO Add Image assets for social posts to Assets section.
#
#     @property
#     def type(self):
#         return "Social Post."


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


#-----------------------------------------------------------------------#
#   Assets:
#   ImageAsset, DocumentAsset, AudioAsset, VideoAsset,
#-----------------------------------------------------------------------#

#-----------------------------------------------------------------------#
#   Image Asset
#-----------------------------------------------------------------------#

class ImageAssetManager(models.Manager):
    """Custom manager for ImageAsset."""

    def create_imageasset(self, owner, organization, asset_title, asset_description, asset_attribution, photo, image_type, keywords):
        """Method for quick creation of an image asset."""
        imageasset=self.create(owner=owner, organization=organization, asset_title=asset_title, asset_description=asset_description, asset_attribution=asset_attribution, photo=photo, image_type=image_type, keywords=keywords)
        return imageasset


@python_2_unicode_compatible
class ImageAsset(models.Model):
    """ Uploaded Image Asset. """

    owner = models.ForeignKey(
        User,
        related_name='image_asset_owner',
    )

    organization = models.ForeignKey(
        Organization,
        related_name='image_asset_organization'
    )

    original = models.BooleanField(
        default=True,
        help_text='This content originally belonged to this organization.'
    )

    asset_title = models.CharField(
        max_length=200,
        help_text='Text for file name. Name it intuitively.',
        blank=True,
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

    photo = models.ImageField(
        upload_to='photos',
        blank=True,
    )

    display_photo = ImageSpecField(
        source='photo',
        format='JPEG',
    )

    #Choices for Asset type
    PHOTO = 'PIC'
    GRAPHIC = 'GRAPH'

    IMAGE_TYPE_CHOICES = (
        (PHOTO, 'Photograph'),
        (GRAPHIC, 'Graphic'),
    )

    image_type = models.CharField(
        max_length=20,
        choices = IMAGE_TYPE_CHOICES,
        help_text='The kind of image.'
    )

    creation_date = models.DateTimeField(
        auto_now_add=True,
        help_text='When the asset was created.'
    )

    keywords = ArrayField(
        models.CharField(max_length=100),
        default=list,
        help_text='List of keywords for search.',
        blank=True,
    )

    objects = ImageAssetManager()

    class Meta:
        verbose_name = "Image"
        verbose_name_plural = "Images"

    def get_image_usage(self):
        """Return facets an image is associated with."""

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

    def copy_image(self):
        """ Create a copy of an image for a partner organization in a network.

        Copied images keep all associated information. Organization is set to
        the copier's organization and the original flag is set to false.
        Triggering a copy also triggers the creation of an image copy detail record."""

        image_copy = get_object_or_404(ImageAsset, id=self.id)
        #set the id = None to create the copy of the image instance
        image_copy.id = None
        image_copy.save()
        image_copy.original = False
        image_copy.save()
        return image_copy

    def get_image_download_info(self):
        """Return rst of image information for download."""

        title = self.asset_title.encode('utf-8')
        description = self.asset_description.encode('utf-8')
        attribution = self.attribution.encode('utf-8')

        image_info="""
        Image
        =======
        {title}.jpg
        Description: {description}
        Attribution: {attribution}
        Type: {type}
        Creation Date: {date}
        Owner: {owner}
        Organization: {organization}
        Original: {original}
        Keywords: {keywords}
        """.format(title=title, description=description, attribution=attribution,
        type=self.image_type, date=self.creation_date, owner=self.owner,
        organization=self.organization.name, original=self.original,
        keywords=self.keywords)

        return image_info

    def __str__(self):
        return self.asset_title

    def get_absolute_url(self):
        return reverse('image_asset_detail', kwargs={'pk': self.id})

    @property
    def description(self):
        return self.asset_description.encode('utf-8')

    @property
    def search_title(self):
        return self.asset_title

    @property
    def type(self):
        return "Image"

#-----------------------------------------------------------------------#
# DocumentAsset
#-----------------------------------------------------------------------#

class DocumentAssetManager(models.Manager):
    """Custom manager for DocumentAsset."""

    def create_documentasset(self, owner, organization, asset_title, asset_description, asset_attribution, document, doc_type, keywords):
        """Method for quick creation of a document asset."""
        documentasset=self.create(owner=owner, organization=organization, asset_title=asset_title, asset_description=asset_description, asset_attribution=asset_attribution, document=document, doc_type=doc_type, keywords=keywords)
        return documentasset


@python_2_unicode_compatible
class DocumentAsset(models.Model):
    """ Uploaded Document Asset. """

    owner = models.ForeignKey(
        User,
        related_name='document_asset_owner',
    )

    organization = models.ForeignKey(
        Organization,
        related_name='document_asset_organization'
    )

    original = models.BooleanField(
        default=True,
        help_text='This content originally belonged to this organization.'
    )

    asset_title = models.CharField(
        max_length=200,
        help_text='Text for file name. Name it intuitively.',
        blank=True,
    )

    asset_description = models.TextField(
        max_length=300,
        help_text='What is the asset.',
        blank=True,
    )

    attribution = models.TextField(
        max_length=200,
        help_text='The appropriate information for crediting the asset.',
        blank=True,
    )

    document = models.FileField(
        upload_to='documents',
        blank=True,
    )

    #Choices for Asset type
    PDF = 'PDF'
    WORD = 'WORD DOC'
    TXT =  'TEXT'
    CSV = 'COMMA SEPARATED'
    XLS = 'EXCEL'
    OTHER = 'OTHER'

    DOCUMENT_TYPE_CHOICES = (
        (PDF, 'Adobe PDF'),
        (WORD, 'Word Doc'),
        (TXT, 'Text File'),
        (CSV, 'Comma Separated'),
        (XLS, 'Excel File'),
        (OTHER, 'Other'),
    )

    doc_type = models.CharField(
        max_length=20,
        choices = DOCUMENT_TYPE_CHOICES,
        help_text='The kind of document.'
    )

    creation_date = models.DateTimeField(
        auto_now_add=True,
        help_text='When the asset was created.'
    )

    keywords = ArrayField(
        models.CharField(max_length=100),
        default=list,
        help_text='List of keywords for search.',
        blank=True,
    )

    objects = DocumentAssetManager()

    class Meta:
        verbose_name = "Document"
        verbose_name_plural = "Documents"

    def get_document_usage(self):
        """Return facets a document is associated with."""

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

    def copy_document(self):
        """ Create a copy of a document for a partner organization in a network.

        Copied documents keep all associated information. Organization is set to
        the copier's organization and the original flag is set to false.
        Triggering a copy also triggers the creation of an document copy detail record."""

        document_copy = get_object_or_404(DocumentAsset, id=self.id)
        #set the id = None to create the copy of the document instance
        document_copy.id = None
        document_copy.save()
        document_copy.original = False
        document_copy.save()
        return document_copy

    def get_document_download_info(self):
        """Return rst of document information for download."""

        title = self.asset_title.encode('utf-8')
        description = self.asset_description.encode('utf-8')
        attribution = self.attribution.encode('utf-8')

        document_info="""
        Document
        =======
        {title}.jpg
        Description: {description}
        Attribution: {attribution}
        Type: {type}
        Creation Date: {date}
        Owner: {owner}
        Organization: {organization}
        Original: {original}
        Keywords: {keywords}
        """.format(title=title, description=description, attribution=attribution,
        type=self.doc_type, date=self.creation_date, owner=self.owner,
        organization=self.organization.name, original=self.original,
        keywords=self.keywords)

        return document_info

    def __str__(self):
        return self.asset_title

    # def get_absolute_url(self):
    #     return reverse('document_asset_detail', kwargs={'pk': self.id})

    @property
    def description(self):
        return self.asset_description.encode('utf-8')

    @property
    def search_title(self):
        return self.asset_title

    @property
    def type(self):
        return "Document"

#-----------------------------------------------------------------------#
# AudioAsset
#-----------------------------------------------------------------------#

class AudioAssetManager(models.Manager):
    """Custom manager for AudioAsset."""

    def create_audioasset(self, owner, organization, asset_title, asset_description, asset_attribution, audio, audio_type, keywords):
        """Method for quick creation of a audio asset."""
        audioasset=self.create(owner=owner, organization=organization, asset_title=asset_title, asset_description=asset_description, asset_attribution=asset_attribution, audio=audio, audio_type=audio_type, keywords=keywords)
        return audioasset


@python_2_unicode_compatible
class AudioAsset(models.Model):
    """ Uploaded Audio Asset. """

    owner = models.ForeignKey(
        User,
        related_name='audio_asset_owner',
    )

    organization = models.ForeignKey(
        Organization,
        related_name='audio_asset_organization'
    )

    original = models.BooleanField(
        default=True,
        help_text='This content originally belonged to this organization.'
    )

    asset_title = models.CharField(
        max_length=200,
        help_text='Text for file name. Name it intuitively.',
        blank=True,
    )

    asset_description = models.TextField(
        max_length=300,
        help_text='What is the asset.',
        blank=True,
    )

    attribution = models.TextField(
        max_length=200,
        help_text='The appropriate information for crediting the asset.',
        blank=True,
    )

    audio = models.FileField(
        upload_to='audio',
        blank=True,
    )

    link = models.URLField(
        max_length=400,
        help_text='Link to audio file on SoundCloud',
        blank=True,
    )

    #Choices for Asset type
    MP3 = 'MP3'
    WAV = 'WAV'
    SOUNDCLOUD = 'SC'

    AUDIO_TYPE_CHOICES = (
        (MP3, 'mp3'),
        (WAV, 'wav'),
        (SOUNDCLOUD, 'SoundCloud')
    )

    audio_type = models.CharField(
        max_length=20,
        choices = AUDIO_TYPE_CHOICES,
        help_text='The kind of audio.'
    )

    creation_date = models.DateTimeField(
        auto_now_add=True,
        help_text='When the asset was created.'
    )

    keywords = ArrayField(
        models.CharField(max_length=100),
        default=list,
        help_text='List of keywords for search.',
        blank=True,
    )

    objects = AudioAssetManager()

    class Meta:
        verbose_name = "Audio Asset"
        verbose_name_plural = "Audio Assets"

    def get_audio_usage(self):
        """Return facets an audio file is associated with."""

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

    def copy_audio(self):
        """ Create a copy of an audiofile for a partner organization in a network.

        Copied audio keep all associated information. Organization is set to
        the copier's organization and the original flag is set to false.
        Triggering a copy also triggers the creation of an audiofile copy detail record."""

        audio_copy = get_object_or_404(AudioAsset, id=self.id)
        #set the id = None to create the copy of the audio instance
        audio_copy.id = None
        audio_copy.save()
        audio_copy.original = False
        audio_copy.save()
        return audio_copy

    def get_audio_download_info(self):
        """Return rst of audio information for download."""

        title = self.asset_title.encode('utf-8')
        description = self.asset_description.encode('utf-8')
        attribution = self.attribution.encode('utf-8')

        audio_info = """
        Audio
        =======
        {title}.jpg
        Description: {description}
        Attribution: {attribution}
        Type: {type}
        Creation Date: {date}
        Owner: {owner}
        Organization: {organization}
        Original: {original}
        Keywords: {keywords}
        """.format(title=title, description=description, attribution=attribution,
        type=self.audio_type, date=self.creation_date, owner=self.owner,
        organization=self.organization.name, original=self.original,
        keywords=self.keywords)

        return audio_info

    def __str__(self):
        return self.asset_title

    # def get_absolute_url(self):
    #     return reverse('asset_detail', kwargs={'pk': self.id})

    @property
    def description(self):
        return self.asset_description.encode('utf-8')

    @property
    def search_title(self):
        return self.asset_title

    @property
    def type(self):
        return "Audio"

#-----------------------------------------------------------------------#
#VideoAsset
#-----------------------------------------------------------------------#

class VideoAssetManager(models.Manager):
    """Custom manager for VideoAsset."""

    def create_videoasset(self, owner, organization, asset_title, asset_description, asset_attribution, video, video_type, keywords):
        """Method for quick creation of a video asset."""
        videoasset=self.create(owner=owner, organization=organization, asset_title=asset_title, asset_description=asset_description, asset_attribution=asset_attribution, video=video, video_type=video_type, keywords=keywords)
        return videoasset


@python_2_unicode_compatible
class VideoAsset(models.Model):
    """ Uploaded Video Asset. """

    owner = models.ForeignKey(
        User,
        related_name='video_asset_owner',
    )

    organization = models.ForeignKey(
        Organization,
        related_name='video_asset_organization'
    )

    original = models.BooleanField(
        default=True,
        help_text='This content originally belonged to this organization.'
    )

    asset_title = models.CharField(
        max_length=200,
        help_text='Text for file name. Name it intuitively.',
        blank=True,
    )

    asset_description = models.TextField(
        max_length=300,
        help_text='What is the asset.',
        blank=True,
    )

    attribution = models.TextField(
        max_length=200,
        help_text='The appropriate information for crediting the asset.',
        blank=True,
    )

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

    #Choices for Asset type
    MP4 = 'MP4'
    YT = 'YOUTUBE'
    VIM = 'VIMEO'

    VIDEO_TYPE_CHOICES = (
        (MP4, 'mp4'),
        (YT, 'YouTube'),
        (VIM, 'Vimeo')
    )

    video_type = models.CharField(
        max_length=20,
        choices = VIDEO_TYPE_CHOICES,
        help_text='The kind of video.'
    )

    creation_date = models.DateTimeField(
        auto_now_add=True,
        help_text='When the asset was created.'
    )

    keywords = ArrayField(
        models.CharField(max_length=100),
        default=list,
        help_text='List of keywords for search.',
        blank=True,
    )

    objects = VideoAssetManager()

    class Meta:
        verbose_name = "Video Asset"
        verbose_name_plural = "Video Assets"

    def get_video_usage(self):
        """Return facets an video file is associated with."""

        video_usage = []

        video_webfacets = WebFacet.objects.filter(Q(video_assets=self))
        video_printfacets = PrintFacet.objects.filter(Q(video_assets=self))
        video_videofacets = VideoFacet.objects.filter(Q(video_assets=self))
        video_usage.extend(video_webfacets)
        video_usage.extend(video_printfacets)
        video_usage.extend(video_videofacets)
        video_usage.extend(video_videofacets)
        return video_usage

    def copy_video(self):
        """ Create a copy of a video for a partner organization in a network.

        Copied video keep all associated information. Organization is set to
        the copier's organization and the original flag is set to false.
        Triggering a copy also triggers the creation of a video copy detail record."""

        video_copy = get_object_or_404(VideoAsset, id=self.id)
        #set the id = None to create the copy of the video instance
        video_copy.id = None
        video_copy.save()
        video_copy.original = False
        video_copy.save()
        return video_copy

    def get_video_download_info(self):
        """Return rst of video information for download."""

        title = self.asset_title.encode('utf-8')
        description = self.asset_description.encode('utf-8')
        attribution = self.attribution.encode('utf-8')

        video_info="""
        Video
        =======
        {title}.jpg
        Description: {description}
        Attribution: {attribution}
        Type: {type}
        Creation Date: {date}
        Owner: {owner}
        Organization: {organization}
        Original: {original}
        Keywords: {keywords}
        """.format(title=title, description=description, attribution=attribution,
        type=self.doc_type, date=self.creation_date, owner=self.owner,
        organization=self.organization.name, original=self.original,
        keywords=self.keywords)

        return video_info

    def __str__(self):
        return self.asset_title

    # def get_absolute_url(self):
    #     return reverse('asset_detail', kwargs={'pk': self.id})

    @property
    def description(self):
        return self.asset_description.encode('utf-8')

    @property
    def search_title(self):
        return self.asset_title

    @property
    def type(self):
        return "Video"


#-----------------------------------------------------------------------#
# GoverningDocumentAsset

class GoverningDocumentAssetManager(models.Manager):
    """Custom manager for GoverningDocumentAsset."""

    def create_governingdocumentasset(self, owner, organization, asset_title, asset_description, asset_attribution, document, doc_type, keywords):
        """Method for quick creation of a document asset."""
        documentasset=self.create(owner=owner, organization=organization, asset_title=asset_title, asset_description=asset_description, asset_attribution=asset_attribution, document=document, doc_type=doc_type, keywords=keywords)
        return documentasset


@python_2_unicode_compatible
class GoverningDocumentAsset(models.Model):
    """ Uploaded Governing Document Asset. """

    owner = models.ForeignKey(
        User,
        related_name='governing_document_asset_owner',
    )

    organization = models.ForeignKey(
        Organization,
        related_name='governing_document_asset_organization'
    )

    original = models.BooleanField(
        default=True,
        help_text='This content originally belonged to this organization.'
    )

    asset_title = models.CharField(
        max_length=200,
        help_text='Text for file name. Name it intuitively.',
        blank=True,
    )

    asset_description = models.TextField(
        max_length=300,
        help_text='What is the asset.',
        blank=True,
    )

    attribution = models.TextField(
        max_length=200,
        help_text='The appropriate information for crediting the asset.',
        blank=True,
    )

    document = models.FileField(
        upload_to='governing documents',
        blank=True,
    )

    #Choices for Asset type
    PDF = 'PDF'
    WORD = 'WORD DOC'
    TXT =  'TEXT'
    CSV = 'COMMA SEPARATED'
    XLS = 'EXCEL'
    OTHER = 'OTHER'

    DOCUMENT_TYPE_CHOICES = (
        (PDF, 'Adobe PDF'),
        (WORD, 'Word Doc'),
        (TXT, 'Text File'),
        (CSV, 'Comma Separated'),
        (XLS, 'Excel File'),
        (OTHER, 'Other'),
    )

    doc_type = models.CharField(
        max_length=20,
        choices = DOCUMENT_TYPE_CHOICES,
        help_text='The kind of document.'
    )

    creation_date = models.DateTimeField(
        auto_now_add=True,
        help_text='When the asset was created.'
    )

    keywords = ArrayField(
        models.CharField(max_length=100),
        default=list,
        help_text='List of keywords for search.',
        blank=True,
    )

    objects = GoverningDocumentAssetManager()

    class Meta:
        verbose_name = "Governing Document"
        verbose_name_plural = "Governing Documents"

    def __str__(self):
        return self.asset_title

    # def get_absolute_url(self):
    #     return reverse('document_asset_detail', kwargs={'pk': self.id})

    @property
    def description(self):
        return self.asset_description.encode('utf-8')

    @property
    def search_title(self):
        return self.asset_title

    @property
    def type(self):
        return "Governing Document"



#-----------------------------------------------------------------------#
# ProjectDocumentAsset

class ProjectDocumentAssetManager(models.Manager):
    """Custom manager for ProjectDocumentAsset."""

    def create_projectdocumentasset(self, owner, organization, asset_title, asset_description, asset_attribution, document, doc_type, keywords):
        """Method for quick creation of a document asset."""
        documentasset=self.create(owner=owner, organization=organization, asset_title=asset_title, asset_description=asset_description, asset_attribution=asset_attribution, document=document, doc_type=doc_type, keywords=keywords)
        return documentasset


@python_2_unicode_compatible
class ProjectDocumentAsset(models.Model):
    """ Uploaded Project Document Asset. """

    owner = models.ForeignKey(
        User,
        related_name='project_document_asset_owner',
    )

    organization = models.ForeignKey(
        Organization,
        related_name='project_document_asset_organization'
    )

    original = models.BooleanField(
        default=True,
        help_text='This content originally belonged to this organization.'
    )

    asset_title = models.CharField(
        max_length=200,
        help_text='Text for file name. Name it intuitively.',
        blank=True,
    )

    asset_description = models.TextField(
        max_length=300,
        help_text='What is the asset.',
        blank=True,
    )

    attribution = models.TextField(
        max_length=200,
        help_text='The appropriate information for crediting the asset.',
        blank=True,
    )

    document = models.FileField(
        upload_to='project documents',
        blank=True,
    )

    #Choices for Asset type
    PDF = 'PDF'
    WORD = 'WORD DOC'
    TXT =  'TEXT'
    CSV = 'COMMA SEPARATED'
    XLS = 'EXCEL'
    OTHER = 'OTHER'

    DOCUMENT_TYPE_CHOICES = (
        (PDF, 'Adobe PDF'),
        (WORD, 'Word Doc'),
        (TXT, 'Text File'),
        (CSV, 'Comma Separated'),
        (XLS, 'Excel File'),
        (OTHER, 'Other'),
    )

    doc_type = models.CharField(
        max_length=20,
        choices = DOCUMENT_TYPE_CHOICES,
        help_text='The kind of document.'
    )

    creation_date = models.DateTimeField(
        auto_now_add=True,
        help_text='When the asset was created.'
    )

    keywords = ArrayField(
        models.CharField(max_length=100),
        default=list,
        help_text='List of keywords for search.',
        blank=True,
    )

    objects = ProjectDocumentAssetManager()

    class Meta:
        verbose_name = "Project Document"
        verbose_name_plural = "Project Documents"

    def __str__(self):
        return self.asset_title

    # def get_absolute_url(self):
    #     return reverse('document_asset_detail', kwargs={'pk': self.id})

    @property
    def description(self):
        return self.asset_description.encode('utf-8')

    @property
    def search_title(self):
        return self.asset_title

    @property
    def type(self):
        return "Project Document"


#-----------------------------------------------------------------------#
#   Notes:
#   Note, NetworkNote, OrganizationNote, UserNote, SeriesNote, StoryNote
#-----------------------------------------------------------------------#


@python_2_unicode_compatible
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

    def __str__(self):
        return self.title

    @property
    def description(self):
        return "Keywords: {keywords}".format(keywords = self.keywords)

    @property
    def search_title(self):
        return self.title


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

    def get_absolute_url(self):
        return reverse('network_detail', kwargs={'pk': self.network.id})

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

    def get_absolute_url(self):
        return reverse('org_detail', kwargs={'pk': self.organization.id})

    @property
    def type(self):
        return "Organization Note"


class UserNote(Note):
    """ General purpose notes from a user. """

    owner = models.ForeignKey(
        User,
        related_name='usernote_owner'
    )

    def get_absolute_url(self):
        return reverse('user_detail', kwargs={'pk': self.owner.id})

    @property
    def type(self):
        return "User Note"


class ProjectNote(Note):
    """ General purpose notes for a project."""

    owner=models.ForeignKey(
        User,
        related_name='projectnote_owner'
    )

    organization=models.ForeignKey(
        Organization,
        related_name="projectnote_org"
    )

    project = models.ForeignKey(
        Project,
        related_name="projectnote",
    )

    def get_absolute_url(self):
        return reverse('project_detail', kwargs={'pk': self.project.id})

    @property
    def type(self):
        return "Project Note"


class SeriesNote(Note):
    """ A note attached to a series."""

    owner = models.ForeignKey(
        User,
        related_name='seriesnote_owner'
    )

    organization=models.ForeignKey(
        Organization,
        related_name="seriesnote_org"
    )

    series = models.ForeignKey(
        Series,
        related_name="seriesnote",
    )

    def get_absolute_url(self):
        return reverse('series_detail', kwargs={'pk': self.series.id})

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

    organization=models.ForeignKey(
        Organization,
        related_name="storynote_org"
    )

    story = models.ForeignKey(
        Story,
    )

    def __str__(self):
        return "StoryNote: {storynote} for Story: {story}".format(
                                storynote=self.id,
                                story=self.story.id,
                                )

    def get_absolute_url(self):
        return reverse('story_detail', kwargs={'pk': self.story.id})

    @property
    def type(self):
        return "Story Note"

#-----------------------------------------------------------------------#
#   Discussion:
#   Discussion, PrivateDiscussion, PrivateMessage, Comment, CommentReadStatus
#-----------------------------------------------------------------------#

class DiscussionManager(models.Manager):
    """ Custom manager for discussions."""

    def create_discussion(self, discussion_type):
        """ Method for quick creation of a discussion."""
        discussion = self.create(discussion_type=discussion_type)
        return discussion


@python_2_unicode_compatible
class Discussion(models.Model):
    """ Class for  for related comments. """

    # Choices for Discussion type
    ORGANIZATION = 'ORG'
    NETWORK = 'NET'
    PRIVATE = 'PRI'
    PROJECT = 'PRO'
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
        (PROJECT, 'Project Conversation'),
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


@python_2_unicode_compatible
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


@python_2_unicode_compatible
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

    class Meta:
        verbose_name = 'Private Message'
        verbose_name_plural = "Private Messages"
        ordering = ['date']

    def __str__(self):
        return self.subject

    @property
    def type(self):
        return "Private Message"


class CommentManager(models.Manager):
    """ Custom manager for comments."""

    def create_comment(self, user, discussion, text):
        """ Method for quick creation of a discussion."""
        comment = self.create(user=user, discussion=discussion, text=text)
        return comment


@python_2_unicode_compatible
class Comment(models.Model):
    """An individual comment.

    Comments can be made on a seriesplan, storyplan, webfacet,
    audiofacet, videofacet, or between one or more people privately.
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


@python_2_unicode_compatible
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
