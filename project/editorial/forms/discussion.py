"""Forms for Discussion and related entities."""

from django import forms
from django.forms import Textarea

from editorial.models import (
    PrivateMessage,
    Comment,
)


class PrivateMessageForm(forms.ModelForm):
    """Message form for private messages."""

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(PrivateMessageForm, self).__init__(*args, **kwargs)

        if self.request.org:
            # FIXME Limit Private Message Recipient list to org team members or network partner team members
            # If the organization manages contractors, allow private messages between contractors and editors
            self.fields['recipient'].queryset = self.request.user.get_user_contact_list_vocab()

    class Meta:
        model = PrivateMessage

        fields = ['recipient', 'subject', 'text']

        widgets = {
            'subject': Textarea(
                attrs={'id': 'private-comment-subject', 'required': True,
                       'placeholder': 'Subject', 'class': 'form-control', 'rows': 1}
            ),
            'text': Textarea(
                attrs={'id': 'private-comment', 'required': True, 'placeholder': 'Message',
                       'class': 'form-control', 'rows': 10}
            ),
        }


class CommentForm(forms.ModelForm):
    """Generic comment form."""

    class Meta:
        model = Comment

        fields = ['text']

        widgets = {
            'text': Textarea(
                attrs={'id': 'comment-text', 'required': True, 'placeholder': 'Comment',
                       'class': 'form-control', 'rows': 2}
            ),
        }
