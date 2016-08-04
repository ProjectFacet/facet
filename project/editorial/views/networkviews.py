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
from django.core.serializers.json import DjangoJSONEncoder
import datetime
import json

from editorial.forms import (
    NetworkForm,
    AddToNetworkForm,
    InviteToNetworkForm,
    NetworkCommentForm,
    NetworkNoteForm,)

from editorial.models import (
    User,
    Organization,
    Network,
    Story,
    WebFacet,
    PrintFacet,
    AudioFacet,
    VideoFacet,
    ImageAsset,
    DocumentAsset,
    AudioAsset,
    VideoAsset,
    Comment,
    PrivateMessage,
    Discussion,
    StoryCopyDetail,
    WebFacetCopyDetail,
    PrintFacetCopyDetail,
    AudioFacetCopyDetail,
    VideoFacetCopyDetail,
    ImageAssetCopyDetail,
    DocumentAssetCopyDetail,
    AudioAssetCopyDetail,
    VideoAssetCopyDetail,
    NetworkNote,)


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
            network.organizations.add(owner_org)
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
    network_list = Organization.get_org_networks(organization)

    return render(request, 'editorial/networklist.html', {'network_list': network_list})


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

    organization = request.user.organization
    networks = Organization.get_org_networks(organization)

    shared_networkstories = []
    for network in networks:
        stories = Network.get_network_shared_stories(network)
        shared_networkstories.extend(stories)
    shared_networkstories = [story for story in shared_networkstories if story.organization != organization]
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
        story_copy_record = StoryCopyDetail.objects.create_story_copy_record(
            original_org=original_org,
            partner=partner,
            original_story=original_story,
            partner_story=copied_story
            )
        print "Story Copied"

        # Create copy of facets if they exist
        # Copy the WebFacet
        if original_webfacet:
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
            print "Webfacet Copied"

            #create copy of webfacet images
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
                #add image to copied webfacet
                copied_webfacet.image_assets.add(copied_image)
                copied_webfacet.save()

            #create copy of webfacet documents
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
                #add document to copied webfacet
                copied_webfacet.document_assets.add(copied_document)
                copied_webfacet.save()


            #create copy of webfacet audio
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
                #add audio to copied webfacet
                copied_webfacet.audio_assets.add(copied_audio)
                copied_webfacet.save()

            #create copy of webfacet video
            # original_webfacet_video = WebFacet.get_webfacet_video(original_webfacet[0])
            # for video in original_webfacet_videos:
            #     copied_video = VideoAsset.copy_video(video)
            #     copied_video.owner = user
            #     copied_video.organization = organization
            #     copied_video.save()
            #     videoasset_copy_record = VideoAssetCopyDetail.objects.create_videoasset_copy_record(
            #         original_org=original_org,
            #         partner=partner,
            #         original_videoasset=video,
            #         partner_videoasset=copied_video
            #     )
            #     #add video to copied webfacet
            #     copied_webfacet.video_assets.add(copied_video)
            #     copied_webfacet.save()

        # Copy the PrintFacet
        if original_printfacet:
            print original_printfacet[0]
            copied_printfacet = PrintFacet.copy_printfacet(original_printfacet[0])
            copied_printfacet.story = copied_story
            copied_printfacet.owner = user
            copied_printfacet.organization = organization
            copied_printfacet.save()
            printfacet_copy_record = PrintFacetCopyDetail.objects.create_printfacet_copy_record(
                original_org=original_org,
                partner=partner,
                original_printfacet=original_printfacet,
                partner_printfacet=copied_printfacet
            )
            print "Printfacet Copied"

            #create copy of printfacet images
            original_printfacet_images = PrintFacet.get_printfacet_images(original_printfacet[0])
            for image in original_printfacet_images:
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
                #add image to copied printfacet
                copied_printfacet.image_assets.add(copied_image)
                copied_printfacet.save()

            #create copy of printfacet documents
            original_printfacet_documents = PrintFacet.get_printfacet_documents(original_printfacet[0])
            for document in original_printfacet_documents:
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
                #add document to copied printfacet
                copied_printfacet.document_assets.add(copied_document)
                copied_printfacet.save()


            #create copy of printfacet audio
            original_printfacet_audiofiles = PrintFacet.get_printfacet_audio(original_printfacet[0])
            for audio in original_printfacet_audios:
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
                #add audio to copied printfacet
                copied_printfacet.audio_assets.add(copied_audio)
                copied_printfacet.save()

            # create copy of printfacet video
            # original_printfacet_video = PrintFacet.get_printfacet_video(original_printfacet[0])
            # for video in original_printfacet_videos:
            #     copied_video = VideoAsset.copy_video(video)
            #     copied_video.owner = user
            #     copied_video.organization = organization
            #     copied_video.save()
            #     videoasset_copy_record = VideoAssetCopyDetail.objects.create_videoasset_copy_record(
            #         original_org=original_org,
            #         partner=partner,
            #         original_videoasset=video,
            #         partner_videoasset=copied_video
            #     )
            #     #add video to copied printfacet
            #     copied_printfacet.video_assets.add(copied_video)
            #     copied_printfacet.save()

        # Copy the AudioFacet
        if original_audiofacet:
            print original_audiofacet[0]
            copied_audiofacet = AudioFacet.copy_audiofacet(original_audiofacet[0])
            copied_audiofacet.story = copied_story
            copied_audiofacet.owner = user
            copied_audiofacet.organization = organization
            copied_audiofacet.save()
            audiofacet_copy_record = AudioFacetCopyDetail.objects.create_audiofacet_copy_record(
                original_org=original_org,
                partner=partner,
                original_audiofacet=original_audiofacet,
                partner_audiofacet=copied_audiofacet
            )
            print "Audiofacet Copied"

            #create copy of audiofacet images
            original_audiofacet_images = AudioFacet.get_audiofacet_images(original_audiofacet[0])
            for image in original_audiofacet_images:
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
                #add image to copied audiofacet
                copied_audiofacet.image_assets.add(copied_image)
                copied_audiofacet.save()

            #create copy of audiofacet documents
            original_audiofacet_documents = AudioFacet.get_audiofacet_documents(original_audiofacet[0])
            for document in original_audiofacet_documents:
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
                #add document to copied audiofacet
                copied_audiofacet.document_assets.add(copied_document)
                copied_audiofacet

            #create copy of audiofacet audio
            original_audiofacet_audiofiles = AudioFacet.get_audiofacet_audio(original_audiofacet[0])
            for audio in original_audiofacet_audios:
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
                #add audio to copied audiofacet
                copied_audiofacet.audio_assets.add(copied_audio)
                copied_audiofacet.save()

            # create copy of audiofacet video
            # original_audiofacet_video = AudioFacet.get_audiofacet_video(original_audiofacet[0])
            # for video in original_audiofacet_videos:
            #     copied_video = VideoAsset.copy_video(video)
            #     copied_video.owner = user
            #     copied_video.organization = organization
            #     copied_video.save()
            #     videoasset_copy_record = VideoAssetCopyDetail.objects.create_videoasset_copy_record(
            #         original_org=original_org,
            #         partner=partner,
            #         original_videoasset=video,
            #         partner_videoasset=copied_video
            #     )
            #     #add video to copied audiofacet
            #     copied_audiofacet.video_assets.add(copied_video)
            #     copied_audiofacet.save()

        # Copy the VideoFacet
        if original_videofacet:
            print original_videofacet[0]
            copied_videofacet = VideoFacet.copy_videofacet(original_videofacet[0])
            copied_videofacet.story = copied_story
            copied_videofacet.owner = user
            copied_videofacet.organization = organization
            copied_videofacet.save()
            videofacet_copy_record = VideoFacetCopyDetail.objects.create_videofacet_copy_record(
                original_org=original_org,
                partner=partner,
                original_videofacet=original_videofacet,
                partner_videofacet=copied_videofacet
            )
            print "Videofacet Copied"


            #create copy of videofacet images
            original_videofacet_images = VideoFacet.get_videofacet_images(original_videofacet[0])
            for image in original_videofacet_images:
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
                #add image to copied videofacet
                partner_videofacet.image_assets.add(copied_image)
                partner_videofacet.save()

            #create copy of videofacet documents
            original_videofacet_documents = VideoFacet.get_videofacet_documents(original_videofacet[0])
            for document in original_videofacet_documents:
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
                #add document to copied videofacet
                partner_documentasset.document_assets.add(copied_document)
                partner_documentasset.save()


            #create copy of videofacet audio
            original_videofacet_audiofiles = VideoFacet.get_videofacet_audio(original_videofacet[0])
            for audio in original_videofacet_audiofiles:
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
                #add audio to copied audiofacet
                partner_audioasset.audio_assets.add(copied_audio)
                partner_audioasset.save()

            # create copy of videofacet video
            # original_videofacet_video = VideoFacet.get_videofacet_video(original_videofacet[0])
            # for video in original_videofacet_videos:
            #     copied_video = VideoAsset.copy_video(video)
            #     copied_video.owner = user
            #     copied_video.organization = organization
            #     copied_video.save()
            #     videoasset_copy_record = VideoAssetCopyDetail.objects.create_videoasset_copy_record(
            #         original_org=original_org,
            #         partner=partner,
            #         original_videoasset=video,
            #         partner_videoasset=copied_video
            #     )
            #     #add video to copied videofacet
            #     partner_videoasset.video_assets.add(copied_video)
            #     partner_videoasset.save()



    return redirect('network_stories')
