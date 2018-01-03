from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import Q
from django.utils.encoding import python_2_unicode_compatible
from imagekit.models import ImageSpecField
from pilkit.processors import SmartResize

from . import SimpleImage, SimpleDocument, SimpleAudio, SimpleVideo
from . import User, Organization, Network


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

    notes = models.ManyToManyField(
        'Note',
        blank=True,
    )

    # project site if different than organization
    website = models.URLField(
        max_length=250,
        blank=True,
    )

    # assets
    simple_image_assets = models.ManyToManyField(
        SimpleImage,
        blank=True,
    )

    simple_document_assets = models.ManyToManyField(
        SimpleDocument,
        blank=True,
    )

    simple_audio_assets = models.ManyToManyField(
        SimpleAudio,
        blank=True,
    )

    simple_video_assets = models.ManyToManyField(
        SimpleVideo,
        blank=True,
    )


    class Meta:
        verbose_name = 'Project'
        verbose_name_plural = "Projects"
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('project_detail', kwargs={'pk': self.id})

    def get_project_team_vocab(self):
        """Return queryset with org users and users from collaboration orgs for a project."""

        collaborators = self.collaborate_with.all()
        project_team = User.objects.filter(Q(Q(organization=self.organization) | Q(organization__in=collaborators)))
        return project_team

    def get_project_images(self):
        """Return all image assets associated with facets that are part of a project."""

        from .story import Story

        # get all stories associated with a project
        project_stories = self.story_set.all()
        # get all image assets associated with those stories.
        project_images = []
        for story in project_stories:
            images=Story.get_story_images(story)
            project_images.extend(images)
        return set(project_images)

    def get_project_documents(self):
        """Return all document assets associated with facets that are part of a project."""

        # get all stories associated with a project
        project_stories = self.story_set.all()
        # get all document assets associated with those stories.
        project_documents = []
        for story in project_stories:
            documents=story.get_story_documents()
            project_documents.extend(documents)
        return set(project_documents)

    def get_project_audio(self):
        """Return all audio assets associated with facets that are part of a project."""

        # get all stories associated with a project
        project_stories = self.story_set.all()
        # get all audio assets associated with those stories.
        project_audio = []
        for story in project_stories:
            audio=story.get_story_audio()
            project_audio.extend(audio)
        return set(project_audio)

    def get_project_video(self):
        """Return all video assets associated with facets that are part of a project."""

        # get all stories associated with a project
        project_stories = self.story_set.all()
        # get all video assets associated with those stories.
        project_video = []
        for story in project_stories:
            videos=story.get_story_video()
            project_video.extend(videos)
        return set(project_video)

    def get_project_tasks(self):
        """Return all tasks associated with a project."""
        return self.task_set.all()

    def get_project_stories(self):
        """Return all stories associated with a project."""
        return self.story_set.all()

    def get_project_story_events(self):
        """Return all story events associated with a project."""
        return self.event_set.all()

    def get_project_event(self):
        """Return all events and story dates associated with a project."""

        # get all Event object events
        events = self.event_set.all()
        # get all stories
        return events

    @property
    def description(self):
        return "{description}".format(description=self.project_description)

    @property
    def search_title(self):
        return self.name

    @property
    def type(self):
        return "Project"
