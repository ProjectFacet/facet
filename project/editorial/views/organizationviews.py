""" Organization views for editorial app.

    editorial/views/organization.py
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

from editorial.forms import (
    AddUserForm,
    UserProfileForm,
    OrganizationForm,
    NetworkForm,
    SeriesForm,
    StoryForm,
    WebFacetForm,
    PrintFacetForm,
    AudioFacetForm,
    VideoFacetForm,
    ImageAssetForm,
    AddImageForm,
    AddToNetworkForm,
    InviteToNetworkForm,
    PrivateMessageForm,
    OrganizationCommentForm,
    NetworkCommentForm,
    SeriesCommentForm,
    StoryCommentForm,
    WebFacetCommentForm,
    PrintFacetCommentForm,
    AudioFacetCommentForm,
    VideoFacetCommentForm,
    NetworkNoteForm,
    OrganizationNoteForm,
    UserNoteForm,
    SeriesNoteForm,
    StoryNoteForm,)

from editorial.models import (
    User,
    Organization,
    Network,
    Series,
    Story,
    WebFacet,
    PrintFacet,
    AudioFacet,
    VideoFacet,
    SeriesNote,
    StoryNote,
    ImageAsset,
    Comment,
    PrivateMessage,
    Discussion,
    StoryCopyDetail,
    WebFacetCopyDetail,
    PrintFacetCopyDetail,
    AudioFacetCopyDetail,
    VideoFacetCopyDetail,
    NetworkNote,
    OrganizationNote,
    UserNote,
    SeriesNote,
    StoryNote,)

# Org notes are managed in notes.py

#----------------------------------------------------------------------#
#   Organization Views
#----------------------------------------------------------------------#

def org_new(request):
    """ A user can create an organization after signing up.
    Ex. A member of a news organization creates an organization account for the newsroom.
    Ex. A freelancer can create their own organization to form a network with any newsroom
    they regularly contribute to.
    """

    orgform = OrganizationForm()
    if request.method == "POST":
        import pdb; pdb.set_trace()
        orgform = OrganizationForm(request.POST, request.FILES)
        if orgform.is_valid():
            organization = orgform.save(commit=False)
            organization.owner = request.user
            organization.creation_date = timezone.now()
            organization.logo = request.FILES['logo']
            discussion = Discussion.objects.create_discussion("ORG")
            organization.discussion = discussion
            organization.save()
            # update user to connect them to the organization
            current_user = get_object_or_404(User, pk=request.user.id)
            current_user.organization = organization
            current_user.save()
            return redirect('org_detail', pk=organization.pk)
    else:
        form = OrganizationForm()
    return render(request, 'editorial/organizationnew.html', {
            'orgform': orgform,
            })


def org_detail(request, pk):
    """ The public profile of an organization.

    Visible to users/organizations in the same networks.
    Displays the organization's name, logo, description, team members, most recent
    shared content, admin email addresses.
    """

    organization = get_object_or_404(Organization, pk=pk)
    organizationnoteform = OrganizationNoteForm()
    organizationnotes = OrganizationNote.objects.filter(organization=organization)[:5]
    users = Organization.get_org_users(organization)
    organizationcomments = Comment.objects.filter(discussion=organization.discussion).order_by('-date')
    organizationcommentform = OrganizationCommentForm()

    return render(request, 'editorial/organizationdetail.html', {
        'organization': organization,
        'organizationnoteform': organizationnoteform,
        'organizationnotes': organizationnotes,
        'organizationcomments': organizationcomments,
        'organizationcommentform': organizationcommentform,
        })


def org_edit(request, pk):
    """ Edit organization page."""

    organization = get_object_or_404(Organization, pk=pk)

    if request.method == "POST":
        orgform = OrganizationForm(request.POST, request.FILES, instance=organization)
        if orgform.is_valid():
            orgform.save()
            return redirect('org_detail', pk=organization.id)
    else:
        orgform = OrganizationForm(instance=organization)

    return render(request, 'editorial/organizationedit.html', {
            'organization': organization,
            'orgform': orgform,
    })
