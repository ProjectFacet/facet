""" Forms for editorial app."""

import datetime
from bootstrap3_datetime.widgets import DateTimePicker
from ourwidgets import OurDateTimePicker
from django import forms
from django.utils.safestring import mark_safe
from django.contrib.auth import get_user_model
from django.forms import Textarea, TextInput, RadioSelect, Select, NumberInput, CheckboxInput, CheckboxSelectMultiple, FileField
from django.contrib.postgres.fields import ArrayField
from datetimewidget.widgets import DateTimeWidget
from tinymce.widgets import TinyMCE
# from django.contrib.staticfiles.templatetags.staticfiles import static

from editorial.models import (
    User,
    Organization,
    Network,
    Platform,
    PlatformAccount,
    Project,
    Story,
    Series,
    Facet,
    ContentLicense,
    WebFacet,
    PrintFacet,
    AudioFacet,
    VideoFacet,
    Task,
    Event,
    PrivateMessage,
    Comment,
    NetworkNote,
    OrganizationNote,
    UserNote,
    ProjectNote,
    SeriesNote,
    StoryNote,
    ImageAsset,
    DocumentAsset,
    AudioAsset,
    VideoAsset,
    FacetTemplate,
    )

from .models.facets import COMMON_FIELDS


# FACETTEMPLATE_FIELD_CHOICES = (
#     ('excerpt', 'Excerpt'),
#     ('update_note', 'Update Note'),
#     ('share_note', 'Share Note'),
#     ('edit_note', 'Edit Note'),
#     ('dateline', 'Dateline'),
#     ('topic_code', 'Topic Code'),
#     ('internal_code', 'Internal Code'),
#     ('content_license', 'Content License'),
#     ('length', 'Length'),
#     ('wordcount', 'Wordcount'),
#     ('related_links', 'Related Links'),
#     ('github_link', 'Github Link'),
#     ('embeds', 'Embeds'),
#     ('sources', 'Sources'),
#     ('pronounciations', 'Pronounciations'),
#     ('sponsors', 'Sponsors'),
#     ('pull_quotes', 'Pull Quotes'),
#     ('sidebar_content', 'Sidebar Content'),
#     ('producer', 'Producer'),
#     ('series_title', 'Series Title'),
#     ('episode_number', 'Episode Number'),
#     ('usage_rights', 'Usage Rights'),
#     ('tape_datetime', 'Tape Datetime'),
#     ('locations', 'Locations'),
#     ('custom_one', 'Custom One'),
#     ('custom_two', 'Custom Two'),
#     ('custom_three', 'Custom Three'),
#     ('custom_four', 'Custom Four'),
#     ('custom_five', 'Custom Five'),
# )

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
                'editor': Select(attrs={'class': 'form-control'}),
                'credit': ArrayFieldSelectMultiple(attrs={'class': 'chosen-select form-control facet-select', 'id':'facet-credit', 'data-placeholder': 'Select Credited Team'}),
                'status': Select(attrs={'class': 'form-control'}),
                'keywords': TextInput(attrs={'class': 'form-control', 'placeholder': 'Keywords'}),
                #Optional Fields
                'excerpt': TextInput(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Excerpt'}),
                'update_note': TextInput(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Updates to this facet.'}),
                'share_note': TextInput(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Notes for sharing this facet.'}),
                'edit_note': TextInput(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Notes on editing this facet'}),
                'dateline': TextInput(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Label'}),
                'topic_code': TextInput(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Label'}),
                'internal_code': TextInput(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Label'}),
                'length': TextInput(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Label'}),
                'wordcount': TextInput(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Label'}),
                'content_license': Select(attrs={'class': 'form-control'}),
                'related_links': TextInput(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Label'}),
                'github_link': TextInput(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Label'}),
                'sources': TextInput(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Label'}),
                'pronunciations': TextInput(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Label'}),
                'sponsors': TextInput(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Label'}),
                'pull_quotes': TextInput(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Label'}),
                'embeds': TextInput(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Label'}),
                'sidebar_content': TextInput(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Label'}),
                # 'producer': Select(attrs={'class': 'form-control'}),
                'series_title': TextInput(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Label'}),
                'episode_number': TextInput(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Label'}),
                'usage_rights': TextInput(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Label'}),
                'locations': TextInput(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Label'}),
                'custom_one': TextInput(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Label'}),
                'custom_two': TextInput(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Label'}),
                'custom_three': TextInput(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Label'}),
                'custom_four': TextInput(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Label'}),
                'custom_five': TextInput(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Label'}),
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



# ------------------------------ #
#        Parent Forms            #
# ------------------------------ #

class ArrayFieldSelectMultiple(forms.SelectMultiple):

    def __init__(self, *args, **kwargs):
        self.delimiter = kwargs.pop('delimiter', ',')
        super(ArrayFieldSelectMultiple, self).__init__(*args, **kwargs)

    def render_options(self, choices, value):
        if isinstance(value, basestring):
            value = value.split(self.delimiter)
        return super(ArrayFieldSelectMultiple, self).render_options(choices, value)


# ------------------------------ #
#          User Forms            #
# ------------------------------ #

class AddUserForm(forms.ModelForm):
    """ Handles creating users for an organization."""

    class Meta:
        model = User
        fields = ['email', 'password', 'username', 'is_superuser', 'is_staff', 'user_type']
        widgets = {
            'email': TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'password': TextInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
            'username': TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'is_superuser': CheckboxInput(attrs={'class': 'c-indicator c-indicator-default'}),
            'is_staff': CheckboxInput(attrs={'class': 'c-indicator c-indicator-default'}),
            'user_type': Select(attrs={'class': 'c-select', 'id':'user-type'}),
            }

class UserProfileForm(forms.ModelForm):
    """ Handle a user completing their profile."""

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'credit_name', 'title', 'phone', 'email', 'bio', 'location',
                 'expertise', 'website', 'photo']
        widgets = {
            'first_name': TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'credit_name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Credit Name'}),
            'username': TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'title': TextInput(attrs={'class': 'form-control', 'placeholder': 'Title'}),
            'location': TextInput(attrs={'class': 'form-control', 'placeholder': 'Location'}),
            'email': TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'phone': TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone'}),
            'website': TextInput(attrs={'class': 'form-control', 'placeholder': 'Website'}),
            'bio': Textarea(attrs={'class': 'form-control', 'rows':2, 'placeholder': 'Professional Bio'}),
            'expertise': Textarea(attrs={'class': 'form-control', 'rows':2, 'placeholder': 'Expertise'}),
        }

# ------------------------------ #
#      Organization Forms        #
# ------------------------------ #

class OrganizationForm(forms.ModelForm):
    """ Create an Organization. """

    class Meta:
        model = Organization
        fields = ['name', 'org_description', 'location', 'logo']
        widgets = {
            'name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Organization Name'}),
            'location': TextInput(attrs={'class': 'form-control', 'placeholder': 'Organization Location'}),
            'org_description': Textarea(attrs={'class': 'form-control', 'placeholder': 'Organization Description'}),
            }

# ------------------------------ #
#         Network Forms          #
# ------------------------------ #

class NetworkForm(forms.ModelForm):
    """ Create a new network. """

    class Meta:
        model = Network
        fields = ['name', 'network_description', 'logo']
        widgets = {
            'name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Network Name'}),
            'network_description': Textarea(attrs={'class': 'form-control', 'placeholder': 'Description'}),
            }


class AddToNetworkForm(forms.Form):
    """ Add an organization to a network."""
    pass


class InviteToNetworkForm(forms.Form):
    """ Send private message inviting an organization to a network."""

    invited_user = forms.CharField(max_length=100)


# ------------------------------ #
#          Project Forms          #
# ------------------------------ #

class ProjectForm(forms.ModelForm):
    """ Form to create a new project. """

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(ProjectForm, self).__init__(*args, **kwargs)
        self.fields['collaborate_with'].queryset = Organization.get_org_collaborators_vocab(self.request.user.organization)
        self.fields['team'].queryset = Organization.get_org_users(self.request.user.organization)

    class Meta:
        model = Project
        fields = ['name', 'project_description', 'collaborate', 'collaborate_with', 'team']
        widgets = {
            'name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Project Name'}),
            'project_description': Textarea(attrs={'class': 'form-control', 'placeholder': 'Description'}),
            'team': ArrayFieldSelectMultiple(attrs={'class': 'chosen-select form-control facet-select', 'id':'project-team', 'data-placeholder': 'Select Project Team'}),
            'collaborate': CheckboxInput(attrs={'class': 'c-indicator c-indicator-default'}),
            'collaborate_with': ArrayFieldSelectMultiple(attrs={'class': 'chosen-select form-control facet-select', 'id':'collaborate-with', 'data-placeholder': 'Select Collaborators'}),
            }

    class Media:
        css = {
            'all': ('css/bootstrap-datetimepicker.css', 'css/chosen.min.css')
        }
        js = ('scripts/chosen.jquery.min.js',)


# ------------------------------ #
#          Series Forms          #
# ------------------------------ #

class SeriesForm(forms.ModelForm):
    """ Form to create a new series. """

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(SeriesForm, self).__init__(*args, **kwargs)
        self.fields['collaborate_with'].queryset = Organization.get_org_collaborators_vocab(self.request.user.organization)
        self.fields['team'].queryset = Organization.get_org_users(self.request.user.organization)

    class Meta:
        model = Series
        fields = ['name', 'series_description', 'collaborate', 'collaborate_with', 'team']
        widgets = {
            'name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Series Name'}),
            'series_description': Textarea(attrs={'class': 'form-control', 'placeholder': 'Description'}),
            'team': ArrayFieldSelectMultiple(attrs={'class': 'chosen-select form-control facet-select', 'id':'series-team', 'data-placeholder': 'Select Series Team'}),
            'collaborate': CheckboxInput(attrs={'class': 'c-indicator c-indicator-default'}),
            'collaborate_with': ArrayFieldSelectMultiple(attrs={'class': 'chosen-select form-control facet-select', 'id':'collaborate-with', 'data-placeholder': 'Select Collaborators'}),
            }

    class Media:
        css = {
            'all': ('css/bootstrap-datetimepicker.css', 'css/chosen.min.css')
        }
        js = ('scripts/chosen.jquery.min.js',)

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

    series = forms.ModelChoiceField(
        queryset=Series.objects.all(),
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
        }

    # class Media:
    #     css = {
    #         'all': ('css/bootstrap-datetimepicker.css', 'css/chosen.min.css')
    #     }
    #     js = ('scripts/chosen.jquery.min.js',)

# ------------------------------ #
#          Facet Forms           #
# ------------------------------ #



# ------------------------------ #
#          Task Forms          #
# ------------------------------ #

class TaskForm(forms.ModelForm):
    """ Form to create/edit a task. """

    def __init__(self, *args, **kwargs):
        print "IN TASKFORM INIT"
        org = kwargs.pop("organization")
        print "TASKFORM ORG: ", org
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
            # 'upload',
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


# ------------------------------ #
#          Event Forms           #
# ------------------------------ #
class EventForm(forms.ModelForm):
    """ Form to create/edit an event. """

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(EventForm, self).__init__(*args, **kwargs)
        self.fields['team'].queryset = Organization.get_org_users(self.request.user.organization)
        self.fields['evt_organization'].queryset = Organization.get_org_collaborators_vocab(self.request.user.organization)
        self.fields['event_type'].empty_label='Event Type'
        self.fields['evt_organization'].empty_label='Select an Organization'
        self.fields['project'].empty_label='Select a Project'
        self.fields['series'].empty_label='Select a Series'
        self.fields['story'].empty_label='Select a Story'


    projects = forms.ModelChoiceField(
        queryset=Project.objects.all(),
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

    event_date = forms.DateTimeField(
        required=False,
        widget=OurDateTimePicker(
            options={'format': 'YYYY-MM-DD HH:mm'},
            attrs={'id': 'event_eventdate_picker'}
        )
    )

    class Meta:
        model = Event
        fields = [
            'name',
            'text',
            'team',
            'event_type',
            'event_date',
            'venue',
            'evt_organization',
            'project',
            'series',
            'story',
        ]
        widgets = {
            'name': Textarea(attrs={'class': 'form-control', 'rows':2, 'placeholder': 'Name'}),
            'text': Textarea(attrs={'class': 'form-control', 'id':'task-text', 'rows':20, 'placeholder': 'Details'}),
            'team': ArrayFieldSelectMultiple(attrs={'class': 'chosen-select form-control facet-select', 'id':'event-team', 'data-placeholder': 'Team'}),
            'event_type': Select(attrs={'class': 'custom-select', 'id':'task-status'}),
            'evt_organization': Select(attrs={'class': 'custom-select', 'id':'event-organization'}),
            'project': Select(attrs={'class': 'custom-select', 'id':'event-project'}),
            'series': Select(attrs={'class': 'custom-select', 'id':'event-series'}),
            'story': Select(attrs={'class': 'custom-select', 'id':'event-story'}),
            }

    class Media:
        css = {
            'all': ('css/bootstrap-datetimepicker.css', 'css/chosen.min.css')
        }
        js = ('scripts/chosen.jquery.min.js',)


# ------------------------------ #
#          Asset Forms           #
# ------------------------------ #

class ImageAssetForm(forms.ModelForm):
    """Upload image to a facet."""

    class Meta:
        model = ImageAsset
        fields = [
            'title',
            'description',
            'attribution',
            'photo',
            'asset_type',
            'keywords',
        ]
        widgets = {
            'title': TextInput(attrs={'class': 'form-control', 'placeholder': 'Asset Title'}),
            'description': Textarea(attrs={'class': 'form-control', 'rows':3, 'placeholder': 'Description'}),
            'attribution': Textarea(attrs={'class': 'form-control', 'rows':3, 'placeholder': 'Attribution'}),
            'asset_type': Select(attrs={'class': 'form-control'}),
            'keywords': Textarea(attrs={'class': 'form-control', 'rows':2, 'placeholder': 'Keywords'}),
        }


class DocumentAssetForm(forms.ModelForm):
    """Upload document to a facet."""

    class Meta:
        model = DocumentAsset
        fields = [
            'title',
            'description',
            'attribution',
            'document',
            'asset_type',
            'keywords',
        ]
        widgets = {
            'title': TextInput(attrs={'class': 'form-control', 'placeholder': 'Asset Title'}),
            'description': Textarea(attrs={'class': 'form-control', 'rows':3, 'placeholder': 'Description'}),
            'attribution': Textarea(attrs={'class': 'form-control', 'rows':3, 'placeholder': 'Attribution'}),
            'asset_type': Select(attrs={'class': 'form-control'}),
            'keywords': Textarea(attrs={'class': 'form-control', 'rows':2, 'placeholder': 'Keywords'}),
        }


class AudioAssetForm(forms.ModelForm):
    """Upload audio to a facet."""

    class Meta:
        model = AudioAsset
        fields = [
            'title',
            'description',
            'attribution',
            'audio',
            'link',
            'asset_type',
            'keywords',
        ]
        widgets = {
            'title': TextInput(attrs={'class': 'form-control', 'placeholder': 'Asset Title'}),
            'description': Textarea(attrs={'class': 'form-control', 'rows':3, 'placeholder': 'Description'}),
            'attribution': Textarea(attrs={'class': 'form-control', 'rows':3, 'placeholder': 'Attribution'}),
            'link': TextInput(attrs={'class': 'form-control', 'placeholder': 'Link'}),
            'asset_type': Select(attrs={'class': 'form-control'}),
            'keywords': Textarea(attrs={'class': 'form-control', 'rows':2, 'placeholder': 'Keywords'}),
        }


class VideoAssetForm(forms.ModelForm):
    """Upload video to a facet."""

    class Meta:
        model = VideoAsset
        fields = [
            'title',
            'description',
            'attribution',
            'video',
            'link',
            'asset_type',
            'keywords',
        ]
        widgets = {
            'title': TextInput(attrs={'class': 'form-control', 'placeholder': 'Asset Title'}),
            'description': Textarea(attrs={'class': 'form-control', 'rows':3, 'placeholder': 'Description'}),
            'attribution': Textarea(attrs={'class': 'form-control', 'rows':3, 'placeholder': 'Attribution'}),
            'link': TextInput(attrs={'class': 'form-control', 'placeholder': 'Link'}),
            'asset_type': Select(attrs={'class': 'form-control'}),
            'keywords': Textarea(attrs={'class': 'form-control', 'rows':2, 'placeholder': 'Keywords'}),
        }


# ------------------------------ #
#         Comment Forms          #
# ------------------------------ #

class PrivateMessageForm(forms.ModelForm):
    """ Message form for private messages. """

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(PrivateMessageForm, self).__init__(*args, **kwargs)
        if self.request.user.organization:
            self.fields['recipient'].queryset = User.get_user_contact_list_vocab(self.request.user)


    class Meta:
        model = PrivateMessage
        fields = ['recipient', 'subject', 'text']
        widgets = {
            'subject': Textarea(
                attrs={'id':'private-comment-subject', 'required': True, 'placeholder': 'Subject', 'class': 'form-control', 'rows':1}
            ),
            'text': Textarea(
                attrs={'id':'private-comment', 'required': True, 'placeholder': 'Message', 'class': 'form-control', 'rows':10}
            ),
        }


class OrganizationCommentForm(forms.ModelForm):
    """ Comment form for organization. """

    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': Textarea(
                attrs={'id':'organization-comment', 'required': True, 'placeholder': 'Comment', 'class': 'form-control', 'rows':2}
            ),
        }

class NetworkCommentForm(forms.ModelForm):
    """ Comment form for a network. """

    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': Textarea(
                attrs={'id':'network-comment', 'required': True, 'placeholder': 'Comment', 'class': 'form-control', 'rows':2}
            ),
        }


class ProjectCommentForm(forms.ModelForm):
    """ Project comment form."""

    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': Textarea(
                attrs={'id':'project-comment', 'required': True, 'placeholder': 'Comment', 'class': 'form-control', 'rows':1}
            ),
        }


class SeriesCommentForm(forms.ModelForm):
    """ Comment form. """

    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': Textarea(
                attrs={'id':'series-comment', 'required': True, 'placeholder': 'Comment', 'class': 'form-control', 'rows':2}
            ),
        }


class StoryCommentForm(forms.ModelForm):
    """ Comment form. """

    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': Textarea(
                attrs={'id':'story-comment', 'required': True, 'placeholder': 'Comment', 'class': 'form-control', 'rows':2}
            ),
        }

class FacetCommentForm(forms.ModelForm):
    """ Comment form. """

    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': Textarea(
                attrs={'id':'comment', 'required': True, 'placeholder': 'Comment', 'class': 'form-control', 'rows':2}
            ),
        }


# ------------------------------ #
#           Note Forms           #
# ------------------------------ #

class NetworkNoteForm(forms.ModelForm):
    """ Note form for a network note. """

    class Meta:
        model=NetworkNote
        fields = ['title', 'text', 'keywords']
        widgets = {
            'title': Textarea(
                attrs={'id': 'nn-title', 'required': True, 'placeholder': 'Note Title', 'class': 'form-control', 'rows': 1}
            ),
            'text': Textarea(
                attrs={'id':'nn-text', 'required': True, 'placeholder': 'Note', 'class': 'form-control', 'rows':10}
            ),
        }


class OrganizationNoteForm(forms.ModelForm):
    """ Note form for an organization note. """

    class Meta:
        model=OrganizationNote
        fields = ['title', 'text', 'keywords']
        widgets = {
            'title': Textarea(
                attrs={'id': 'on-title', 'required': True, 'placeholder': 'Note Title', 'class': 'form-control', 'rows': 1}
            ),
            'text': Textarea(
                attrs={'id':'on-text', 'required': True, 'placeholder': 'Note', 'class': 'form-control', 'rows':10}
            ),
        }


class ProjectNoteForm(forms.ModelForm):
    """ Note form for a project note. """

    class Meta:
        model=ProjectNote
        fields = ['title', 'text', 'keywords']
        widgets = {
            'title': Textarea(
                attrs={'id': 'project-note-title', 'required': True, 'placeholder': 'Note Title', 'class': 'form-control', 'rows': 1}
            ),
            'text': Textarea(
                attrs={'id':'project-note-text', 'required': True, 'placeholder': 'Note', 'class': 'form-control', 'rows':10}
            ),
        }


class SeriesNoteForm(forms.ModelForm):
    """ Note form for a series note. """

    class Meta:
        model=SeriesNote
        fields = ['title', 'text', 'keywords']
        widgets = {
            'title': Textarea(
                attrs={'id': 'series-title', 'required': True, 'placeholder': 'Note Title', 'class': 'form-control', 'rows': 1}
            ),
            'text': Textarea(
                attrs={'id':'series-text', 'required': True, 'placeholder': 'Note', 'class': 'form-control', 'rows':10}
            ),
        }


class StoryNoteForm(forms.ModelForm):
    """ Note form for a story notes. """

    class Meta:
        model=StoryNote
        fields = ['title', 'text', 'keywords']
        widgets = {
            'title': Textarea(
                attrs={'id': 'story-title', 'required': True, 'placeholder': 'Note Title', 'class': 'form-control', 'rows': 1}
            ),
            'text': Textarea(
                attrs={'id':'story-text', 'required': True, 'placeholder': 'Note', 'class': 'form-control', 'rows':10}
            ),
        }


class UserNoteForm(forms.ModelForm):
    """ Note form for a user note. """

    class Meta:
        model=UserNote
        fields = ['title', 'text', 'keywords']
        widgets = {
            'title': Textarea(
                attrs={'id': 'un-title', 'required': True, 'placeholder': 'Note Title', 'class': 'form-control', 'rows': 1}
            ),
            'text': Textarea(
                attrs={'id':'un-text', 'required': True, 'placeholder': 'Note', 'class': 'form-control', 'rows':10}
            ),
        }

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
