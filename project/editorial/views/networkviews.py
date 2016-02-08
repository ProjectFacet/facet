""" Network views for editorial app.

    editorial/views/networkviews.py
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

# All imports are included for use in test view

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


#----------------------------------------------------------------------#
#   Network Views
#----------------------------------------------------------------------#

def network_new(request):
    """ Create a new network. """

    networkform = NetworkForm()
    owner_org = request.user.organization
    if request.method == "POST":
        networkform = NetworkForm(request.POST or None)
        if networkform.is_valid():
            network = networkform.save(commit=False)
            network.owner_organization = owner_org
            network.creation_date = timezone.now()
            discussion = Discussion.objects.create_discussion("NET")
            network.discussion = discussion
            network.save()
            network.network_organization.add(owner_org)
            network.save()
            return redirect('network_detail', pk=network.pk)
    else:
        networkform = NetworkForm()
    return render(request, 'editorial/networknew.html', {
            'networkform': networkform
        })


def delete_network(request, pk):
    """ Delete a network and dependent records."""

    if request == "POST":
        network = get_object_or_404(Network, pk=pk)
        # if request.user == network.owner_organization
        network.delete()
        return redirect('network_list')


def send_network_invite(request):
    """ Send private message with link to join a network."""

    network = request.POST.get('network')
    print "Post Network", network
    network = get_object_or_404(Network, id=network)
    user_email = request.POST.get('invited_user')
    print "USER EMAIL", user_email
    user = get_object_or_404(User, email=user_email)
    print "USER: ", user
    organization = get_object_or_404(Organization, id=user.organization_id)
    print "ORG: ", organization
    message_subject = "Invitation for {organization} to join {network}".format(organization = organization.name, network=network.name)
    print "MESSAGE SUBJECT", message_subject
    message_text = '<form action="/network/invitation/accept/" method="POST" class="post-form"><input type="hidden" name="network" value="{network}" /><button type="submit" class="btn btn-primary">Accept Invitation</button></form>'.format(network=network.id)
    print "MESSAGE TEXT: ", message_text
    discussion = Discussion.objects.create_discussion('PRI')
    invitation_message = PrivateMessage.objects.create_private_message(user=request.user, recipient=user, discussion=discussion, subject=message_subject, text=message_text)
    print "Successfully joined Network!"
    return redirect('network_detail', pk=network.pk)


@csrf_exempt
def confirm_network_invite(request):
    """ Receive confirmed networkwork invitation and create new NetworkOrganization
    connection."""

    network_id = request.POST.get('network')
    network = get_object_or_404(Network, id=network_id)
    organization = request.user.organization
    network.network_organization.add(organization)
    network.save()
    print "Successfully joined Network!"
    return redirect('network_detail', pk=network.pk)


def org_to_network(request, pk):
    """ Form to add an organization to a network. """

    network = get_object_or_404(Network, pk=pk)

    if request.method == "POST":
        form = AddToNetworkForm(request.POST or None)
        if form.is_valid():
            connection = form.save(commit=False)
            return redirect('network_detail', pk=network.pk)
    else:
        form = AddToNetworkForm()
    return render(request, 'editorial/networkdetail.html', {'form': form})


def network_detail(request, pk):
    """ Public profile of a network. """

    network = get_object_or_404(Network, pk=pk)
    networknoteform = NetworkNoteForm()
    networkinvitationform = InviteToNetworkForm()
    networknotes = NetworkNote.objects.filter(network=network)
    networkcomments = Comment.objects.filter(discussion=network.discussion).order_by('-date')
    networkcommentform = NetworkCommentForm()

    return render(request, 'editorial/networkdetail.html', {
        'network': network,
        'networkinvitationform': networkinvitationform,
        'networknoteform': networknoteform,
        'networknotes': networknotes,
        'networkcomments': networkcomments,
        'networkcommentform': networkcommentform,
        })


def network_edit(request, pk):
    """ Edit network page. """

    network = get_object_or_404(Network, pk=pk)

    if request.method == "POST":
        networkform = NetworkForm(data=request.POST, instance=network)
        if networkform.is_valid():
            networkform.save()
            return redirect('network_detail', pk=network.id)
    else:
        networkform = NetworkForm(instance=network)

    return render(request, 'editorial/networkedit.html', {
            'network': network,
            'networkform': networkform,
        })


def network_list(request):
    """ Table of networks your org is member of."""

    organization = request.user.organization
    print "org id: ", organization
    network_list = Organization.get_org_networks(organization)
    print "network_list: ", network_list

    return render(request, 'editorial/networklist.html', {'network_list': network_list})


def network_stories(request):
    """ Displays a filterable table of stories marked as shared/ready to share by any
    organizations that a user's organization is a part of.

    Initial display organizes content by story>facet>est. run date
    Filterable by story name, facet type, facet name, due for edit, est. run date, credit,
    editor, status.

    Stories marked as share appear but are greyed out/inaccessible until the owner marks
    them as Ready to Share. (This is so partners know it will exist and can plan to incorporate
    it once it becomes available.)
    """

    org_id = request.user.organization_id
    organization = get_object_or_404(Organization, id=org_id)

    networks = Organization.get_org_networks(organization)

    shared_networkstories = []
    for network in networks:
        stories = Network.get_network_shared_stories(network)
        shared_networkstories.extend(stories)

    networkstories = set(shared_networkstories)

    return render(request, 'editorial/networkstories.html', {
        'networkstories': networkstories,
        })


def copy_network_story(request, pk):
    """ Copy a story and related facets. """

    original_story = get_object_or_404(Story, pk=pk)
    original_org = original_story.organization

    original_webfacet = original_story.webfacetstory.all()
    original_printfacet = original_story.printfacetstory.all()
    original_audiofacet = original_story.audiofacetstory.all()
    original_videofacet = original_story.videofacetstory.all()

    user = request.user
    organization = request.user.organization
    partner = request.user.organization

    if request.method == "POST":

        #Create a copy of the story and a storycopydetail record
        copied_story = Story.copy_story(original_story)
        copied_story.owner = user
        copied_story.organization = organization
        copied_story.save()
        partner_story = copied_story
        story_copy_record = StoryCopyDetail.objects.create_story_copy_record(
            original_org=original_org,
            partner=partner,
            original_story=original_story,
            partner_story=partner_story
            )
        print "Story Copied"

        # Create copy of facets if they exist
        if original_webfacet:
            print original_webfacet[0]
            copied_webfacet = WebFacet.copy_webfacet(original_webfacet[0])
            copied_webfacet.story = partner_story
            copied_webfacet.owner = user
            copied_webfacet.organization = organization
            copied_webfacet.save()
            partner_webfacet = copied_webfacet
            webfacet_copy_record = WebFacetCopyDetail.objects.create_webfacet_copy_record(
                original_org=original_org,
                partner=partner,
                original_webfacet=original_webfacet[0],
                partner_webfacet=partner_webfacet
            )
            print "Webfacet Copied"

        if original_printfacet:
            print original_printfacet[0]
            copied_printfacet = PrintFacet.copy_printfacet(original_printfacet[0])
            copied_printfacet.story = partner_story
            copied_printfacet.owner = user
            copied_printfacet.organization = organization
            copied_printfacet.save()
            partner_printfacet = copied_printfacet
            printfacet_copy_record = PrintFacetCopyDetail.objects.create_printfacet_copy_record(
                original_org=original_org,
                partner=partner,
                original_printfacet=original_printfacet,
                partner_printfacet=partner_printfacet
            )
            print "Printfacet Copied"

        if original_audiofacet:
            print original_audiofacet[0]
            copied_audiofacet = AudioFacet.copy_audiofacet(original_audiofacet[0])
            copied_audiofacet.story = partner_story
            copied_audiofacet.owner = user
            copied_audiofacet.organization = organization
            copied_audiofacet.save()
            partner_audiofacet = copied_audiofacet
            audiofacet_copy_record = AudioFacetCopyDetail.objects.create_audiofacet_copy_record(
                original_org=original_org,
                partner=partner,
                original_audiofacet=original_audiofacet,
                partner_audiofacet=partner_audiofacet
            )
            print "Audiofacet Copied"

        if original_videofacet:
            print original_videofacet[0]
            copied_videofacet = VideoFacet.copy_videofacet(original_videofacet[0])
            copied_videofacet.story = partner_story
            copied_videofacet.owner = user
            copied_videofacet.organization = organization
            copied_videofacet.save()
            partner_videofacet = copied_videofacet
            videofacet_copy_record = VideoFacetCopyDetail.objects.create_videofacet_copy_record(
                original_org=original_org,
                partner=partner,
                original_videofacet=original_videofacet,
                partner_videofacet=partner_videofacet
            )
            print "Videofacet Copied"

    return redirect('network_stories')
