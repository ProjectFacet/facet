"""Forms for Note and related entities.

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
    NetworkNote,
    OrganizationNote,
    ProjectNote,
    SeriesNote,
    StoryNote,
    UserNote
)



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
