""" Network views for editorial app.

    editorial/views/networkviews.py
"""

# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponse
from django.utils import timezone
from django.views.generic import TemplateView , UpdateView, DetailView, CreateView, ListView, DeleteView, View, RedirectView
from django.views.decorators.csrf import csrf_exempt
from django.core.serializers.json import DjangoJSONEncoder
import datetime
import json
from actstream import action
from django.db.models import Q
from braces.views import LoginRequiredMixin, FormMessagesMixin

from editorial.forms import (
    NetworkForm,
    AddToNetworkForm,
    InviteToNetworkForm,
    CommentForm,
    NoteForm,
    SimpleImageForm,
    SimpleDocumentForm,
    )

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
    Note,
    )


#----------------------------------------------------------------------#
#   Network Views
#----------------------------------------------------------------------#

# ACCESS: Only org admins have access
class NetworkCreateView(LoginRequiredMixin, CreateView):
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


# ACCESS: Only org admins can edit networks their org owns.
class NetworkUpdateView(LoginRequiredMixin, UpdateView):
    """ Update a network."""

    model = Network
    form_class = NetworkForm

    def get_success_url(self):
        """Record action for activity stream."""

        action.send(self.request.user, verb="edited", action_object=self.object)
        return super(NetworkUpdateView, self).get_success_url()


# ACCESS: All org users can see list of networks an org is owner/member
class NetworkListView(LoginRequiredMixin, ListView):
    """Display a list of all the networks and organization is either
    the owner of or a member of.
    """

    context_object_name = 'networks'

    def get_queryset(self):
        """return relevant networks for an organization."""
        org = self.request.user.organization
        return org.get_org_networks()


# ACCESS: All org users can see details of networks an org is owner/member
class NetworkDetailView(LoginRequiredMixin, DetailView):
    """Return all the detail for a network."""

    model = Network

    def get_context_data(self, **kwargs):
        """Get network related info."""

        context = super(NetworkDetailView, self).get_context_data(**kwargs)

        form = NoteForm()
        notes = self.object.notes.order_by('-creation_date')[:4]
        comments = self.object.discussion.comment_set.all().order_by('date')
        commentform = CommentForm()
        networkinvitationform = InviteToNetworkForm()

        context.update({
                'notes': notes,
                'form': form,
                'comments': comments,
                'commentform': commentform,
                'networkinvitationform': networkinvitationform,
        })

        return context

    def simple_images(self):
        """Return simple images."""

        images = self.object.simple_image_assets.all()
        form = SimpleImageForm()

        return {'images': images, 'form': form}

    def simple_documents(self):
        """Return simple documents."""

        documents = self.object.simple_document_assets.all()
        form = SimpleDocumentForm()
        return {'documents': documents, 'form': form}


# ACCESS: Only an admin of an org that owns a network can delete a network
class NetworkDeleteView(LoginRequiredMixin, FormMessagesMixin, DeleteView):
    """View for handling deletion of a network.

    In this project, we expect deletion to be done via a JS pop-up UI; we don't expect to
    actually use the "do you want to delete this?" Django-generated page. However, this is
    available if useful.
    """

    model = Network
    template_name = "editorial/network_delete.html"

    form_valid_message = "Deleted."
    form_invalid_message = "Please check form."

    def get_success_url(self):
        """Post-deletion, return to the story URL."""

        return reverse('network_list')


# ACCESS: Only an admin of an org that owns a network can invite other admins
# to a network

class NetworkInvitationSend(LoginRequiredMixin, FormMessagesMixin, RedirectView):
    """Send invite email and redirect back to network page."""

    permanent = False
    msg_subject = "Invitation for {organization} to join {network}"
    msg_body = """{sender} has invited {organization} to join {network}."""

    def get_redirect_url(self, pk):
        """ Send private message with link to join a network."""

        network = get_object_or_404(Network, id=pk)
        recip_email = self.request.POST.get('invited_user')
        recip = get_object_or_404(User, email=recip_email)
        organization = recip.organization
        sender = self.request.user
        message_subject = self.msg_subject.format(organization=organization.name, network=network.name)
        message_text = self.msg_body.format(sender=sender)
        discussion = Discussion.objects.create_discussion('PRI')
        invitation_message = PrivateMessage.objects.create_private_message(
                user=sender,
                recipient=recip,
                discussion=discussion,
                subject=message_subject,
                text=message_text,
                network_invitation=network)

        return reverse('network_detail', kwargs={'pk': network.pk})


class NetworkInvitationAccept(LoginRequiredMixin, FormMessagesMixin, RedirectView):
    """ Receive confirmed networkwork invitation and create new NetworkOrganization
    connection."""

    def get_redirect_url(self, pk):
        network = get_object_or_404(Network, id=pk)
        organization = self.request.user.organization
        network.organizations.add(organization)
        # network.save()
        print "Successfully joined Network!"
        return reverse('network_detail', kwargs={'pk': network.pk})


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


# ACCESS: Org users should be able to see network content for their organization
class NetworkStoryListView(LoginRequiredMixin, ListView):
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

        # get list of stories an organization has copied
        org_copied_content = organization.get_org_copied_content()

        # temp attribute showing whether the user org has already copied a story
        for story in networkstories:
            if story in org_copied_content:
                story.already_picked_up=True
            else:
                story.already_picked_up=False

        return networkstories


# ACCESS: Org users that are editors or admins should be able to copy network stories.
class CopyNetworkStoryView(LoginRequiredMixin, View):
    """Copy a story and related facets.

    A user should be able to click and copy a partner story
    this should make a copy of the story for the new organization
    it should come with all associated assets - image, doc, audio, video
    it should not come with events, notes, tasks, or simple assets
    After a user has copied a story, there should be a visual cue in the interface
    or a js alert (something) that notifies a user should they try to copy a
    story that another user from their org has already copied that specific story.

    Phases of Functionality:
    1. A user can copy a story from a sharing partner. This accomplished what's
    listed above.
    2. A user should be able to select the specific facets of a story they
    want to copy. (Doesn't need to be more granular than that, they don't need to
    select images like in download)
    3. A story that's been updated since it was marked ready_to_share has a visual cue
    that it has been updated. Users who have already copied it, should get some sort
    of notification that updates are available. This is important in the case of
    corrections.

    """

    def post(self, request, story):
        print "In post"
        story = self.kwargs['story']
        original_story = get_object_or_404(Story, id=story)
        original_org = original_story.organization
        original_facets = original_story.facet_set.all()

        user = self.request.user
        organization = self.request.user.organization
        partner = self.request.user.organization

        print "stuff is happening"
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
            # get facet templates and make copies if org is not null
            print "if original facets"
            for facet in original_facets:
                print "copy the facet template"
                print "FT: ", facet.template
                if facet.template.organization:
                    copied_facet_template = facet.template.copy()
                else:
                    copied_facet_template = facet.template
                print "facet template copied"
                copied_facet = facet.copy()
                print "Copied Facet exists"
                print "CF: ", copied_facet
                copied_facet.story = copied_story
                print "CFS"
                copied_facet.owner = user
                print "CFO"
                copied_facet.organization = organization
                print "CFOR"
                copied_facet.template = copied_facet_template
                print "CFT"
                copied_facet.save()
                print "CF Saved"
                facet_copy_record = FacetCopyDetail.objects.create_facet_copy_record(
                    original_org=original_org,
                    partner=partner,
                    original_facet=facet,
                    partner_facet=copied_facet
                )
                print "facet copy record"

            # create copy of facet images
            original_facet_images = original_story.get_story_images()
            print "original facet images"
            for image in original_facet_images:
                copied_image = image.copy()
                copied_image.owner = user
                copied_image.organization = organization
                copied_image.save()
                imageasset_copy_record = ImageAssetCopyDetail.objects.create_imageasset_copy_record(
                    original_org=original_org,
                    partner=partner,
                    original_imageasset=image,
                    partner_imageasset=copied_image
                )
                # add image to copied facet
                copied_facet.image_assets.add(copied_image)
                copied_facet.save()

            # create copy of facet documents
            original_facet_documents = original_story.get_story_documents()
            print "original facet documents"
            for document in original_facet_documents:
                copied_document = document.copy()
                copied_document.owner = user
                copied_document.organization = organization
                copied_document.save()
                documentasset_copy_record = DocumentAssetCopyDetail.objects.create_documentasset_copy_record(
                    original_org=original_org,
                    partner=partner,
                    original_documentasset=document,
                    partner_documentasset=copied_document
                )
                # add document to copied facet
                copied_facet.document_assets.add(copied_document)
                copied_facet.save()


            # create copy of facet audio
            original_facet_audiofiles = original_story.get_story_audio()
            print "original facet audio"
            for audio in original_facet_audiofiles:
                copied_audio = audio.copy()
                copied_audio.owner = user
                copied_audio.organization = organization
                copied_audio.save()
                audioasset_copy_record = AudioAssetCopyDetail.objects.create_audioasset_copy_record(
                    original_org=original_org,
                    partner=partner,
                    original_audioasset=audio,
                    partner_audioasset=copied_audio
                )
                # add audio to copied facet
                copied_facet.audio_assets.add(copied_audio)
                copied_facet.save()

            # create copy of facet video
            original_facet_videos = original_story.get_story_video()
            print "original facet video"
            for video in original_facet_videos:
                copied_video = video.copy()
                copied_video.owner = user
                copied_video.organization = organization
                copied_video.save()
                videoasset_copy_record = VideoAssetCopyDetail.objects.create_videoasset_copy_record(
                    original_org=original_org,
                    partner=partner,
                    original_videoasset=video,
                    partner_videoasset=copied_video
                )
                # add video to copied facet
                copied_facet.video_assets.add(copied_video)
                copied_facet.save()

        # record action for activity story_team
        # action.send(self.request.user, verb="picked up", action_object=original_story)

        return redirect('network_stories')


# def copy_network_story(request, pk):
#     """ Copy a story and related facets. """
#
#     print "copy time"
#     original_story = get_object_or_404(Story, pk=pk)
#     original_org = original_story.organization
#
#     original_facets = original_story.facet_set.all()
#
#     user = request.user
#     organization = request.user.organization
#     partner = request.user.organization
#
#     # record action for activity story_team
#     # action.send(request.user, verb="picked up", action_object=original_story)
#
#     if request.method == "POST":
#         print "stuff is happening"
#         # Create a copy of the story and a storycopydetail record
#         copied_story = Story.copy_story(original_story)
#         copied_story.owner = user
#         copied_story.organization = organization
#         copied_story.save()
#         story_copy_record = StoryCopyDetail.objects.create_story_copy_record(
#             original_org=original_org,
#             partner=partner,
#             original_story=original_story,
#             partner_story=copied_story
#             )
#
#         # Create copy of facets if they exist
#         # Copy the Facet
#         if original_facets:
#             print "if original facets"
#             for facet in original_facets:
#                 copied_facet = Facet.copy_facet(original_facet[0])
#                 copied_facet.story = copied_story
#                 copied_facet.owner = user
#                 copied_facet.organization = organization
#                 copied_facet.save()
#                 facet_copy_record = FacetCopyDetail.objects.create_facet_copy_record(
#                     original_org=original_org,
#                     partner=partner,
#                     original_facet=facet,
#                     partner_facet=copied_facet
#             )
#
#             # create copy of facet images
#             original_facet_images = original_story.get_story_images()
#             print "original facet images"
#             for image in original_facet_images:
#                 copied_image = ImageAsset.copy_image(image)
#                 copied_image.owner = user
#                 copied_image.organization = organization
#                 copied_image.save()
#                 imageasset_copy_record = ImageAssetCopyDetail.objects.create_imageasset_copy_record(
#                     original_org=original_org,
#                     partner=partner,
#                     original_imageasset=image,
#                     partner_imageasset=copied_image
#                 )
#                 # add image to copied facet
#                 copied_facet.image_assets.add(copied_image)
#                 copied_facet.save()
#
#             # create copy of facet documents
#             original_facet_documents = original_story.get_story_documents()
#             print "original facet documents"
#             for document in original_facet_documents:
#                 copied_document = DocumentAsset.copy_document(document)
#                 copied_document.owner = user
#                 copied_document.organization = organization
#                 copied_document.save()
#                 documentasset_copy_record = DocumentAssetCopyDetail.objects.create_documentasset_copy_record(
#                     original_org=original_org,
#                     partner=partner,
#                     original_documentasset=document,
#                     partner_documentasset=copied_document
#                 )
#                 # add document to copied facet
#                 copied_facet.document_assets.add(copied_document)
#                 copied_facet.save()
#
#
#             # create copy of facet audio
#             original_facet_audiofiles = original_story.get_story_audio()
#             print "original facet audio"
#             for audio in original_facet_audiofiles:
#                 copied_audio = AudioAsset.copy_audio(audio)
#                 copied_audio.owner = user
#                 copied_audio.organization = organization
#                 copied_audio.save()
#                 audioasset_copy_record = AudioAssetCopyDetail.objects.create_audioasset_copy_record(
#                     original_org=original_org,
#                     partner=partner,
#                     original_audioasset=audio,
#                     partner_audioasset=copied_audio
#                 )
#                 # add audio to copied facet
#                 copied_facet.audio_assets.add(copied_audio)
#                 copied_facet.save()
#
#             # create copy of facet video
#             original_facet_videos = original_story.get_story_video()
#             print "original facet video"
#             for video in original_facet_videos:
#                 copied_video = VideoAsset.copy_video(video)
#                 copied_video.owner = user
#                 copied_video.organization = organization
#                 copied_video.save()
#                 videoasset_copy_record = VideoAssetCopyDetail.objects.create_videoasset_copy_record(
#                     original_org=original_org,
#                     partner=partner,
#                     original_videoasset=video,
#                     partner_videoasset=copied_video
#                 )
#                 # add video to copied facet
#                 copied_facet.video_assets.add(copied_video)
#                 copied_facet.save()
#
#
#     return redirect('network_stories')


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
