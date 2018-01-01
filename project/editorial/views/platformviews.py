""" Platform views for editorial app.

    editorial/views/platformviews.py
"""

# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.views.generic import FormView
from django.conf import settings
from braces.views import LoginRequiredMixin, FormMessagesMixin

from editorial.forms import (
    PlatformAccountFormSet,
)

from editorial.models import PlatformAccount, User
from extra_views import InlineFormSetView, ModelFormSetView

# ----------------------------------------------------------------------#
#   Platform Views
# ----------------------------------------------------------------------#

class UserPlatformAccountCreateView(LoginRequiredMixin, FormView):
    """Display formset to add social accounts to a user, organization or project."""

    # handle users that are not logged in
    login_url = settings.LOGIN_URL

    form_class = PlatformAccountFormSet
    template_name = "editorial/platformaccounts_form.html"

    def get_initial(self):
        """Pass user/organization to subform."""

        # Older versions of Django don't have a nice way to pass things to forms within
        # formsets except using initial data, so we shoe-horn it into here
        return [{"user": self.request.user, 'organization': self.request.user.organization}]

    def form_valid(self, form):
        """Save data."""

        # One day, this may want to grow to handle deleting platform accounts, using a
        # tick-to-delete. Or, with a newer Django version, this could move to extra_views,
        # which has a nice built-in for formset editing.

        for subform in form:
            if subform.cleaned_data:
                subform.save()

        return super(UserPlatformAccountCreateView, self).form_valid(form)

    def get_success_url(self):
        """Return to user profile."""

        return reverse("user_edit", kwargs={"pk": self.request.user.id})
