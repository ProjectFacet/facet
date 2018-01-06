from datetime import datetime, timedelta, time

from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import Q
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from imagekit.models import ImageSpecField
from pilkit.processors import SmartResize


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

    # Made optional for users not pushing content to an org (freelancers)
    organization = models.ForeignKey(
        'Organization',
        blank=True,
        null=True,
    )

    ADMIN = 'Admin'
    EDITOR = 'Editor'
    STAFF = 'Staff'
    OTHER = 'Other'
    USER_TYPE_CHOICES = (
        (ADMIN, 'Admin'),
        (EDITOR, 'Editor'),
        (STAFF, 'Staff'),
        (OTHER, 'Other'),
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
        max_length=255,
        blank=True,
    )

    expertise = ArrayField(
        models.CharField(max_length=255),
        default=list,
        help_text='Array of user skills and beats to filter/search by.',
        blank=True,
    )

    notes = models.ManyToManyField(
        'Note',
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
        projects_owner = self.project_owner.all()
        projects_team = self.project_team_member.all()
        series_owner = self.series_owner.all()
        series_team = self.series_team_member.all()
        story_owner = self.story_owner.all()
        story_team = self.story_team_member.all()
        facet_owner = self.facetowner.all()
        # facet_team = self.team.all()
        user_content.extend(projects_owner)
        user_content.extend(projects_team)
        user_content.extend(series_owner)
        user_content.extend(series_team)
        user_content.extend(story_owner)
        user_content.extend(story_team)
        user_content.extend(facet_owner)

        return user_content

    def get_user_assets(self):
        """Return assets that a user is associated with."""

        user_assets = []
        images_owner = self.imageasset_set.all()
        documents_owner = self.documentasset_set.all()
        audio_owner = self.audioasset_set.all()
        video_owner = self.videoasset_set.all()
        user_assets.extend(images_owner)
        user_assets.extend(documents_owner)
        user_assets.extend(audio_owner)
        user_assets.extend(video_owner)

        return user_assets


    def inbox_comments(self):
        """ Return list of comments from discussions the user is a participant in.

        Collects all relevant comments for a specific user to show in their
        dashboard and inbox.
        """

        from . import Comment

        discussion_ids = self.comment_set.all().values('discussion_id')
        user_comments = self.comment_set.all()
        all_comments = Comment.objects.filter(discussion_id__in=discussion_ids)
        inbox_comments = all_comments.exclude(id__in=user_comments)
        return inbox_comments

    def recent_comments(self):
        """Return list of comments from discussions the user is a participant in
        since the user's last login.

        For display on primary dashboard.
        """

        from . import Comment

        discussion_ids = self.comment_set.all().values('discussion_id')
        user_comments = self.comment_set.all()
        all_comments = Comment.objects.filter(discussion_id__in=discussion_ids, date__gte=self.last_login)
        recent_comments = all_comments.exclude(id__in=user_comments)
        return recent_comments

    # formerly get_user_contact_list
    def get_user_contact_list_vocab(self):
        """ Return queryset containing all users a specific user can contact.
        This includes any user that's a member of an organization in network.

        This vocab list populates to selection for messaging.
        """

        organization = self.organization
        org_collaborators = organization.get_org_collaborators_vocab()
        contact_list = User.objects.filter(Q(Q(organization__in=org_collaborators) | Q(organization=organization)))
        return contact_list

    def private_messages_received(self):
        """ Return all private messages a user is a recipient of.

        Displayed in user inbox under 'inbox'.
        """
        return self.private_message_recipient.all()

    def private_messages_sent(self):
        """ Return all private messages a user has sent.

        Displayed in user inbox under 'sent'.
        """
        return self.private_message_sender.all()

    def get_user_searchable_content(self):
        """ Return queryset of user specific content that is searchable.

        A user can return their own notes in search results.
        """
        return self.usernote_owner.all()

    @property
    def description(self):
        org = self.organization.name if self.organization else "Contractor"

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
        max_length=255,
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

    notes = models.ManyToManyField(
        'Note',
        blank=True,
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
        """ Return queryset of all users in an organization.

        Used for organization dashboards, team views and context processors.
        """
        return self.user_set.all()

    def get_org_networks(self):
        """ Return list of all the networks that an organization is connected to as
        owner or member of.

        Used for dashboard, network dashboards and network content.
        """

        from . import Network

        all_organization_networks = Network.objects.filter(Q(Q(owner_organization=self) | Q(organizations=self)))
        # not necessary but leaving in for now, check to make sure unique list of networks
        organization_networks = all_organization_networks.distinct()
        return organization_networks

    def get_org_network_content(self):
        """Return queryset of content shared with any network an organization is a member of excluding their own content."""

        from . import Story

        networks = Organization.get_org_networks(self)
        network_content = Story.objects.filter(share_with__in=networks).select_related('organization')

        return network_content

    # formerly get_org_collaborators
    def get_org_collaborators_vocab(self):
        """ Return list of all organizations that are members of the same networks as self.

        Used to for selecting organizations to collaborate with and for displaying partners
        in team dashboard. Also used to create get_user_contact_list_vocab.
        """

        # get list of networks that an org is a member of
        networks = self.get_org_networks()
        # get list of organizations that are members of any of those networks
        all_organizations = Organization.objects.filter(Q(network_organization__in=networks))
        # remove user's organization from queryset
        organizations = all_organizations.exclude(id=self.id)
        # get distinct list of organizations
        unique_collaborators = organizations.distinct()
        return unique_collaborators

    def get_org_image_library(self):
        """ Return list of all images associated with an organization.

        Used to display images in media gallery.
        """
        return self.imageasset_set.all()

    def get_org_document_library(self):
        """ Return list of all documents associated with an organization.

        Used to display documents in media gallery.
        """
        return self.documentasset_set.all()

    def get_org_audio_library(self):
        """ Return list of all audio files associated with an organization.

        Used to display audio in media gallery.
        """
        return self.audioasset_set.all()

    def get_org_video_library(self):
        """ Return list of all video files associated with an organization.

        Used to display videos in media gallery.
        """
        return self.videoasset_set.all()

    def get_org_user_comments(self):
        """Retrieve all the comments associated with users of an organization.

        Effectively 'all' comments for an organization. Used in user inbox
        to display streams of all comments.
        """

        from . import Comment

        users = self.get_org_users()
        org_user_comments = Comment.objects.filter(Q(user__in=users))

        return org_user_comments

    def get_org_comments(self):
        """Retrieve all organization comments.

        Used to display all organization comments in dashboard and inbox.
        """

        from . import Comment
        organization_comments = Comment.objects.filter(discussion__discussion_type='ORG', user__organization=self)
        return organization_comments

    def get_network_comments(self):
        """Retrieve all comments for networks an organization is a member of.

        Used to display all network comments in dashboard and inbox.
        """

        from . import Comment

        networks = self.get_org_networks()
        network_discussions = [network.discussion for network in networks]
        network_comments = Comment.objects.filter(discussion__in=network_discussions)
        return network_comments


    def get_project_comments(self):
        """Retrieve all comments for projects belonging to an organization.

        Used to display all project comments in dashboard and inbox."""

        from . import Project, Comment

        org_projects = self.project_organization.all()
        project_discussions = [project.discussion for project in org_projects]
        project_comments = Comment.objects.filter(discussion__in=project_discussions)
        return project_comments

    def get_story_comments(self):
        """Retrieve all comments for stories belonging to an organization.

        Used to display all story comments in dashboard and inbox.
        """

        from . import Story, Comment

        org_stories = Story.objects.filter(organization=self)
        story_discussions = [story.discussion for story in org_stories]
        story_comments = Comment.objects.filter(discussion__in=story_discussions)
        return story_comments

    def get_series_comments(self):
        """Retrieve all comments for series belonging to an organization.

        Used to display all series comments in dashboard and inbox.
        """
        from . import Series, Comment
        org_series = Series.objects.filter(organization=self)
        series_discussions = [series.discussion for series in org_series]
        series_comments = Comment.objects.filter(discussion__in=series_discussions)
        return series_comments

    def get_facet_comments(self):
        """Retrieve all comments for facets belonging to stories of an organization.

        Used to display all facet comments in dashboard and inbox.
        """
        from .facets import Facet
        from .discussion import Comment
        # WJB XXX: this seems inefficient, we should reduce to discussion fields on orig
        # querysets

        org_facets = self.facet_set.all()
        facet_discussions = [facet.discussion for facet in org_facets]
        facet_comments = Comment.objects.filter(discussion__in=facet_discussions)
        return facet_comments

    def get_org_collaborative_content(self):
        """ Return list of all content that an org is a collaborator on.

        All of the collaborative content an organization is participating in
        is displaying in a collaborative content dashboard.
        """

        from .story import Story
        org_collaborative_content = []
        external_stories = Story.objects.filter(Q(collaborate_with=self))
        internal_stories = self.story_set.filter(Q(organization=self) & Q(collaborate=True))
        org_collaborative_content.extend(external_stories)
        org_collaborative_content.extend(internal_stories)
        return org_collaborative_content

    def get_org_external_collaborations(self):
        """ Return all content from partner orgs that an organization is a
        collaborator on.
        """

        from .projects import Project
        from .series import Series
        from .story import Story
        external_collaborative_content = []
        external_projects = Project.objects.filter(Q(collaborate_with=self))
        external_series = Series.objects.filter(Q(collaborate_with=self))
        external_stories = Story.objects.filter(Q(collaborate_with=self))
        external_collaborative_content.extend()
        external_collaborative_content.extend()
        external_collaborative_content.extend()
        return external_collaborative_content

    def get_org_internal_collaborations(self):
        """ Return all content that an organization owns that is a collaboration
        with partner organizations.
        """

        internal_collaborative_content = []
        internal_projects = self.project_set.filter(Q(collaborate=True))
        internal_series = self.series_set.filter(Q(collaborate=True))
        internal_stories = self.story_set.filter(Q(collaborate=True))
        internal_collaborative_content.extend()
        internal_collaborative_content.extend()
        internal_collaborative_content.extend()
        return internal_collaborative_content

    def get_org_stories_running_today(self):
        """Return list of content scheduled to run today.

        Used to display content scheduled to run on any given day
        on the primary dashboard.
        """

        from . import Facet

        # establish timeliness of content
        today = timezone.now().date()
        tomorrow = today + timedelta(1)
        today_start = datetime.combine(today, time())
        today_end = datetime.combine(tomorrow, time())

        # facets where run_date=today
        running_today = Facet.objects.filter(run_date__range=(today_start, today_end), organization=self)

        return running_today

    def get_org_stories_due_for_edit_today(self):
        """Return list of content scheduled for edit today.

        Used to display content scheduled for edit on any given day
        on the primary dashboard.
        """

        from .facets import Facet

        # establish timeliness of content
        today = timezone.now().date()
        tomorrow = today + timedelta(1)
        today_start = datetime.combine(today, time())
        today_end = datetime.combine(tomorrow, time())

        edit_today = Facet.objects.filter(due_edit__range=(today_start, today_end), organization=self)

        return edit_today

    def get_org_projects(self):
        """Return queryset of projects associated with an organization for
        use in PlatformAccount forms.
        """

        from . import Project
        projects = []
        networks = Organization.get_org_networks(self)
        network_projects = Project.objects.filter(share_with__in=networks)
        org_projects = Project.objects.filter(organization=self)
        projects.extend(network_projects)
        projects.extend(org_projects)
        return projects

    def get_org_searchable_content(self):
        """Return queryset of all objects that can be searched by a user."""

        #TODO add tasks, events, notes and comments

        from .projects import Project
        from .series import Series
        from .story import Story
        from .facets import Facet

        #additional required info
        networks = self.get_org_networks()

        searchable_objects = []

        projects = Project.objects.filter(Q(Q(organization=self) | Q(collaborate_with=self)))
        series = Series.objects.filter(Q(Q(organization=self) | Q(collaborate_with=self)))
        stories = Story.objects.filter(Q(Q(organization=self) | Q(collaborate_with=self)))
        facets = Facet.objects.filter(Q(organization=self))
        imageassets = self.imageasset_set.all()

        searchable_objects.append(projects)
        searchable_objects.append(series)
        searchable_objects.append(stories)
        searchable_objects.append(facets)
        searchable_objects.append(imageassets)
        # searchable_objects.append(notes)    FIXME: where should notes come from

        return searchable_objects

    def get_org_facettemplates(self):
        """Return queryset of facet templates that should be available of org facets."""

        from . import FacetTemplate

        return FacetTemplate.objects.filter(Q(organization_id__isnull=True) | Q(organization=self) & Q(is_active=True))


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
    from . import Discussion

    if not instance.discussion:
        instance.discussion = Discussion.objects.create_discussion("ORG")
        instance.save()


class OrganizationSubscriptionManager(models.Manager):
    """Custom manager for Subscription."""

    def create_subscription(self, organization, subscription_type, collaborations, contractors):
        """Method for quick creation of subscription."""

        subscription = self.create(
                        organization,
                        collaborations=collaborations,
                        contractors=contractors,
                        )

        return subscription


@python_2_unicode_compatible
class OrganizationSubscription(models.Model):
    """Details of an organization subscription."""

    # if subscription is for an org account, associate with that org
    organization = models.ForeignKey(
        Organization,
        help_text='Organization associated with this subscription if Org subscription type.',
        on_delete=models.CASCADE,
    )

    # Organization functionality
    collaborations = models.BooleanField(
        default=True,
        help_text='If an organization is using the account for base features of editorial workflow, project management and collaboration.',
    )

    contractors = models.BooleanField(
        default=False,
        help_text='If an organization is using the account to manage contractors.',
    )

    objects = OrganizationSubscriptionManager()

    def __str__(self):
        return "Organization Subscription - {organization}".format(organization=self.organization.name)


#-----------------------------------------------------------------------#

@python_2_unicode_compatible
class Network(models.Model):
    """A group of organizations.

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

    notes = models.ManyToManyField(
        'Note',
        blank=True,
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

        from .story import Story

        network_stories = Story.objects.filter(Q(share_with=self))
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
