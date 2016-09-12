""" User views for editorial app.

    editorial/views/userviews.py
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponse
from django.utils import timezone
from django.views.generic import TemplateView , UpdateView, DetailView
from django.views.decorators.csrf import csrf_exempt
import datetime
import json
from actstream import action

from editorial.forms import (
    AddUserForm,
    UserProfileForm,
    UserNoteForm,
    # FullUserEditForm,
    )

from editorial.models import (
    User,
    UserNote,)


#----------------------------------------------------------------------#
#   User Views
#----------------------------------------------------------------------#

def user_new(request):
    """ Quick form for making a new user and inviting them to login. """

    if request.method == "POST":
        form = AddUserForm(request.POST or None)
        if form.is_valid():
            user = form.save(commit=False)
            user.organization = request.user.organization
            user.save()
            # notify new user of of account creation
            mail_subject = "New Facet User Details"
            message = "You've been added to Facet. Your login is your email and your password is please."
            recipient = [user.email]
            sender_email = request.user.email
            send_mail(mail_subject, message, settings.EMAIL_HOST_USER, recipient, fail_silently=True)
            # record action for activity stream
            print "USER PK: ", user.pk
            new_user = get_object_or_404(User, pk=user.pk)
            action.send(request.user, verb="added", action_object=new_user)
            print "ACTION Recorded"
        return redirect('team_list')
    else:
        form=AddUserForm()
        return render(request, 'editorial/usernew.html', {'form': form})


def user_detail(request, pk):
    """ The public profile of a user.

    Displays the user's organization, title, credit name, email, phone,
    bio, expertise, profile photo, social media links and most recent content.
    """

    print "in USER DETAIL"
    user = get_object_or_404(User, pk=pk)
    user_stories = User.get_user_stories(user)
    user_content = User.get_user_content(user)
    usernotes = UserNote.objects.filter(owner_id=user.id)[:4]
    usernoteform = UserNoteForm()

    content = user.get_user_content()

    return render(request, 'editorial/userdetail.html', {
        'user': user,
        'user_stories': user_stories,
        'user_content': user_content,
        'usernotes': usernotes,
        'usernoteform': usernoteform
        })


def user_edit(request, pk):
    """ Edit the user's profile."""

    user = get_object_or_404(User, pk=pk)

    if request.method == "POST":
        # import pdb; pdb.set_trace()
        userform = UserProfileForm(request.POST, request.FILES, instance=user)
        # print "userform exists: ", userform
        if userform.is_valid():
            userform.save()
            return redirect('user_detail', pk = user.id)
    else:
        userform = UserProfileForm(instance=user)

    return render(request, 'editorial/useredit.html', {
            'user': user,
            'userform': userform
    })


@csrf_exempt
def user_deactivate(request):
    """ Deactivate a user."""

    if request.method == "POST":
        user_id = request.POST.get('user_id')
        user = get_object_or_404(User, pk=user_id)
        print "USER ID: ", user_id
        user.is_active = False
        print "User Status: ", user.is_active
        user.save()
        print "This user has been deactivated."

    return redirect('org_edit', pk=user.organization.id)


@csrf_exempt
def user_activate(request):
    """ Activate a user."""

    if request.method == "POST":
        user_id = request.POST.get('user_id')
        user = get_object_or_404(User, pk=user_id)
        print "USER ID: ", user_id
        user.is_active = True
        print "User Status: ", user.is_active
        user.save()
        print "This user has been activated."

    return redirect('org_edit', pk=user.organization.id)
