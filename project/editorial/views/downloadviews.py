""" Download views for editorial app. """

# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponse
from django.utils import timezone
from django.views.generic import TemplateView , UpdateView, DetailView
from django.views.decorators.csrf import csrf_exempt
from cStringIO import StringIO
from zipfile import ZipFile
import datetime
import json

from editorial.forms import StoryDownloadForm

from editorial.models import (
    Story,
    WebFacet,
    PrintFacet,
    AudioFacet,
    VideoFacet,
    ImageAsset,
    DocumentAsset,
    AudioAsset,
)

#TODO Refactor queries for better use of Django query methods

#----------------------------------------------------------------------#
#   Download View
#----------------------------------------------------------------------#

def create_download(request, pk):
    """ Process download form to collect objects and create download file."""

    # get the story and associated facets no matter what options are selected
    story_id = request.POST.get('story')
    story = get_object_or_404(Story, id=pk)
    story_txt = Story.get_story_download(story)
    select_all_images = []
    image_txt = ""
    select_all_documents = []
    document_txt = ""
    select_all_audio = []
    audio_txt = ""

    if story.webfacetstory.all():
        webfacet = story.webfacetstory.all()[0]
        webfacet_images = WebFacet.get_webfacet_images(webfacet)
        webfacet_documents = WebFacet.get_webfacet_documents(webfacet)
        webfacet_audio = WebFacet.get_webfacet_audio(webfacet)
        select_all_images.extend(webfacet_images)
        select_all_documents.extend(webfacet_documents)
        select_all_audio.extend(webfacet_audio)
        webfacet_txt = WebFacet.get_webfacet_download(webfacet)
    if story.printfacetstory.all():
        printfacet = story.printfacetstory.all()[0]
        printfacet_images = PrintFacet.get_printfacet_images(printfacet)
        printfacet_documents = PrintFacet.get_printfacet_documents(printfacet)
        printfacet_audio = PrintFacet.get_printfacet_audio(printfacet)
        select_all_images.extend(printfacet_images)
        select_all_documents.extend(printfacet_documents)
        select_all_audio.extend(printfacet_audio)
        printfacet_txt = PrintFacet.get_printfacet_download(printfacet)
    if story.audiofacetstory.all():
        audiofacet = story.audiofacetstory.all()[0]
        audiofacet_images = AudioFacet.get_audiofacet_images(audiofacet)
        audiofacet_documents = AudioFacet.get_audiofacet_documents(audiofacet)
        audiofacet_audio = AudioFacet.get_audiofacet_audio(audiofacet)
        select_all_images.extend(audiofacet_images)
        select_all_documents.extend(audiofacet_documents)
        select_all_audio.extend(audiofacet_audio)
        audiofacet_txt = AudioFacet.get_audiofacet_download(audiofacet)
    if story.videofacetstory.all():
        videofacet = story.videofacetstory.all()[0]
        videofacet_images = VideoFacet.get_videofacet_images(videofacet)
        videofacet_documents = VideoFacet.get_videofacet_documents(videofacet)
        videofacet_audio = VideoFacet.get_videofacet_audio(videofacet)
        select_all_images.extend(videofacet_images)
        select_all_documents.extend(videofacet_documents)
        select_all_audio.extend(videofacet_audio)
        videofacet_txt = VideoFacet.get_videofacet_download(videofacet)

    # Set up zip file
    fp = StringIO()
    z = ZipFile(fp, mode="w")
    # Always Zip up story meta
    z.writestr("story.txt", story_txt)

    # ------------------------------ #
    #          IF SELECT ALL         #
    # ------------------------------ #
    # if select_all is chosen, then all items will be downloaded
    select_all = request.POST.get('select_all')
    print "select all: ", select_all

    if select_all:
        # Zip up all facets and assets including story metadata
        if story.webfacetstory.all():
            z.writestr("webstory.txt", webfacet_txt)
        if story.printfacetstory.all():
            z.writestr("printstory.txt", printfacet_txt)
        if story.audiofacetstory.all():
            z.writestr("audiostory.txt", audiofacet_txt)
        if story.videofacetstory.all():
            z.writestr("videostory.txt", videofacet_txt)
        for image in select_all_images:
            z.writestr("{image}.jpg".format(image=image.asset_title), image.photo.read())
            new_info = ImageAsset.get_image_download_info(image)
            image_txt += new_info
        for document in select_all_documents:
            if document.doc_type == "PDF":
                z.writestr("{document}.pdf".format(document=document.asset_title), document.document.read())
                new_info = DocumentAsset.get_document_download_info(document)
                document_txt += new_info
            if document.doc_type == "WORD":
                z.writestr("{document}.docx".format(document=document.asset_title), document.document.read())
                new_info = DocumentAsset.get_document_download_info(document)
                document_txt += new_info
            if document.doc_type == "TXT":
                z.writestr("{document}.txt".format(document=document.asset_title), document.document.read())
                new_info = DocumentAsset.get_document_download_info(document)
                document_txt += new_info
            if document.doc_type == "CSV":
                z.writestr("{document}.csv".format(document=document.asset_title), document.document.read())
                new_info = DocumentAsset.get_document_download_info(document)
                document_txt += new_info
            if document.doc_type == "XLS":
                z.writestr("{document}.xls".format(document=document.asset_title), document.document.read())
                new_info = DocumentAsset.get_document_download_info(document)
                document_txt += new_info
        for audiofile in select_all_audio:
            if audiofile.audio_type == "MP3":
                z.writestr("{audiofile}.mp3".format(audiofile=document.asset_title), audiofile.audio.read())
                new_info = AudioAsset.get_audio_download_info(audiofile)
                audio_txt += new_info
            if audiofile.audio_type == "WAV":
                z.writestr("{audiofile}.wav".format(audiofile=document.asset_title), audiofile.audio.read())
                new_info = AudioAsset.get_audio_download_info(audiofile)
                audio_txt += new_info

    # user can also select download all items associated with certain facets
    # ------------------------------ #
    #        IF WEBFACET ALL         #
    # ------------------------------ #
    webfacet_sa = request.POST.get('webfacet_sa')
    print "WSA: ", webfacet_sa

    if webfacet_sa:
        # Zip up story meta, webfacet content and webfacet images
        if story.webfacetstory.all():
            z.writestr("webstory.txt", webfacet_txt)
        for image in webfacet_images:
            z.writestr("{image}.jpg".format(image=image.asset_title), image.photo.read())
            new_info = ImageAsset.get_image_download_info(image)
            image_txt += new_info
        for document in webfacet_documents:
            if document.doc_type == "PDF":
                z.writestr("{document}.pdf".format(document=document.asset_title), document.document.read())
                new_info = DocumentAsset.get_document_download_info(document)
                document_txt += new_info
            if document.doc_type == "WORD":
                z.writestr("{document}.docx".format(document=document.asset_title), document.document.read())
                new_info = DocumentAsset.get_document_download_info(document)
                document_txt += new_info
            if document.doc_type == "TXT":
                z.writestr("{document}.txt".format(document=document.asset_title), document.document.read())
                new_info = DocumentAsset.get_document_download_info(document)
                document_txt += new_info
            if document.doc_type == "CSV":
                z.writestr("{document}.csv".format(document=document.asset_title), document.document.read())
                new_info = DocumentAsset.get_document_download_info(document)
                document_txt += new_info
            if document.doc_type == "XLS":
                z.writestr("{document}.xls".format(document=document.asset_title), document.document.read())
                new_info = DocumentAsset.get_document_download_info(document)
                document_txt += new_info
        for audiofile in webfacet_audio:
            if audiofile.audio_type == "MP3":
                z.writestr("{audiofile}.mp3".format(audiofile=document.asset_title), audiofile.audio.read())
                new_info = AudioAsset.get_audio_download_info(audiofile)
                audio_txt += new_info
            if audiofile.audio_type == "WAV":
                z.writestr("{audiofile}.wav".format(audiofile=document.asset_title), audiofile.audio.read())
                new_info = AudioAsset.get_audio_download_info(audiofile)
                audio_txt += new_info

    # ------------------------------ #
    #       IF PRINTFACET ALL        #
    # ------------------------------ #
    printfacet_sa = request.POST.get('printfacet_sa')
    print "PSA: ", printfacet_sa

    if printfacet_sa:
        # Zip up story meta, printfacet content and printfacet images
        if story.printfacetstory.all():
            z.writestr("printstory.txt", printfacet_txt)
        for image in printfacet_images:
            z.writestr("{image}.jpg".format(image=image.asset_title), image.photo.read())
            new_info = ImageAsset.get_image_download_info(image)
            image_txt += new_info
        for document in printfacet_documents:
            if document.doc_type == "PDF":
                z.writestr("{document}.pdf".format(document=document.asset_title), document.document.read())
                new_info = DocumentAsset.get_document_download_info(document)
                document_txt += new_info
            if document.doc_type == "WORD":
                z.writestr("{document}.docx".format(document=document.asset_title), document.document.read())
                new_info = DocumentAsset.get_document_download_info(document)
                document_txt += new_info
            if document.doc_type == "TXT":
                z.writestr("{document}.txt".format(document=document.asset_title), document.document.read())
                new_info = DocumentAsset.get_document_download_info(document)
                document_txt += new_info
            if document.doc_type == "CSV":
                z.writestr("{document}.csv".format(document=document.asset_title), document.document.read())
                new_info = DocumentAsset.get_document_download_info(document)
                document_txt += new_info
            if document.doc_type == "XLS":
                z.writestr("{document}.xls".format(document=document.asset_title), document.document.read())
                new_info = DocumentAsset.get_document_download_info(document)
                document_txt += new_info
        for audiofile in printfacet_audio:
            if audiofile.audio_type == "MP3":
                z.writestr("{audiofile}.mp3".format(audiofile=document.asset_title), audiofile.audio.read())
                new_info = AudioAsset.get_audio_download_info(audiofile)
                audio_txt += new_info
            if audiofile.audio_type == "WAV":
                z.writestr("{audiofile}.wav".format(audiofile=document.asset_title), audiofile.audio.read())
                new_info = AudioAsset.get_audio_download_info(audiofile)
                audio_txt += new_info


    # ------------------------------ #
    #       IF AUDIOFACET ALL        #
    # ------------------------------ #
    audiofacet_sa = request.POST.get('audiofacet_sa')
    print "ASA: ", audiofacet_sa

    if audiofacet_sa:
        # Zip up story meta, audiofacet content and audiofacet images
        if story.audiofacetstory.all():
            z.writestr("audiostory.txt", audiofacet_txt)
        for image in audiofacet_images:
            z.writestr("{image}.jpg".format(image=image.asset_title), image.photo.read())
            new_info = ImageAsset.get_image_download_info(image)
            image_txt += new_info
        for document in audiofacet_documents:
            if document.doc_type == "PDF":
                z.writestr("{document}.pdf".format(document=document.asset_title), document.document.read())
                new_info = DocumentAsset.get_document_download_info(document)
                document_txt += new_info
            if document.doc_type == "WORD":
                z.writestr("{document}.docx".format(document=document.asset_title), document.document.read())
                new_info = DocumentAsset.get_document_download_info(document)
                document_txt += new_info
            if document.doc_type == "TXT":
                z.writestr("{document}.txt".format(document=document.asset_title), document.document.read())
                new_info = DocumentAsset.get_document_download_info(document)
                document_txt += new_info
            if document.doc_type == "CSV":
                z.writestr("{document}.csv".format(document=document.asset_title), document.document.read())
                new_info = DocumentAsset.get_document_download_info(document)
                document_txt += new_info
            if document.doc_type == "XLS":
                z.writestr("{document}.xls".format(document=document.asset_title), document.document.read())
                new_info = DocumentAsset.get_document_download_info(document)
                document_txt += new_info
        for audiofile in audiofacet_audio:
            if audiofile.audio_type == "MP3":
                z.writestr("{audiofile}.mp3".format(audiofile=document.asset_title), audiofile.audio.read())
                new_info = AudioAsset.get_audio_download_info(audiofile)
                audio_txt += new_info
            if audiofile.audio_type == "WAV":
                z.writestr("{audiofile}.wav".format(audiofile=document.asset_title), audiofile.audio.read())
                new_info = AudioAsset.get_audio_download_info(audiofile)
                audio_txt += new_info


    # ------------------------------ #
    #       IF VIDEOFACET ALL        #
    # ------------------------------ #
    videofacet_sa = request.POST.get('videofacet_sa')
    print "VDS: ", videofacet_sa

    if videofacet_sa:
        # Zip up story meta, audiofacet content and audiofacet images
        if story.videofacetstory.all():
            z.writestr("videostory.txt", videofacet_txt)
        for image in videofacet_images:
            z.writestr("{image}.jpg".format(image=image.asset_title), image.photo.read())
            new_info = ImageAsset.get_image_download_info(image)
            image_txt += new_info
        for document in videofacet_documents:
            if document.doc_type == "PDF":
                z.writestr("{document}.pdf".format(document=document.asset_title), document.document.read())
                new_info = DocumentAsset.get_document_download_info(document)
                document_txt += new_info
            if document.doc_type == "WORD":
                z.writestr("{document}.docx".format(document=document.asset_title), document.document.read())
                new_info = DocumentAsset.get_document_download_info(document)
                document_txt += new_info
            if document.doc_type == "TXT":
                z.writestr("{document}.txt".format(document=document.asset_title), document.document.read())
                new_info = DocumentAsset.get_document_download_info(document)
                document_txt += new_info
            if document.doc_type == "CSV":
                z.writestr("{document}.csv".format(document=document.asset_title), document.document.read())
                new_info = DocumentAsset.get_document_download_info(document)
                document_txt += new_info
            if document.doc_type == "XLS":
                z.writestr("{document}.xls".format(document=document.asset_title), document.document.read())
                new_info = DocumentAsset.get_document_download_info(document)
                document_txt += new_info
        for audiofile in videofacet_audio:
            if audiofile.audio_type == "MP3":
                z.writestr("{audiofile}.mp3".format(audiofile=document.asset_title), audiofile.audio.read())
                new_info = AudioAsset.get_audio_download_info(audiofile)
                audio_txt += new_info
            if audiofile.audio_type == "WAV":
                z.writestr("{audiofile}.wav".format(audiofile=document.asset_title), audiofile.audio.read())
                new_info = AudioAsset.get_audio_download_info(audiofile)
                audio_txt += new_info


    # if not select all OR facet select all, then user chooses the facet and the images
    # ------------------------------ #
    #      IF WEBFACET SPECIFIC      #
    # ------------------------------ #
    webfacet_only = request.POST.get('webfacet')
    if webfacet_only:
        z.writestr("webstory.txt", webfacet_txt)

    # ------------------------------ #
    #    IF PRINTFACET SPECIFIC      #
    # ------------------------------ #
    printfacet_only = request.POST.get('printfacet')
    if printfacet_only:
        z.writestr("printstory.txt", printfacet_txt)

    # ------------------------------ #
    #      IF AUDIOFACET SPECIFIC    #
    # ------------------------------ #
    audiofacet_only = request.POST.get('audiofacet')
    if audiofacet_only:
        z.writestr("audiostory.txt", audiofacet_txt)

    # ------------------------------ #
    #      IF VIDEOFACET SPECIFIC    #
    # ------------------------------ #
    videofacet_only = request.POST.get('videofacet')
    if videofacet_only:
        z.writestr("videostory.txt", videofacet_txt)

    # ------------------------------ #
    #       IF SPECIFIC IMAGES       #
    # ------------------------------ #
    # if not select all or by facet, then user chooses specific images
    images = request.POST.getlist('images')
    images = ImageAsset.objects.filter(pk__in=images)
    print "Images: ", images
    if images:
        for image in images:
            z.writestr("{image}.jpg".format(image=image.asset_title), image.photo.read())
            new_info = ImageAsset.get_image_download_info(image)
            image_txt += new_info

    # ------------------------------ #
    #     IF SPECIFIC DOCUMENTS      #
    # ------------------------------ #
    # if not select all or by facet, then user chooses specific documents
    documents = request.POST.getlist('documents')
    documents = DocumentAsset.objects.filter(pk__in=documents)
    print "Documents: ", documents
    if documents:
        for document in documents:
            if document.doc_type == "PDF":
                z.writestr("{document}.pdf".format(document=document.asset_title), document.document.read())
                new_info = DocumentAsset.get_document_download_info(document)
                document_txt += new_info
            if document.doc_type == "WORD":
                z.writestr("{document}.docx".format(document=document.asset_title), document.document.read())
                new_info = DocumentAsset.get_document_download_info(document)
                document_txt += new_info
            if document.doc_type == "TXT":
                z.writestr("{document}.txt".format(document=document.asset_title), document.document.read())
                new_info = DocumentAsset.get_document_download_info(document)
                document_txt += new_info
            if document.doc_type == "CSV":
                z.writestr("{document}.csv".format(document=document.asset_title), document.document.read())
                new_info = DocumentAsset.get_document_download_info(document)
                document_txt += new_info
            if document.doc_type == "XLS":
                z.writestr("{document}.xls".format(document=document.asset_title), document.document.read())
                new_info = DocumentAsset.get_document_download_info(document)
                document_txt += new_info

    # ------------------------------ #
    #       IF SPECIFIC AUDIO        #
    # ------------------------------ #
    # if not select all or by facet, then user chooses specific audiofiles

    audiofiles = request.POST.getlist('audiofiles')
    audiofiles = AudioAsset.objects.filter(pk__in=audiofiles)
    print "Audiofiles: ", audiofiles
    if audiofiles:
        for audiofile in audiofiles:
            if audiofile.audio_type == "MP3":
                z.writestr("{audiofile}.mp3".format(audiofile=document.asset_title), audiofile.audio.read())
                new_info = AudioAsset.get_audio_download_info(audiofile)
                audio_txt += new_info
            if audiofile.audio_type == "WAV":
                z.writestr("{audiofile}.wav".format(audiofile=document.asset_title), audiofile.audio.read())
                new_info = AudioAsset.get_audio_download_info(audiofile)
                audio_txt += new_info

    # ------------------------------ #
    #         Create download        #
    # ------------------------------ #
    #Take the final version of image_txt and write it.
    z.writestr("image.txt", image_txt)
    z.writestr("document.txt", document_txt)
    z.writestr("audio.txt", audio_txt)

    z.close()
    fp.seek(0)
    response = HttpResponse(fp, content_type='application/zip')
    fp.close()


    return response
