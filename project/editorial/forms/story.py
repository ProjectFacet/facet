"""Forms for Stories and related entities."""

from bootstrap3_datetime.widgets import DateTimePicker
from django import forms
from django.db.models import Q
from django.forms import Textarea, TextInput, Select

from editorial.models import (
    Project,
    Series,
    Story,
)

from editorial.widgets import ArrayFieldSelectMultiple


class StoryForm(forms.ModelForm):
    """Form to create/edit a new story."""

    def __init__(self, *args, **kwargs):
        org = kwargs.pop("organization")
        story = kwargs.pop("story", None)
        super(StoryForm, self).__init__(*args, **kwargs)

        self.fields['share_with'].queryset = org.get_org_networks()
        self.fields['collaborate_with'].queryset = org.get_org_collaborators_vocab()
        # TODO future should include eligible contractors
        if story:
            self.fields['team'].queryset = story.get_story_team_vocab()
        else:
            self.fields['team'].queryset = org.get_org_users()

        # limit project and series to those owned by org or part of content and org is collaborator for
        self.fields['project'].queryset = Project.objects.filter(
            Q(organization=org) | Q(collaborate_with=org))
        self.fields['series'].queryset = Series.objects.filter(
            Q(organization=org) | Q(collaborate_with=org))

        # set empty labels
        self.fields['series'].empty_label = 'Select a series'
        self.fields['project'].empty_label = 'Select a project'

    embargo_datetime = forms.DateTimeField(
        required=False,
        widget=DateTimePicker(
            options={'format': 'YYYY-MM-DD HH:mm'},
            attrs={'id': 'story-embargo-picker'})
    )

    share_with_date = forms.DateTimeField(
        required=False,
        widget=DateTimePicker(
            options={'format': 'YYYY-MM-DD HH:mm'},
            attrs={'id': 'story-share-picker'})
    )

    class Meta:
        model = Story
        fields = ['name',
                  'story_description',
                  'project',
                  'series',
                  'collaborate',
                  'collaborate_with',
                  'team',
                  'embargo',
                  'embargo_datetime',
                  'sensitive',
                  'share',
                  'ready_to_share',
                  'share_with',
                  'share_with_date',
                  'archived',
                  ]
        widgets = {
            'name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Story Name'}),
            'story_description': Textarea(
                attrs={'class': 'form-control', 'placeholder': 'Description'}),
            'team': ArrayFieldSelectMultiple(
                attrs={'class': 'chosen-select', 'id': 'story-team',
                       'data-placeholder': 'Select Team'}),
            'collaborate_with': ArrayFieldSelectMultiple(
                attrs={'class': 'chosen-select', 'id': 'collaborate-with',
                       'data-placeholder': 'Select Partners'}),
            'share_with': ArrayFieldSelectMultiple(
                attrs={'class': 'chosen-select', 'id': 'share-with',
                       'data-placeholder': 'Select Networks'}),
            'series': Select(attrs={'class': 'c-select', 'id': 'story-series'}),
            'project': Select(attrs={'class': 'c-select', 'id': 'story-project'}),
        }

    # class Media:
    #     css = {
    #         'all': ('css/bootstrap-datetimepicker.css', 'css/chosen.min.css')
    #     }
    #     js = ('scripts/chosen.jquery.min.js',)

# ------------------------------ #
#        Download Form           #
# ------------------------------ #

# class StoryDownloadForm(forms.Form):
#     """ Select content and assets to download."""
#
#     def __init__(self, *args, **kwargs):
#         story = kwargs.pop('story')
#         super(StoryDownloadForm, self).__init__(*args, **kwargs)
#
#         if story.facet_set.all():
#             for facet in story.facet_set.all():
#                 self.fields['facet_images'].queryset = facet.get_facet_images()
#
#     select_all = forms.BooleanField(
#         widget=CheckboxInput,
#     )
#
#     facet = forms.BooleanField(
#         widget=CheckboxInput,
#     )
#
#     facet_sa = forms.BooleanField(
#         widget=CheckboxInput,
#     )
#
#     facet_images = forms.ModelMultipleChoiceField(
#         widget=CheckboxSelectMultiple,
#         queryset = ImageAsset.objects.all()
#     )
