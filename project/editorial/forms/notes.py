"""Forms for Note and related entities."""

from django import forms
from django.forms import Textarea

from editorial.models import (
    Note,
)


class NoteForm(forms.ModelForm):
    """Note form for a note."""

    class Meta:
        model = Note

        fields = ['title', 'text', 'important']

        widgets = {
            'title': Textarea(
                attrs={'id': 'nn-title', 'required': True, 'placeholder': 'Note Title',
                       'class': 'form-control', 'rows': 1}
            ),
            'text': Textarea(
                attrs={'id': 'nn-text', 'required': True, 'placeholder': 'Note',
                       'class': 'form-control', 'rows': 10}
            ),
            # 'keywords': TextInput(attrs={'class': 'form-control', 'placeholder': 'Keywords'}),
        }
