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
        'series': series
        })


def story_edit(request, pk):
    """ Edit story page. """

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
    })


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

# ------------------------------ #
#           webfacet             #
# ------------------------------ #

    # create these here for efficiency
    webform=WebFacetForm()
    webcommentform=WebFacetCommentForm()
    webfacet_imageform=ImageAssetForm()

    try:
        webfacet = get_object_or_404(WebFacet, story=story)
        print "WEBFACET CREDIT", webfacet.credit.all()

        # IF WEBFACET EXISTS DO ALL OF THE FOLLOWING
        # rebind webform to include webfacet instance
        webform = WebFacetForm(instance=webfacet)
        # retrieve discussion and comments
        webfacetdiscussion = get_object_or_404(Discussion, id=webfacet.discussion.id)
        webcomments = Comment.objects.filter(discussion=webfacetdiscussion).order_by('-date')[:3]
        # retrieve history
        webhistory = webfacet.edit_history.all()[:5]
        # update an existing webfacet
        if request.method == "POST":
            print "WF Try If Post"
            if 'webform' in request.POST:
                print "WF Try If Post If webform"
                webform = WebFacetForm(data=request.POST, instance=webfacet)
                #import pdb; pdb.set_trace()
                if webform.is_valid():
                    print "WF Try If Post If Webform Valid"
                    webform.save()
                    print "webfacet updated"
                    return redirect('story_detail', pk=story.pk)
    except:
        print "WF Except"
    # except WebFacet.DoesNotExist:
        # display form and save a new webfacet
        webcomments = []
        webhistory = []
        if request.method == "POST":
            print "WF Except Post"
            if 'webform' in request.POST:
                print "WF Except Post If webform"
                webform = WebFacetForm(request.POST or None)
                if webform.is_valid():
                    # #import pdb; pdb.set_trace()
                    print "WF Except Post If webform Valid"
                    webfacet = webform.save(commit=False)
                    print "webfacet = webform.save(commit=False)"
                    webfacet.story = story
                    webfacet.owner = request.user
                    webfacet.organization = request.user.organization
                    webfacet.creation_date = timezone.now()
                    discussion = Discussion.objects.create_discussion("WF")
                    webfacet.discussion = discussion
                    webfacet.save()
                    webform.save_m2m()
                    print "webfacet created"
                    # create history of the webfacet
                    webhistory = webfacet.edit_history.all()[:5]
                    return redirect('story_detail', pk=story.pk)

# ------------------------------ #
#           printfacet           #
# ------------------------------ #

    # create these here for efficiency
    printform=PrintFacetForm()
    printcommentform=PrintFacetCommentForm()
    printfacet_imageform=ImageAssetForm()

    try:
        print "PF Try"
        printfacet = get_object_or_404(PrintFacet, story=story)
        # IF PRINTFACET EXISTS DO ALL OF THE FOLLOWING
        printform = PrintFacetForm(instance=printfacet)
        # retrieve discussion and comments
        printfacetdiscussion = get_object_or_404(Discussion, id=printfacet.discussion.id)
        printcomments = Comment.objects.filter(discussion=printfacetdiscussion).order_by('-date')[:3]
        # retrieve history
        printhistory = printfacet.edit_history.all()[:5]
        # update an existing printfacet
        if request.method == "POST":
            print "PF Try If Post"
            if 'printform' in request.POST:
                print "PF Try If Post If printform"
                #import pdb; pdb.set_trace()
                printform = PrintFacetForm(data=request.POST, instance=printfacet)
                if printform.is_valid():
                    print "PF Try If Post If printform Valid"
                    printform.save()
                    print "printfacet updated"
                    return redirect('story_detail', pk=story.pk)
    except:
        print "PF Except"
    # except PrintFacet.DoesNotExist:
        # display form and save a new printfacet
        printcomments = []
        printhistory = []
        if request.method == "POST":
            print "PF Except If Post"
            if 'printform' in request.POST:
                print "PF Except If Post If printform"
                # #import pdb; pdb.set_trace()
                printform = PrintFacetForm(request.POST or None)
                if printform.is_valid():
                    print "PF Except If Post If printform Valid"
                    printfacet = printform.save(commit=False)
                    print "printfacet = printform.save(commit=False)"
                    printfacet.story = story
                    printfacet.owner = request.user
                    printfacet.organization = request.user.organization
                    printfacet.creation_date = timezone.now()
                    discussion = Discussion.objects.create_discussion("WF")
                    printfacet.discussion = discussion
                    printfacet.save()
                    printform.save_m2m()
                    print "printfacet created"
                    # create history of the printfacet
                    printhistory = printfacet.edit_history.all()[:5]
                    return redirect('story_detail', pk=story.pk)

# ------------------------------ #
#           audiofacet           #
# ------------------------------ #

    # create these here for efficiency
    audioform=AudioFacetForm()
    audiocommentform=AudioFacetCommentForm()
    audiofacet_imageform=ImageAssetForm()

    try:
        print "AF Try"
        audiofacet = get_object_or_404(AudioFacet, story=story)
        print "AUDIOFACET CREDIT: ", audiofacet.credit.all()
        # IF WEBFACET EXISTS DO ALL OF THE FOLLOWING
        audioform = AudioFacetForm(instance=audiofacet)
        # retrieve discussion and comments
        audiofacetdiscussion = get_object_or_404(Discussion, id=audiofacet.discussion.id)
        audiocomments = Comment.objects.filter(discussion=audiofacetdiscussion).order_by('-date')[:3]
        # retrieve history
        audiohistory = audiofacet.edit_history.all()[:5]
        # update an existing audiofacet
        if request.method == "POST":
            print "AF Try If Post"
            if 'audioform' in request.POST:
                print "AF Try If Post If Audioform"
                # #import pdb; pdb.set_trace()
                audioform = AudioFacetForm(data=request.POST, instance=audiofacet)
                if audioform.is_valid():
                    print "AF Try If Post If Audioform Valid"
                    audioform.save()
                    print "audiofacet updated"
                    return redirect('story_detail', pk=story.pk)
    except:
        print "AF Except"
    # except AudioFacet.DoesNotExist:
        # display form and save a new audiofacet
        audiocomments = []
        audiohistory = []
        if request.method == "POST":
            print "AF Except If Post"
            if 'audioform' in request.POST:
                print "AF Except If Post If Audioform"
                # #import pdb; pdb.set_trace()
                audioform = AudioFacetForm(request.POST or None)
                if audioform.is_valid():
                    print "AF Except If Post If Audioform Valid"
                    audiofacet = audioform.save(commit=False)
                    print "audiofacet = audioform.save(commit=False)"
                    audiofacet.story = story
                    audiofacet.owner = request.user
                    audiofacet.organization = request.user.organization
                    audiofacet.creation_date = timezone.now()
                    discussion = Discussion.objects.create_discussion("WF")
                    audiofacet.discussion = discussion
                    audiofacet.save()
                    audioform.save_m2m()
                    print "audiofacet created"
                    # create history of the audiofacet
                    audiohistory = audiofacet.edit_history.all()[:5]
                    return redirect('story_detail', pk=story.pk)

# ------------------------------ #
#           videofacet           #
# ------------------------------ #

    # create these here for efficiency
    videoform=VideoFacetForm()
    videocommentform=VideoFacetCommentForm()
    videofacet_imageform=ImageAssetForm()

    try:
        print "VF Try"
        videofacet = get_object_or_404(VideoFacet, story=story)
        # IF WEBFACET EXISTS DO ALL OF THE FOLLOWING
        videoform = VideoFacetForm(instance=videofacet)
        # retrieve discussion and comments
        videofacetdiscussion = get_object_or_404(Discussion, id=videofacet.discussion.id)
        videocomments = Comment.objects.filter(discussion=videofacetdiscussion).order_by('-date')[:3]
        # retrieve history
        videohistory = videofacet.edit_history.all()[:5]
        # update an existing videofacet
        if request.method == "POST":
            print "VF Try If Post"
            if 'videoform' in request.POST:
                print "VF Try If Post If Videoform"
                # # #import pdb; pdb.set_trace()
                videoform = VideoFacetForm(data=request.POST, instance=videofacet)
                if videoform.is_valid():
                    print "VF Try If Post If Videoform Valid"
                    videoform.save()
                    print "videofacet updated"
                    return redirect('story_detail', pk=story.pk)
    except:
        print "VF Except If Post If Videoform Valid"
    # except VideoFacet.DoesNotExist:
        # display form and save a new videofacet
        videocomments = []
        videohistory = []
        if request.method == "POST":
            print "VF Except If Post"
            if 'videoform' in request.POST:
                print "VF Except If Post If Videoform"
                videoform = VideoFacetForm(request.POST or None)
                if videoform.is_valid():
                    # #import pdb; pdb.set_trace()
                    print "VF Except If Post If Videoform Valid"
                    videofacet = videoform.save(commit=False)
                    print "videofacet = videoform.save(commit=False)"
                    videofacet.story = story
                    videofacet.owner = request.user
                    videofacet.organization = request.user.organization
                    videofacet.creation_date = timezone.now()
                    discussion = Discussion.objects.create_discussion("VF")
                    videofacet.discussion = discussion
                    videofacet.save()
                    videoform.save_m2m()
                    print "videofacet created"
                    # create history of the videofacet
                    videohistory = videofacet.edit_history.all()[:5]
                    return redirect('story_detail', pk=story.pk)

    # ------------------------------ #
    #        Download Options        #
    # ------------------------------ #
    if story.webfacetstory.all():
        webfacet = get_object_or_404(WebFacet, story=story)
        webfacet_images = WebFacet.get_webfacet_images(webfacet)
    else:
        webfacet_images = []
    if story.printfacetstory.all():
        printfacet = get_object_or_404(PrintFacet, story=story)
        printfacet_images = PrintFacet.get_printfacet_images(printfacet)
    else:
        printfacet_images = []
    if story.audiofacetstory.all():
        audiofacet = get_object_or_404(AudioFacet, story=story)
        audiofacet_images = AudioFacet.get_audiofacet_images(audiofacet)
    else:
        audiofacet_images = []
    if story.videofacetstory.all():
        videofacet = get_object_or_404(VideoFacet, story=story)
        videofacet_images = VideoFacet.get_videofacet_images(videofacet)
    else:
        videofacet_images =[]
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
        'webfacet_imageform': webfacet_imageform,
        'printfacet_imageform': printfacet_imageform,
        'audiofacet_imageform': audiofacet_imageform,
        'videofacet_imageform': videofacet_imageform,
        'images': images,
        'webfacet_images': webfacet_images,
        'printfacet_images': printfacet_images,
        'audiofacet_images': audiofacet_images,
        'videofacet_images': videofacet_images,
        })
