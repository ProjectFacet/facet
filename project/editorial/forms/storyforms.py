"""Forms for Stories and related entities.

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
    Facet,
    ImageAsset,
    DocumentAsset,
    AudioAsset,
    VideoAsset,
)


# ------------------------------ #
#          Story Forms           #
# ------------------------------ #

class StoryForm(forms.ModelForm):
    """ Form to create/edit a new story. """

    def __init__(self, *args, **kwargs):
        org = kwargs.pop("organization")
        super(StoryForm, self).__init__(*args, **kwargs)
        self.fields['share_with'].queryset = org.get_org_networks()
        self.fields['collaborate_with'].queryset = org.get_org_collaborators_vocab()
        self.fields['team'].queryset = org.get_org_users()
        self.fields['series'].empty_label = 'Select a series'
        self.fields['project'].empty_label = 'Select a project'

    series = forms.ModelChoiceField(
        queryset=Series.objects.all(),
        widget=forms.Select,
        required=False,
    )

    project = forms.ModelChoiceField(
        queryset=Project.objects.all(),
        widget=forms.Select,
        required=False,
    )

    embargo_datetime = forms.DateTimeField(
        required=False,
        widget=OurDateTimePicker(
            options={'format': 'YYYY-MM-DD HH:mm'},
            attrs={'id': 'story-embargo-picker'})
    )

    share_with_date = forms.DateTimeField(
        required=False,
        widget=OurDateTimePicker(
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
            'story_description': Textarea(attrs={'class': 'form-control', 'placeholder': 'Description'}),
            'team': ArrayFieldSelectMultiple(attrs={'class': 'chosen-select', 'id':'story-team', 'data-placeholder': 'Select Team'}),
            'collaborate_with': ArrayFieldSelectMultiple(attrs={'class': 'chosen-select', 'id':'collaborate-with', 'data-placeholder': 'Select Partners'}),
            'share_with': ArrayFieldSelectMultiple(attrs={'class': 'chosen-select', 'id':'share-with', 'data-placeholder': 'Select Networks'}),
            'series': Select(attrs={'class': 'c-select', 'id':'story-series'}),
            'project': Select(attrs={'class': 'c-select', 'id':'story-project'}),
        }

    # class Media:
    #     css = {
    #         'all': ('css/bootstrap-datetimepicker.css', 'css/chosen.min.css')
    #     }
    #     js = ('scripts/chosen.jquery.min.js',)


# ------------------------------ #
#        Download Form           #
# ------------------------------ #

class StoryDownloadForm(forms.Form):
    """ Select content and assets to download."""

    def __init__(self, *args, **kwargs):
        self.story = kwargs.pop('story')
        super(StoryDownloadForm, self).__init__(*args, **kwargs)

        if self.story.webfacetstory.all():
            webfacet = self.story.webfacetstory.all()[0]
            self.fields['webfacet_images'].queryset = WebFacet.get_webfacet_images(webfacet)
        if self.story.printfacetstory.all():
            printfacet = self.story.printfacetstory.all()[0]
            self.fields['printfacet_images'].queryset = PrintFacet.get_printfacet_images(printfacet)
        if self.story.audiofacetstory.all():
            audiofacet = self.story.audiofacetstory.all()[0]
            self.fields['audiofacet_images'].queryset = AudioFacet.get_audiofacet_images(audiofacet)
        if self.story.videofacetstory.all():
            videofacet = self.story.videofacetstory.all()[0]
            self.fields['videofacet_images'].queryset = VideoFacet.get_videofacet_images(videofacet)

    select_all = forms.BooleanField(
        widget=CheckboxInput,
    )

    webfacet = forms.BooleanField(
        widget=CheckboxInput,
    )

    printfacet = forms.BooleanField(
        widget=CheckboxInput,
    )

    audiofacet = forms.BooleanField(
        widget=CheckboxInput,
    )

    videofacet = forms.BooleanField(
        widget=CheckboxInput,
    )


    webfacet_sa = forms.BooleanField(
        widget=CheckboxInput,
    )

    printfacet_sa = forms.BooleanField(
        widget=CheckboxInput,
    )

    audiofacet_sa = forms.BooleanField(
        widget=CheckboxInput,
    )

    videofacet_sa = forms.BooleanField(
        widget=CheckboxInput,
    )

    webfacet_images = forms.ModelMultipleChoiceField(
        widget=CheckboxSelectMultiple,
        queryset = ImageAsset.objects.all()
    )

    printfacet_images = forms.ModelMultipleChoiceField(
        widget=CheckboxSelectMultiple,
        queryset = ImageAsset.objects.all()
    )

    audiofacet_images = forms.ModelMultipleChoiceField(
        widget=CheckboxSelectMultiple,
        queryset = ImageAsset.objects.all()
    )

    videofacet_images = forms.ModelMultipleChoiceField(
        widget=CheckboxSelectMultiple,
        queryset = ImageAsset.objects.all()
    )
