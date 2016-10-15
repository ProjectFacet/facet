""" Story views for editorial app.

    editorial/views/storyviews.py
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
    StoryForm,
    WebFacetForm,
    PrintFacetForm,
    AudioFacetForm,
    VideoFacetForm,
    ImageAssetForm,
    AddImageForm,
    DocumentAssetForm,
    AddDocumentForm,
    AudioAssetForm,
    AddAudioForm,
    VideoAssetForm,
    AddVideoForm,
    StoryCommentForm,
    WebFacetCommentForm,
    PrintFacetCommentForm,
    AudioFacetCommentForm,
    VideoFacetCommentForm,
    StoryNoteForm,
    StoryDownloadForm,)

from editorial.models import (
    Organization,
    Series,
    Story,
    WebFacet,
    PrintFacet,
    AudioFacet,
    VideoFacet,
    StoryNote,
    ImageAsset,
    DocumentAsset,
    AudioAsset,
    VideoAsset,
    Comment,
    Discussion,
    StoryNote,)


#----------------------------------------------------------------------#
#   Story Views
#----------------------------------------------------------------------#

def story_list(request):
    """ Displays a filterable table of stories.

    Initial display organizes content by story>facet>est. run date
    Filterable by story name, facet type, facet name, due for edit, est. run date, credit,
    editor, status.
    """

    stories = Story.objects.filter(organization=request.user.organization).exclude(archived=True)

    return render(request, 'editorial/storylist.html', {
        'stories': stories,
        }
    )


def story_new(request):
    """ Create story page. """

    organization = request.user.organization
    org_partners = Organization.get_org_networks(organization)

    series = Series.objects.all()
    if request.method == "POST":
        storyform = StoryForm(request.POST, request=request)
        #import pdb; pdb.set_trace()
        if storyform.is_valid():
            story = storyform.save(commit=False)
            story.owner = request.user
            story.organization = request.user.organization
            discussion = Discussion.objects.create_discussion("STO")
            story.discussion = discussion
            story.save()
            storyform.save_m2m()
            return redirect('story_detail', pk=story.pk)
    else:
        storyform = StoryForm(request=request)
    return render(request, 'editorial/storynew.html', {
        'storyform': storyform,
        'series': series,
        'org_partners': org_partners,
        })


def story_edit(request, pk):
    """ Edit story page. """

    organization = request.user.organization
    org_partners = Organization.get_org_networks(organization)

    story = get_object_or_404(Story, pk=pk)

    if request.method == "POST":
        storyform = StoryForm(data=request.POST, instance=story, request=request)
        if storyform.is_valid():
            storyform.save()
            return redirect('story_detail', pk=story.id)
    else:
        storyform = StoryForm(instance=story, request=request)

    return render(request, 'editorial/storyedit.html', {
        'story': story,
        'storyform': storyform,
        'org_partners': org_partners,
    })


def story_delete(request, pk):
    """Delete a story and it's related objects then redirect user to story list."""

    if request.method == "POST":
        story = get_object_or_404(Story, pk=pk)
        story.delete()

    return redirect('story_list')


def story_team_options_json(request, pk):
    """Returns JSON of team members that can be assigned to a story."""

    story = get_object_or_404(Story, pk=pk)
    print story

    team = Story.get_story_team(story)
    story_team = {}
    for item in team:
        story_team[item.id]=item.credit_name
    print story_team
    return HttpResponse(json.dumps(story_team), content_type = "application/json")





def story_detail(request, pk):
    """ The detail page for a story.

    Displays the story's planning notes, discussion, assets, share and collaboration status
    and sensivity status. From here the user can also see any facets, edit them and add new ones.
    """

    story = get_object_or_404(Story, pk=pk)
    storynoteform = StoryNoteForm()
    storynotes = StoryNote.objects.filter(story=story)
    storycommentform = StoryCommentForm()
    storydiscussion = get_object_or_404(Discussion, id=story.discussion.id)
    storycomments = Comment.objects.filter(discussion=storydiscussion).order_by('-date')
    notes = StoryNote.objects.filter(story=story)
    images = Organization.get_org_image_library(request.user.organization)
    documents = Organization.get_org_document_library(request.user.organization)
    audiofiles = Organization.get_org_audio_library(request.user.organization)
    video = Organization.get_org_video_library(request.user.organization)
    imageform=ImageAssetForm()

# ------------------------------ #
#           webfacet             #
# ------------------------------ #

    # create these here for efficiency
    webform=WebFacetForm(request=request, story=story)
    webcommentform=WebFacetCommentForm()
    webfacet_imageform=ImageAssetForm()
    webfacet_documentform=DocumentAssetForm()
    webfacet_audioform=AudioAssetForm()
    webfacet_videoform=VideoAssetForm()

    try:
        webfacet = get_object_or_404(WebFacet, story=story)
        # print "WEBFACET CREDIT", webfacet.credit.all()

        # IF WEBFACET EXISTS DO ALL OF THE FOLLOWING
        # rebind webform to include webfacet instance
        webform = WebFacetForm(instance=webfacet, request=request, story=story)
        # retrieve discussion and comments
        webfacetdiscussion = get_object_or_404(Discussion, id=webfacet.discussion.id)
        webcomments = Comment.objects.filter(discussion=webfacetdiscussion).order_by('-date')[:3]
        # retrieve history
        webhistory = webfacet.edit_history.all()[:5]
        # update an existing webfacet
        if request.method == "POST":
            # print "WF Try If Post"
            if 'webform' in request.POST:
                # print "WF Try If Post If webform"
                webform = WebFacetForm(data=request.POST, instance=webfacet, request=request, story=story)
                #import pdb; pdb.set_trace()
                if webform.is_valid():
                    # print "WF Try If Post If Webform Valid"
                    webform.save()
                    # print "webfacet updated"
                    return redirect('story_detail', pk=story.pk)
    except:
        # print "WF Except"
    # except WebFacet.DoesNotExist:
        # display form and save a new webfacet
        webcomments = []
        webhistory = []
        if request.method == "POST":
            # print "WF Except Post"
            if 'webform' in request.POST:
                # print "WF Except Post If webform"
                webform = WebFacetForm(data=request.POST, request=request, story=story)
                if webform.is_valid():
                    # #import pdb; pdb.set_trace()
                    # print "WF Except Post If webform Valid"
                    webfacet = webform.save(commit=False)
                    # print "webfacet = webform.save(commit=False)"
                    webfacet.story = story
                    webfacet.owner = request.user
                    webfacet.organization = request.user.organization
                    webfacet.creation_date = timezone.now()
                    discussion = Discussion.objects.create_discussion("WF")
                    webfacet.discussion = discussion
                    webfacet.save()
                    webform.save_m2m()
                    # print "webfacet created"
                    # create history of the webfacet
                    webhistory = webfacet.edit_history.all()[:5]
                    return redirect('story_detail', pk=story.pk)

# ------------------------------ #
#           printfacet           #
# ------------------------------ #

    # create these here for efficiency
    printform=PrintFacetForm(request=request, story=story)
    printcommentform=PrintFacetCommentForm()
    printfacet_imageform=ImageAssetForm()
    printfacet_documentform=DocumentAssetForm()
    printfacet_audioform=AudioAssetForm()

    try:
        # print "PF Try"
        printfacet = get_object_or_404(PrintFacet, story=story)
        # IF PRINTFACET EXISTS DO ALL OF THE FOLLOWING
        printform = PrintFacetForm(instance=printfacet, request=request, story=story)
        # retrieve discussion and comments
        printfacetdiscussion = get_object_or_404(Discussion, id=printfacet.discussion.id)
        printcomments = Comment.objects.filter(discussion=printfacetdiscussion).order_by('-date')[:3]
        # retrieve history
        printhistory = printfacet.edit_history.all()[:5]
        # update an existing printfacet
        if request.method == "POST":
            # print "PF Try If Post"
            if 'printform' in request.POST:
                # print "PF Try If Post If printform"
                #import pdb; pdb.set_trace()
                printform = PrintFacetForm(data=request.POST, instance=printfacet, request=request, story=story)
                if printform.is_valid():
                    # print "PF Try If Post If printform Valid"
                    printform.save()
                    # print "printfacet updated"
                    return redirect('story_detail', pk=story.pk)
    except:
        # print "PF Except"
    # except PrintFacet.DoesNotExist:
        # display form and save a new printfacet
        printcomments = []
        printhistory = []
        if request.method == "POST":
            # print "PF Except If Post"
            if 'printform' in request.POST:
                # print "PF Except If Post If printform"
                # #import pdb; pdb.set_trace()
                printform = PrintFacetForm(data=request.POST, request=request, story=story)
                if printform.is_valid():
                    # print "PF Except If Post If printform Valid"
                    printfacet = printform.save(commit=False)
                    # print "printfacet = printform.save(commit=False)"
                    printfacet.story = story
                    printfacet.owner = request.user
                    printfacet.organization = request.user.organization
                    printfacet.creation_date = timezone.now()
                    discussion = Discussion.objects.create_discussion("WF")
                    printfacet.discussion = discussion
                    printfacet.save()
                    printform.save_m2m()
                    # print "printfacet created"
                    # create history of the printfacet
                    printhistory = printfacet.edit_history.all()[:5]
                    return redirect('story_detail', pk=story.pk)

# ------------------------------ #
#           audiofacet           #
# ------------------------------ #

    # create these here for efficiency
    audioform=AudioFacetForm(request=request, story=story)
    audiocommentform=AudioFacetCommentForm()
    audiofacet_imageform=ImageAssetForm()
    audiofacet_documentform=DocumentAssetForm()
    audiofacet_audioform=AudioAssetForm()

    try:
        audiofacet = get_object_or_404(AudioFacet, story=story)
        # print "AUDIOFACET CREDIT: ", audiofacet.credit.all()

        # IF WEBFACET EXISTS DO ALL OF THE FOLLOWING
        audioform = AudioFacetForm(instance=audiofacet, request=request, story=story)
        # retrieve discussion and comments
        audiofacetdiscussion = get_object_or_404(Discussion, id=audiofacet.discussion.id)
        audiocomments = Comment.objects.filter(discussion=audiofacetdiscussion).order_by('-date')[:3]
        # retrieve history
        audiohistory = audiofacet.edit_history.all()[:5]
        # update an existing audiofacet
        if request.method == "POST":
            # print "AF Try If Post"
            if 'audioform' in request.POST:
                # print "AF Try If Post If Audioform"
                # #import pdb; pdb.set_trace()
                audioform = AudioFacetForm(data=request.POST, instance=audiofacet, request=request, story=story)
                if audioform.is_valid():
                    # print "AF Try If Post If Audioform Valid"
                    audioform.save()
                    # print "audiofacet updated"
                    return redirect('story_detail', pk=story.pk)
    except:
        # print "AF Except"
    # except AudioFacet.DoesNotExist:
        # display form and save a new audiofacet
        audiocomments = []
        audiohistory = []
        if request.method == "POST":
            # print "AF Except If Post"
            if 'audioform' in request.POST:
                # print "AF Except If Post If Audioform"
                # #import pdb; pdb.set_trace()
                audioform = AudioFacetForm(data=request.POST, request=request, story=story)
                if audioform.is_valid():
                    # print "AF Except If Post If Audioform Valid"
                    audiofacet = audioform.save(commit=False)
                    # print "audiofacet = audioform.save(commit=False)"
                    audiofacet.story = story
                    audiofacet.owner = request.user
                    audiofacet.organization = request.user.organization
                    audiofacet.creation_date = timezone.now()
                    discussion = Discussion.objects.create_discussion("WF")
                    audiofacet.discussion = discussion
                    audiofacet.save()
                    audioform.save_m2m()
                    # print "audiofacet created"
                    # create history of the audiofacet
                    audiohistory = audiofacet.edit_history.all()[:5]
                    return redirect('story_detail', pk=story.pk)

# ------------------------------ #
#           videofacet           #
# ------------------------------ #

    # create these here for efficiency
    videoform=VideoFacetForm(request=request, story=story)
    videocommentform=VideoFacetCommentForm()
    videofacet_imageform=ImageAssetForm()
    videofacet_documentform=DocumentAssetForm()
    videofacet_audioform=AudioAssetForm()

    try:
        # print "VF Try"
        videofacet = get_object_or_404(VideoFacet, story=story)
        # IF WEBFACET EXISTS DO ALL OF THE FOLLOWING
        videoform = VideoFacetForm(instance=videofacet, request=request, story=story)
        # retrieve discussion and comments
        videofacetdiscussion = get_object_or_404(Discussion, id=videofacet.discussion.id)
        videocomments = Comment.objects.filter(discussion=videofacetdiscussion).order_by('-date')[:3]
        # retrieve history
        videohistory = videofacet.edit_history.all()[:5]
        # update an existing videofacet
        if request.method == "POST":
            # print "VF Try If Post"
            if 'videoform' in request.POST:
                # print "VF Try If Post If Videoform"
                # # #import pdb; pdb.set_trace()
                videoform = VideoFacetForm(data=request.POST, instance=videofacet, request=request, story=story)
                if videoform.is_valid():
                    # print "VF Try If Post If Videoform Valid"
                    videoform.save()
                    # print "videofacet updated"
                    return redirect('story_detail', pk=story.pk)
    except:
        # print "VF Except If Post If Videoform Valid"
    # except VideoFacet.DoesNotExist:
        # display form and save a new videofacet
        videocomments = []
        videohistory = []
        if request.method == "POST":
            # print "VF Except If Post"
            if 'videoform' in request.POST:
                # print "VF Except If Post If Videoform"
                videoform = VideoFacetForm(data=request.POST, request=request, story=story)
                if videoform.is_valid():
                    # #import pdb; pdb.set_trace()
                    # print "VF Except If Post If Videoform Valid"
                    videofacet = videoform.save(commit=False)
                    # print "videofacet = videoform.save(commit=False)"
                    videofacet.story = story
                    videofacet.owner = request.user
                    videofacet.organization = request.user.organization
                    videofacet.creation_date = timezone.now()
                    discussion = Discussion.objects.create_discussion("VF")
                    videofacet.discussion = discussion
                    videofacet.save()
                    videoform.save_m2m()
                    # print "videofacet created"
                    # create history of the videofacet
                    videohistory = videofacet.edit_history.all()[:5]
                    return redirect('story_detail', pk=story.pk)

    # ------------------------------ #
    #        Download Options        #
    # ------------------------------ #
    if story.webfacetstory.all():
        webfacet = get_object_or_404(WebFacet, story=story)
        webfacet_images = WebFacet.get_webfacet_images(webfacet)
        webfacet_documents = WebFacet.get_webfacet_documents(webfacet)
        webfacet_audio = WebFacet.get_webfacet_audio(webfacet)
        webfacet_video = WebFacet.get_webfacet_video(webfacet)
    else:
        webfacet_images = []
        webfacet_documents = []
        webfacet_audio = []
        webfacet_video = []

    if story.printfacetstory.all():
        printfacet = get_object_or_404(PrintFacet, story=story)
        printfacet_images = PrintFacet.get_printfacet_images(printfacet)
        printfacet_documents = PrintFacet.get_printfacet_documents(printfacet)
        printfacet_audio = PrintFacet.get_printfacet_audio(printfacet)
        printfacet_video = PrintFacet.get_printfacet_video(printfacet)
    else:
        printfacet_images = []
        printfacet_documents = []
        printfacet_audio = []
        printfacet_video = []

    if story.audiofacetstory.all():
        audiofacet = get_object_or_404(AudioFacet, story=story)
        audiofacet_images = AudioFacet.get_audiofacet_images(audiofacet)
        audiofacet_documents = AudioFacet.get_audiofacet_documents(audiofacet)
        audiofacet_audio = AudioFacet.get_audiofacet_audio(audiofacet)
        audiofacet_video = AudioFacet.get_audiofacet_video(audiofacet)
    else:
        audiofacet_images = []
        audiofacet_documents = []
        audiofacet_audio = []
        audiofacet_video = []

    if story.videofacetstory.all():
        videofacet = get_object_or_404(VideoFacet, story=story)
        videofacet_images = VideoFacet.get_videofacet_images(videofacet)
        videofacet_documents = VideoFacet.get_videofacet_documents(videofacet)
        videofacet_audio = VideoFacet.get_videofacet_audio(videofacet)
        videofacet_video = VideoFacet.get_videofacet_video(videofacet)
    else:
        videofacet_images = []
        videofacet_documents = []
        videofacet_audio = []
        videofacet_video = []

    storydownloadform = StoryDownloadForm(story=story)

    return render(request, 'editorial/storydetail.html', {
        'story': story,
        'storydownloadform': storydownloadform,
        'storynoteform': storynoteform,
        'storynotes': storynotes,
        'storycommentform': storycommentform,
        'storycomments': storycomments,
        'webform': webform,
        'webcomments': webcomments,
        'webhistory': webhistory,
        'webcommentform': webcommentform,
        'printform': printform,
        'printcomments': printcomments,
        'printhistory': printhistory,
        'printcommentform': printcommentform,
        'audioform': audioform,
        'audiocomments': audiocomments,
        'audiohistory': audiohistory,
        'audiocommentform': audiocommentform,
        'videoform': videoform,
        'videocomments': videocomments,
        'videohistory': videohistory,
        'videocommentform': videocommentform,
        'images': images,
        'imageform': imageform,
        'webfacet_imageform': webfacet_imageform,
        'printfacet_imageform': printfacet_imageform,
        'audiofacet_imageform': audiofacet_imageform,
        'videofacet_imageform': videofacet_imageform,
        'webfacet_images': webfacet_images,
        'printfacet_images': printfacet_images,
        'audiofacet_images': audiofacet_images,
        'videofacet_images': videofacet_images,
        'documents': documents,
        'webfacet_documentform' : webfacet_documentform,
        'printfacet_documentform' : printfacet_documentform,
        'audiofacet_documentform' : audiofacet_documentform,
        'videofacet_documentform' : videofacet_documentform,
        'webfacet_documents': webfacet_documents,
        'printfacet_documents': printfacet_documents,
        'audiofacet_documents': audiofacet_documents,
        'videofacet_documents': videofacet_documents,
        'audiofiles': audiofiles,
        'webfacet_audioform': webfacet_audioform,
        'printfacet_audioform': printfacet_audioform,
        'audiofacet_audioform': audiofacet_audioform,
        'videofacet_audioform': videofacet_audioform,
        'webfacet_audio': webfacet_audio,
        'printfacet_audio': printfacet_audio,
        'audiofacet_audio': audiofacet_audio,
        'videofacet_audio': videofacet_audio,
        'webfacet_videoform': webfacet_videoform,
        'webfacet_video': webfacet_video,
        })


#--------------------Prelim Test Views---------------------------------#
#----------------------------------------------------------------------#
#                Edit Views
#----------------------------------------------------------------------#

    # ------------------------------ #
    #            Story               #
    # ------------------------------ #

    # def update_story_name(request,pk):
    #     """updates story name."""

    # ------------------------------ #
    #            Webfacet            #
    # ------------------------------ #

    # ------------------------------ #
    #           Printfacet           #
    # ------------------------------ #

    # ------------------------------ #
    #           Audiofacet           #
    # ------------------------------ #

    # ------------------------------ #
    #           Videofacet           #
    # ------------------------------ #
