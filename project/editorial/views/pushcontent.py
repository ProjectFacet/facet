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
from braces.views import LoginRequiredMixin, FormMessagesMixin

from editorial.models import (
    User,
    Organization,
    Network,
    Series,
    Story,
    ImageAsset,
    DocumentAsset,
    AudioAsset,
    VideoAsset,)


#----------------------------------------------------------------------#
#   Facet to WordPress Views
#----------------------------------------------------------------------#

@csrf_exempt
def facet_json(request):
    """ Take a specific facet and create a JSON object for use in a WordPress site."""

    if request.method == 'POST':
        facet_id = request.POST.get('facet_id')

    facet = get_object_or_404(Facet, id=facet_id)

    f_json = {}
    f_json["status"] = "pending"
    f_json["title"] = facet.title
    f_json["content"] = facet.content
    f_json["excerpt"] = facet.excerpt
    f_json = json.dumps(f_json)

    # update push to wordpress status
    print facet.pushed_to_wp
    facet.pushed_to_wp = True
    facet.save()
    print facet.pushed_to_wp

    # return HttpResponse(json.dumps(f_json), content_type = "application/json")
    return redirect('story_detail', pk=facet.story.pk)


# def push_facet_wp(request):
#     """Push a facet JSON object to a WordPress site."""
#
#     print "push facet to wp"
