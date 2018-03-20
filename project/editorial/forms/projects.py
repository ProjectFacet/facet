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
        project = kwargs.pop("project", None)
        super(ProjectForm, self).__init__(*args, **kwargs)

        self.fields['collaborate_with'].queryset = org.get_org_collaborators_vocab()

    class Meta:
        model = Project
        fields = ['name', 'project_description', 'collaborate', 'collaborate_with']
        widgets = {
            'name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Project Name'}),
            'project_description': Textarea(
                attrs={'class': 'form-control', 'placeholder': 'Description'}),
            'collaborate_with': ArrayFieldSelectMultiple(
                attrs={'class': 'chosen-select form-control facet-select',
                       'id': 'collaborate-with', 'data-placeholder': 'Select Collaborators'}),
        }

    class Media:
        css = {'all': ('css/bootstrap-datetimepicker.css', 'css/chosen.min.css')}
        js = ('scripts/chosen.jquery.min.js',)


class ProjectTeamForm(forms.ModelForm):
    """ Form to add a team to a project after a project is created."""

    def __init__(self, *args, **kwargs):
        org = kwargs.pop("organization")
        project = kwargs.pop("project", None)
        super(ProjectTeamForm, self).__init__(*args, **kwargs)

        # TODO Future team options should include eligible contractors
        if project:
            self.fields['team'].queryset = project.get_project_team_vocab()
        else:
            self.fields['team'].queryset = org.get_org_users()

    class Meta:
        model = Project
        fields = ['team']
        widgets = {
            'team': ArrayFieldSelectMultiple(
                attrs={'class': 'chosen-select form-control facet-select',
                       'id': 'project-team', 'data-placeholder': 'Select Project Team'}),
        }

    class Media:
        css = {'all': ('css/bootstrap-datetimepicker.css', 'css/chosen.min.css')}
        js = ('scripts/chosen.jquery.min.js',)
