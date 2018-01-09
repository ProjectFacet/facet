"""Forms for Projects and related entities."""

from django import forms
from django.forms import Textarea, TextInput
from editorial.models import (
    Project,
)

from editorial.widgets import ArrayFieldSelectMultiple


class ProjectForm(forms.ModelForm):
    """Form to create a new project. """

    def __init__(self, *args, **kwargs):
        org = kwargs.pop("organization")
        super(ProjectForm, self).__init__(*args, **kwargs)

        self.fields['collaborate_with'].queryset = org.get_org_collaborators_vocab()
        # FIXME should be org users, partner org users and eligible contractors
        self.fields['team'].queryset = org.get_org_users()
        # self.fields['team'].queryset = project.get_project_team_vocab()

    class Meta:
        model = Project
        fields = ['name', 'project_description', 'collaborate', 'collaborate_with', 'team']
        widgets = {
            'name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Project Name'}),
            'project_description': Textarea(
                attrs={'class': 'form-control', 'placeholder': 'Description'}),
            'team': ArrayFieldSelectMultiple(
                attrs={'class': 'chosen-select form-control facet-select',
                       'id': 'project-team', 'data-placeholder': 'Select Project Team'}),
            'collaborate_with': ArrayFieldSelectMultiple(
                attrs={'class': 'chosen-select form-control facet-select',
                       'id': 'collaborate-with', 'data-placeholder': 'Select Collaborators'}),
        }

    class Media:
        css = {'all': ('css/bootstrap-datetimepicker.css', 'css/chosen.min.css')}
        js = ('scripts/chosen.jquery.min.js',)
