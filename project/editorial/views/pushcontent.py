""" General views for editorial app. """

# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import json

from django.shortcuts import redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import UpdateView, CreateView, DeleteView, View
from django.http import HttpResponse, JsonResponse
from django.core import serializers

from editorial.models import (
    Facet,
    Organization,
)

#----------------------------------------------------------------------#
#   Facet to WordPress Views
#----------------------------------------------------------------------#


class OrganizationFacetJSONView(View):
    """Return JSON of all Organization Facets with status Ready."""

    def get(self, request, *args, **kwargs):
        org_id = self.kwargs['pk']
        org = get_object_or_404(Organization, pk=org_id)
        data = serializers.serialize('json', org.facet_set.filter(status="Ready"), fields=('name','content'))
        return JsonResponse(data, safe=False)


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
