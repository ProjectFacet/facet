""" User views for editorial app.

    editorial/views/userviews.py
"""

# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from actstream import action
from braces.views import LoginRequiredMixin
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import UpdateView, DetailView, CreateView, View
from editorial.forms import (
    AddUserForm,
    UserProfileForm,
    NoteForm,
    # FullUserEditForm,

)
from editorial.models import (
    User,
)


#----------------------------------------------------------------------#
#   User Views
#----------------------------------------------------------------------#

class UserCreateView(LoginRequiredMixin, CreateView):
    """Quick form for creating and adding a new user to an organization
    and inviting them to login.
    """

    model = User
    form_class = AddUserForm

    def form_valid(self, form):
        """Save user -- but first set a few values."""

        user = self.object = form.save(commit=False)
        user.organization = self.request.user.organization
        temp_pass = self.request.POST.get('password')
        user.save()

        # notify new user of of account creation
        mail_subject = "New User Details"
        message = "You've been added to Facet. Your login is your email and your password is {pw}. Login to projectfacet.com and update your password.".format(pw=temp_pass)
        print "MESSAGE: ", message
        recipient = [user.email]
        send_mail(mail_subject, message, settings.DEFAULT_FROM_EMAIL, recipient, fail_silently=False)

        # record action for activity stream
        new_user = get_object_or_404(User, pk=user.pk)
        action.send(self.request.user, verb="added", action_object=new_user)

        return redirect(self.get_success_url())


class UserDetailView(LoginRequiredMixin, DetailView):
    """The public profile of a user.

    Displays the user's organization, title, credit name, email, phone,
    bio, expertise, profile photo, social media links and most recent content.
    """

    model = User

    def content(self):
        """Get all content associated with a user."""

        return self.object.get_user_content()

    def assets(self):
        """Get all assets associated with a user."""

        return self.object.get_user_assets()

    def notes(self):
        """Get all user notes associated with user and note form."""

        notes = self.object.note_set.filter(note_type="USER").order_by('-creation_date')
        form = NoteForm()

        return {'notes': notes, 'form': form}


class UserUpdateView(LoginRequiredMixin, UpdateView):
    """Update a user."""

    model = User
    form_class = UserProfileForm

    def get_success_url(self):
        """Record action for activity stream."""

        action.send(self.request.user, verb="edited", action_object=self.object)
        return super(UserUpdateView, self).get_success_url()


class UserDeactivateView(LoginRequiredMixin, View):
    """Deactivate a user."""

    def post(self, request):
        """Handle form submission."""

        user_id = request.POST.get('user_id')
        user = get_object_or_404(User, pk=user_id)
        user.is_active = False
        user.save()

        return redirect('org_edit', pk=user.organization.id)


class UserActivateView(LoginRequiredMixin, View):
    """Activate an org user."""

    def post(self, request):
        """Handle form submission."""

        user_id = request.POST.get('user_id')
        user = get_object_or_404(User, pk=user_id)
        user.is_active = True
        user.save()

        return redirect('org_edit', pk=user.organization.id)
