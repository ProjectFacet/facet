from django.db import models
from django.db.models import Q
from model_utils.models import TimeStampedModel
import time as timemk
from datetime import datetime, timedelta, time
from imagekit.models import ProcessedImageField, ImageSpecField
from django.utils.encoding import python_2_unicode_compatible
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError

from . import User, Organization, Network, Project, Series, Discussion
from . import SimpleImage, SimpleDocument, SimpleAudio, SimpleVideo
# from . import Note

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

    project = models.ForeignKey(
        Project,
        blank=True,
        null=True,
    )

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

    notes = models.ManyToManyField(
        'Note',
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
        verbose_name = 'Story'
        verbose_name_plural = "Stories"
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('story_detail', kwargs={'pk': self.id})

    def copy_story(self):
        """ Create a copy of a story for a partner organization in a network.

        Copied stories keep all attributes.

        Organization is set to the copier's organization and the original_content
        flag is set to false. Triggering a copy also triggers the creation of a
        story copy detail record.
        """

        # XXX Copied stories need to maintain attribution of team

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

        from . import User
        # FIXME add contractors added to a story
        collaborators = self.collaborate_with.all()
        story_team = User.objects.filter(Q(Q(organization=self.organization) | Q(organization__in=collaborators)))
        return story_team

    def get_story_images(self):
        """Return all the images associated with a story."""

        story_images = []
        for facet in self.facet_set.all():
            images = facet.get_facet_images()
            story_images.extend(images)
        return story_images

    def get_story_documents(self):
        """Return all documents associated with a story."""

        story_documents = []
        for facet in self.facet_set.all():
            documents = facet.get_facet_documents()
            story_documents.extend(documents)
        return story_documents

    def get_story_audio(self):
        """Return all audio associated with a story."""

        story_audio = []
        for facet in self.facet_set.all():
            audio = facet.get_facet_audio()
            story_audio.extend(audio)
        return story_audio

    def get_story_video(self):
        """ Return all video associated with a story."""

        story_video = []
        for facet in self.facet_set.all():
            video = facet.get_facet_video()
            story_video.extend(video)
        return story_video

    def get_story_facets(self):
        """Return all existing facets associated with a story."""

        return self.facet_set.all()

        # {% for facet in story.get_story_facets %}
        #    <a href="{{ facet.get_absolute_url }}">{{ facet.name }}</a>
        # {% endfor %}

    def get_story_schedule(self):
        """Return all the deadlines for the facets of a story."""

        data = []
        story = get_object_or_404(Story, pk=self.id)
        # Facet Schedules
        if story.facet_set.all():
            print "IM AT WEB"
            for facet in story.facet_set.all():
                credit = {}
                for user in facet.credit.all():
                    credit['id'] = []
                    credit['id'].append(user.credit_name)
                    credit['id'].append(user.get_absolute_url())
                editor = {}
                for user in facet.editor.all():
                    editor['id'] = []
                    editor['id'].append(user.credit_name)
                    editor['id'].append(user.get_absolute_url())
                print credit
                if facet.due_edit:
                    edit_event_dict = {}
                    edit_event_dict['id'] = facet.id
                    edit_event_dict['title'] = facet.name.encode('utf-8')
                    edit_event_dict['description'] = facet.description.encode('utf-8')
                    edit_event_dict['due-edit'] = timemk.mktime(facet.due_edit.timetuple())
                    edit_event_dict['editor'] = editor
                    edit_event_dict['credit'] = credit
                    edit_event_dict['url'] = facet.get_absolute_url()
                    edit_event_dict['start'] = timemk.mktime(facet.due_edit.timetuple()) * 1000
                    edit_event_dict['end'] = (timemk.mktime(facet.due_edit.timetuple()) * 1000) + 60
                    edit_event_dict['overlap'] = True
                    edit_event_dict['allDay'] = False
                    edit_event_dict['backgroundColor'] = '#00aced'
                    edit_event_dict['textColor'] = '#fff'
                    data.append(edit_event_dict)
                if facet.run_date:
                    run_event_dict = {}
                    run_event_dict['id'] = facet.id
                    run_event_dict['title'] = facet.name.encode('utf-8')
                    run_event_dict['description'] = facet.description.encode('utf-8')
                    run_event_dict['due-edit'] = timemk.mktime(facet.due_edit.timetuple())
                    run_event_dict['editor'] = editor
                    run_event_dict['credit'] = credit
                    run_event_dict['url'] = facet.get_absolute_url()
                    run_event_dict['class'] = 'event_run'
                    run_event_dict['start'] = timemk.mktime(facet.run_date.timetuple()) * 1000
                    run_event_dict['end'] = (timemk.mktime(facet.run_date.timetuple()) * 1000) + 60
                    run_event_dict['overlap'] = True
                    run_event_dict['backgroundColor'] = '#5cb85c'
                    run_event_dict['textColor'] = '#fff'
                    data.append(run_event_dict)

        return data

    def get_story_events(self):
        """Return all story events."""

        return self.event_set.all()


    @property
    def description(self):
        return self.story_description

    @property
    def search_title(self):
        return self.name

    @property
    def type(self):
        return "Story"
