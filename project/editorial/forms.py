import datetime

from django import forms
from django.utils.safestring import mark_safe
from django.contrib.auth import get_user_model
from django.forms import Textarea, TextInput, RadioSelect

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
        self.delimiter = kwargs.pop("delimiter", ",")
        super(ArrayFieldSelectMultiple, self).__init__(*args, **kwargs)

    def render_options(self, choices, value):
        if isinstance(value,str):
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
    """" Form to create a new series. """

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
            "team": ArrayFieldSelectMultiple(
                choices=User.objects.all(), attrs={'class': 'chosen'}),
        }

# ------------------------------ #
#          Facet Forms           #
# ------------------------------ #

class WebFacetForm(forms.ModelForm):
    """ Webfacet form. """

    class Meta:
        model = WebFacet
        fields = [
            'code',
            'title',
            'excerpt',
            'wf_description',
            'content',
            'length',
            'keywords',
            'status',
            'due_edit',
            'run_date',
            'share_note',
        ]
        # widgets = {
        #     "keywords": ArrayFieldSelectMultiple(attrs={'class': 'chosen'}),
        # }


class PrintFacetForm(forms.ModelForm):
    """ Printfacet form. """

    class Meta:
        model = PrintFacet
        fields = [
            'code',
            'title',
            'excerpt',
            'pf_description',
            'content',
            'length',
            'keywords',
            'status',
            'due_edit',
            'run_date',
            'share_note',
        ]


class AudioFacetForm(forms.ModelForm):
    """ Audiofacet form. """

    class Meta:
        model = AudioFacet
        fields = [
            'code',
            'title',
            'excerpt',
            'af_description',
            'content',
            'length',
            'keywords',
            'status',
            'due_edit',
            'run_date',
            'share_note',
        ]

class VideoFacetForm(forms.ModelForm):
    """ Videofacet form. """

    class Meta:
        model = VideoFacet
        fields = [
            'code',
            'title',
            'excerpt',
            'vf_description',
            'content',
            'length',
            'keywords',
            'status',
            'due_edit',
            'run_date',
            'share_note',
        ]

# ------------------------------ #
#         Comment Forms          #
# ------------------------------ #

class CommentForm(forms.ModelForm):
    """ Private Comment form. """

    class Meta:
        model = Comment
        fields = ['text']
