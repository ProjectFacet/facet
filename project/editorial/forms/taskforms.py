"""Forms for Tasks and related entities.

"""

import datetime
from bootstrap3_datetime.widgets import DateTimePicker
from .customwidgets import OurDateTimePicker, ArrayFieldSelectMultiple
from django import forms
from django.utils.safestring import mark_safe
from django.contrib.auth import get_user_model
from django.forms import Textarea, TextInput, RadioSelect, Select, NumberInput, CheckboxInput, CheckboxSelectMultiple, FileField
from django.contrib.postgres.fields import ArrayField
from datetimewidget.widgets import DateTimeWidget
from tinymce.widgets import TinyMCE
# from django.contrib.staticfiles.templatetags.staticfiles import static


from editorial.models import (
    Project,
    Series,
    Story,
    Task,
    Event,
)


# ------------------------------ #
#          Task Forms            #
# ------------------------------ #

class TaskForm(forms.ModelForm):
    """ Form to create/edit a task. """

    def __init__(self, *args, **kwargs):
        org = kwargs.pop("organization")
        super(TaskForm, self).__init__(*args, **kwargs)
        self.fields['assigned_to'].queryset = org.get_org_users()
        self.fields['status'].empty_label='Task Status'
        self.fields['project'].empty_label='Select a Project'
        self.fields['series'].empty_label='Select a Series'
        self.fields['story'].empty_label='Select a Story'
        self.fields['event'].empty_label='Select an Event'

    projects = forms.ModelChoiceField(
        queryset=Project.objects.filter(),
        widget=forms.Select,
        required=False,
    )

    series = forms.ModelChoiceField(
        queryset=Series.objects.all(),
        widget=forms.Select,
        required=False,
    )

    stories = forms.ModelChoiceField(
        queryset=Story.objects.all(),
        widget=forms.Select,
        required=False,
    )

    events = forms.ModelChoiceField(
        queryset=Event.objects.all(),
        widget=forms.Select,
        required=False,
    )

    due_date = forms.DateTimeField(
        required=False,
        widget=OurDateTimePicker(
            options={'format': 'YYYY-MM-DD HH:mm'},
            attrs={'id': 'task_duedate_picker'}
        )
    )

    class Meta:
        model = Task
        fields = [
            'name',
            'text',
            'assigned_to',
            'status',
            'important',
            'due_date',
            'project',
            'series',
            'story',
            'event',
        ]
        widgets = {
            'name': Textarea(attrs={'class': 'form-control', 'rows':2, 'placeholder': 'Name'}),
            'text': Textarea(attrs={'class': 'form-control', 'id':'task-text', 'rows':20, 'placeholder': 'Details'}),
            'assigned_to': ArrayFieldSelectMultiple(attrs={'class': 'chosen-select form-control facet-select', 'id':'task-team', 'data-placeholder': 'Assign to'}),
            'status': Select(attrs={'class': 'custom-select', 'id':'task-status'}),
            'important': CheckboxInput(attrs={'class': ''}),
            'project': Select(attrs={'class': 'custom-select', 'id':'task-projects'}),
            'series': Select(attrs={'class': 'custom-select', 'id':'task-series'}),
            'story': Select(attrs={'class': 'custom-select', 'id':'task-stories'}),
            'event': Select(attrs={'class': 'custom-select', 'id':'task-events'}),
            }

    class Media:
        css = {
            'all': ('css/bootstrap-datetimepicker.css', 'css/chosen.min.css')
        }
        js = ('scripts/chosen.jquery.min.js',)
