""" General views for editorial app. """

# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponse
from django.utils import timezone
from django.views.generic import TemplateView , UpdateView, DetailView
from django.views.decorators.csrf import csrf_exempt
import datetime, time
import json

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
    ImageAsset,
    DocumentAsset,
    AudioAsset,
    VideoAsset,)


#----------------------------------------------------------------------#
#   WebFacet to WordPress Views
#----------------------------------------------------------------------#

@csrf_exempt
def webfacet_json(request):
    """ Take a specific webfacet and create a JSON object for use in a WordPress site."""

    if request.method == 'POST':
        webfacet_id = request.POST.get('webfacet_id')

    webfacet = get_object_or_404(WebFacet, id=webfacet_id)

    wf_json = {}
    wf_json["status"] = "pending"
    wf_json["title"] = webfacet.title
    wf_json["content"] = webfacet.wf_content
    wf_json["excerpt"] = webfacet.excerpt
    wf_json = json.dumps(wf_json)

    # update push to wordpress status
    print webfacet.pushed_to_wp
    webfacet.pushed_to_wp = True
    webfacet.save()
    print webfacet.pushed_to_wp

    # return HttpResponse(json.dumps(wf_json), content_type = "application/json")
    return redirect('story_detail', pk=webfacet.story.pk)


# def push_webfacet_wp(request):
#     """Push a webfacet JSON object to a WordPress site."""
#
#     print "push webfacet to wp"
