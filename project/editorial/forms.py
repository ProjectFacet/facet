import datetime

from bootstrap3_datetime.widgets import DateTimePicker
from django import forms
from django.utils.safestring import mark_safe
from django.contrib.auth import get_user_model
from django.forms import Textarea, TextInput, RadioSelect, Select, NumberInput
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
    Comment,
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

class UserForm(forms.ModelForm):
    """ Handle a user completing their profile."""

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'credit_name', 'title', 'phone', 'bio',
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
        fields = ['name', 'series_description', 'collaborate']

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

    class Meta:
        model = Story
        fields = ['name', 'story_description', 'series', 'collaborate', 'team']
        widgets = {
            'team': ArrayFieldSelectMultiple(
                choices=User.objects.all(), attrs={'class': 'chosen-select'}),
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
            options={'format': 'YYYY-MM-DD HH:mm'}
        )
    )

    run_date = forms.DateTimeField(
        required=False,
        widget=DateTimePicker(
            options={'format': 'YYYY-MM-DD HH:mm'}
        )
    )

    wf_content = forms.CharField(widget=TinyMCE(attrs={'rows':25}))

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
            'credit': ArrayFieldSelectMultiple(
                choices=User.objects.all(), attrs={'class': 'chosen-select form-control'}),
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
            options={'format': 'YYYY-MM-DD HH:mm'}
        )
    )

    run_date = forms.DateTimeField(
        required=False,
        widget=DateTimePicker(
            options={'format': 'YYYY-MM-DD HH:mm'}
        )
    )

    pf_content = forms.CharField(widget=TinyMCE(attrs={'rows':25}))

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
            'credit': ArrayFieldSelectMultiple(
                choices=User.objects.all(), attrs={'class': 'chosen-select form-control'}),
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


class AudioFacetForm(forms.ModelForm):
    """ Audiofacet form. """

    due_edit = forms.DateTimeField(
        required=False,
        widget=DateTimePicker(
            options={'format': 'YYYY-MM-DD HH:mm'}
        )
    )

    run_date = forms.DateTimeField(
        required=False,
        widget=DateTimePicker(
            options={'format': 'YYYY-MM-DD HH:mm'}
        )
    )

    af_content = forms.CharField(widget=TinyMCE(attrs={'rows':25}))

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
            'credit': ArrayFieldSelectMultiple(
                choices=User.objects.all(), attrs={'class': 'chosen-select form-control'}),
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


class VideoFacetForm(forms.ModelForm):
    """ Videofacet form. """

    due_edit = forms.DateTimeField(
        required=False,
        widget=DateTimePicker(
            options={'format': 'YYYY-MM-DD HH:mm'}
        )
    )

    run_date = forms.DateTimeField(
        required=False,
        widget=DateTimePicker(
            options={'format': 'YYYY-MM-DD HH:mm'}
        )
    )

    vf_content = forms.CharField(widget=TinyMCE(attrs={'rows':25}))

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
            'credit': ArrayFieldSelectMultiple(
                choices=User.objects.all(), attrs={'class': 'chosen-select form-control'}),
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

# ------------------------------ #
#         Comment Forms          #
# ------------------------------ #

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
