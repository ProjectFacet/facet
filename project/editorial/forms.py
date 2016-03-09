""" Forms for editorial app."""

import datetime
from bootstrap3_datetime.widgets import DateTimePicker
from ourwidgets import OurDateTimePicker
from django import forms
from django.utils.safestring import mark_safe
from django.contrib.auth import get_user_model
from django.forms import Textarea, TextInput, RadioSelect, Select, NumberInput, CheckboxInput, CheckboxSelectMultiple
from datetimewidget.widgets import DateTimeWidget
from tinymce.widgets import TinyMCE

from editorial.models import (
    User,
    Organization,
    Network,
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
    ImageAsset,
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
        fields = ['first_name', 'last_name', 'username', 'credit_name', 'title', 'phone', 'email', 'bio', 'location',
                 'expertise', 'website', 'facebook', 'github', 'twitter', 'linkedin', 'instagram', 'snapchat', 'vine', 'photo']
        widgets = {
            'expertise': Textarea(attrs={'rows':2}),
        }

# ------------------------------ #
#      Organization Forms        #
# ------------------------------ #

class OrganizationForm(forms.ModelForm):
    """ Create an Organization. """

    class Meta:
        model = Organization
        fields = ['name', 'org_description', 'location', 'logo']


# ------------------------------ #
#         Network Forms          #
# ------------------------------ #

class NetworkForm(forms.ModelForm):
    """ Create a new network. """

    class Meta:
        model = Network
        fields = ['name', 'network_description', 'logo']


class AddToNetworkForm(forms.Form):
    """ Add an organization to a network."""
    pass


class InviteToNetworkForm(forms.Form):
    """ Send private message inviting an organization to a network."""

    invited_user = forms.CharField(max_length=100)

# ------------------------------ #
#          Series Forms          #
# ------------------------------ #

class SeriesForm(forms.ModelForm):
    """ Form to create a new series. """

    class Meta:
        model = Series
        fields = ['name', 'series_description', 'collaborate', 'collaborate_with', 'team']
        widgets = {
            'team': ArrayFieldSelectMultiple(attrs={'class': 'chosen-select', 'id':'series-team'}),
            'collaborate_with': ArrayFieldSelectMultiple(attrs={'class': 'chosen-select', 'id':'collaborate-with'}),
            }

    class Media:
        css = {'all': ('/static/css/chosen.min.css')
        }
        js = ('/static/js/chosen.jquery.min.js')

# ------------------------------ #
#          Story Forms           #
# ------------------------------ #

class StoryForm(forms.ModelForm):
    """ Form to create a new story. """

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(StoryForm, self).__init__(*args, **kwargs)
        self.fields['collaborate_with'].queryset = Organization.get_org_collaborators(self.request.user.organization)
        self.fields['team'].queryset = Organization.get_org_users(self.request.user.organization)

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
            'all': ('/static/css/bootstrap-datetimepicker.css', '/static/css/chosen.min.css')
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
            'length',
            'keywords',
            'status',
            'due_edit',
            'run_date',
            'share_note',
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
            'all': ('/static/css/bootstrap-datetimepicker.css', '/static/css/chosen.min.css')
        }
        js = ('/static/scripts/chosen.jquery.min.js',
         '/static/scripts/moment.js',
         '/static/scripts/jquery.datetimepicker.js',
         '/static/scripts/bootstrap-datetimepicker.js',
         '/static/scripts/tiny_mce/tinymce.min.js',)


class AudioFacetForm(forms.ModelForm):
    """ Audiofacet form. """

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
            'length',
            'keywords',
            'status',
            'due_edit',
            'run_date',
            'share_note',
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
            'all': ('/static/css/bootstrap-datetimepicker.css', '/static/css/chosen.min.css')
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
            'length',
            'keywords',
            'status',
            'due_edit',
            'run_date',
            'share_note',
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
            'all': ('/static/css/bootstrap-datetimepicker.css', '/static/css/chosen.min.css')
        }
        js = ('/static/scripts/chosen.jquery.min.js',
         '/static/scripts/moment.js',
         '/static/scripts/jquery.datetimepicker.js',
         '/static/scripts/bootstrap-datetimepicker.js',
         '/static/scripts/tiny_mce/tinymce.min.js',)


# ------------------------------ #
#          Asset Forms           #
# ------------------------------ #

class ImageAssetForm(forms.ModelForm):
    """Upload image to a facet."""

    class Meta:
        model = ImageAsset
        fields = [
            'asset_title',
            'asset_description',
            'attribution',
            'photo',
            'image_type',
            'keywords',
        ]
        widgets = {
            'asset_description': Textarea(attrs={'rows':3}),
            'attribution': Textarea(attrs={'rows':3}),
            'image_type': Select(attrs={'class': 'form-control'}),
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
