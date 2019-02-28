# from django.core.urlresolvers import reverse
# from django.db import models
# from django.db.models import Q
# from django.utils.encoding import python_2_unicode_compatible
# from imagekit.models import ImageSpecField
# from pilkit.processors import SmartResize
#
# from . import SimpleImage, SimpleDocument, SimpleAudio, SimpleVideo
# from . import User, Organization, Network
#
#
# #-----------------------------------------------------------------------#
# #  SERIES
# #-----------------------------------------------------------------------#
#
#
# @python_2_unicode_compatible
# class Series(models.Model):
#     """ A specific series.
#
#     Series are an organizational component for one or more stories. The primary use is
#     to connect multiple stories on a particular topic. Series are also the method for keeping
#     assets easily available to all stories/facets.
#     """
#
#     name = models.CharField(
#         max_length=75,
#         help_text='The name identifying the series.'
#     )
#
#     description = models.TextField(
#         blank=True,
#         help_text='Short description of a series.',
#     )
#
#     owner = models.ForeignKey(
#         User,
#         related_name='series_owner',
#         help_text='The user that created the series.'
#     )
#
#     organization = models.ForeignKey(
#         Organization,
#         related_name='series_organization',
#         help_text='The org'
#     )
#
#     series_logo = models.ImageField(
#         upload_to='series',
#         blank=True,
#     )
#
#     display_logo = ImageSpecField(
#         source='series_logo',
#         processors=[SmartResize(500, 500)],
#         format='JPEG',
#     )
#
#
#     team = models.ManyToManyField(
#         User,
#         related_name='series_team_member',
#         help_text='User contributing to the series.',
#         blank=True,
#     )
#
#     creation_date = models.DateTimeField(
#         auto_now_add=True,
#     )
#
#     sensitive = models.BooleanField(
#         default=False,
#         help_text='Is a series sensitive, for limited viewing?'
#     )
#
#     collaborate = models.BooleanField(
#         default=False,
#         help_text='The series is being collaborated on with a network.'
#     )
#
#     collaborate_with = models.ManyToManyField(
#         Organization,
#         related_name='series_collaborated_with_organization',
#         help_text='Organization ids that a series is open to collaboration with.',
#         blank=True,
#     )
#
#     archived = models.BooleanField(
#         default=False,
#         help_text='Is the content no longer active and needed?'
#     )
#
#     discussion = models.ForeignKey(
#         'Discussion',
#         help_text='Id of planning discussion for a series.',
#         blank=True,
#         null=True,
#     )
#
#     notes = models.ManyToManyField(
#         'Note',
#         blank=True,
#     )
#
#     # assets
#     simple_image_assets = models.ManyToManyField(
#         SimpleImage,
#         blank=True,
#     )
#
#     simple_document_assets = models.ManyToManyField(
#         SimpleDocument,
#         blank=True,
#     )
#
#     simple_audio_assets = models.ManyToManyField(
#         SimpleAudio,
#         blank=True,
#     )
#
#     simple_video_assets = models.ManyToManyField(
#         SimpleVideo,
#         blank=True,
#     )
#
#     class Meta:
#         verbose_name = 'Series'
#         verbose_name_plural = "Series"
#         ordering = ['name']
#
#     def __str__(self):
#         return self.name
#
#     def get_absolute_url(self):
#         return reverse('series_detail', kwargs={'pk': self.id})
#
#     def get_series_team(self):
#         """Return queryset with org users and users from collaboration orgs for a series."""
#
#         collaborators = self.collaborate_with.all()
#         series_team = User.objects.filter(Q(Q(organization=self.organization) | Q(organization__in=collaborators)))
#         return series_team
#
#     def get_series_images(self):
#         """Return all image assets associated with facets that are part of a series."""
#
#         from .story import Story
#
#         # get all original stories associated with a project
#         series_stories = self.story_set.filter(original_story=True).all()
#         # get all image assets associated with those stories.
#         series_images = []
#         for story in series_stories:
#             images=Story.get_story_images(story)
#             series_images.extend(images)
#         return set(series_images)
#
#     def get_series_documents(self):
#         """Return all document assets associated with facets that are part of a series."""
#
#         # get all original stories associated with a series
#         series_stories = self.story_set.filter(original_story=True).all()
#         # get all document assets associated with those stories.
#         series_documents = []
#         for story in series_stories:
#             documents=story.get_story_documents()
#             series_documents.extend(documents)
#         return set(series_documents)
#
#     def get_series_audio(self):
#         """Return all audio assets associated with facets that are part of a series."""
#
#         # get all original stories associated with a series
#         series_stories = self.story_set.filter(original_story=True).all()
#         # get all audio assets associated with those stories.
#         series_audio = []
#         for story in series_stories:
#             audio=story.get_story_audio()
#             series_audio.extend(audio)
#         return set(series_audio)
#
#     def get_series_video(self):
#         """Return all video assets associated with facets that are part of a series."""
#
#         # get all original stories associated with a series
#         series_stories = self.story_set.filter(original_story=True).all()
#
#         # get all video assets associated with those stories.
#         series_video = []
#
#         for story in series_stories:
#             videos=story.get_story_video()
#             series_video.extend(videos)
#
#         return set(series_video)
#
#     def get_series_event_schedule(self):
#         """Return series events for a series.
#
#         Used for returning a single series' event schedule.
#         """
#
#         data = []
#
#         series = Series.objects.get(pk=self.id)
#
#         # gather schedule dates for all series events
#         if series.event_set.all():
#             for event in series.event_set.filter(event_type="Hosting"):
#                 hosting_event_dict = {}
#
#                 item_date = event.event_date
#
#                 hosting_event_dict['id'] = event.id
#                 hosting_event_dict['title'] = event.name
#                 hosting_event_dict['event_date'] = item_date.isoformat()
#                 hosting_event_dict['url'] = event.get_absolute_url()
#                 hosting_event_dict['start'] = item_date.isoformat()
#                 hosting_event_dict['end'] = item_date.isoformat()
#                 hosting_event_dict['overlap'] = True
#                 hosting_event_dict['all_day'] = False
#                 hosting_event_dict['backgroundColor'] = '#3F51B5'
#                 hosting_event_dict['textColor'] = 'fff'
#                 hosting_event_dict['class'] = "calevent"
#
#                 data.append(hosting_event_dict)
#
#             for event in series.event_set.filter(event_type="Reporting"):
#                 reporting_event_dict = {}
#
#                 item_date = event.event_date
#
#                 reporting_event_dict['id'] = event.id
#                 reporting_event_dict['title'] = event.name
#                 reporting_event_dict['event_date'] = item_date.isoformat()
#                 reporting_event_dict['url'] = event.get_absolute_url()
#                 reporting_event_dict['start'] = item_date.isoformat()
#                 reporting_event_dict['end'] = item_date.isoformat()
#                 reporting_event_dict['overlap'] = True
#                 reporting_event_dict['all_day'] = False
#                 reporting_event_dict['backgroundColor'] = '#2196F3'
#                 reporting_event_dict['textColor'] = 'fff'
#                 reporting_event_dict['class'] = "calevent"
#
#                 data.append(reporting_event_dict)
#
#             for event in series.event_set.filter(event_type="Administrative"):
#                 administrative_event_dict = {}
#
#                 item_date = event.event_date
#
#                 administrative_event_dict['id'] = event.id
#                 administrative_event_dict['title'] = event.name
#                 administrative_event_dict['event_date'] = item_date.isoformat()
#                 administrative_event_dict['url'] = event.get_absolute_url()
#                 administrative_event_dict['start'] = item_date.isoformat()
#                 administrative_event_dict['end'] = item_date.isoformat()
#                 administrative_event_dict['overlap'] = True
#                 administrative_event_dict['all_day'] = False
#                 administrative_event_dict['backgroundColor'] = '#03A9F4'
#                 administrative_event_dict['textColor'] = 'fff'
#                 administrative_event_dict['class'] = "calevent"
#
#                 data.append(administrative_event_dict)
#
#             for event in series.event_set.filter(event_type="Other"):
#                 other_event_dict = {}
#
#                 item_date = event.event_date
#
#                 other_event_dict['id'] = event.id
#                 other_event_dict['title'] = event.name
#                 other_event_dict['event_date'] = item_date.isoformat()
#                 other_event_dict['url'] = event.get_absolute_url()
#                 other_event_dict['start'] = item_date.isoformat()
#                 other_event_dict['end'] = item_date.isoformat()
#                 other_event_dict['overlap'] = True
#                 other_event_dict['all_day'] = False
#                 other_event_dict['backgroundColor'] = '#00BCD4'
#                 other_event_dict['textColor'] = 'fff'
#                 other_event_dict['class'] = "calevent"
#
#                 data.append(other_event_dict)
#
#         return data
#
#     def get_series_schedule(self):
#         """Return all the relevant dates for a series.
#         Used for returning a single series's schedule.
#
#         Includes:
#         From story:
#             story_share_date
#             facet due_edit
#             facet run_date
#         From series:
#             event event_date
#             task due_date
#         """
#
#         data = []
#
#         series = Series.objects.get(pk=self.id)
#
#         # gather dates for story sharing and story facets for a series
#         if series.story_set:
#             for story in series.story_set.all():
#                 single_story_dates = story.get_story_facets_schedule()
#                 data.extend(single_story_dates)
#
#         # gather schedule dates for all story events
#         if series.event_set.all():
#             for event in series.event_set.filter(event_type="Hosting"):
#                 hosting_event_dict = {}
#
#                 item_date = event.event_date
#
#                 hosting_event_dict['id'] = event.id
#                 hosting_event_dict['title'] = event.name
#                 hosting_event_dict['event_date'] = item_date.isoformat()
#                 hosting_event_dict['url'] = event.get_absolute_url()
#                 hosting_event_dict['start'] = item_date.isoformat()
#                 hosting_event_dict['end'] = item_date.isoformat()
#                 hosting_event_dict['overlap'] = True
#                 hosting_event_dict['all_day'] = False
#                 hosting_event_dict['backgroundColor'] = '#3F51B5'
#                 hosting_event_dict['textColor'] = 'fff'
#                 hosting_event_dict['class'] = "calevent"
#
#                 data.append(hosting_event_dict)
#
#             for event in series.event_set.filter(event_type="Reporting"):
#                 reporting_event_dict = {}
#
#                 item_date = event.event_date
#
#                 reporting_event_dict['id'] = event.id
#                 reporting_event_dict['title'] = event.name
#                 reporting_event_dict['event_date'] = item_date.isoformat()
#                 reporting_event_dict['url'] = event.get_absolute_url()
#                 reporting_event_dict['start'] = item_date.isoformat()
#                 reporting_event_dict['end'] = item_date.isoformat()
#                 reporting_event_dict['overlap'] = True
#                 reporting_event_dict['all_day'] = False
#                 reporting_event_dict['backgroundColor'] = '#2196F3'
#                 reporting_event_dict['textColor'] = 'fff'
#                 reporting_event_dict['class'] = "calevent"
#
#                 data.append(reporting_event_dict)
#
#             for event in series.event_set.filter(event_type="Administrative"):
#                 administrative_event_dict = {}
#
#                 item_date = event.event_date
#
#                 administrative_event_dict['id'] = event.id
#                 administrative_event_dict['title'] = event.name
#                 administrative_event_dict['event_date'] = item_date.isoformat()
#                 administrative_event_dict['url'] = event.get_absolute_url()
#                 administrative_event_dict['start'] = item_date.isoformat()
#                 administrative_event_dict['end'] = item_date.isoformat()
#                 administrative_event_dict['overlap'] = True
#                 administrative_event_dict['all_day'] = False
#                 administrative_event_dict['backgroundColor'] = '#03A9F4'
#                 administrative_event_dict['textColor'] = 'fff'
#                 administrative_event_dict['class'] = "calevent"
#
#                 data.append(administrative_event_dict)
#
#             for event in series.event_set.filter(event_type="Other"):
#                 other_event_dict = {}
#
#                 item_date = event.event_date
#
#                 other_event_dict['id'] = event.id
#                 other_event_dict['title'] = event.name
#                 other_event_dict['event_date'] = item_date.isoformat()
#                 other_event_dict['url'] = event.get_absolute_url()
#                 other_event_dict['start'] = item_date.isoformat()
#                 other_event_dict['end'] = item_date.isoformat()
#                 other_event_dict['overlap'] = True
#                 other_event_dict['all_day'] = False
#                 other_event_dict['backgroundColor'] = '#00BCD4'
#                 other_event_dict['textColor'] = 'fff'
#                 other_event_dict['class'] = "calevent"
#
#                 data.append(other_event_dict)
#
#         # gather schedule dates for all story tasks
#         if series.task_set.all():
#             for task in series.task_set.all():
#                 task_event_dict = {}
#
#                 item_date = task.due_date
#
#                 task_event_dict['id'] = task.id
#                 task_event_dict['title'] = task.name
#                 task_event_dict['due_date'] = item_date.isoformat()
#                 task_event_dict['url'] = task.get_absolute_url()
#                 task_event_dict['start'] = item_date.isoformat()
#                 task_event_dict['end'] = item_date.isoformat()
#                 task_event_dict['overlap'] = True
#                 task_event_dict['all_day'] = False
#                 task_event_dict['backgroundColor'] = '#7E57C2'
#                 task_event_dict['textColor'] = 'fff'
#                 task_event_dict['class'] = "calevent"
#
#                 data.append(task_event_dict)
#
#         return data
#
# 
#     @property
#     def search_title(self):
#         return self.name
#
#     @property
#     def type(self):
#         return "Series"
