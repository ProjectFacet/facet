""" Account management views for editorial app. """

# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponse
from django.utils import timezone
from django.views.generic import TemplateView , UpdateView, DetailView, ListView, CreateView
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta, time
import json
from django.template.loader import render_to_string


from editorial.models import (
    User,
    Organization,
    ContractorProfile,
    OrganizationSubscription,
    ContractorSubscription,
    )

from editorial.forms import (
    OrganizationSubscriptionForm,
    ContractorSubscriptionForm,
)

#----------------------------------------------------------------------#
#   Account Selection View
#----------------------------------------------------------------------#

class AccountSelectionView(TemplateView):
    """ After user signup, the user is directed to account selection to
    choose between creating an organization with a team account or a
    contractor profile for an independent account.
    """

    template_name = 'editorial/account_selection.html'


class OrganizationSubscriptionUpdateView(UpdateView):
    """ View for editing organization subscription details."""

    model = OrganizationSubscription
    form_class = OrganizationSubscriptionForm


class ContractorSubscriptionUpdateView(UpdateView):
    """ View for editing contractor subscription details."""

    model = ContractorSubscription
    form_class = ContractorSubscriptionForm
