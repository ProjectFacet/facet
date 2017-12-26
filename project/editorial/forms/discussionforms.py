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
from django.db.models import Q
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
            # FIXME Limit Private Message Recipient list to org team members or network partner team members
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


class CommentForm(forms.ModelForm):
    """Generic comment form."""

    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': Textarea(
                attrs={'id':'comment-text', 'required': True, 'placeholder': 'Comment', 'class': 'form-control', 'rows':2}
            ),
        }
