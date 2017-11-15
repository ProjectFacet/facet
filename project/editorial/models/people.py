from django.db import models
from django.db.models import Q
from django.contrib.postgres.fields import ArrayField# from simple_history.models import
from imagekit.models import ProcessedImageField, ImageSpecField
from pilkit.processors import ResizeToFit, SmartResize
from django.contrib.auth.models import AbstractUser
from django.utils.encoding import python_2_unicode_compatible
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.db.models.signals import post_save
from django.dispatch import receiver

# from .discussion import Discussion, Comment, PrivateMessage

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
    CONTRIBUTOR = 'Contributor'
    USER_TYPE_CHOICES = (
        (ADMIN, 'Admin'),
        (EDITOR, 'Editor'),
        (STAFF, 'Staff'),
        (CONTRIBUTOR, 'Contributor'),
    )

    # relevant for editors of organizations managing contributors
    # relevant for user accounts of contributors
    # user will appear in public search results for editors accepting contact
    # from contributors and vice versa
    public = models.BooleanField(
        default=False,
        help_text='If an editor or contributor, is the user publicly listed?',
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

        from . import Series, Story, WebFacet, PrintFacet, AudioFacet, VideoFacet

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

        from . import Story

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

        from . import Comment

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

        from . import Comment

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

        return self.private_message_recipient.all()

        # from . import PrivateMessage
        #
        # messages_received = PrivateMessage.objects.filter(recipient=self)
        # return messages_received

    def private_messages_sent(self):
        """ Return all private messages a user has sent.

        Displayed in user inbox under 'sent'.
        """

        from . import PrivateMessage

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
        org = self.organization.name if self.organization else "Contributor"

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


@receiver(post_save, sender=Organization)
def add_discussion(sender, instance, **kwargs):
    if not instance.discussion:
        instance.discussion = Discussion.objects.create_discussion("ORG")


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
