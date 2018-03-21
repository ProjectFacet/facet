"""Forms for Series and related entities."""

from django import forms
from django.forms import Textarea, TextInput
from editorial.models import (
    Series,
)

from editorial.widgets import ArrayFieldSelectMultiple


class SeriesForm(forms.ModelForm):
    """Form to create a new series."""

    def __init__(self, *args, **kwargs):
        org = kwargs.pop("organization")
        series = kwargs.pop("series", None)
        super(SeriesForm, self).__init__(*args, **kwargs)

        self.fields['collaborate_with'].queryset = org.get_org_collaborators_vocab()

    class Meta:
        model = Series
        fields = [
            'name',
            'description',
            'collaborate',
            'collaborate_with',
        ]
        widgets = {
            'name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Series Name'}),
            'description': Textarea(
                attrs={'class': 'form-control', 'placeholder': 'Description'}),
            'collaborate_with': ArrayFieldSelectMultiple(
                attrs={'class': 'chosen-select form-control facet-select',
                       'id': 'collaborate-with', 'data-placeholder': 'Select Collaborators'}),
        }

    class Media:
        css = {'all': ('css/bootstrap-datetimepicker.css', 'css/chosen.min.css')}
        js = ('scripts/chosen.jquery.min.js',)



class SeriesTeamForm(forms.ModelForm):
    """Form to add and edit a series team."""

    def __init__(self, *args, **kwargs):
        org = kwargs.pop("organization")
        series = kwargs.pop("series", None)
        super(SeriesTeamForm, self).__init__(*args, **kwargs)

        # TODO Future should include eligible contractors
        if series:
            self.fields['team'].queryset = series.get_series_team()
        else:
            self.fields['team'].queryset = org.get_org_users()

    class Meta:
        model = Series
        fields = ['team']
        widgets = {
            'team': ArrayFieldSelectMultiple(
                attrs={'class': 'chosen-select form-control facet-select', 'id': 'series-team',
                       'data-placeholder': 'Select Series Team'}),
        }

    class Media:
        css = {'all': ('css/bootstrap-datetimepicker.css', 'css/chosen.min.css')}
        js = ('scripts/chosen.jquery.min.js',)
