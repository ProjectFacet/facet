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
from .organization import Organization


class OrganizationSubscriptionManager(models.Manager):
    """Custom manager for Subscription."""

    def create_subscription(self, organization, collaborations, contractors):
        """Method for quick creation of subscription."""

        subscription = self.create(
                        organization=organization,
                        collaborations=collaborations,
                        contractors=contractors,
                        partner_discovery=partner_discovery,
                        )
        return subscription


@python_2_unicode_compatible
class OrganizationSubscription(models.Model):
    """Details of an organization subscription."""

    # if subscription is for an org account, associate with that org
    # FIXME should be a one to one relationship
    organization = models.OneToOneField(
        Organization,
        help_text='Organization associated with this subscription if Org subscription type.',
        on_delete=models.CASCADE,
    )

    # Organization functionality
    collaborations = models.BooleanField(
        default=False,
        help_text='The organization is using the account for base features of editorial workflow, project management and collaboration.',
    )

    contractors = models.BooleanField(
        default=False,
        help_text='The organization is using the account to manage contractors.',
    )

    partner_discovery = models.BooleanField(
        default=True,
        help_text='Base level subscription. Allows organization to be publicly listed for search as a potential collaborative partner. Allows org users to see other publicly listed orgs.',
    )

    objects = OrganizationSubscriptionManager()

    def __str__(self):
        return "Organization Subscription - {organization}".format(organization=self.organization.name)


class ContractorSubscriptionManager(models.Manager):
    """Custom manager for contractor subscription."""

    def create_subscription(self, user, standard):
        """Method for quick creation of subscription."""

        subscription = self.create(
                        user=user,
                        standard=standard,
                        )

        return subscription


@python_2_unicode_compatible
class ContractorSubscription(models.Model):
    """Details of a contractor subscription.

    V1.0 limited utility but future-facing necessity.

    """

    # if subscription is for an org account, associate with that org
    user = models.ForeignKey(
        User,
        help_text='User associated with this subscription.',
        on_delete=models.CASCADE,
    )

    # Organization functionality
    standard = models.BooleanField(
        default=True,
        help_text='If an organization is using the account for base features of editorial workflow, project management and collaboration.',
    )

    objects = ContractorSubscriptionManager()

    def __str__(self):
        return "Contractor Subscription - {user}".format(user=self.user.credit_name)
