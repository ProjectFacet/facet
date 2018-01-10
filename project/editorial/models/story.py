import time as timemk

from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.utils.encoding import python_2_unicode_compatible
from datetime import datetime
import time

from . import SimpleImage, SimpleDocument, SimpleAudio, SimpleVideo
from . import User, Organization, Network, Project, Series, Discussion


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
        """Return rst formatted string for downloading story meta."""

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
        # TODO future: add contractors added to a story
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

    def get_story_facets_schedule(self):
        """Return deadlines of a story and its facets.
        Used for inclusion with project and series schedules.

        Includes:
        story_share_date
        facet due_edit
        facet run_date
        """

        data = []

        story = Story.objects.get(pk=self.id)

        # gather story dates for stories to be shared
        if story.share_with_date:
            shared_story_dict = {}

            item_date = story.share_with_date

            shared_story_dict['id'] = story.id
            shared_story_dict['title'] = story.name
            shared_story_dict['share_with_date'] = item_date.isoformat()
            shared_story_dict['url'] = story.get_absolute_url()
            shared_story_dict['start'] = item_date.isoformat()
            shared_story_dict['end'] = item_date.isoformat()
            shared_story_dict['overlap'] = True
            shared_story_dict['all_day'] = False
            shared_story_dict['backgroundColor'] = '#F44336'
            shared_story_dict['textColor'] = 'fff'
            shared_story_dict['class'] = "calevent"

            data.append(shared_story_dict)

        # gather schedule dates for all story facets
        if story.facet_set.all():
            for facet in story.facet_set.all():
                if facet.due_edit:
                    facet_edit_dict = {}

                    item_date = facet.due_edit

                    facet_edit_dict['id'] = facet.id
                    facet_edit_dict['title'] = facet.name
                    facet_edit_dict['due_edit'] = item_date.isoformat()
                    facet_edit_dict['url'] = facet.get_absolute_url()
                    facet_edit_dict['start'] = item_date.isoformat()
                    facet_edit_dict['end'] = item_date.isoformat()
                    facet_edit_dict['overlap'] = True
                    facet_edit_dict['all_day'] = False
                    facet_edit_dict['backgroundColor'] = '#FFA000'
                    facet_edit_dict['textColor'] = 'fff'
                    facet_edit_dict['class'] = "calevent"

                    data.append(facet_edit_dict)

                if facet.run_date:
                    facet_run_dict = {}

                    item_date = facet.run_date

                    facet_run_dict['id'] = facet.id
                    facet_run_dict['title'] = facet.name
                    facet_run_dict['run_date'] = item_date.isoformat()
                    facet_run_dict['url'] = facet.get_absolute_url()
                    facet_run_dict['start'] = item_date.isoformat()
                    facet_run_dict['end'] = item_date.isoformat()
                    facet_run_dict['overlap'] = True
                    facet_run_dict['all_day'] = False
                    facet_run_dict['backgroundColor'] = '#7CB342'
                    facet_run_dict['textColor'] = 'fff'
                    facet_run_dict['class'] = "calevent"

                    data.append(facet_run_dict)

        return data

    def get_story_event_schedule(self):
        """Return story events for a story.

        Used for returning a single story's event schedule.
        """

        data = []

        story = Story.objects.get(pk=self.id)

        # gather schedule dates for all story events
        if story.event_set.all():
            for event in story.event_set.filter(event_type="Hosting"):
                hosting_event_dict = {}

                item_date = event.event_date

                hosting_event_dict['id'] = event.id
                hosting_event_dict['title'] = event.name
                hosting_event_dict['event_date'] = item_date.isoformat()
                hosting_event_dict['url'] = event.get_absolute_url()
                hosting_event_dict['start'] = item_date.isoformat()
                hosting_event_dict['end'] = item_date.isoformat()
                hosting_event_dict['overlap'] = True
                hosting_event_dict['all_day'] = False
                hosting_event_dict['backgroundColor'] = '#3F51B5'
                hosting_event_dict['textColor'] = 'fff'
                hosting_event_dict['class'] = "calevent"

                data.append(hosting_event_dict)

            for event in story.event_set.filter(event_type="Reporting"):
                reporting_event_dict = {}

                item_date = event.event_date

                reporting_event_dict['id'] = event.id
                reporting_event_dict['title'] = event.name
                reporting_event_dict['event_date'] = item_date.isoformat()
                reporting_event_dict['url'] = event.get_absolute_url()
                reporting_event_dict['start'] = item_date.isoformat()
                reporting_event_dict['end'] = item_date.isoformat()
                reporting_event_dict['overlap'] = True
                reporting_event_dict['all_day'] = False
                reporting_event_dict['backgroundColor'] = '#2196F3'
                reporting_event_dict['textColor'] = 'fff'
                reporting_event_dict['class'] = "calevent"

                data.append(reporting_event_dict)

            for event in story.event_set.filter(event_type="Administrative"):
                administrative_event_dict = {}

                item_date = event.event_date

                administrative_event_dict['id'] = event.id
                administrative_event_dict['title'] = event.name
                administrative_event_dict['event_date'] = item_date.isoformat()
                administrative_event_dict['url'] = event.get_absolute_url()
                administrative_event_dict['start'] = item_date.isoformat()
                administrative_event_dict['end'] = item_date.isoformat()
                administrative_event_dict['overlap'] = True
                administrative_event_dict['all_day'] = False
                administrative_event_dict['backgroundColor'] = '#03A9F4'
                administrative_event_dict['textColor'] = 'fff'
                administrative_event_dict['class'] = "calevent"

                data.append(administrative_event_dict)

            for event in story.event_set.filter(event_type="Other"):
                other_event_dict = {}

                item_date = event.event_date

                other_event_dict['id'] = event.id
                other_event_dict['title'] = event.name
                other_event_dict['event_date'] = item_date.isoformat()
                other_event_dict['url'] = event.get_absolute_url()
                other_event_dict['start'] = item_date.isoformat()
                other_event_dict['end'] = item_date.isoformat()
                other_event_dict['overlap'] = True
                other_event_dict['all_day'] = False
                other_event_dict['backgroundColor'] = '#00BCD4'
                other_event_dict['textColor'] = 'fff'
                other_event_dict['class'] = "calevent"

                data.append(other_event_dict)

        return data

    def get_story_schedule(self):
        """Return all the relevant dates for a story.
        Used for returning a single story's schedule.

        Includes:
        story_share_date
        facet due_edit
        facet run_date
        event event_date
        task due_date
        """

        data = []

        story = Story.objects.get(pk=self.id)

        # gather story dates for stories to be shared
        if story.share_with_date:
            shared_story_dict = {}

            item_date = story.share_with_date

            shared_story_dict['id'] = story.id
            shared_story_dict['title'] = story.name
            shared_story_dict['share_with_date'] = item_date.isoformat()
            shared_story_dict['url'] = story.get_absolute_url()
            shared_story_dict['start'] = item_date.isoformat()
            shared_story_dict['end'] = item_date.isoformat()
            shared_story_dict['overlap'] = True
            shared_story_dict['all_day'] = False
            shared_story_dict['backgroundColor'] = '#F44336'
            shared_story_dict['textColor'] = 'fff'
            shared_story_dict['class'] = "calevent"

            data.append(shared_story_dict)

        # gather schedule dates for all story facets
        if story.facet_set.all():
            for facet in story.facet_set.all():
                if facet.due_edit:
                    facet_edit_dict = {}

                    item_date = facet.due_edit

                    facet_edit_dict['id'] = facet.id
                    facet_edit_dict['title'] = facet.name
                    facet_edit_dict['due_edit'] = item_date.isoformat()
                    facet_edit_dict['url'] = facet.get_absolute_url()
                    facet_edit_dict['start'] = item_date.isoformat()
                    facet_edit_dict['end'] = item_date.isoformat()
                    facet_edit_dict['overlap'] = True
                    facet_edit_dict['all_day'] = False
                    facet_edit_dict['backgroundColor'] = '#FFA000'
                    facet_edit_dict['textColor'] = 'fff'
                    facet_edit_dict['class'] = "calevent"

                    data.append(facet_edit_dict)

                if facet.run_date:
                    facet_run_dict = {}

                    item_date = facet.run_date

                    facet_run_dict['id'] = facet.id
                    facet_run_dict['title'] = facet.name
                    facet_run_dict['run_date'] = item_date.isoformat()
                    facet_run_dict['url'] = facet.get_absolute_url()
                    facet_run_dict['start'] = item_date.isoformat()
                    facet_run_dict['end'] = item_date.isoformat()
                    facet_run_dict['overlap'] = True
                    facet_run_dict['all_day'] = False
                    facet_run_dict['backgroundColor'] = '#7CB342'
                    facet_run_dict['textColor'] = 'fff'
                    facet_run_dict['class'] = "calevent"

                    data.append(facet_run_dict)

        # gather schedule dates for all story events
        if story.event_set.all():
            for event in story.event_set.filter(event_type="Hosting"):
                hosting_event_dict = {}

                item_date = event.event_date

                hosting_event_dict['id'] = event.id
                hosting_event_dict['title'] = event.name
                hosting_event_dict['event_date'] = item_date.isoformat()
                hosting_event_dict['url'] = event.get_absolute_url()
                hosting_event_dict['start'] = item_date.isoformat()
                hosting_event_dict['end'] = item_date.isoformat()
                hosting_event_dict['overlap'] = True
                hosting_event_dict['all_day'] = False
                hosting_event_dict['backgroundColor'] = '#3F51B5'
                hosting_event_dict['textColor'] = 'fff'
                hosting_event_dict['class'] = "calevent"

                data.append(hosting_event_dict)

            for event in story.event_set.filter(event_type="Reporting"):
                reporting_event_dict = {}

                item_date = event.event_date

                reporting_event_dict['id'] = event.id
                reporting_event_dict['title'] = event.name
                reporting_event_dict['event_date'] = item_date.isoformat()
                reporting_event_dict['url'] = event.get_absolute_url()
                reporting_event_dict['start'] = item_date.isoformat()
                reporting_event_dict['end'] = item_date.isoformat()
                reporting_event_dict['overlap'] = True
                reporting_event_dict['all_day'] = False
                reporting_event_dict['backgroundColor'] = '#2196F3'
                reporting_event_dict['textColor'] = 'fff'
                reporting_event_dict['class'] = "calevent"

                data.append(reporting_event_dict)

            for event in story.event_set.filter(event_type="Administrative"):
                administrative_event_dict = {}

                item_date = event.event_date

                administrative_event_dict['id'] = event.id
                administrative_event_dict['title'] = event.name
                administrative_event_dict['event_date'] = item_date.isoformat()
                administrative_event_dict['url'] = event.get_absolute_url()
                administrative_event_dict['start'] = item_date.isoformat()
                administrative_event_dict['end'] = item_date.isoformat()
                administrative_event_dict['overlap'] = True
                administrative_event_dict['all_day'] = False
                administrative_event_dict['backgroundColor'] = '#03A9F4'
                administrative_event_dict['textColor'] = 'fff'
                administrative_event_dict['class'] = "calevent"

                data.append(administrative_event_dict)

            for event in story.event_set.filter(event_type="Other"):
                other_event_dict = {}

                item_date = event.event_date

                other_event_dict['id'] = event.id
                other_event_dict['title'] = event.name
                other_event_dict['event_date'] = item_date.isoformat()
                other_event_dict['url'] = event.get_absolute_url()
                other_event_dict['start'] = item_date.isoformat()
                other_event_dict['end'] = item_date.isoformat()
                other_event_dict['overlap'] = True
                other_event_dict['all_day'] = False
                other_event_dict['backgroundColor'] = '#00BCD4'
                other_event_dict['textColor'] = 'fff'
                other_event_dict['class'] = "calevent"

                data.append(other_event_dict)

        # gather schedule dates for all story tasks
        if story.task_set.all():
            for task in story.task_set.all():
                task_event_dict = {}

                item_date = task.due_date

                task_event_dict['id'] = task.id
                task_event_dict['title'] = task.name
                task_event_dict['due_date'] = item_date.isoformat()
                task_event_dict['url'] = task.get_absolute_url()
                task_event_dict['start'] = item_date.isoformat()
                task_event_dict['end'] = item_date.isoformat()
                task_event_dict['overlap'] = True
                task_event_dict['all_day'] = False
                task_event_dict['backgroundColor'] = '#7E57C2'
                task_event_dict['textColor'] = 'fff'
                task_event_dict['class'] = "calevent"

                data.append(task_event_dict)

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

    def is_editable_by_org(self, org):
        """Can this story be edited by this org?"""

        # FIXME: add contractor access?

        return (org == self.organization or
             (self.collaborate and org in self.collaborate_with.all()))
