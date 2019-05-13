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

from .user import User
from .notes import Note

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

    list_publicly = models.BooleanField(
        default=False,
        help_text='Whether the organization is listed publicly in discovery.',
    )

    public_profile = models.OneToOneField(
        'OrganizationPublicProfile',
        help_text = 'ID of public profile for an organization',
        blank=True,
        null=True,
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

    # simple assets
    simple_image_assets = models.ManyToManyField(
        'SimpleImage',
        related_name='organization_simple_image',
        blank=True,
    )

    simple_document_assets = models.ManyToManyField(
        'SimpleDocument',
        related_name='organization_simple_document',
        blank=True,
    )

    simple_audio_assets = models.ManyToManyField(
        'SimpleAudio',
        related_name='organization_simple_audio',
        blank=True,
    )

    simple_video_assets = models.ManyToManyField(
        'SimpleVideo',
        related_name='organization_simple_video',
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

        # FIXME: does this actually exclude their own content? - Joel

        from . import Story

        networks = self.get_org_networks()
        network_content = Story.objects.filter(share_with__in=networks).select_related('organization')

        return network_content

    def get_org_copied_content(self):
        """Returns queryset of content that an organization has picked up from
        a network partner."""

        from . import StoryCopyDetail
        from . import Story

        copyrecords = StoryCopyDetail.objects.exclude(original_org=self)
        org_copied_content = [record.original_story for record in copyrecords]

        return org_copied_content

    # formerly get_org_collaborators
    def get_org_collaborators_vocab(self):
        """ Return list of all organizations that are members of the same networks as self.

        Used to for selecting organizations to collaborate with and for displaying partners
        in team dashboard. Also used to create get_user_contact_list_vocab.
        """

        # get list of networks that an org is a member of
        networks = self.get_org_networks()
        # get list of organizations that are owners of any of those networks
        # get list of organizations that are members of any of those networks
        # exclude self org
        unique_collaborators = Organization.objects.filter(Q(network_organization__in=networks) | Q(id__in=networks.values('owner_organization'))).exclude(id=self.id)

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

    def get_org_recent_media(self):
        """ Return 24 most recently uploaded media asset files."""

        # FIXME how to best query for the 24 most recent media assets across types.
        images = self.imageasset_set.all().order_by("-creation_date")[:12]
        docs = self.documentasset_set.all().order_by("-creation_date")[:12]
        audio = self.audioasset_set.all().order_by("-creation_date")[:12]
        video = self.videoasset_set.all().order_by("-creation_date")[:12]
        recentmedia = []
        recentmedia.extend(images)
        recentmedia.extend(docs)
        recentmedia.extend(audio)
        recentmedia.extend(video)
        print "RECENT MEDIA: ", recentmedia

        return recentmedia

    def get_org_simple_image_library(self):
        """ Return queryset of all simple images associated with an organization."""

        return self.simpleimage_set.all()

    def get_org_simple_document_library(self):
        """ Return queryset of all simple documents associated with an organizaiton."""

        return self.simpledocument_set.all()

    def get_org_simple_audio_library(self):
        """ Return queryset of all simple audio associated with an organization."""

        return self.simpleaudio_set.all()

    def get_org_simple_video_library(self):
        """ Return queryset of all simple video associated with an organization."""

        return self.simplevideo_set.all()

    def get_org_simple_asset_library(self):
        """ Return organization simple assets."""

        recent_internal_assets = []
        simple_images = self.simpleimage_set.all().order_by("-creation_date")[:12]
        simple_documents = self.simpledocument_set.all().order_by("-creation_date")[:12]
        simple_audio = self.simpleaudio_set.all().order_by("-creation_date")[:12]
        simple_video = self.simplevideo_set.all().order_by("-creation_date")[:12]
        recent_internal_assets.extend(simple_images)
        recent_internal_assets.extend(simple_documents)
        recent_internal_assets.extend(simple_audio)
        recent_internal_assets.extend(simple_video)

        return recent_internal_assets

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

        # TODO include projects that are collaborative
        org_projects = self.project_organization.all()
        project_discussions = [project.discussion for project in org_projects]
        project_comments = Comment.objects.filter(discussion__in=project_discussions)
        return project_comments

    def get_story_comments(self):
        """Retrieve all comments for stories belonging to an organization.

        Used to display all story comments in dashboard and inbox.
        """

        from . import Story, Comment

        # TODO include stories that are collaborative
        org_stories = Story.objects.filter(organization=self)
        story_discussions = [story.discussion for story in org_stories]
        story_comments = Comment.objects.filter(discussion__in=story_discussions)
        return story_comments

    def get_facet_comments(self):
        """Retrieve all comments for facets belonging to stories of an organization.

        Used to display all facet comments in dashboard and inbox.
        """
        from .facets import Facet
        from .discussion import Comment
        # WJB XXX: this seems inefficient, we should reduce to discussion fields on orig
        # querysets

        # TODO include facets on stories that are collaborative
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

        from . import Project
        from . import Story
        external_collaborative_content = []
        external_projects = Project.objects.filter(Q(collaborate_with=self))
        external_stories = Story.objects.filter(Q(collaborate_with=self))
        external_collaborative_content.extend(external_projects)
        external_collaborative_content.extend(external_stories)
        return external_collaborative_content

    def get_org_internal_collaborations(self):
        """ Return all content that an organization owns that is a collaboration
        with partner organizations.
        """

        internal_collaborative_content = []
        internal_projects = self.project_set.filter(Q(collaborate=True))
        internal_stories = self.story_set.filter(Q(collaborate=True))
        internal_collaborative_content.extend(internal_projects)
        internal_collaborative_content.extend(internal_stories)
        return internal_collaborative_content

    def get_org_stories_running_today(self):
        """Return list of content scheduled to run today.

        Used to display content scheduled to run on any given day
        on the primary dashboard.
        """

        from . import Facet

        #FIXME today, tomorrow if off by one day (hacky fix in place)
        # establish timeliness of content
        today = timezone.now().date() - timedelta(1)
        tomorrow = timezone.now().date()
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

        #FIXME today, tomorrow if off by one day (hacky fix in place)
        # establish timeliness of content
        today = timezone.now().date() - timedelta(1)
        tomorrow = timezone.now().date()
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

    def get_org_content_tasks(self):
        """Return all the tasks associated with projects, stories, or events.

        This includes items from content that is collaborative.
        """

        return self.task_set.all()

    def get_org_events(self):
        """Return all the events associated with the org or org content.

        This includes items from content that is collaborative.
        """
        return self.event_set.all()

    def get_org_searchable_comments(self):
        """Return all the comments that should appear in search results.

        This includes comments from items that are collaborative.
        """
        return self.get_org_user_comments()

    def get_org_searchable_notes(self):
        """Return all the notes that should appear in search results.
        This includes notes from items that are collaborative."""

        return Note.objects.filter(user__organization=self).exclude(note_type='User')

    def get_org_searchable_content(self):
        """Return queryset of all objects that can be searched by a user."""

        from .projects import Project
        from .story import Story
        from .facets import Facet

        #additional required info
        networks = self.get_org_networks()

        searchable_objects = []

        projects = Project.objects.filter(Q(Q(organization=self) | Q(collaborate_with=self)))
        stories = Story.objects.filter(Q(Q(organization=self) | Q(collaborate_with=self)))
        facets = Facet.objects.filter(Q(organization=self))
        imageassets = self.imageasset_set.all()
        documentassets = self.documentasset_set.all()
        audioassets = self.audioasset_set.all()
        tasks = self.get_org_content_tasks()
        events = self.get_org_events()
        comments = self.get_org_searchable_comments()
        notes = self.get_org_searchable_notes()

        searchable_objects.append(projects)
        searchable_objects.append(stories)
        searchable_objects.append(facets)
        searchable_objects.append(imageassets)
        searchable_objects.append(documentassets)
        searchable_objects.append(audioassets)
        searchable_objects.append(tasks)
        searchable_objects.append(events)
        searchable_objects.append(notes)
        searchable_objects.append(comments)

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
    from . import OrganizationPublicProfile

    if not instance.discussion:
        instance.discussion = Discussion.objects.create_discussion("ORG")
    if not instance.public_profile:
        instance.public_profile = OrganizationPublicProfile.objects.create_public_profile()
        instance.save()


class OrganizationPublicProfileManager(models.Manager):
    """Custom manager for public profiles."""

    def create_public_profile(self):
        """Method for automatic creation of a public profile."""
        organization_public_profile = self.create()
        return organization_public_profile


class OrganizationPublicProfile(models.Model):
    """
    Details for display in public listing of organization.
    """

    NONPROFIT = 'Nonprofit'
    FORPROFIT = 'For profit'
    OTHER = 'Other'
    ORG_TYPE_CHOICES = (
        (NONPROFIT, 'Nonprofit'),
        (FORPROFIT, 'For profit'),
        (OTHER, 'Other'),
    )

    org_structure = models.CharField(
        max_length=50,
        choices=ORG_TYPE_CHOICES,
        help_text='Financial structure of the organization.',
        blank=True,
    )

    #platforms
    platform_print = models.BooleanField(
        default=False,
        help_text='Organization publishes in print.',
    )

    platform_online = models.BooleanField(
        default=False,
        help_text='Organization publishes online.',
    )

    platform_social = models.BooleanField(
        default=False,
        help_text='Organization publishes content on social platforms.',
    )

    platform_network_tv = models.BooleanField(
        default=False,
        help_text='Organization airs on network television.',
    )

    platform_cable_tv = models.BooleanField(
        default=False,
        help_text='Organization airs on cable television.',
    )

    platform_radio = models.BooleanField(
        default=False,
        help_text='Organization airs on radio.',
    )

    platform_podcast = models.BooleanField(
        default=False,
        help_text='Organization produces podcasts.',
    )

    platform_newsletter = models.BooleanField(
        default=False,
        help_text='Organization publishes newsletters.',
    )

    platform_streaming_video = models.BooleanField(
        default=False,
        help_text='Organization content airs on streaming video.',
    )

    primary_audience = models.CharField(
        max_length=255,
        blank=True,
        help_text='Is the audience geographic, topic or of a special community.'
    )

    ownership = models.CharField(
        max_length=255,
        blank=True,
        help_text='What is the ownership structure of the organization. What or who owns the organization.'
    )

    business_model = models.CharField(
        max_length=255,
        blank=True,
        help_text='What are the sources of support for the organization.'
    )

    unionized_workforce = models.CharField(
        max_length=255,
        blank=True,
        help_text='Is any part of the organization workforce unionized.'
    )

    diversity = models.TextField(
        help_text="The makeup of the organization and any programs or efforts to help ensure diversity in staffing.",
        blank=True,
    )

    special_skills = models.TextField(
        help_text="Any special skills or strengths this newsroom has.",
        blank=True,
    )

    good_partner = models.TextField(
        help_text="What about this organization makes it a good collaborative partner.",
        blank=True,
    )

    best_coverage = models.TextField(
        help_text="What coverage has this organization been involved in that the newsroom is proud of.",
        blank=True,
    )

    collab_experience = models.CharField(
        max_length=500,
        blank=True,
        help_text='Has the organization collaborated before and how often.'
    )

    class Meta:
        verbose_name = 'Organization Public Profile'
        verbose_name_plural = "Organization Public Profiles"

    objects = OrganizationPublicProfileManager()

    def __str__(self):
        return "{organization} - Public Profile".format(organization=self.organization.name)

    @property
    def description(self):
        return "{description}".format(description=self.organization.description)

    @property
    def search_title(self):
        return "{organization} - Public Profile".format(organization=self.organization.name)

    @property
    def type(self):
        return "Organization Public Profile"
