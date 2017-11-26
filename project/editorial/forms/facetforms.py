"""Forms for Facets and related entities.

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
    Facet,
    FacetTemplate,
    ContentLicense,
)

from editorial.models.facets import COMMON_FIELDS


class FacetTemplateForm(forms.ModelForm):
    """Form for editing facet templates."""

    def clean_fields_used(self):
        """There may be spaces around entries; strip these off."""

        return [f.strip() for f in self.cleaned_data['fields_used']]

    # fields = forms.ArrayField(
    #     required=True,
    #     widget=forms.CheckboxSelectMultiple,
    #     choices=FACETTEMPLATE_FIELD_CHOICES,
    # )

    class Meta:
        model = FacetTemplate
        fields = "__all__"
        widgets = {
            'name': TextInput(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Label'}),
            'description': Textarea(attrs={'class': 'form-control', 'rows':3, 'placeholder': 'Description'}),
            'is_active': CheckboxInput(attrs={'class': 'c-input c-checkbox c-indicator c-indicator-default'}),
            # 'fields': CheckboxSelectMultiple(attrs={'class': 'c-input c-checkbox c-indicator c-indicator-default'}),
        }


def get_facet_form_for_template(template_id):
    """Return custom facet form."""

    extra_fields = FacetTemplate.objects.get(id=template_id).fields_used

    class FacetForm(forms.ModelForm):
        """Form for a facet. Dynamically selects fields based on template."""

        def __init__(self, *args, **kwargs):
            self.story = kwargs.pop("story")
            super(FacetForm, self).__init__(*args, **kwargs)
            self.fields['credit'].queryset = self.story.get_story_team_vocab()
            self.fields['editor'].queryset = self.story.get_story_team_vocab()
            # self.fields['producer'].queryset = self.story.get_story_team_vocab()
            self.fields['content_license'].empty_label='Select a license'
            # self.fields['producer'].empty_label='Select a producer'

        due_edit = forms.DateTimeField(
            required=False,
            widget=OurDateTimePicker(
                options={'format': 'YYYY-MM-DD HH:mm'},
                attrs={'id': 'dueedit_picker'}
            )
        )

        run_date = forms.DateTimeField(
            required=False,
            widget=OurDateTimePicker(
                options={'format': 'YYYY-MM-DD HH:mm'},
                attrs={'id': 'rundate_picker'}
            )
        )

        tape_datetime = forms.DateTimeField(
            required=False,
            widget=OurDateTimePicker(
                options={'format': 'YYYY-MM-DD HH:mm'},
                attrs={'id': 'tapedate_picker'}
            )
        )

        #FIXME To be limited to the licenses belonging to the org + CC
        content_license = forms.ModelChoiceField(
            queryset=ContentLicense.objects.all(),
            widget=forms.Select,
            required=False,
        )

        content = forms.CharField(widget=TinyMCE(attrs={'rows':20, 'id': 'content'}))

        class Meta:
            model = Facet
            fields = list(COMMON_FIELDS) + extra_fields

            widgets = {
                'name': TextInput(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Label'}),
                'headline': TextInput(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Headline'}),
                'description': Textarea(attrs={'class': 'form-control', 'rows':3, 'placeholder': 'Description'}),
                'editor': ArrayFieldSelectMultiple(attrs={'class': 'chosen-select form-control facet-select', 'id':'facet-editor', 'data-placeholder': 'Select Editing Team'}),
                'credit': ArrayFieldSelectMultiple(attrs={'class': 'chosen-select form-control facet-select', 'id':'facet-credit', 'data-placeholder': 'Select Credited Team'}),
                'status': Select(attrs={'class': 'form-control'}),
                'keywords': TextInput(attrs={'class': 'form-control', 'placeholder': 'Keywords'}),
                #Optional Fields
                'excerpt': TextInput(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Excerpt'}),
                'update_note': TextInput(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Updates to this facet.'}),
                'share_note': TextInput(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Notes for sharing this facet.'}),
                'edit_note': TextInput(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Notes on editing this facet'}),
                'dateline': TextInput(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Dateline'}),
                'topic_code': TextInput(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Topic'}),
                'internal_code': TextInput(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Internal code'}),
                'length': TextInput(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Length (time)'}),
                'wordcount': TextInput(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Wordcount'}),
                'content_license': Select(attrs={'class': 'form-control'}),
                'related_links': TextInput(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Related links (urls)'}),
                'github_link': TextInput(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Github Link'}),
                'sources': TextInput(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Sources in this story'}),
                'pronounciations': TextInput(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Pronounciations'}),
                'sponsors': TextInput(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Sponsors'}),
                'pull_quotes': TextInput(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Pull quotes'}),
                'embeds': TextInput(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Embeds (html)'}),
                'sidebar_content': TextInput(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Sidebar content'}),
                'producer': Select(attrs={'class': 'form-control'}),
                'series_title': TextInput(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Series Title'}),
                'episode_number': TextInput(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Episode Number'}),
                'usage_rights': TextInput(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Usage Rights'}),
                'locations': TextInput(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Filming Locations'}),
                'custom_one': TextInput(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Custom One'}),
                'custom_two': TextInput(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Custom Two'}),
                'custom_three': TextInput(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Custom Three'}),
                'custom_four': TextInput(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Custom Four'}),
                'custom_five': TextInput(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Custom Five'}),
            }

        def get_fields_to_show(self):
            """Returns list of extra fields, to display on form."""

            return [self[f] for f in extra_fields]

    return FacetForm


class FacetPreCreateForm(forms.Form):
    """Form to "pre-create" a facet; used to create correct Facet form."""

    name = forms.CharField(
        label="Facet Name",
    )

    template = forms.ModelChoiceField(
        FacetTemplate.objects.all(),
    )

    # class Meta:
    #     widgets = {
    #         'name': TextInput(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Label'}),
    #         'template': Select(attrs={'class': 'form-control'}),
    #     }
