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

from .people import User, Organization

#-----------------------------------------------------------------------#
#   People:
#   ContractorInfo, OrganizationContractorInfo
#-----------------------------------------------------------------------#


class ContractorInfo(models.Model):
    """A User who is a freelancer or contractor has a ContractorInfo
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


class OrganizationContractorInfo(models.Model):
    """Information tracked by an organization about contractors.

    Basic info like email, bio, skillset, availability, current_location, gear
    are available on ContractorInfo.

    The data captured here is intended to reflect an Organization's internal
    notes regarding a Contractor.
    """

    organization = models.ForeignKey(
        "Organization",
    )

    contractor_info = models.ForeignKey(
        "ContractorInfo",
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

    # status: Is this contractor currently in use?

    # request for running total of assignments contractor has done for an org
    # request for running total of how much an org has paid a contractor
    # request for ability to see mark assignments as paid and sort accordingly
