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

    name_pronunciation = models.TextField(
        help_text="Instruction on the proper pronunciation of the users name.",
        blank=True,
    )

    pronoun = models.CharField(
        max_length=50,
        help_text='Users preferred pronoun.',
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
        story_owner = self.story_owner.all()
        story_team = self.story_team_member.all()
        facet_owner = self.facetowner.all()
        # facet_team = self.team.all()
        user_content.extend(projects_owner)
        user_content.extend(projects_team)
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

    def get_user_tasks(self):
        """Return all the tasks for a user."""

        from . import Task

        tasks = Task.objects.filter(Q(owner=self) | Q(assigned_to=self))
        return tasks

    def inbox_comments(self):
        """Return list of comments from discussions the user is a participant in.

        Collects all relevant comments for a specific user to show in their
        dashboard and inbox.
        """

        from . import Comment

        user_discussion_ids = self.comment_set.all().values('discussion_id')

        return (Comment
                .objects
                .filter(discussion_id__in=user_discussion_ids)
                .exclude(user_id=self.id)
                .select_related('user', 'discussion')
                )

    def recent_comments(self):
        """Recent comments in users's discussions.

        Return list of comments:
         - from discussions the user is a participant in
         - since the user's last login
         - where the user isn't the author

        For display on primary dashboard.
        """

        # FIXME: this appear to just be a subset of inbox_comments; can this use that?

        from . import Comment

        # Discussions user is involved in
        user_discussion_ids = self.comment_set.all().values('discussion_id')

        # Comments tht
        return (Comment
                .objects
                .filter(discussion_id__in=user_discussion_ids,
                        date__gte=self.last_login)
                .exclude(user_id=self.id)
               )

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
