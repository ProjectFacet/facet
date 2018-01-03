"""Account management views for editorial app."""

# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from braces.views import LoginRequiredMixin
from django.views.generic import TemplateView, UpdateView
from editorial.forms import (
    OrganizationSubscriptionForm,
    ContractorSubscriptionForm,
)
from editorial.models import (
    OrganizationSubscription,
    ContractorSubscription,
)


class AccountSelectionView(LoginRequiredMixin, TemplateView):
    """View for selecting account type.

    After user signup, the user is directed to account selection to
    choose between creating an organization with a team account or a
    contractor profile for an independent account.
    """

    template_name = 'editorial/account_selection.html'


# ACCESS: Only org admins should be able to update and org's subscription
class OrganizationSubscriptionUpdateView(LoginRequiredMixin, UpdateView):
    """View for editing organization subscription details."""

    model = OrganizationSubscription
    form_class = OrganizationSubscriptionForm


# ACCESS: Only user with contractorprofile should be able to update their subscription
class ContractorSubscriptionUpdateView(LoginRequiredMixin, UpdateView):
    """View for editing contractor subscription details."""

    model = ContractorSubscription
    form_class = ContractorSubscriptionForm
