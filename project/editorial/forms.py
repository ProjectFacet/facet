import datetime

from bootstrap3_datetime.widgets import DateTimePicker
from django import forms
from django.utils.safestring import mark_safe
from django.contrib.auth import get_user_model
from django.forms import Textarea, TextInput, RadioSelect, Select, NumberInput, CheckboxInput
from datetimewidget.widgets import DateTimeWidget
from tinymce.widgets import TinyMCE

from editorial.models import (
    User,
    Organization,
    Network,
    NetworkOrganization,
    Story,
    Series,
    WebFacet,
    PrintFacet,
    AudioFacet,
    VideoFacet,
    PrivateMessage,
    Comment,
    NetworkNote,
    OrganizationNote,
    UserNote,
    SeriesNote,
    StoryNote,
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


class UserProfileForm(forms.ModelForm):
    """ Handle a user completing their profile."""

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'credit_name', 'title', 'phone', 'bio', 'location',
                 'expertise', 'facebook', 'twitter', 'linkedin', 'instagram', 'snapchat', 'vine',]

# ------------------------------ #
#      Organization Forms        #
# ------------------------------ #

class CreateOrganization(forms.ModelForm):
    """ Create an Organization. """

    class Meta:
        model = Organization
        fields = ['name', 'org_description']


class EditOrganization(forms.ModelForm):
    """ Edit an Organization. """

    class Meta:
        model = Organization
        fields = ['name', 'org_description']

# ------------------------------ #
#         Network Forms          #
# ------------------------------ #

class NetworkForm(forms.ModelForm):
    """ Create a new network. """

    class Meta:
        model = Network
        fields = ['name', 'network_description']


class AddToNetworkForm(forms.ModelForm):
    """ Add an organization to a network."""

    class Meta:
        model = NetworkOrganization
        fields = []

# ------------------------------ #
#          Series Forms          #
# ------------------------------ #

class SeriesForm(forms.ModelForm):
    """ Form to create a new series. """

    class Meta:
        model = Series
        fields = ['name', 'series_description', 'collaborate', 'collaborate_with', 'team']
        widgets = {
            'team': ArrayFieldSelectMultiple(attrs={'class': 'chosen-select', 'id':'seriies-team'}),
            'collaborate_with': ArrayFieldSelectMultiple(attrs={'class': 'chosen-select', 'id':'collaborate-with'}),
            }

# ------------------------------ #
#          Story Forms           #
# ------------------------------ #

class StoryForm(forms.ModelForm):
    """ Form to create a new story. """

    series = forms.ModelChoiceField(
        queryset=Series.objects.all(),
        widget=forms.Select,
        required=False,
    )

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
        fields = ['name', 'story_description', 'series', 'collaborate', 'collaborate_with','team', 'embargo', 'embargo_datetime', 'sensitive', 'share', 'ready_to_share', 'share_with', 'share_with_date', 'archived' ]
        widgets = {
            'team': ArrayFieldSelectMultiple(attrs={'class': 'chosen-select', 'id':'story-team'}),
            'collaborate_with': ArrayFieldSelectMultiple(attrs={'class': 'chosen-select', 'id':'collaborate-with'}),
            'share_with': ArrayFieldSelectMultiple(attrs={'class': 'chosen-select', 'id':'share-with'}),
            'series': Select(attrs={'class': 'form-control'}),
        }

    class Media:
        css = {'all': ('/static/css/chosen.min.css')
        }
        js = ('/static/js/chosen.jquery.min.js')

# ------------------------------ #
#          Facet Forms           #
# ------------------------------ #

class WebFacetForm(forms.ModelForm):
    """ Webfacet form. """

    due_edit = forms.DateTimeField(
        required=False,
        widget=DateTimePicker(
            options={'format': 'YYYY-MM-DD HH:mm'},
            attrs={'id': 'wf_dueedit_picker'}
        )
    )

    run_date = forms.DateTimeField(
        required=False,
        widget=DateTimePicker(
            options={'format': 'YYYY-MM-DD HH:mm'},
            attrs={'id': 'wf_rundate_picker'}
        )
    )

    wf_content = forms.CharField(widget=TinyMCE(attrs={'rows':25, 'id': 'wf_content'}))

    class Meta:
        model = WebFacet
        fields = [
            'code',
            'title',
            'excerpt',
            'wf_description',
            'wf_content',
            'length',
            'keywords',
            'status',
            'due_edit',
            'run_date',
            'share_note',
            'captions',
            'editor',
            'credit',
        ]
        widgets = {
            'credit': ArrayFieldSelectMultiple(attrs={'class': 'chosen-select form-control', 'id':'webfacet-credit'}),
            'title': Textarea(attrs={'rows':2}),
            'wf_description': Textarea(attrs={'rows':3}),
            'excerpt': Textarea(attrs={'rows':4}),
            'captions': Textarea(attrs={'rows':5}),
            'share_note': Textarea(attrs={'rows':5}),
            'editor': Select(attrs={'class': 'form-control'}),
            'status': Select(attrs={'class': 'form-control'}),
            'length': NumberInput(attrs={'class': 'form-control'}),
        }

    class Media:
        css = {
            'all': ('static/css/bootstrap-datetimepicker.css', '/static/css/chosen.min.css')
        }
        js = ('/static/js/chosen.jquery.min.js',
         '/static/scripts/moment.js',
         '/static/scripts/jquery.datetimepicker.js',
         '/static/scripts/bootstrap-datetimepicker.js',
         '/static/scripts/tiny_mce/tinymce.min.js',)


class PrintFacetForm(forms.ModelForm):
    """ Printfacet form. """

    due_edit = forms.DateTimeField(
        required=False,
        widget=DateTimePicker(
            options={'format': 'YYYY-MM-DD HH:mm'},
            attrs={'id': 'pf_dueedit_picker'}
        )
    )

    run_date = forms.DateTimeField(
        required=False,
        widget=DateTimePicker(
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
            'length',
            'keywords',
            'status',
            'due_edit',
            'run_date',
            'share_note',
            'captions',
            'editor',
            'credit',
        ]
        widgets = {
            'credit': ArrayFieldSelectMultiple(attrs={'class': 'chosen-select form-control', 'id':'printfacet-credit'}),
            'title': Textarea(attrs={'rows':2}),
            'pf_description': Textarea(attrs={'rows':3}),
            'excerpt': Textarea(attrs={'rows':4}),
            'captions': Textarea(attrs={'rows':5}),
            'share_note': Textarea(attrs={'rows':5}),
            'editor': Select(attrs={'class': 'form-control'}),
            'status': Select(attrs={'class': 'form-control'}),
            'length': NumberInput(attrs={'class': 'form-control'}),
        }

    class Media:
        css = {
            'all': ('static/css/bootstrap-datetimepicker.css', '/static/css/chosen.min.css')
        }
        js = ('/static/js/chosen.jquery.min.js',
         '/static/scripts/moment.js',
         '/static/scripts/jquery.datetimepicker.js',
         '/static/scripts/bootstrap-datetimepicker.js',
         '/static/scripts/tiny_mce/tinymce.min.js',)


class AudioFacetForm(forms.ModelForm):
    """ Audiofacet form. """

    due_edit = forms.DateTimeField(
        required=False,
        widget=DateTimePicker(
            options={'format': 'YYYY-MM-DD HH:mm'},
            attrs={'id': 'af_dueedit_picker'}
        )
    )

    run_date = forms.DateTimeField(
        required=False,
        widget=DateTimePicker(
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
            'length',
            'keywords',
            'status',
            'due_edit',
            'run_date',
            'share_note',
            'captions',
            'editor',
            'credit',
        ]
        widgets = {
            'credit': ArrayFieldSelectMultiple(attrs={'class': 'chosen-select form-control', 'id':'audiofacet-credit'}),
            'title': Textarea(attrs={'rows':2}),
            'af_description': Textarea(attrs={'rows':3}),
            'excerpt': Textarea(attrs={'rows':4}),
            'captions': Textarea(attrs={'rows':5}),
            'share_note': Textarea(attrs={'rows':5}),
            'editor': Select(attrs={'class': 'form-control'}),
            'status': Select(attrs={'class': 'form-control'}),
            'length': NumberInput(attrs={'class': 'form-control'}),
        }

    class Media:
        css = {
            'all': ('static/css/bootstrap-datetimepicker.css', '/static/css/chosen.min.css')
        }
        js = ('/static/js/chosen.jquery.min.js',
         '/static/scripts/moment.js',
         '/static/scripts/jquery.datetimepicker.js',
         '/static/scripts/bootstrap-datetimepicker.js',
         '/static/scripts/tiny_mce/tinymce.min.js',)


class VideoFacetForm(forms.ModelForm):
    """ Videofacet form. """

    due_edit = forms.DateTimeField(
        required=False,
        widget=DateTimePicker(
            options={'format': 'YYYY-MM-DD HH:mm'},
            attrs={'id': 'vf_dueedit_picker'}
        )
    )

    run_date = forms.DateTimeField(
        required=False,
        widget=DateTimePicker(
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
            'length',
            'keywords',
            'status',
            'due_edit',
            'run_date',
            'share_note',
            'captions',
            'editor',
            'credit',
        ]
        widgets = {
            'credit': ArrayFieldSelectMultiple(attrs={'class': 'chosen-select form-control', 'id':'videofacet-credit'}),
            'title': Textarea(attrs={'rows':2}),
            'vf_description': Textarea(attrs={'rows':3}),
            'excerpt': Textarea(attrs={'rows':4}),
            'captions': Textarea(attrs={'rows':5}),
            'share_note': Textarea(attrs={'rows':5}),
            'editor': Select(attrs={'class': 'form-control'}),
            'status': Select(attrs={'class': 'form-control'}),
            'length': NumberInput(attrs={'class': 'form-control'}),
        }

    class Media:
        css = {
            'all': ('static/css/bootstrap-datetimepicker.css', '/static/css/chosen.min.css')
        }
        js = ('/static/js/chosen.jquery.min.js',
         '/static/scripts/moment.js',
         '/static/scripts/jquery.datetimepicker.js',
         '/static/scripts/bootstrap-datetimepicker.js',
         '/static/scripts/tiny_mce/tinymce.min.js',)

# ------------------------------ #
#         Comment Forms          #
# ------------------------------ #

class PrivateMessageForm(forms.ModelForm):
    """ Message form for private messages. """

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
#         Note Forms          #
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
