""" Series views for editorial app.

    editorial/views/seriesviews.py
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
    SeriesForm,
    SeriesCommentForm,
    SeriesNoteForm,)

from editorial.models import (
    Series,
    SeriesNote,
    ImageAsset,
    Comment,
    Discussion,
    SeriesNote,)

#----------------------------------------------------------------------#
#   Series Views
#----------------------------------------------------------------------#

def series_list(request):
    """ Displays a filterable table of series.

    Initial display organizes content by series name.
    """

    series = Series.objects.filter(organization=request.user.organization)

    return render(request, 'editorial/serieslist.html', {'series': series})


def series_new(request):
    """ A logged in user can create a series.

    Series serve as a linking mechanism to connect related stories and to share
    assets between them. Series allow users to create planning notes at a series level
    have planning discussions and upload assets. Assets are always associated with a series
    so they are easily accessible to stories and all facets. This means that even single
    stories technically have a series, but in that case the user does not interact with any
    series interface.
    """

    seriesform = SeriesForm()
    if request.method == "POST":
        seriesform = SeriesForm(request.POST or None)
    if seriesform.is_valid():
        series = seriesform.save(commit=False)
        series.owner = request.user
        series.organization = request.user.organization
        series.creation_date = timezone.now()
        discussion = Discussion.objects.create_discussion("SER")
        series.discussion = discussion
        series.save()
        seriesform.save_m2m()
        return redirect('series_detail', pk=series.pk)
    else:
        form = SeriesForm()
    return render(request, 'editorial/seriesnew.html', {'seriesform': seriesform})


def series_detail(request, pk):
    """ The detail page for a series.

    Displays the series' planning notes, discussion, assets, share and collaboration status
    and sensivity status.
    """

    series = get_object_or_404(Series, pk=pk)
    seriesnoteform = SeriesNoteForm()
    seriesnotes = SeriesNote.objects.filter(series=series)[:10]
    seriescommentform = SeriesCommentForm()
    seriescomments = Comment.objects.filter(discussion=series.discussion).order_by('-date')

    return render(request, 'editorial/seriesdetail.html', {
        'series': series,
        'seriesnoteform': seriesnoteform,
        'seriesnotes': seriesnotes,
        'seriescomments': seriescomments,
        'seriescommentform': seriescommentform,
    })


def series_edit(request, pk):
    """ Edit series page."""

    series = get_object_or_404(Series, pk=pk)

    if request.method =="POST":
        seriesform = SeriesForm(data=request.POST, instance=series)
        if seriesform.is_valid():
            seriesform.save()
            return redirect('series_detail', pk=series.id)
    else:
        seriesform = SeriesForm(instance=series)

    return render(request, 'editorial/seriesedit.html', {
        'series': series,
        'seriesform': seriesform,
        })
