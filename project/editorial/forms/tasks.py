"""Forms for Tasks and related entities."""

from bootstrap3_datetime.widgets import DateTimePicker
from django import forms
from django.db.models import Q
from django.forms import Textarea, Select, CheckboxInput
from editorial.models import (
    Project,
    Series,
    Story,
    Task,
    Event,
)

from editorial.widgets import ArrayFieldSelectMultiple


class TaskForm(forms.ModelForm):
    """Form to create/edit a task."""

    def __init__(self, *args, **kwargs):
        org = kwargs.pop("organization")
        super(TaskForm, self).__init__(*args, **kwargs)
        # TODO make assignment team include org users, partner users and collaborators assigned to content
        self.fields['assigned_to'].queryset = org.get_org_users()
        # limit project, series and stories to those owned by org or part of content and org is collaborator for
        self.fields['project'].queryset = Project.objects.filter(
            Q(collaborate_with=org) | (Q(organization=org)))
        self.fields['series'].queryset = Series.objects.filter(
            Q(collaborate_with=org) | (Q(organization=org)))
        self.fields['story'].queryset = Story.objects.filter(
            Q(collaborate_with=org) | (Q(organization=org)))
        self.fields['event'].queryset = Event.objects.filter(
            Q(organization=org) | (Q(evt_organization=org)))
        # set empty labels
        self.fields['status'].empty_label = 'Task Status'
        self.fields['project'].empty_label = 'Select a Project'
        self.fields['series'].empty_label = 'Select a Series'
        self.fields['story'].empty_label = 'Select a Story'
        self.fields['event'].empty_label = 'Select an Event'

    due_date = forms.DateTimeField(
        required=False,
        widget=DateTimePicker(
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
            'name': Textarea(
                attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Name'}),
            'text': Textarea(attrs={'class': 'form-control', 'id': 'task-text', 'rows': 17,
                                    'placeholder': 'Details'}),
            'assigned_to': ArrayFieldSelectMultiple(
                attrs={'class': 'chosen-select form-control task-assign-select',
                       'id': 'task-team', 'data-placeholder': 'Assign to'}),
            'status': Select(attrs={'class': 'custom-select', 'id': 'task-status'}),
            'important': CheckboxInput(attrs={'class': ''}),
            'project': Select(attrs={'class': 'custom-select', 'id': 'task-projects'}),
            'series': Select(attrs={'class': 'custom-select', 'id': 'task-series'}),
            'story': Select(attrs={'class': 'custom-select', 'id': 'task-stories'}),
            'event': Select(attrs={'class': 'custom-select', 'id': 'task-events'}),
        }

    class Media:
        css = {'all': ('css/bootstrap-datetimepicker.css', 'css/chosen.min.css')}
        js = ('scripts/chosen.jquery.min.js',)
