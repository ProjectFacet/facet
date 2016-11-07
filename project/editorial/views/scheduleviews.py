""" Schedule views for editorial app. """

from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponse
from django.utils import timezone
from django.views.generic import TemplateView , UpdateView, DetailView
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response
from django.utils.safestring import mark_safe
import datetime, time

import json

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
#   Schedule Views
#----------------------------------------------------------------------#

def schedule(request):
    """ Display schedules of upcoming content.
    Calendar: Longterm view displaying only the name/title of an item with a
    link-text
    Agenda: Daily in-depth rundown of content for edit/running.
    """

    return render(request, 'editorial/schedule.html', {})


def schedule_content(request):
    """ Return JSON of event information."""

    stories = Story.objects.filter(organization=request.user.organization).exclude(archived=True)

    # data = {}
    # data['success'] = 1
    # data['result'] = []
    data = []

    for story in stories:
        # Web Facet Schedules
        for webfacet in story.webfacetstory.all():
            credit = {}
            for user in webfacet.credit.all():
                credit['id'] = []
                credit['id'].append(user.credit_name)
                credit['id'].append(user.get_absolute_url())
            print credit
            if webfacet.due_edit:
                edit_event_dict = {}
                edit_event_dict['id'] = webfacet.id
                edit_event_dict['title'] = webfacet.title.encode('utf-8')
                edit_event_dict['description'] = webfacet.description.encode('utf-8')
                edit_event_dict['due-edit'] = time.mktime(webfacet.due_edit.timetuple())
                edit_event_dict['editor'] = webfacet.editor.credit_name
                edit_event_dict['credit'] = credit
                edit_event_dict['url'] = webfacet.get_absolute_url()
                edit_event_dict['start'] = time.mktime(webfacet.due_edit.timetuple()) * 1000
                edit_event_dict['end'] = (time.mktime(webfacet.due_edit.timetuple()) * 1000) + 60
                edit_event_dict['overlap'] = True
                edit_event_dict['allDay'] = False
                edit_event_dict['backgroundColor'] = '#00aced'
                edit_event_dict['textColor'] = '#fff'
                data.append(edit_event_dict)
            if webfacet.run_date:
                run_event_dict = {}
                run_event_dict['id'] = webfacet.id
                run_event_dict['title'] = webfacet.title.encode('utf-8')
                run_event_dict['description'] = webfacet.description.encode('utf-8')
                run_event_dict['due-edit'] = time.mktime(webfacet.due_edit.timetuple())
                run_event_dict['editor'] = webfacet.editor.credit_name
                run_event_dict['credit'] = credit
                run_event_dict['url'] = webfacet.get_absolute_url()
                run_event_dict['class'] = 'event_run'
                run_event_dict['start'] = time.mktime(webfacet.run_date.timetuple()) * 1000
                run_event_dict['end'] = (time.mktime(webfacet.run_date.timetuple()) * 1000) + 60
                run_event_dict['overlap'] = True
                run_event_dict['backgroundColor'] = '#5cb85c'
                run_event_dict['textColor'] = '#fff'
                data.append(run_event_dict)
        # Print Facet Schedules
        for printfacet in story.printfacetstory.all():
            credit = {}
            for user in printfacet.credit.all():
                credit['id'] = []
                credit['id'].append(user.credit_name)
                credit['id'].append(user.get_absolute_url())
            print credit
            if printfacet.due_edit:
                edit_event_dict = {}
                edit_event_dict['id'] = printfacet.id
                edit_event_dict['title'] = printfacet.title.encode('utf-8')
                edit_event_dict['description'] = printfacet.description.encode('utf-8')
                edit_event_dict['due-edit'] = time.mktime(printfacet.due_edit.timetuple())
                edit_event_dict['editor'] = printfacet.editor.credit_name
                edit_event_dict['credit'] = credit
                edit_event_dict['url'] = printfacet.get_absolute_url()
                edit_event_dict['class'] = 'event_edit'
                edit_event_dict['start'] = time.mktime(printfacet.due_edit.timetuple()) * 1000
                edit_event_dict['end'] = (time.mktime(printfacet.due_edit.timetuple()) * 1000) + 60
                edit_event_dict['overlap'] = True
                edit_event_dict['backgroundColor'] = '#00aced'
                edit_event_dict['textColor'] = '#fff'
                data.append(edit_event_dict)
            if printfacet.run_date:
                run_event_dict = {}
                run_event_dict['id'] = printfacet.id
                run_event_dict['title'] = printfacet.title.encode('utf-8')
                run_event_dict['description'] = printfacet.description.encode('utf-8')
                run_event_dict['due-edit'] = time.mktime(printfacet.due_edit.timetuple())
                run_event_dict['editor'] = printfacet.editor.credit_name
                run_event_dict['credit'] = credit
                run_event_dict['url'] = printfacet.get_absolute_url()
                run_event_dict['class'] = 'event_run'
                run_event_dict['start'] = time.mktime(printfacet.run_date.timetuple()) * 1000
                run_event_dict['end'] = (time.mktime(printfacet.run_date.timetuple()) * 1000) + 60
                run_event_dict['overlap'] = True
                run_event_dict['backgroundColor'] = '#5cb85c'
                run_event_dict['textColor'] = '#fff'
                data.append(run_event_dict)
        # Audio Facet Schedules
        for audiofacet in story.audiofacetstory.all():
            for user in audiofacet.credit.all():
                credit['id'] = []
                credit['id'].append(user.credit_name)
                credit['id'].append(user.get_absolute_url())
            print credit
            if audiofacet.due_edit:
                edit_event_dict = {}
                edit_event_dict['id'] = audiofacet.id
                edit_event_dict['title'] = audiofacet.title.encode('utf-8')
                edit_event_dict['description'] = audiofacet.description.encode('utf-8')
                edit_event_dict['due-edit'] = time.mktime(audiofacet.due_edit.timetuple())
                edit_event_dict['editor'] = audiofacet.editor.credit_name
                edit_event_dict['credit'] = credit
                edit_event_dict['url'] = audiofacet.get_absolute_url()
                edit_event_dict['class'] = 'event_edit'
                edit_event_dict['start'] = time.mktime(audiofacet.due_edit.timetuple()) * 1000
                edit_event_dict['end'] = (time.mktime(audiofacet.due_edit.timetuple()) * 1000) + 60
                edit_event_dict['overlap'] = True
                edit_event_dict['backgroundColor'] = '#00aced'
                edit_event_dict['textColor'] = '#fff'
                data.append(edit_event_dict)
            if audiofacet.run_date:
                run_event_dict = {}
                run_event_dict['id'] = audiofacet.id
                run_event_dict['title'] = audiofacet.title.encode('utf-8')
                run_event_dict['description'] = audiofacet.description.encode('utf-8')
                run_event_dict['due-edit'] = time.mktime(audiofacet.due_edit.timetuple())
                run_event_dict['editor'] = audiofacet.editor.credit_name
                run_event_dict['credit'] = credit
                run_event_dict['url'] = audiofacet.get_absolute_url()
                run_event_dict['class'] = 'event_run'
                run_event_dict['start'] = time.mktime(audiofacet.run_date.timetuple()) * 1000
                run_event_dict['end'] = (time.mktime(audiofacet.run_date.timetuple()) * 1000) + 60
                run_event_dict['overlap'] = True
                run_event_dict['backgroundColor'] = '#5cb85c'
                run_event_dict['textColor'] = '#fff'
                data.append(run_event_dict)
        # Video Facet Schedules
        for videofacet in story.videofacetstory.all():
            for user in videofacet.credit.all():
                credit['id'] = []
                credit['id'].append(user.credit_name)
                credit['id'].append(user.get_absolute_url())
            print credit
            if videofacet.due_edit:
                edit_event_dict = {}
                edit_event_dict['id'] = videofacet.id
                edit_event_dict['title'] = videofacet.title.encode('utf-8')
                edit_event_dict['description'] = videofacet.description.encode('utf-8')
                edit_event_dict['due-edit'] = time.mktime(videofacet.due_edit.timetuple())
                edit_event_dict['editor'] = videofacet.editor.credit_name
                edit_event_dict['credit'] = credit
                edit_event_dict['url'] = videofacet.get_absolute_url()
                edit_event_dict['class'] = 'event_edit'
                edit_event_dict['start'] = time.mktime(videofacet.due_edit.timetuple()) * 1000
                edit_event_dict['end'] = (time.mktime(videofacet.due_edit.timetuple()) * 1000) + 60
                edit_event_dict['overlap'] = True
                edit_event_dict['backgroundColor'] = '#00aced'
                edit_event_dict['textColor'] = '#fff'
                data.append(edit_event_dict)
            if videofacet.run_date:
                run_event_dict = {}
                run_event_dict['id'] = videofacet.id
                run_event_dict['title'] = videofacet.title.encode('utf-8')
                run_event_dict['description'] = videofacet.description.encode('utf-8')
                run_event_dict['due-edit'] = time.mktime(videofacet.due_edit.timetuple())
                run_event_dict['editor'] = videofacet.editor.credit_name
                run_event_dict['credit'] = credit
                run_event_dict['url'] = videofacet.get_absolute_url()
                run_event_dict['class'] = 'event_run'
                run_event_dict['start'] = time.mktime(videofacet.run_date.timetuple()) * 1000
                run_event_dict['end'] = (time.mktime(videofacet.run_date.timetuple()) * 1000) + 60
                run_event_dict['overlap'] = True
                run_event_dict['backgroundColor'] = '#5cb85c'
                run_event_dict['textColor'] = '#fff'
                data.append(run_event_dict)

    # print "DATA: ", data

    return HttpResponse(json.dumps(data), content_type='application/json')
