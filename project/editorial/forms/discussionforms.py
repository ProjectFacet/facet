"""Forms for Discussion and related entities.

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
    PrivateMessage,
    Discussion,
    Comment,
    User,
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
            # TODO Limit Private Message Recipient list to org team members or network partner team members
            # If the organization manages contractors, allow private messages between contractors and editors
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


class TaskCommentForm(forms.ModelForm):
    """ Comment form. """

    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': Textarea(
                attrs={'id':'comment', 'required': True, 'placeholder': 'Comment', 'class': 'form-control', 'rows':2}
            ),
        }


class EventCommentForm(forms.ModelForm):
    """ Comment form. """

    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': Textarea(
                attrs={'id':'comment', 'required': True, 'placeholder': 'Comment', 'class': 'form-control', 'rows':2}
            ),
        }
