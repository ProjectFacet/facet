""" Model for editorial application.

    Tables
    ---------
    People:
    - User, Organization, Network

    Content:
    - Series, Story, WebFacet, PrintFacet, AudioFacet, VideoFacet

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
from datetime import timedelta
from imagekit.models import ProcessedImageField, ImageSpecField
from pilkit.processors import ResizeToFit, SmartResize
from django.contrib.auth.models import AbstractUser
from django.utils.encoding import python_2_unicode_compatible
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.shortcuts import get_object_or_404
from itertools import chain
from embed_video.fields import EmbedVideoField

#----------------------------------------------------------------------#
#   People:
#   User, Organization, Network
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
        processors=[SmartResize(500,500)],
        format='JPEG',
    )

    facebook = models.URLField(
        max_length=250,
        blank=True,
    )

    twitter = models.URLField(
        max_length=250,
        blank=True,
    )

    github = models.URLField(
        max_length=300,
        blank=True,
    )

    linkedin = models.URLField(
        max_length=250,
        blank=True,
    )

    instagram = models.URLField(
        max_length=250,
        blank=True,
    )

    snapchat = models.URLField(
        max_length=250,
        blank=True,
    )

    vine = models.URLField(
        max_length=250,
        blank=True,
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
        owner, editor, team or credit."""

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

    def get_user_stories(self):
        """Return list of stories that a user is associated with."""

        user_stories = Story.objects.filter(Q(Q(owner=self) | Q(team=self)))
        return user_stories


    def inbox_comments(self):
        """ Return list of comments from discussions the user is a participant in."""

        discussion_ids = {cd['discussion_id'] for cd in Comment.objects.filter(user_id=self.id).values('discussion_id')}
        user_comments = Comment.objects.filter(user_id=self.id)
        all_comments = Comment.objects.filter(discussion_id__in=discussion_ids)
        inbox_comments = all_comments.exclude(id__in=user_comments)
        return inbox_comments

    def recent_comments(self):
        """Return list of comments from discussions the user is a participant in
        since the user's last login."""

        discussion_ids = {cd['discussion_id'] for cd in Comment.objects.filter(user_id=self.id).values('discussion_id')}
        user_comments = Comment.objects.filter(user_id=self.id)
        all_comments = Comment.objects.filter(discussion_id__in=discussion_ids, date__gte=self.last_login)
        recent_comments = all_comments.exclude(id__in=user_comments)
        return recent_comments

    def get_user_contact_list(self):
        """ Return queryset containing all users a specific user can contact.
        This includes any user that's a member of an organization in network.
        """

        organization = self.organization
        org_collaborators = Organization.get_org_collaborators(organization)
        contact_list = User.objects.filter(Q(Q(organization=org_collaborators) | Q(organization=organization)))
        print "Contact List: ", contact_list
        return contact_list


    def private_messages_received(self):
        """ Return all private messages a user is a recipient of."""

        messages_received = PrivateMessage.objects.filter(recipient=self)
        return messages_received

    def private_messages_sent(self):
        """ Return all private messages a user is a recipient of."""

        messages_sent = PrivateMessage.objects.filter(user=self)
        return messages_sent

    def get_user_searchable_content(self):
        """ Return queryset of user specific content that is searchable."""

        usernotes = UserNote.objects.filter(Q(owner=self))

        return usernotes

    @property
    def description(self):
        return "{user}, {title}, {org}".format(
                                        user=self.credit_name,
                                        title=self.title,
                                        org=self.organization.name
                                        )

    @property
    def search_title(self):
        return self.credit_name

#----------------------------------------------------------------------#

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
        processors=[SmartResize(500,500)],
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

    class Meta:
        verbose_name = 'Organization'
        verbose_name_plural = "Organizations"
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
      return reverse('org_detail', kwargs={'pk': self.id})

    def get_org_users(self):
        """ Return queryset of all users in an organization."""

        organization_users = User.objects.filter(organization=self)
        return organization_users

    def get_org_networks(self):
        """ Return list of all the networks that an organization is owner of or member of."""

        all_organization_networks = Network.objects.filter(Q(Q(owner_organization=self) | Q(organizations=self)))
        # not necessary but leaving in for now, check to make sure unique list of networks
        organization_networks = all_organization_networks.distinct()
        return organization_networks

    def get_org_collaborators(self):
        """ Return list of all organizations that are members of the same networks as self."""

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
        """ Return list of all images associated with an organization. """

        images = ImageAsset.objects.filter(organization=self)
        return images

    def get_org_document_library(self):
        """ Return list of all documents associated with an organization. """

        documents = DocumentAsset.objects.filter(organization=self)
        return documents

    def get_org_audio_library(self):
        """ Return list of all audio files associated with an organization. """

        audio = AudioAsset.objects.filter(organization=self)
        return audio

    def get_org_video_library(self):
        """ Return list of all video files associated with an organization. """

        videos = VideoAsset.objects.filter(organization=self)
        return videos

    def get_org_collaborative_content(self):
        """ Return list of all content that an org is a collaborator on."""

        org_collaborative_content = []
        external_stories = Story.objects.filter(Q(collaborate_with=self))
        internal_stories = Story.objects.filter(organization=self).filter(collaborate=True)
        org_collaborative_content.extend(external_stories)
        org_collaborative_content.extend(internal_stories)

        return org_collaborative_content

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

#----------------------------------------------------------------------#

@python_2_unicode_compatible
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
        upload_to='networks',
        blank=True,
    )

    display_logo = ImageSpecField(
        source='logo',
        processors=[SmartResize(500,500)],
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
        """ Return list of stories shared with a network. """

        network_stories = Story.objects.filter(share_with = self.id)
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

#-----------------------------------------------------------------------#
#   Content:
#   Series, Story, WebFacet, PrintFacet, AudioFacet, VideoFacet
#   (A Facet is always part of a story, even if there is only one facet.)
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

#----------------------------------------------------------------------#
#  STORY
#----------------------------------------------------------------------#

@python_2_unicode_compatible
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
        """ Return rst formatted string for downloading story meta."""

        # loop over m2m and get the values as string
        team = self.team.all()
        team = [ user.credit_name for user in team]
        team = ",".join(team)

        share_with = self.share_with.all()
        share_with = [ org.name for org in share_with ]
        share_with = ",".join(share_with)

        collaborate_with = self.share_with.all()
        collaborate_with = [ org.name for org in collaborate_with ]
        collaborate_with = ",".join(collaborate_with)

        # verify the text area fields have correct encoding
        name = self.name.encode('utf-8')
        # print "NAME: ", name
        description = self.story_description.encode('utf-8')

        if self.series:
            series_name = self.series.name
        else:
            series_name = ""

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

    def get_story_team(self):
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
        """Return all documents associated with a story."""

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


    @property
    def description(self):
        return "{description}".format(description=self.story_description)

    @property
    def search_title(self):
        return self.name

    @property
    def type(self):
        return "Story"

#----------------------------------------------------------------------#
#   WEBFACET
#----------------------------------------------------------------------#

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
        verbose_name = 'Webfacet'
        verbose_name_plural = 'Webfacets'
        ordering = ['creation_date']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('story_detail', kwargs={'pk': self.story.id})

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

        webfacet_video = AudioAsset.objects.filter(webfacet=self)
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
        Length: {length}\n
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
        credit=credits, code=self.code, excerpt=excerpt, length=self.length,
        keywords=self.keywords, status=self.status, dueedit=self.due_edit, rundate=self.run_date,
        sharenote=share_note, images=images, captions=self.captions, documents=documents,
        audiofiles=audiofiles, content=content)

        return webfacet_download


    @property
    def description(self):
        return "{desc}".format(desc=self.wf_description)

    @property
    def search_title(self):
        return self.title

    @property
    def type(self):
        return "WebFacet"

#----------------------------------------------------------------------#
#   PRINTFACET
#----------------------------------------------------------------------#

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

        printfacet_video = AudioAsset.objects.filter(printfacet=self)
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
        Length: {length}\n
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
        credit=credits, code=self.code, excerpt=excerpt, length=self.length,
        keywords=self.keywords, status=self.status, dueedit=self.due_edit, rundate=self.run_date,
        sharenote=share_note, images=images, captions=self.captions, documents=documents,
        audiofiles=audiofiles, content=content)

        return printfacet_download

    @property
    def description(self):
        return "{desc}".format(desc=self.pf_description)

    @property
    def search_title(self):
        return self.title

    @property
    def type(self):
        return "PrintFacet"

#----------------------------------------------------------------------#
#   AUDIOFACET
#----------------------------------------------------------------------#

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

        audiofacet_video = AudioAsset.objects.filter(audiofacet=self)
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
        Length: {length}\n
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
        credit=credits, code=self.code, excerpt=excerpt, length=self.length,
        keywords=self.keywords, status=self.status, dueedit=self.due_edit, rundate=self.run_date,
        sharenote=share_note, images=images, captions=self.captions, documents=documents,
        audiofiles=audiofiles, content=content)

        return audiofacet_download


    @property
    def description(self):
        return "{desc}".format(desc=self.af_description)

    @property
    def search_title(self):
        return self.title

    @property
    def type(self):
        return "AudioFacet"

#----------------------------------------------------------------------#
#   VIDEOFACET
#----------------------------------------------------------------------#

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

        videofacet_video = AudioAsset.objects.filter(videofacet=self)
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
        Length: {length}\n
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
        credit=credits, code=self.code, excerpt=excerpt, length=self.length,
        keywords=self.keywords, status=self.status, dueedit=self.due_edit, rundate=self.run_date,
        sharenote=share_note, images=images, captions=self.captions, documents=documents,
        audiofiles=audiofiles, content=content)

        return videofacet_download

    @property
    def description(self):
        return "{desc}".format(desc=self.vf_description)

    @property
    def search_title(self):
        return self.title

    @property
    def type(self):
        return "VideoFacet"


#----------------------------------------------------------------------#
#   Contributor Associations:
#   WebFacetContributor, PrintFacetContributor,
#   AudioFacetContributor, VideoFacetContributor
#----------------------------------------------------------------------#

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

#----------------------------------------------------------------------#
#   CopyDetails:
#   SeriesCopyDetail, StoryCopyDetail, WebFacetCopyDetail,
#   PrintFacetCopyDetail, AudioFacetCopyDetail, VideoFacetCopyDetail
#----------------------------------------------------------------------#

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

#----------------------------------------------------------------------#
#   Assets:
#   ImageAsset, DocumentAsset, AudioAsset, VideoAsset,
#----------------------------------------------------------------------#

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
        return reverse('asset_detail', kwargs={'pk': self.id})

    @property
    def description(self):
        return "{desc}".format(desc=self.asset_description.encode('utf-8'))

    @property
    def search_title(self):
        return self.asset_title

    @property
    def type(self):
        return "Image Asset"

#----------------------------------------------------------------------#
# DocumentAsset

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
    #     return reverse('asset_detail', kwargs={'pk': self.id})

    @property
    def description(self):
        return "{desc}".format(desc=self.asset_description.encode('utf-8'))

    @property
    def search_title(self):
        return self.asset_title

    @property
    def type(self):
        return "Document Asset"

#----------------------------------------------------------------------#
# AudioAsset

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

    def get_audio_download_info(self):
        """Return rst of audio information for download."""

        title = self.asset_title.encode('utf-8')
        description = self.asset_description.encode('utf-8')
        attribution = self.attribution.encode('utf-8')

        audio_info="""
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
        return "{desc}".format(desc=self.asset_description.encode('utf-8'))

    @property
    def search_title(self):
        return self.asset_title

    @property
    def type(self):
        return "Audio Asset"

#----------------------------------------------------------------------#
#VideoAsset

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
        video_videofacets = VideoFacet.objects.filter(Q(video_assets=self))
        video_usage.extend(video_webfacets)
        video_usage.extend(video_printfacets)
        video_usage.extend(video_videofacets)
        video_usage.extend(video_videofacets)
        return video_usage

    # def get_video_download_info(self):
    #     """Return rst of video information for download."""

    #     title = self.asset_title.encode('utf-8')
    #     description = self.asset_description.encode('utf-8')
    #     attribution = self.attribution.encode('utf-8')

    #     video_info="""
    #     Video
    #     =======
    #     {title}.jpg
    #     Description: {description}
    #     Attribution: {attribution}
    #     Type: {type}
    #     Creation Date: {date}
    #     Owner: {owner}
    #     Organization: {organization}
    #     Original: {original}
    #     Keywords: {keywords}
    #     """.format(title=title, description=description, attribution=attribution,
    #     type=self.doc_type, date=self.creation_date, owner=self.owner,
    #     organization=self.organization.name, original=self.original,
    #     keywords=self.keywords)

    #     return video_info

    def __str__(self):
        return self.asset_title

    # def get_absolute_url(self):
    #     return reverse('asset_detail', kwargs={'pk': self.id})

    @property
    def description(self):
        return "{desc}".format(desc=self.asset_description.encode('utf-8'))

    @property
    def search_title(self):
        return self.asset_title

    @property
    def type(self):
        return "Video Asset"


#----------------------------------------------------------------------#
#   Notes:
#   Note, NetworkNote, OrganizationNote, UserNote, SeriesNote, StoryNote
#----------------------------------------------------------------------#


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

#----------------------------------------------------------------------#
#   Discussion:
#   Discussion, PrivateDiscussion, PrivateMessage, Comment, CommentReadStatus
#----------------------------------------------------------------------#

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
