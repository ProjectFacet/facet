""" Platform views for editorial app.

    editorial/views/platformviews.py
"""

# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.views.generic import TemplateView, UpdateView, DetailView, CreateView

from editorial.forms import (
    PlatformAccountForm,
    PlatformAccountFormSet,
)


# ----------------------------------------------------------------------#
#   Platform Views
# ----------------------------------------------------------------------#

class UserPlatformAccountCreateView(CreateView):
    """Display formset to add social accounts to a user, organization or project."""

    form_class = PlatformAccountFormSet
    template_name = "editorial/platformaccounts_form.html"

    def get_form_kwargs(self):
        """Pass curent user and organization to the form."""

        kw = super(UserPlatformAccountCreateView, self).get_form_kwargs()
        kw.update({'organization': self.request.user.organization, 'user': self.request.user})
        return kw

    #
    # def get_context_data(self, **kwargs):
    #     data = super(UserPlatformAccountCreateView, self).get_context_data(**kwargs)
    #     if self.request.POST:
    #         data['accounts'] = PlatformAccountFormSet(self.request.POST)
    #     else:
    #         data['accounts'] = PlatformAccountFormSet()
    #     return data
    #
    # def form_valid(self, form):
    #     context = self.get_context_data()
    #     accounts = context['accounts']
    #     with transaction.atomic():
    #         self.object = form.save()
    #
    #         if accounts.is_valid():
    #             accounts.instance = self.object
    #             accounts.save()
    #     return super(UserPlatformAccountCreateView, self).form_valid(form)
