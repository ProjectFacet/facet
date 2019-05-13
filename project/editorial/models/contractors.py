from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import Q
from django.utils.encoding import python_2_unicode_compatible

from .assets import SimpleImage, SimpleAudio, SimpleVideo, SimpleDocument
from .facets import Facet
from .user import User
from .organization import Organization
from .story import Story


#-----------------------------------------------------------------------#
#   People:
#   ContractorInfo, OrganizationContractorInfo
#-----------------------------------------------------------------------#


class ContractorProfile(models.Model):
    """A User who is a freelancer or contractor has a ContractorProfile
    record on Facet.

    ContractorInfo tracks additional information about the user as a
    contractor.
    """

    # user account created for the contractor
    user = models.OneToOneField(
        User,
    )

    resume = models.FileField(
        upload_to='resumes/%Y/%m/%d',
        blank=True,
        null=True,
        help_text='PDF of contractor resume.',
    )

    address = models.TextField(
        blank=True,
        help_text='Mailing address.',
    )

    availability = models.TextField(
        help_text="Notes on when a contractor is available or not.",
        blank=True,
    )

    # differs from user.location
    # user.location is intended as general base. ie. San Francisco
    # current_location is intended for finding contractors that are near
    # a newsworthy thing. ie. "Berkely Campus" during a protest
    current_location = models.TextField(
        help_text="Contractor's specific location.",
        blank=True,
    )

    gear = models.TextField(
        help_text="Gear that a contractor has access to and skills for.",
        blank=True,
    )

    # contractors will appear in public search results for contractors accepting work
    public = models.BooleanField(
        default=True,
        help_text='Is the contractor publicly listed?',
    )

    portfolio_link1 = models.URLField(
        max_length=500,
        help_text='Link to portfolio item.',
        blank=True,
        null=True,
    )

    portfolio_link2 = models.URLField(
        max_length=500,
        help_text='Link to portfolio item.',
        blank=True,
        null=True,
    )

    portfolio_link3 = models.URLField(
        max_length=500,
        help_text='Link to portfolio item.',
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.user.credit_name


    def get_active_assignments(self):
        """Return all active assignment."""
        return self.assignment_set.filter(complete=False)


    def get_active_pitches(self):
        """Return all active assignment."""
        return self.pitch_set.filter(Q(status="Pitched")|Q(status="Accepted"))


    @property
    def search_title(self):
        return self.user.credit_name

    @property
    def description(self):
        return "{user}, {title}".format(
                                        user=self.user.credit_name,
                                        title="Contractor",
                                        )

    @property
    def type(self):
        return "Contractor"

    def get_absolute_url(self):
        return reverse('contractor_detail', kwargs={'pk': self.id})


class OrganizationContractorAffiliation(models.Model):
    """Information tracked by an organization about contractors.

    Basic info like email, bio, skillset, availability, current_location, gear
    are available on ContractorInfo.

    The data captured here is intended to reflect an Organization's internal
    notes regarding a Contractor.
    """

    organization = models.ForeignKey(
        "Organization",
    )

    contractor = models.ForeignKey(
        "ContractorProfile",
    )

    w9_on_file = models.BooleanField(
        default=False,
        help_text='Does the organization have a W9 on file.',
    )

    rates = models.TextField(
        blank=True,
        help_text='The rates the contractor is paid by the org.',
    )

    strengths = models.TextField(
        blank=True,
        help_text='Internal notes on strengths of the contractor.',
    )

    conflicts = models.TextField(
        blank=True,
        help_text='Any conflicts of interest the contractor has.',
    )

    editor_notes = models.TextField(
        blank=True,
        help_text='Any notes for editors on things to know when working with this contractor.',
    )

    # a contractor in an organizations contractor pool can be available
    # for assigning to projects, stories, and tasks through the regular team picker.
    talent_pool = models.BooleanField(
        default=False,
        help_text='Is this contractor a trusted regular?',
    )

    status = models.BooleanField(
        default=True,
        help_text='Is this contractor currently working for the organization?'
    )

    # request for running total of assignments contractor has done for an org
    # request for running total of how much an org has paid a contractor
    # request for ability to see mark assignments as paid and sort accordingly

    def __str__(self):
        return "{organization} - {contractor}".format(
                                        organization=self.organization.name,
                                        contractor=self.contractor.user.credit_name,
                                        )

    @property
    def search_title(self):
        return "{organization} - {contractor}".format(
                                        organization=self.organization.name,
                                        contractor=self.contractor.user.credit_name,
                                        )

    @property
    def description(self):
        return "Organization, Contractor Relationship Detail"

    @property
    def type(self):
        return "Organization, Contractor Relationship Detail"

    def get_absolute_url(self):
        return reverse('affiliation_detail', kwargs={'pk': self.id})


class TalentEditorProfile(models.Model):
    """A team user who manages contract talent."""

    # team user account associated with talent editor profile
    user = models.OneToOneField(
        User,
    )

    # relevant for editors and admins of organizations managing contractors
    # user will appear in public search results for editors accepting contact
    # from contractors
    # contractor related views sorted by this profile
    public = models.BooleanField(
        default=False,
        help_text='Is this talent editor publicly listed?',
    )

    def __str__(self):
        return self.user.credit_name

    @property
    def search_title(self):
        return self.user.credit_name

    @property
    def description(self):
        return "Talent Editor - {user}/{org}".format(
                                                    user=self.user.credit_name,
                                                    org=self.user.organization,
                                                    )

    @property
    def type(self):
        return "Talent Editor"

    def get_absolute_url(self):
        return reverse('talent_editor_detail', kwargs={'pk': self.id})


class Call(models.Model):
    """Calls are requests from editors/organizations for pitches.

    They contain details for what pitches they are requesting.
    """

    owner = models.ForeignKey(
        TalentEditorProfile,
        help_text='Editor that owns this call.'
    )

    organization = models.ForeignKey(
        Organization,
        help_text='Organization that is making this call.'
    )

    name = models.CharField(
        max_length=50,
        help_text='Title of the call.',
    )

    text = models.TextField(
        help_text='Text of the call.',
    )

    creation_date = models.DateTimeField(
        auto_now_add=True,
        help_text='Day/Time call was created.',
        blank=True,
    )

    # optional expiration date for call
    # at this point is_active will set to false automatically
    expiration_date = models.DateTimeField(
        help_text='Day/Time call ends.',
        blank=True,
        null=True,
    )

    is_active = models.BooleanField(
        default=True,
        help_text='Is this call active?'
    )

    urgent = models.BooleanField(
        default=False,
        help_text='Is this call urgent?'
    )

    timeframe = models.CharField(
        max_length=100,
        help_text='What is the timeframe for responses?',
        blank=True,
        null=True,
    )

    DRAFT = 'Draft'
    PUBLISHED = 'Published'
    COMPLETE = 'Complete'

    CALL_STATUS_CHOICES = (
        (DRAFT, 'Draft'),
        (PUBLISHED, 'Published'),
        (COMPLETE, 'Complete'),
    )

    # internal draft management. Only published calls are visible
    # to contractors.
    # status is determined by user that owns the call.
    status = models.CharField(
        max_length=25,
        choices=CALL_STATUS_CHOICES,
        help_text='Pitch status choice.'
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

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('call_detail', kwargs={'pk': self.id})

    @property
    def search_title(self):
        return self.name

    @property
    def type(self):
        return "Call"

    @property
    def description(self):
        return self.text


class Pitch(models.Model):
    """ Pitches for content from a contractor to an Organization."""

    contractor = models.ForeignKey(
        ContractorProfile,
    )

    recipient = models.ForeignKey(
        TalentEditorProfile,
        help_text='To whom is this pitch directed?'
    )

    name = models.TextField(
        help_text='Title of the pitch.',
    )

    text = models.TextField(
        help_text='Text of the pitch.',
    )

    creation_date = models.DateTimeField(
        auto_now_add=True,
        help_text='Day pitch was created.',
        blank=True,
    )

    DRAFT = 'Draft'
    PITCHED = 'Pitched'
    ACCEPTED = 'Accepted'
    COMPLETE = 'Complete'

    PITCH_STATUS_CHOICES = (
        (DRAFT, 'Draft'),
        (PITCHED, 'Pitched'),
        (ACCEPTED, 'Accepted'),
        (COMPLETE, 'Complete'),
    )

    #status is determined by contributor that owns the pitch
    status = models.CharField(
        max_length=25,
        choices=PITCH_STATUS_CHOICES,
        help_text='Pitch status choice.'
    )

    exclusive = models.BooleanField(
        default=False,
        help_text='Is this pitch for an assignment exclusive to the recipient?',
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

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Pitch'
        verbose_name_plural = 'Pitches'

    @property
    def search_title(self):
        return self.name

    @property
    def description(self):
        return self.text

    def get_absolute_url(self):
        return reverse('pitch_edit', kwargs={'pk': self.id})

    @property
    def type(self):
        return "Pitch"


class Assignment(models.Model):
    """The details of an assignment to a contractor from an organization."""

    contractor = models.ForeignKey(
        ContractorProfile,
    )

    editor = models.ForeignKey(
        TalentEditorProfile,
        help_text='Editor responsible for this assignment.',
    )

    organization = models.ForeignKey(
        Organization,
        help_text='Organization that owns this assignment.',
    )

    name = models.TextField(
        help_text='Name of the assignment.',
    )

    text = models.TextField(
        help_text='Details of the assignment.',
    )

    creation_date = models.DateTimeField(
        auto_now_add=True,
        help_text='Day assignment was created.',
        blank=True,
    )

    rate = models.CharField(
        max_length=100,
        help_text='Rate at which the assignment is being completed.',
    )

    # An assignment can be connected to a story, giving the contractor access
    # to all details of the story.
    # OR an assignment can be connected to a specific facet, giving the contractor
    # access to only that facet of the story.
    # The story or facet could be an existing one or newly created through the assignment.
    story = models.ForeignKey(
        Story,
        blank=True,
        null=True,
        help_text='Which story is this assignment related to?',
    )

    facet = models.ForeignKey(
        Facet,
        blank=True,
        null=True,
        help_text='Which facet is this assignment related to?',
    )

    call = models.ManyToManyField(
        Call,
        blank=True,
        help_text='If this assignment is related to a call, which one?',
    )

    pitch = models.ForeignKey(
        Pitch,
        blank=True,
        null=True,
        help_text='If this assignment is related to a pitch, which one?',
    )

    complete = models.BooleanField(
        default=False,
        help_text='Is the assignment complete?',
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

    @property
    def search_title(self):
        return self.name

    @property
    def description(self):
        return self.text

    @property
    def type(self):
        return "Assignment"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('assignment_detail', kwargs={'pk': self.id})
