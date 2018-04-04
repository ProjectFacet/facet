""" Download views for editorial app. """

# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponse
from django.utils import timezone
from django.views.generic import TemplateView , UpdateView, DetailView, FormView, View
from django.views.decorators.csrf import csrf_exempt
from cStringIO import StringIO
from zipfile import ZipFile
import datetime
import json
from braces.views import LoginRequiredMixin, FormMessagesMixin
from editorial.views import CustomUserTest

# from editorial.forms import StoryDownloadForm

from editorial.models import (
    Story,
    Facet,
    ImageAsset,
    DocumentAsset,
    AudioAsset,
    VideoAsset
)

#----------------------------------------------------------------------#
#   Download View
#----------------------------------------------------------------------#

class StoryDownloadTemplateView(CustomUserTest, TemplateView):
    """Display form for a story download."""

    template_name = 'editorial/story_download_form.html'

    def test_user(self, user):
        """User must be member of an org."""

        if user.organization:
            return True
        raise PermissionDenied()

    def get_context_data(self, pk):
        story = Story.objects.get(id=pk)
        story_images = story.get_story_images()
        story_documents = story.get_story_documents()
        story_audio = story.get_story_audio()
        story_video = story.get_story_video()
        return {
            'story': story,
            'story_images': story_images,
            'story_documents': story_documents,
            'story_audio': story_audio,
            'story_video': story_video,
        }


# ACCESS: Any org user, or user from an organization that is in collaborate_with
# should be able to download a story
# Contractors should not be able to download
class StoryDownloadProcessView(CustomUserTest, View):
    """Create the download for a story and its facets."""

    def test_user(self, user):
        """User must be member of an org."""

        if user.organization:
            return True
        raise PermissionDenied()

    def post(self, request, pk):
        """ Process download form to collect objects and create download file."""

        # get the story and associated facets no matter what options are selected
        story_id = request.POST.get('story')
        story = get_object_or_404(Story, id=pk)
        story_txt = story.get_story_download()
        select_all_images = story.get_story_images()
        select_all_documents = story.get_story_documents()
        select_all_audio = story.get_story_audio()
        select_all_video = story.get_story_video()
        image_txt = ""
        document_txt = ""
        audio_txt = ""
        video_txt = ""

        # Set up zip file
        fp = StringIO()
        z = ZipFile(fp, mode="w")
        # Always Zip up story meta
        z.writestr("story_detail.txt", story_txt)

        # ------------------------------ #
        #          IF SELECT ALL         #
        # ------------------------------ #
        # if select_all is chosen, then all items will be downloaded
        story_sa_id = request.POST.get('select_all')
        print "STORY ALL: ", story_sa_id

        if story_sa_id:
            story = get_object_or_404(Story, id=story_sa_id)

        if story_sa_id:
            # Zip up all facets and assets including story metadata
            for facet in story.facet_set.all():
                z.writestr("{name}.txt".format(name=facet.name), facet.get_facet_download())

            for image in select_all_images:
                z.writestr("{image}.jpg".format(image=image.title), image.photo.read())
                new_info = image.get_asset_download_info()
                image_txt += new_info
            for document in select_all_documents:
                if document.asset_type == "PDF":
                    z.writestr("{document}.pdf".format(document=document.title), document.document.read())
                    new_info = document.get_asset_download_info()
                    document_txt += new_info
                if document.asset_type == "WORD":
                    z.writestr("{document}.docx".format(document=document.title), document.document.read())
                    new_info = document.get_asset_download_info()
                    document_txt += new_info
                if document.asset_type == "TXT":
                    z.writestr("{document}.txt".format(document=document.title), document.document.read())
                    new_info = document.get_asset_download_info()
                    document_txt += new_info
                if document.asset_type == "CSV":
                    z.writestr("{document}.csv".format(document=document.title), document.document.read())
                    new_info = document.get_asset_download_info()
                    document_txt += new_info
                if document.asset_type == "XLS":
                    z.writestr("{document}.xls".format(document=document.title), document.document.read())
                    new_info = document.get_asset_download_info()
                    document_txt += new_info
            for audiofile in select_all_audio:
                if audiofile.asset_type == "MP3":
                    z.writestr("{audiofile}.mp3".format(audiofile=audiofile.title), audiofile.audio.read())
                    new_info = audiofile.get_asset_download_info()
                    audio_txt += new_info
                if audiofile.asset_type == "WAV":
                    z.writestr("{audiofile}.wav".format(audiofile=audiofile.title), audiofile.audio.read())
                    new_info = audiofile.get_asset_download_info()
                    audio_txt += new_info
            for video in select_all_video:
                if video.asset_type == "YOUTUBE":
                    # text = video.link.encode('utf-8')
                    # title = video.title.encode('utf-8')
                    # z.writestr("{title}_youtube_link.txt".format(title=title), text)
                    new_info = video.get_asset_download_info()
                    video_txt += new_info
                if video.asset_type == "VIMEO":
                    # text = video.link.encode('utf-8')
                    # title = video.title.encode('utf-8')
                    # z.writestr("{title}_vimeo_link.txt".format(title=title), text)
                    new_info = video.get_asset_download_info()
                    video_txt += new_info

        # user can also select download all items associated with specific facets
        # ------------------------------ #
        #        IF FACET ALL         #
        # ------------------------------ #
        facet_sa_id = request.POST.getlist('facet_select_all')

        if facet_sa_id:
            for facet in facet_sa_id:
                facet = get_object_or_404(Facet, id=facet)
                # Zip up story meta, facet content and facet images
                if facet:
                    z.writestr("{name}.txt".format(name=facet.name), facet.get_facet_download())
                for image in facet.image_assets.all():
                    z.writestr("{image}.jpg".format(image=image.title), image.photo.read())
                    new_info = image.get_asset_download_info()
                    image_txt += new_info
                for document in facet.document_assets.all():
                    if document.asset_type == "PDF":
                        z.writestr("{document}.pdf".format(document=document.title), document.document.read())
                        new_info = document.get_asset_download_info()
                        document_txt += new_info
                    if document.asset_type == "WORD":
                        z.writestr("{document}.docx".format(document=document.title), document.document.read())
                        new_info = document.get_asset_download_info()
                        document_txt += new_info
                    if document.asset_type == "TXT":
                        z.writestr("{document}.txt".format(document=document.title), document.document.read())
                        new_info = document.get_asset_download_info()
                        document_txt += new_info
                    if document.asset_type == "CSV":
                        z.writestr("{document}.csv".format(document=document.title), document.document.read())
                        new_info = document.get_asset_download_info()
                        document_txt += new_info
                    if document.asset_type == "XLS":
                        z.writestr("{document}.xls".format(document=document.title), document.document.read())
                        new_info = document.get_asset_download_info()
                        document_txt += new_info
                for audiofile in facet.audio_assets.all():
                    if audiofile.asset_type == "MP3":
                        z.writestr("{audiofile}.mp3".format(audiofile=audiofile.title), audiofile.audio.read())
                        new_info = audiofile.get_asset_download_info()
                        audio_txt += new_info
                    if audiofile.asset_type == "WAV":
                        z.writestr("{audiofile}.wav".format(audiofile=audiofile.title), audiofile.audio.read())
                        new_info = audiofile.get_asset_download_info()
                        audio_txt += new_info
                for video in facet.video_assets.all():
                    if video.asset_type == "YOUTUBE":
                        # text = video.link.encode('utf-8')
                        # title = video.title.encode('utf-8')
                        # z.writestr("{title}_youtube_link.txt".format(title=title), text)
                        new_info = video.get_asset_download_info()
                        video_txt += new_info
                    if video.asset_type == "VIMEO":
                        # text = video.link.encode('utf-8')
                        # title = video.title.encode('utf-8')
                        # z.writestr("{title}_vimeo_link.txt".format(title=title), text)
                        new_info = video.get_asset_download_info()
                        video_txt += new_info


        # if not select all OR facet select all, then user chooses the facet and the images
        # ------------------------------ #
        #      IF FACET SPECIFIC      #
        # ------------------------------ #
        facet_sp_id = request.POST.getlist('facet_specific_content')
        print "FACET SPECIFIC"

        if facet_sp_id:
            for facet_id in facet_sp_id:
                facet = get_object_or_404(Facet, id=facet_id)
                z.writestr("{name}.txt".format(name=facet.name), facet.get_facet_download())


        # ------------------------------ #
        #       IF SPECIFIC IMAGES       #
        # ------------------------------ #
        # if not select all or by facet, then user chooses specific images
        images = request.POST.getlist('images')
        print "SPECIFIC IMAGES: ", images

        images = ImageAsset.objects.filter(pk__in=images)
        print "IMAGES: ", images

        if images:
            for image in images:
                z.writestr("{image}.jpg".format(image=image.title), image.photo.read())
                new_info = image.get_asset_download_info()
                image_txt += new_info


        # ------------------------------ #
        #     IF SPECIFIC DOCUMENTS      #
        # ------------------------------ #
        # if not select all or by facet, then user chooses specific documents
        documents = request.POST.getlist('documents')
        print "SPECIFIC DOCUMENTS: ", documents

        documents = DocumentAsset.objects.filter(pk__in=documents)
        print "DOCUMENTS: ", documents

        if documents:
            for document in documents:
                if document.asset_type == "PDF":
                    z.writestr("{document}.pdf".format(document=document.title), document.document.read())
                    new_info = document.get_asset_download_info()
                    document_txt += new_info
                if document.asset_type == "WORD":
                    z.writestr("{document}.docx".format(document=document.title), document.document.read())
                    new_info = document.get_asset_download_info()
                    document_txt += new_info
                if document.asset_type == "TXT":
                    z.writestr("{document}.txt".format(document=document.title), document.document.read())
                    new_info = document.get_asset_download_info()
                    document_txt += new_info
                if document.asset_type == "CSV":
                    z.writestr("{document}.csv".format(document=document.title), document.document.read())
                    new_info = document.get_asset_download_info()
                    document_txt += new_info
                if document.asset_type == "XLS":
                    z.writestr("{document}.xls".format(document=document.title), document.document.read())
                    new_info = document.get_asset_download_info()
                    document_txt += new_info


        # ------------------------------ #
        #       IF SPECIFIC AUDIO        #
        # ------------------------------ #
        # if not select all or by facet, then user chooses specific audiofiles
        audiofiles = request.POST.getlist('audiofiles')
        print "SPECIFIC AUDIO: ", audiofiles

        audiofiles = AudioAsset.objects.filter(pk__in=audiofiles)
        print "AUDIOFILES: ", audiofiles

        if audiofiles:
            for audiofile in audiofiles:
                if audiofile.asset_type == "MP3":
                    z.writestr("{audiofile}.mp3".format(audiofile=audiofile.title), audiofile.audio.read())
                    new_info = audiofile.get_asset_download_info()
                    audio_txt += new_info
                if audiofile.asset_type == "WAV":
                    z.writestr("{audiofile}.wav".format(audiofile=audiofile.title), audiofile.audio.read())
                    new_info = audiofile.get_asset_download_info()
                    audio_txt += new_info


        # ------------------------------ #
        #       IF SPECIFIC VIDEO        #
        # ------------------------------ #
        # if not select all or by facet, then user chooses specific video files
        videos = request.POST.getlist('videofiles')
        print "SPECIFIC VIDEO: ", videos

        videos = VideoAsset.objects.filter(pk__in=videos)
        print "VIDEO: ", videos

        if videos:
            for video in videos:
                if video.asset_type == "YOUTUBE":
                    # text = video.link.encode('utf-8')
                    # title = video.title.encode('utf-8')
                    # z.writestr("{title}_youtube_link.txt".format(title=title), text)
                    new_info = video.get_asset_download_info()
                    video_txt += new_info
                if video.asset_type == "VIMEO":
                    # text = video.link.encode('utf-8')
                    # title = video.title.encode('utf-8')
                    # z.writestr("{title}_vimeo_link.txt".format(title=title), text)
                    new_info = video.get_asset_download_info()
                    video_txt += new_info


        # ------------------------------ #
        #         Create download        #
        # ------------------------------ #
        #Take the final version of asset_txts and write it.
        if image_txt:
            z.writestr("image.txt", image_txt)
        if document_txt:
            z.writestr("document.txt", document_txt)
        if audio_txt:
            z.writestr("audio.txt", audio_txt)
        if video_txt:
            z.writestr("video.txt", video_txt)


        z.close()
        fp.seek(0)
        response = HttpResponse(fp, content_type='application/zip')
        fp.close()


        return response
