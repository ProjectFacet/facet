"""Forms for Assets and related entities."""

from django import forms
from django.forms import Textarea, TextInput, Select, Form

from editorial.models import (
    ImageAsset,
    DocumentAsset,
    AudioAsset,
    VideoAsset,
    SimpleImage,
    SimpleDocument,
    SimpleAudio,
    SimpleVideo,
)


##############################################################################################
# Convenience API:
#
# To reduce repetition in widgets (all get class=form-control, etc), these functions simplify
# the API for widgets in forms.
#
# This is experimental for now (Joel); if useful, this should be our pattern.
#
# This stuff should be moved out of this file into editorial/widgets.py, and this thinking
# should be used in the other forms/*.py files.

def _TextInput(placeholder=None):
    """Convenience wrapper for TextInput widgets."""

    attrs = {'class': 'form-control'}

    if placeholder:
        attrs['placeholder'] = placeholder

    return TextInput(attrs=attrs)


def _Textarea(placeholder=None, rows=None):
    """Convenience wrapper for Textarea widgets."""

    attrs = {'class': 'form-control'}

    if placeholder:
        attrs['placeholder'] = placeholder

    if rows:
        attrs['rows'] = rows

    return Textarea(attrs=attrs)


def _Select():
    """Convenience wrapper for Select widgets."""

    return Select(attrs={'class': 'form-control'})


##############################################################################################
# Asset Forms:  adding assets to a facet

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
            'title': _TextInput('Asset Title'),
            'description': _Textarea('Description', rows=3),
            'attribution': _Textarea('Attribution', rows=3),
            'asset_type': _Select(),
            'keywords': _Textarea('Keywords', rows=2),
        }


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
            'title': _TextInput('Asset Title'),
            'description': _Textarea('Description', rows=3),
            'attribution': _Textarea('Attribution', rows=3),
            'asset_type': _Select(),
            'keywords': _Textarea('Keywords', rows=2),
        }


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
            'title': _TextInput('Asset Title'),
            'description': _Textarea('Description', rows=3),
            'attribution': _Textarea('Attribution', rows=3),
            'link': _TextInput('Link'),
            'asset_type': _Select(),
            'keywords': _Textarea('Keywords', rows=2),
        }


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
            'title': _TextInput('Asset Title'),
            'description': _Textarea('Description', rows=3),
            'attribution': _Textarea('Attribution', rows=3),
            'link': _TextInput('Link'),
            'asset_type': _Select(),
            'keywords': _Textarea('Keywords', rows=2),
        }


##############################################################################################
# Associating Forms: associating existing library assets to a facet.

class LibraryImageAssociateForm(Form):
    """Form for adding existing library images to a facet."""

    def __init__(self, *args, **kwargs):
        """Add field with vocabulary set to organization's assets."""

        org = kwargs.pop("organization")
        super(LibraryImageAssociateForm, self).__init__(*args, **kwargs)

        self.fields['images'] = forms.ModelMultipleChoiceField(
            queryset=org.imageasset_set.all(),
            required=False)


class LibraryDocumentAssociateForm(Form):
    """Form for adding existing library documents to a facet."""

    def __init__(self, *args, **kwargs):
        """Add field with vocabulary set to organization's assets."""

        org = kwargs.pop("organization")
        super(LibraryDocumentAssociateForm, self).__init__(*args, **kwargs)

        self.fields['documents'] = forms.ModelMultipleChoiceField(
            queryset=org.documentasset_set.all(),
            required=False)


class LibraryAudioAssociateForm(Form):
    """Form for adding existing library audio to a facet."""

    def __init__(self, *args, **kwargs):
        """Add field with vocabulary set to organization's assets."""

        org = kwargs.pop("organization")
        super(LibraryAudioAssociateForm, self).__init__(*args, **kwargs)

        self.fields['audio'] = forms.ModelMultipleChoiceField(
            queryset=org.audioasset_set.all(),
            required=False)


class LibraryVideoAssociateForm(Form):
    """Form for adding existing library video to a facet."""

    def __init__(self, *args, **kwargs):
        """Add field with vocabulary set to organization's assets."""

        org = kwargs.pop("organization")
        super(LibraryVideoAssociateForm, self).__init__(*args, **kwargs)
        self.fields['video'] = forms.ModelMultipleChoiceField(
            queryset=org.videoasset_set.all(),
            required=False)


##############################################################################################
# Simple Asset Forms

class SimpleImageForm(forms.ModelForm):
    """Upload a simple image."""

    class Meta:
        model = SimpleImage

        fields = [
            'title',
            'description',
            'photo',
        ]

        widgets = {
            'title': _TextInput('Title'),
            'description': _Textarea('Description', rows=3),
        }


class SimpleDocumentForm(forms.ModelForm):
    """Upload a simple document."""

    class Meta:
        model = SimpleDocument

        fields = [
            'title',
            'description',
            'document',
        ]

        widgets = {
            'title': _TextInput('Title'),
            'description': _Textarea('Description', rows=3),
        }


class SimpleAudioForm(forms.ModelForm):
    """Upload a simple audio file."""

    class Meta:
        model = SimpleAudio

        fields = [
            'title',
            'description',
            'audio',
            'link',
        ]

        widgets = {
            'title': _TextInput('Title'),
            'description': _Textarea('Description', rows=3),
            'link': _TextInput('Link'),
        }


class SimpleVideoForm(forms.ModelForm):
    """Add a simple video."""

    class Meta:
        model = SimpleVideo

        fields = [
            'title',
            'description',
            'link',
        ]

        widgets = {
            'title': _TextInput('Title'),
            'description': _Textarea('Description', rows=3),
            'link': _TextInput('Link'),
        }


class SimpleImageLibraryAssociateForm(Form):
    """Form for adding existing simple images to an Organization, Network,
    Project, Series, Task or Event."""

    def __init__(self, *args, **kwargs):
        """Add field with vocabulary set to organization's assets."""

        org = kwargs.pop("organization")
        super(SimpleImageLibraryAssociateForm, self).__init__(*args, **kwargs)

        self.fields['simpleimages'] = forms.ModelMultipleChoiceField(
            queryset=org.simpleimage_set.all(),
            required=False)


class SimpleDocumentLibraryAssociateForm(Form):
    """Form for adding existing simple documents to an Organization, Network,
    Project, Series, Task or Event."""

    def __init__(self, *args, **kwargs):
        """Add field with vocabulary set to organization's assets."""

        org = kwargs.pop("organization")
        super(SimpleDocumentLibraryAssociateForm, self).__init__(*args, **kwargs)

        self.fields['simpledocuments'] = forms.ModelMultipleChoiceField(
            queryset=org.simpledocument_set.all(),
            required=False)


class SimpleAudioLibraryAssociateForm(Form):
    """Form for adding existing simple audio files to an Organization, Network,
    Project, Series, Task or Event."""

    def __init__(self, *args, **kwargs):
        """Add field with vocabulary set to organization's assets."""

        org = kwargs.pop("organization")
        super(SimpleAudioLibraryAssociateForm, self).__init__(*args, **kwargs)

        self.fields['simpleaudio'] = forms.ModelMultipleChoiceField(
            queryset=org.simpleaudio_set.all(),
            required=False)


class SimpleVideoLibraryAssociateForm(Form):
    """Form for adding existing simple video to an Organization, Network,
    Project, Series, Task or Event."""

    def __init__(self, *args, **kwargs):
        """Add field with vocabulary set to organization's assets."""

        org = kwargs.pop("organization")
        super(SimpleVideoLibraryAssociateForm, self).__init__(*args, **kwargs)

        self.fields['simplevideo'] = forms.ModelMultipleChoiceField(
            queryset=org.simplevideo_set.all(),
            required=False)
