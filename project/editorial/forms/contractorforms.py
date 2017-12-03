"""Forms for Contractors and related entities.

    Contractor
    Call
    Pitch
    Assignment

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
    User,
    Organization,
    ContractorProfile,
    OrganizationContractorAffiliation,
    Call,
    Pitch,
    Assignment,
    SimpleImage,
    SimpleDocument,
    SimpleAudio,
    SimpleVideo,
)


class ContractorProfileForm(forms.ModelForm):
    """Handles creation and editing of a contractor's profile."""

    class Meta:
        model = ContractorProfile
        fields = [
            'resume',
            'address',
            'availability',
            'current_location',
            'gear',
            'portfolio_link1',
            'portfolio_link2',
            'portfolio_link3',
        ]
        widgets = {
            'address': Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Address'}),
            'availability': TextInput(attrs={'class': 'form-control', 'placeholder': 'Availability'}),
            'current_location': TextInput(attrs={'class': 'form-control', 'placeholder': 'Current Location'}),
            'gear': Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Gear'}),
            'portfolio_link1': TextInput(attrs={'class': 'form-control', 'placeholder': 'Portfolio Link 1'}),
            'portfolio_link2': TextInput(attrs={'class': 'form-control', 'placeholder': 'Portfolio Link 2'}),
            'portfolio_link3': TextInput(attrs={'class': 'form-control', 'placeholder': 'Portfolio Link 3'}),
        }


class OrganizationContractorRelationshipForm(forms.ModelForm):
    """Handles creation and editing of the details of a contractor's
    relationship with a specific organization.
    """

    class Meta:
        model = OrganizationContractorAffiliation
        fields = [
            'w9_on_file',
            'rates',
            'strengths',
            'conflicts',
            'editor_notes',
            'talent_pool',
            'status',
        ]
        widgets = {
            'rates': TextInput(attrs={'class': 'form-control', 'placeholder': 'Rates'}),
            'strengths': TextInput(attrs={'class': 'form-control', 'placeholder': 'Strengths'}),
            'conflicts': TextInput(attrs={'class': 'form-control', 'placeholder': 'Conflicts'}),
            'editor_notes': TextInput(attrs={'class': 'form-control', 'placeholder': 'Editor Notes'}),
            'status': Select(attrs={'class': 'c-select', 'id':'contractor-status'}),
        }


class CallForm(forms.ModelForm):
    """Handles creation and editing of a call."""

    class Meta:
        model = Call
        fields = [
            'name',
            'text',
            'expiration_date',
            'is_active',
            'urgent',
            'timeframe',
            'status',
        ]
        widgets = {
            'name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}),
            'text': Textarea(attrs={'class': 'form-control', 'placeholder': 'Text'}),
            'timeframe': TextInput(attrs={'class': 'form-control', 'placeholder': 'Timeframe'}),
            'status': Select(attrs={'class': 'c-select', 'id':'call-status'}),
        }


class PitchForm(forms.ModelForm):
    """Handles creation and editing of a pitch."""

    class Meta:
        model = Pitch
        fields = [
            'name',
            'text',
            'status',
            'exclusive',
        ]
        widgets = {
            'name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}),
            'text': Textarea(attrs={'class': 'form-control', 'placeholder': 'Text'}),
            'status': Select(attrs={'class': 'c-select', 'id':'pitch-status'}),
        }


class AssignmentForm(forms.ModelForm):
    """Handles creation and editing of a assignment."""

    class Meta:
        model = Assignment
        fields = [
            'name',
            'text',
            'rate',
        ]
        widgets = {
            'name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}),
            'text': Textarea(attrs={'class': 'form-control', 'placeholder': 'Text'}),
            'rate': TextInput(attrs={'class': 'form-control', 'placeholder': 'Rates'}),
        }
