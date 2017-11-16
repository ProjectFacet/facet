""" Forms for editorial app."""

import datetime
from bootstrap3_datetime.widgets import DateTimePicker
from ourwidgets import OurDateTimePicker
from django import forms
from django.utils.safestring import mark_safe
from django.contrib.auth import get_user_model
from django.forms import Textarea, TextInput, RadioSelect, Select, NumberInput, CheckboxInput, CheckboxSelectMultiple, FileField
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


def get_facet_form_for_template(template_id):
    """Return custom facet form."""

    extra_fields = FacetTemplate.objects.get(id=template_id).fields_used

    class FacetForm(forms.ModelForm):
        """Form for a facet. Dynamically selects fields based on template."""

        class Meta:
            model = Facet
            fields = list(COMMON_FIELDS) + extra_fields

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

# class FullUserEditForm(forms.ModelForm):
#     """Form for organization owner or a user to edit a user's full profile."""
#
#     class Meta:
#         model = User
#         fields = ['first_name', 'last_name', 'username', 'credit_name', 'title', 'phone', 'email', 'bio', 'location',
#                  'expertise', 'website', 'facebook', 'github', 'twitter', 'linkedin', 'instagram', 'snapchat', 'vine', 'photo',
#                  'password', 'is_superuser', 'is_staff', 'user_type']
#         widgets = {
#             'expertise': Textarea(attrs={'rows':2}),
#         }

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
    """ Form to create a new story. """

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

class WebFacetForm(forms.ModelForm):
    """ Webfacet form. """

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        self.story = kwargs.pop("story")
        super(WebFacetForm, self).__init__(*args, **kwargs)
        self.fields['credit'].queryset = Story.get_story_team_vocab(self.story)
        self.fields['editor'].queryset = Story.get_story_team_vocab(self.story)


    due_edit = forms.DateTimeField(
        required=False,
        widget=OurDateTimePicker(
            options={'format': 'YYYY-MM-DD HH:mm'},
            attrs={'id': 'wf_dueedit_picker'}
        )
    )

    run_date = forms.DateTimeField(
        required=False,
        widget=OurDateTimePicker(
            options={'format': 'YYYY-MM-DD HH:mm'},
            attrs={'id': 'wf_rundate_picker'}
        )
    )

    wf_content = forms.CharField(widget=TinyMCE(attrs={'rows':40, 'id': 'wf_content'}))

    class Meta:
        model = WebFacet
        fields = [
            'code',
            'title',
            'excerpt',
            'wf_description',
            'wf_content',
            'keywords',
            'status',
            'due_edit',
            'run_date',
            'share_note',
            'editor',
            'credit',
        ]
        widgets = {
            'title': TextInput(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Title'}),
            'code': TextInput(attrs={'class': 'form-control', 'placeholder': 'Code'}),
            'credit': ArrayFieldSelectMultiple(attrs={'class': 'chosen-select form-control facet-select', 'id':'webfacet-credit', 'data-placeholder': 'Select Credited Team'}),
            'editor': Select(attrs={'class': 'form-control'}),
            'wf_description': Textarea(attrs={'class': 'form-control', 'rows':2, 'placeholder': 'Description'}),
            'excerpt': Textarea(attrs={'class': 'form-control', 'rows':2, 'placeholder': 'Excerpt'}),
            'share_note': Textarea(attrs={'class': 'form-control', 'rows':2, 'placeholder': 'Share Note'}),
            'keywords': TextInput(attrs={'class': 'form-control', 'placeholder': 'Keywords'}),
            'status': Select(attrs={'class': 'form-control'}),
        }

    # class Media:
    #     css = {
    #         'all': ('css/bootstrap-datetimepicker.css', 'css/chosen.min.css')
    #     }
    #     js = ('scripts/chosen.jquery.min.js',
    #      'scripts/moment.js',
    #      'scripts/jquery.datetimepicker.js',
    #      'scripts/bootstrap-datetimepicker.js',)


class PrintFacetForm(forms.ModelForm):
    """ Printfacet form. """

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        self.story = kwargs.pop("story")
        super(PrintFacetForm, self).__init__(*args, **kwargs)
        self.fields['credit'].queryset = Story.get_story_team_vocab(self.story)
        self.fields['editor'].queryset = Story.get_story_team_vocab(self.story)

    due_edit = forms.DateTimeField(
        required=False,
        widget=OurDateTimePicker(
            options={'format': 'YYYY-MM-DD HH:mm'},
            attrs={'id': 'pf_dueedit_picker'}
        )
    )

    run_date = forms.DateTimeField(
        required=False,
        widget=OurDateTimePicker(
            options={'format': 'YYYY-MM-DD HH:mm'},
            attrs={'id': 'pf_rundate_picker'}
        )
    )

    pf_content = forms.CharField(widget=TinyMCE(attrs={'rows':25, 'id': 'pf_content'}))

    class Meta:
        model = PrintFacet
        fields = [
            'code',
            'title',
            'excerpt',
            'pf_description',
            'pf_content',
            'keywords',
            'status',
            'due_edit',
            'run_date',
            'share_note',
            'editor',
            'credit',
        ]
        widgets = {
            'title': TextInput(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Title'}),
            'code': TextInput(attrs={'class': 'form-control', 'placeholder': 'Code'}),
            'credit': ArrayFieldSelectMultiple(attrs={'class': 'chosen-select form-control facet-select', 'id':'printfacet-credit', 'data-placeholder': 'Select Credited Team'}),
            'editor': Select(attrs={'class': 'form-control'}),
            'pf_description': Textarea(attrs={'class': 'form-control', 'rows':2, 'placeholder': 'Description'}),
            'excerpt': Textarea(attrs={'class': 'form-control', 'rows':2, 'placeholder': 'Excerpt'}),
            'share_note': Textarea(attrs={'class': 'form-control', 'rows':2, 'placeholder': 'Share Note'}),
            'keywords': TextInput(attrs={'class': 'form-control', 'placeholder': 'Keywords'}),
            'status': Select(attrs={'class': 'form-control'}),
        }

    # class Media:
    #     css = {
    #         'all': ('css/bootstrap-datetimepicker.css', 'css/chosen.min.css')
    #     }
    #     js = ('scripts/chosen.jquery.min.js',
    #      'scripts/moment.js',
    #      'scripts/jquery.datetimepicker.js',
    #      'scripts/bootstrap-datetimepicker.js',)


class AudioFacetForm(forms.ModelForm):
    """ Audiofacet form. """

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        self.story = kwargs.pop("story")
        super(AudioFacetForm, self).__init__(*args, **kwargs)
        self.fields['credit'].queryset = Story.get_story_team_vocab(self.story)
        self.fields['editor'].queryset = Story.get_story_team_vocab(self.story)

    due_edit = forms.DateTimeField(
        required=False,
        widget=OurDateTimePicker(
            options={'format': 'YYYY-MM-DD HH:mm'},
            attrs={'id': 'af_dueedit_picker'}
        )
    )

    run_date = forms.DateTimeField(
        required=False,
        widget=OurDateTimePicker(
            options={'format': 'YYYY-MM-DD HH:mm'},
            attrs={'id': 'af_rundate_picker'}
        )
    )

    af_content = forms.CharField(widget=TinyMCE(attrs={'rows':25, 'id': 'af_content'}))

    class Meta:
        model = AudioFacet
        fields = [
            'code',
            'title',
            'excerpt',
            'af_description',
            'af_content',
            'keywords',
            'status',
            'due_edit',
            'run_date',
            'share_note',
            'editor',
            'credit',
        ]
        widgets = {
            'title': TextInput(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Title'}),
            'code': TextInput(attrs={'class': 'form-control', 'placeholder': 'Code'}),
            'credit': ArrayFieldSelectMultiple(attrs={'class': 'chosen-select form-control facet-select', 'id':'audiofacet-credit', 'data-placeholder': 'Select Credited Team'}),
            'editor': Select(attrs={'class': 'form-control'}),
            'af_description': Textarea(attrs={'class': 'form-control', 'rows':2, 'placeholder': 'Description'}),
            'excerpt': Textarea(attrs={'class': 'form-control', 'rows':2, 'placeholder': 'Excerpt'}),
            'share_note': Textarea(attrs={'class': 'form-control', 'rows':2, 'placeholder': 'Share Note'}),
            'keywords': TextInput(attrs={'class': 'form-control', 'placeholder': 'Keywords'}),
            'status': Select(attrs={'class': 'form-control'}),
        }

    # class Media:
    #     css = {
    #         'all': ('css/bootstrap-datetimepicker.css', 'css/chosen.min.css')
    #     }
    #     js = ('scripts/chosen.jquery.min.js',
    #      'scripts/moment.js',
    #      'scripts/jquery.datetimepicker.js',
    #      'scripts/bootstrap-datetimepicker.js',)


class VideoFacetForm(forms.ModelForm):
    """ Videofacet form. """

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        self.story = kwargs.pop("story")
        super(VideoFacetForm, self).__init__(*args, **kwargs)
        self.fields['credit'].queryset = Story.get_story_team_vocab(self.story)
        self.fields['editor'].queryset = Story.get_story_team_vocab(self.story)

    due_edit = forms.DateTimeField(
        required=False,
        widget=OurDateTimePicker(
            options={'format': 'YYYY-MM-DD HH:mm'},
            attrs={'id': 'vf_dueedit_picker'}
        )
    )

    run_date = forms.DateTimeField(
        required=False,
        widget=OurDateTimePicker(
            options={'format': 'YYYY-MM-DD HH:mm'},
            attrs={'id': 'vf_rundate_picker'}
        )
    )

    vf_content = forms.CharField(widget=TinyMCE(attrs={'rows':25, 'id': 'vf_content'}))

    class Meta:
        model = VideoFacet
        fields = [
            'code',
            'title',
            'excerpt',
            'vf_description',
            'vf_content',
            'keywords',
            'status',
            'due_edit',
            'run_date',
            'share_note',
            'editor',
            'credit',
        ]
        widgets = {
            'title': TextInput(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Title'}),
            'code': TextInput(attrs={'class': 'form-control', 'placeholder': 'Code'}),
            'credit': ArrayFieldSelectMultiple(attrs={'class': 'chosen-select form-control facet-select', 'id':'videofacet-credit', 'data-placeholder': 'Select Credited Team'}),
            'editor': Select(attrs={'class': 'form-control'}),
            'vf_description': Textarea(attrs={'class': 'form-control', 'rows':2, 'placeholder': 'Description'}),
            'excerpt': Textarea(attrs={'class': 'form-control', 'rows':2, 'placeholder': 'Excerpt'}),
            'share_note': Textarea(attrs={'class': 'form-control', 'rows':2, 'placeholder': 'Share Note'}),
            'keywords': TextInput(attrs={'class': 'form-control', 'placeholder': 'Keywords'}),
            'status': Select(attrs={'class': 'form-control'}),
        }

    # class Media:
    #     css = {
    #         'all': ('css/bootstrap-datetimepicker.css', 'css/chosen.min.css')
    #     }
    #     js = ('scripts/chosen.jquery.min.js',
    #      'scripts/moment.js',
    #      'scripts/jquery.datetimepicker.js',
    #      'scripts/bootstrap-datetimepicker.js',)


# ------------------------------ #
#          Task Forms          #
# ------------------------------ #

class TaskForm(forms.ModelForm):
    """ Form to create/edit a task. """

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(TaskForm, self).__init__(*args, **kwargs)
        self.fields['assigned_to'].queryset = Organization.get_org_users(self.request.user.organization)
        self.fields['status'].empty_label='Task Status'
        self.fields['project'].empty_label='Select a Project'
        self.fields['series'].empty_label='Select a Series'
        self.fields['story'].empty_label='Select a Story'
        self.fields['event'].empty_label='Select an Event'

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


class AddImageForm(forms.Form):
    """ Add existing image(s) to a facet."""

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(AddImageForm, self).__init__(*args, **kwargs)
        self.fields['images'].queryset = Organization.get_org_image_library(self.request.user.organization)

    images = forms.ModelMultipleChoiceField(
        widget=CheckboxSelectMultiple,
        queryset = ImageAsset.objects.all()
    )


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


class AddDocumentForm(forms.Form):
    """ Add existing document(s) to a facet."""

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(AddDocumentForm, self).__init__(*args, **kwargs)
        self.fields['documents'].queryset = Organization.get_org_document_library(self.request.user.organization)

    documents = forms.ModelMultipleChoiceField(
        widget=CheckboxSelectMultiple,
        queryset = DocumentAsset.objects.all()
    )


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


class AddAudioForm(forms.Form):
    """ Add existing audio to a facet."""

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(AddAudioForm, self).__init__(*args, **kwargs)
        self.fields['audio'].queryset = Organization.get_org_audio_library(self.request.user.organization)

    audio = forms.ModelMultipleChoiceField(
        widget=CheckboxSelectMultiple,
        queryset = AudioAsset.objects.all()
    )


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


class AddVideoForm(forms.Form):
    """ Add existing video to a facet."""

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(AddVideoForm, self).__init__(*args, **kwargs)
        self.fields['documents'].queryset = Organization.get_org_video_library(self.request.user.organization)

    video = forms.ModelMultipleChoiceField(
        widget=CheckboxSelectMultiple,
        queryset = VideoAsset.objects.all()
    )


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


class WebFacetCommentForm(forms.ModelForm):
    """ Comment form. """

    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': Textarea(
                attrs={'id':'wf-comment', 'required': True, 'placeholder': 'Comment', 'class': 'form-control', 'rows':2}
            ),
        }

class PrintFacetCommentForm(forms.ModelForm):
    """ Comment form. """

    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': Textarea(
                attrs={'id':'pf-comment', 'required': True, 'placeholder': 'Comment', 'class': 'form-control', 'rows':2}
            ),
        }

class AudioFacetCommentForm(forms.ModelForm):
    """ Comment form. """

    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': Textarea(
                attrs={'id':'af-comment', 'required': True, 'placeholder': 'Comment', 'class': 'form-control', 'rows':2}
            ),
        }

class VideoFacetCommentForm(forms.ModelForm):
    """ Comment form. """

    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': Textarea(
                attrs={'id':'vf-comment', 'required': True, 'placeholder': 'Comment', 'class': 'form-control', 'rows':2}
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


class FacetTemplateForm(forms.ModelForm):
    """Form for editing facet templates."""

    def clean_fields_used(self):
        """There may be spaces around entries; strip these off."""

        return [f.strip() for f in self.cleaned_data['fields_used']]

    class Meta:
        model = FacetTemplate
        fields = "__all__"
