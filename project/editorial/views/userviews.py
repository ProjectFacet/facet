""" User views for editorial app.

    editorial/views/userviews.py
"""

# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponse
from django.utils import timezone
from django.views.generic import TemplateView , UpdateView, DetailView, CreateView, View
from django.views.decorators.csrf import csrf_exempt
from django.forms import formset_factory
import datetime
import json
from actstream import action
from braces.views import LoginRequiredMixin, FormMessagesMixin

from editorial.forms import (
    AddUserForm,
    UserProfileForm,
    NoteForm,
    # FullUserEditForm,

    )

from editorial.models import (
    User,
    Note,
    )


#----------------------------------------------------------------------#
#   User Views
#----------------------------------------------------------------------#
class UserCreateView(LoginRequiredMixin, CreateView):
    """Quick form for creating and adding a new user to an organization
    and inviting them to login.
    """

    # handle users that are not logged in
    login_url = settings.LOGIN_URL

    model = User
    form_class = AddUserForm

    def form_valid(self, form):
        """Save user -- but first set a few values."""

        user = form.save(commit=False)
        user.organization = self.request.user.organization
        user.save()

        # notify new user of of account creation
        mail_subject = "New User Details"
        message = "You've been added to Facet. Your login is your email and your password is please."
        recipient = [user.email]
        sender_email = self.request.user.email
        send_mail(mail_subject, message, settings.EMAIL_HOST_USER, recipient, fail_silently=True)

        # record action for activity stream
        new_user = get_object_or_404(User, pk=user.pk)
        action.send(self.request.user, verb="added", action_object=new_user)

        return redirect(self.get_success_url())


class UserDetailView(LoginRequiredMixin, DetailView):
    """ The public profile of a user.

    Displays the user's organization, title, credit name, email, phone,
    bio, expertise, profile photo, social media links and most recent content.
    """

    # handle users that are not logged in
    login_url = settings.LOGIN_URL

    model = User

    def content(self):
        """Get all content associated with a user."""

        self.object = self.get_object()
        return self.object.get_user_content()

    def assets(self):
        """Get all assets associated with a user."""

        self.object = self.get_object()
        return self.object.get_user_assets()

    def notes(self):
        """Get all user notes associated with user and note form."""

        self.object = self.get_object()
        notes = self.object.note_set.filter(note_type="USER").order_by('-creation_date')
        form = NoteForm()
        return {'notes': notes, 'form': form,}


class UserUpdateView(LoginRequiredMixin, UpdateView):
    """Update a user."""

    # handle users that are not logged in
    login_url = settings.LOGIN_URL

    model = User
    form_class = UserProfileForm

    def get_success_url(self):
        """Record action for activity stream."""

        action.send(self.request.user, verb="edited", action_object=self.object)
        return super(UserUpdateView, self).get_success_url()


# FIXME still having csrf_token problem
class UserDeactivateView(LoginRequiredMixin, View):
    """Deactivate an org user."""

    # handle users that are not logged in
    login_url = settings.LOGIN_URL

    def post(self):
        user_id = self.request.POST.get('user_id')
        user = get_object_or_404(User, pk=user_id)
        print "USER ID: ", user_id
        user.is_active = False
        print "User Status: ", user.is_active
        user.save()
        print "This user has been deactivated."

        return redirect('org_edit', pk=user.organization.id)


# FIXME still having csrf_token problem
class UserActivateView(LoginRequiredMixin, View):
    """Activate an org user."""

    # handle users that are not logged in
    login_url = settings.LOGIN_URL

    def post(self):
        user_id = request.POST.get('user_id')
        user = get_object_or_404(User, pk=user_id)
        print "USER ID: ", user_id
        user.is_active = True
        print "User Status: ", user.is_active
        user.save()
        print "This user has been activated."

        return redirect('org_edit', pk=user.organization.id)
