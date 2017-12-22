""" Network views for editorial app.

    editorial/views/networkviews.py
"""

# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponse
from django.utils import timezone
from django.views.generic import TemplateView , UpdateView, DetailView, CreateView, ListView
from django.views.decorators.csrf import csrf_exempt
from django.core.serializers.json import DjangoJSONEncoder
import datetime
import json
from actstream import action

from editorial.forms import (
    NetworkForm,
    AddToNetworkForm,
    InviteToNetworkForm,
    CommentForm,
    NetworkNoteForm,)

from editorial.models import (
    User,
    Organization,
    Network,
    Story,
    Facet,
    ImageAsset,
    DocumentAsset,
    AudioAsset,
    VideoAsset,
    Comment,
    PrivateMessage,
    Discussion,
    StoryCopyDetail,
    FacetCopyDetail,
    ImageAssetCopyDetail,
    DocumentAssetCopyDetail,
    AudioAssetCopyDetail,
    VideoAssetCopyDetail,
    NetworkNote,)


#----------------------------------------------------------------------#
#   Network Views
#----------------------------------------------------------------------#

class NetworkCreateView(CreateView):
    """Create a new network."""

    model = Network
    form_class = NetworkForm

    def form_valid(self, form):
        """Save -- but first add owner organization."""

        self.object = network = form.save(commit=False)

        discussion = Discussion.objects.create_discussion("NET")
        network.discussion = discussion

        network.owner_organization = self.request.user.organization

        network.save()
        form.save_m2m()

        action.send(self.request.user, verb="created", action_object=self.object)

        return redirect(self.get_success_url())


class NetworkUpdateView(UpdateView):
    """ Update a network."""

    model = Network
    form_class = NetworkForm

    def get_success_url(self):
        """Record action for activity stream."""

        action.send(self.request.user, verb="edited", action_object=self.object)
        return super(NetworkUpdateView, self).get_success_url()


class NetworkListView(ListView):
    """Display a list of all the networks and organization is either
    the owner of or a member of.
    """

    context_object_name = 'networks'

    def get_queryset(self):
        """return relevant networks for an organization."""
        org = self.request.user.organization
        return org.get_org_networks()


class NetworkDetailView(DetailView):
    """Return all the detail for a network."""

    model = Network

    def get_context_data(self, **kwargs):
        """Get network related info."""

        context = super(NetworkDetailView, self).get_context_data(**kwargs)

        notes = self.object.networknote_network.all()
        noteform = NetworkNoteForm()
        comments = self.object.discussion.comment_set.all()
        commentform = CommentForm()
        networkinvitationform = InviteToNetworkForm()

        context.update({
                'notes': notes,
                'noteform': noteform,
                'comments': comments,
                'commentform': commentform,
                'networkinvitationform': networkinvitationform,
        })

        return context


def delete_network(request, pk):
    """ Delete a network and dependent records."""

    if request == "POST":
        # network = get_object_or_404(Network, pk=pk)
        # if request.user == network.owner_organization
        #     network.delete()
        return redirect('network_list')


def send_network_invite(request):
    """ Send private message with link to join a network."""

    network = request.POST.get('network')
    network = get_object_or_404(Network, id=network)
    user_email = request.POST.get('invited_user')
    user = get_object_or_404(User, email=user_email)
    organization = get_object_or_404(Organization, id=user.organization_id)
    message_subject = "Invitation for {organization} to join {network}".format(organization = organization.name, network=network.name)
    message_text = '<form action="/network/invitation/accept/" method="POST" class="post-form"><input type="hidden" name="network" value="{network}" /><button type="submit" class="btn btn-primary">Accept Invitation</button></form>'.format(network=network.id)
    discussion = Discussion.objects.create_discussion('PRI')
    invitation_message = PrivateMessage.objects.create_private_message(user=request.user, recipient=user, discussion=discussion, subject=message_subject, text=message_text)
    return redirect('network_detail', pk=network.pk)

    # on Priv?essage, add field for .org_invite_id
    # on message render view:   {% if msg.org_invite_id %} <form...> {% csrf_Except %} ... </form>


@csrf_exempt
def confirm_network_invite(request):
    """ Receive confirmed networkwork invitation and create new NetworkOrganization
    connection."""

    network_id = request.POST.get('network')
    network = get_object_or_404(Network, id=network_id)
    organization = request.user.organization
    network.organizations.add(organization)
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


class NetworkStoryListView(ListView):
    """ Displays a filterable table of stories marked as shared/ready to share by any
    organizations that a user's organization is a part of.

    Initial display organizes content by story>facet>est. run date
    Filterable by story name, facet type, facet name, due for edit, est. run date, credit,
    editor, status.

    Stories marked as share appear but are greyed out/inaccessible until the owner marks
    them as Ready to Share. (This is so partners know it will exist and can plan to incorporate
    it once it becomes available.)
    """

    context_object_name = 'networkstories'
    template_name = 'editorial/networkstory_list.html'

    def get_queryset(self):
        """Return network stories."""

        organization = self.request.user.organization
        networks = Organization.get_org_networks(organization)

        shared_networkstories = []
        for network in networks:
            stories = network.get_network_shared_stories()
            shared_networkstories.extend(stories)
        shared_networkstories = [story for story in shared_networkstories if story.organization != organization]
        networkstories = set(shared_networkstories)

        return networkstories


# class CopyNetworkStory(FormView):
#     """Copy a story and related facets.
#
#     TODO Needs to let user select story and facets/assets for copying.
#     """
#
#     original_org = original_story.organization
#     original_story = get_object_or_404(Story, pk=pk)
#     original_facets = original_story.facet_set.all()
#





def copy_network_story(request, pk):
    """ Copy a story and related facets. """

    original_story = get_object_or_404(Story, pk=pk)
    original_org = original_story.organization

    # FIXME refactor for facets
    original_facets = original_story.facet_set.all()

    user = request.user
    organization = request.user.organization
    partner = request.user.organization

    # record action for activity story_team
    # action.send(request.user, verb="picked up", action_object=original_story)

    if request.method == "POST":

        # Create a copy of the story and a storycopydetail record
        copied_story = Story.copy_story(original_story)
        copied_story.owner = user
        copied_story.organization = organization
        copied_story.save()
        story_copy_record = StoryCopyDetail.objects.create_story_copy_record(
            original_org=original_org,
            partner=partner,
            original_story=original_story,
            partner_story=copied_story
            )

        # Create copy of facets if they exist
        # Copy the Facet
        if original_facets:
            print original_webfacet[0]
            copied_webfacet = WebFacet.copy_webfacet(original_webfacet[0])
            copied_webfacet.story = copied_story
            copied_webfacet.owner = user
            copied_webfacet.organization = organization
            copied_webfacet.save()
            webfacet_copy_record = WebFacetCopyDetail.objects.create_webfacet_copy_record(
                original_org=original_org,
                partner=partner,
                original_webfacet=original_webfacet[0],
                partner_webfacet=copied_webfacet
            )

            # create copy of webfacet images
            original_webfacet_images = WebFacet.get_webfacet_images(original_webfacet[0])
            for image in original_webfacet_images:
                copied_image = ImageAsset.copy_image(image)
                copied_image.owner = user
                copied_image.organization = organization
                copied_image.save()
                imageasset_copy_record = ImageAssetCopyDetail.objects.create_imageasset_copy_record(
                    original_org=original_org,
                    partner=partner,
                    original_imageasset=image,
                    partner_imageasset=copied_image
                )
                # add image to copied webfacet
                copied_webfacet.image_assets.add(copied_image)
                copied_webfacet.save()

            # create copy of webfacet documents
            original_webfacet_documents = WebFacet.get_webfacet_documents(original_webfacet[0])
            for document in original_webfacet_documents:
                copied_document = DocumentAsset.copy_document(document)
                copied_document.owner = user
                copied_document.organization = organization
                copied_document.save()
                documentasset_copy_record = DocumentAssetCopyDetail.objects.create_documentasset_copy_record(
                    original_org=original_org,
                    partner=partner,
                    original_documentasset=document,
                    partner_documentasset=copied_document
                )
                # add document to copied webfacet
                copied_webfacet.document_assets.add(copied_document)
                copied_webfacet.save()


            # create copy of webfacet audio
            original_webfacet_audiofiles = WebFacet.get_webfacet_audio(original_webfacet[0])
            for audio in original_webfacet_audiofiles:
                copied_audio = AudioAsset.copy_audio(audio)
                copied_audio.owner = user
                copied_audio.organization = organization
                copied_audio.save()
                audioasset_copy_record = AudioAssetCopyDetail.objects.create_audioasset_copy_record(
                    original_org=original_org,
                    partner=partner,
                    original_audioasset=audio,
                    partner_audioasset=copied_audio
                )
                # add audio to copied webfacet
                copied_webfacet.audio_assets.add(copied_audio)
                copied_webfacet.save()

            # create copy of webfacet video
            original_webfacet_videos = WebFacet.get_webfacet_video(original_webfacet[0])
            for video in original_webfacet_videos:
                copied_video = VideoAsset.copy_video(video)
                copied_video.owner = user
                copied_video.organization = organization
                copied_video.save()
                videoasset_copy_record = VideoAssetCopyDetail.objects.create_videoasset_copy_record(
                    original_org=original_org,
                    partner=partner,
                    original_videoasset=video,
                    partner_videoasset=copied_video
                )
                # add video to copied webfacet
                copied_webfacet.video_assets.add(copied_video)
                copied_webfacet.save()


    return redirect('network_stories')


# def network_stories_json(request):
#     """Return JSON of network story objects."""
#
#     organization = request.user.organization
#     networks = Organization.get_org_networks(organization)
#
#     shared_networkstories = []
#     for network in networks:
#         stories = Network.get_network_shared_stories(network)
#         shared_networkstories.extend(stories)
#     shared_networkstories = [story for story in shared_networkstories if story.organization != organization]
#     stories = set(shared_networkstories)
#     # networkstories = json.dumps(list(stories), cls=DjangoJSONEncoder)
#
#     org_network_content = Organization.get_org_network_content(organization)
#     print "ONC: ", org_network_content
#
#     return HttpResponse(json.dumps(networkstories), content_type='application/json')
