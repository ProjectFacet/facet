"""Forms for Facets and related entities."""

from bootstrap3_datetime.widgets import DateTimePicker
from django import forms
from django.db.models import Q
from django.forms import Textarea, TextInput, Select, CheckboxInput
from editorial.models import (
    Facet,
    FacetTemplate,
    ContentLicense,
)
from editorial.models.facets import COMMON_FIELDS
from tinymce.widgets import TinyMCE

from editorial.widgets import ArrayFieldSelectMultiple


# from django.contrib.staticfiles.templatetags.staticfiles import static


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
            'name': TextInput(
                attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Label'}),
            'description': Textarea(
                attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Description'}),
            'is_active': CheckboxInput(
                attrs={'class': 'c-input c-checkbox c-indicator c-indicator-default'}),
            # 'fields': CheckboxSelectMultiple(attrs={'class': 'c-input c-checkbox c-indicator c-indicator-default'}),
        }


def get_facet_form_for_template(template_id):
    """Return custom facet form."""

    extra_fields = FacetTemplate.objects.get(id=template_id).fields_used

    class FacetForm(forms.ModelForm):
        """Form for a facet. Dynamically selects fields based on template."""

        def __init__(self, *args, **kwargs):
            story = kwargs.pop('story', None)
            user = kwargs.pop('user', None)
            template = kwargs.pop('template', None)
            organization = kwargs.pop('organization', None)

            super(FacetForm, self).__init__(*args, **kwargs)

            if story:
                self.instance.story = story
            if template:
                self.instance.template = template
            if user:
                self.instance.owner = user
            if organization:
                self.instance.organization = organization

            # limit to org users or users or a collaborating organization (done via model method)
            self.fields['credit'].queryset = self.instance.story.get_story_team_vocab()
            self.fields['editor'].queryset = self.instance.story.get_story_team_vocab()

            if 'content_license' in self.fields:
                self.fields['content_license'].queryset = ContentLicense.objects.filter(
                    Q(organization=self.instance.story.organization) | Q(
                        organization__isnull=True))
                self.fields['content_license'].empty_label = 'Select a license'
            if 'producer' in self.fields:
                self.fields['producer'].queryset = self.instance.story.get_story_team_vocab()
                self.fields['producer'].empty_label = 'Select a producer'

        due_edit = forms.DateTimeField(
            required=False,
            widget=DateTimePicker(
                options={'format': 'YYYY-MM-DD HH:mm'},
                attrs={'id': 'dueedit_picker'}
            )
        )

        run_date = forms.DateTimeField(
            required=False,
            widget=DateTimePicker(
                options={'format': 'YYYY-MM-DD HH:mm'},
                attrs={'id': 'rundate_picker'}
            )
        )

        tape_datetime = forms.DateTimeField(
            required=False,
            widget=DateTimePicker(
                options={'format': 'YYYY-MM-DD HH:mm'},
                attrs={'id': 'tapedate_picker'}
            )
        )

        content = forms.CharField(widget=TinyMCE(attrs={'rows': 20, }))

        class Meta:
            model = Facet
            fields = list(COMMON_FIELDS) + extra_fields

            widgets = {
                'name': TextInput(
                    attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Label'}),
                'headline': TextInput(
                    attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Headline'}),
                'description': Textarea(
                    attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Description'}),
                'editor': ArrayFieldSelectMultiple(
                    attrs={'class': 'chosen-select form-control facet-select',
                           'id': 'facet-editor', 'data-placeholder': 'Select Editing Team'}),
                'credit': ArrayFieldSelectMultiple(
                    attrs={'class': 'chosen-select form-control facet-select',
                           'id': 'facet-credit', 'data-placeholder': 'Select Credited Team'}),
                'status': Select(attrs={'class': 'form-control'}),
                'keywords': TextInput(
                    attrs={'class': 'form-control', 'placeholder': 'Keywords'}),
                # Optional Fields
                'excerpt': TextInput(
                    attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Excerpt'}),
                'update_note': TextInput(attrs={'class': 'form-control', 'rows': 2,
                                                'placeholder': 'Updates to this facet.'}),
                'share_note': TextInput(attrs={'class': 'form-control', 'rows': 2,
                                               'placeholder': 'Notes for sharing this facet.'}),
                'edit_note': TextInput(attrs={'class': 'form-control', 'rows': 2,
                                              'placeholder': 'Notes on editing this facet'}),
                'dateline': TextInput(
                    attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Dateline'}),
                'topic_code': TextInput(
                    attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Topic'}),
                'internal_code': TextInput(attrs={'class': 'form-control', 'rows': 2,
                                                  'placeholder': 'Internal code'}),
                'length': TextInput(attrs={'class': 'form-control', 'rows': 2,
                                           'placeholder': 'Length (time)'}),
                'wordcount': TextInput(
                    attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Wordcount'}),
                'content_license': Select(attrs={'class': 'form-control'}),
                'related_links': TextInput(attrs={'class': 'form-control', 'rows': 2,
                                                  'placeholder': 'Related links (urls)'}),
                'github_link': TextInput(
                    attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Github Link'}),
                'sources': TextInput(attrs={'class': 'form-control', 'rows': 2,
                                            'placeholder': 'Sources in this story'}),
                'pronounciations': TextInput(attrs={'class': 'form-control', 'rows': 2,
                                                    'placeholder': 'Pronounciations'}),
                'sponsors': TextInput(
                    attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Sponsors'}),
                'pull_quotes': TextInput(
                    attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Pull quotes'}),
                'embeds': TextInput(attrs={'class': 'form-control', 'rows': 2,
                                           'placeholder': 'Embeds (html)'}),
                'sidebar_content': TextInput(attrs={'class': 'form-control', 'rows': 2,
                                                    'placeholder': 'Sidebar content'}),
                'producer': Select(attrs={'class': 'form-control'}),
                'series_title': TextInput(
                    attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Series Title'}),
                'episode_number': TextInput(attrs={'class': 'form-control', 'rows': 2,
                                                   'placeholder': 'Episode Number'}),
                'usage_rights': TextInput(
                    attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Usage Rights'}),
                'locations': TextInput(attrs={'class': 'form-control', 'rows': 2,
                                              'placeholder': 'Filming Locations'}),
                'custom_one': TextInput(attrs={'class': 'form-control', 'rows': 2,
                                               'placeholder': 'Custom Info One'}),
                'custom_two': TextInput(attrs={'class': 'form-control', 'rows': 2,
                                               'placeholder': 'Custom Info Two'}),
                'custom_three': TextInput(attrs={'class': 'form-control', 'rows': 2,
                                                 'placeholder': 'Custom Info Three'}),
                'custom_four': TextInput(attrs={'class': 'form-control', 'rows': 2,
                                                'placeholder': 'Custom Info Four'}),
                'custom_five': TextInput(attrs={'class': 'form-control', 'rows': 2,
                                                'placeholder': 'Custom Info Five'}),
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
