""" Schedule views for editorial app. """

# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import json
import time

from django.http import HttpResponse
from django.shortcuts import render
from editorial.models import (
    Story,
)


#----------------------------------------------------------------------#
#   Schedule Views
#----------------------------------------------------------------------#

# ACCESS: An org user should be able to see all events associated with an org
# class Schedule(LoginRequiredMixin, TemplateView):
#     """Display calendar of all deadlines and events for an organization."""
#
#     # handle users that are not logged in
#     login_url = settings.LOGIN_URL


def schedule(request):
    """ Display schedules of upcoming content.
    Calendar: Longterm view displaying only the name/title of an item with a
    link-text
    Agenda: Daily in-depth rundown of content for edit/running.
    """

    return render(request, 'editorial/schedule.html', {})


# class ScheduleContent(LoginRequiredMixin, View):
#     """Return JSON of all deadlines and events for an organization."""
#
#     # handle users that are not logged in
#     login_url = settings.LOGIN_URL


def schedule_content(request):
    """ Return JSON of event information."""

    stories = Story.objects.filter(organization=request.user.organization).exclude(archived=True)

    # data = {}
    # data['success'] = 1
    # data['result'] = []
    data = []

    for story in stories:
        # Facet Schedules
        for facet in story.facetstory.all():
            credit = {}
            for user in facet.credit.all():
                credit['id'] = []
                credit['id'].append(user.credit_name)
                credit['id'].append(user.get_absolute_url())
            editor = {}
            for user in facet.editor.all():
                editor['id'] = []
                editor['id'].append(user.credit_name)
                editor['id'].append(user.get_absolute_url())
            print credit
            if facet.due_edit:
                edit_event_dict = {}
                edit_event_dict['id'] = facet.id
                edit_event_dict['title'] = facet.name.encode('utf-8')
                edit_event_dict['description'] = facet.description.encode('utf-8')
                edit_event_dict['due-edit'] = time.mktime(facet.due_edit.timetuple())
                edit_event_dict['editor'] = facet.editor.credit_name
                edit_event_dict['credit'] = credit
                edit_event_dict['url'] = facet.get_absolute_url()
                edit_event_dict['start'] = time.mktime(facet.due_edit.timetuple()) * 1000
                edit_event_dict['end'] = (time.mktime(facet.due_edit.timetuple()) * 1000) + 60
                edit_event_dict['overlap'] = True
                edit_event_dict['allDay'] = False
                edit_event_dict['backgroundColor'] = '#00aced'
                edit_event_dict['textColor'] = '#fff'
                data.append(edit_event_dict)
            if facet.run_date:
                run_event_dict = {}
                run_event_dict['id'] = facet.id
                run_event_dict['title'] = facet.name.encode('utf-8')
                run_event_dict['description'] = facet.description.encode('utf-8')
                run_event_dict['due-edit'] = time.mktime(facet.due_edit.timetuple())
                run_event_dict['editor'] = facet.editor.credit_name
                run_event_dict['credit'] = credit
                run_event_dict['url'] = facet.get_absolute_url()
                run_event_dict['class'] = 'event_run'
                run_event_dict['start'] = time.mktime(facet.run_date.timetuple()) * 1000
                run_event_dict['end'] = (time.mktime(facet.run_date.timetuple()) * 1000) + 60
                run_event_dict['overlap'] = True
                run_event_dict['backgroundColor'] = '#5cb85c'
                run_event_dict['textColor'] = '#fff'
                data.append(run_event_dict)

    # print "DATA: ", data

    return HttpResponse(json.dumps(data), content_type='application/json')
