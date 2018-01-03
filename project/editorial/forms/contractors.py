"""Forms for Contractors and related entities.

    Contractor
    Call
    Pitch
    Assignment

"""

from bootstrap3_datetime.widgets import DateTimePicker
from django import forms
from django.db.models import Q
from django.forms import Textarea, TextInput, Select

from editorial.models import (
    ContractorProfile,
    TalentEditorProfile,
    ContractorSubscription,
    OrganizationContractorAffiliation,
    Story,
    Facet,
    Call,
    Pitch,
    Assignment,
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
            'public',
        ]

        widgets = {
            'address': Textarea(
                attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Address'}),
            'availability': TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Availability'}),
            'current_location': TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Current Location'}),
            'gear': Textarea(
                attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Gear'}),
            'portfolio_link1': TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Portfolio Link 1'}),
            'portfolio_link2': TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Portfolio Link 2'}),
            'portfolio_link3': TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Portfolio Link 3'}),
        }


class OrganizationContractorAffiliationForm(forms.ModelForm):
    """Handles creation and editing of the details of a contractor's
    relationship with a specific organization.
    """

    # def __init__(self, *args, **kwargs):
    #     super(CallForm, self).__init__(*args, **kwargs)
    #     # set empty label
    #     self.fields['status'].empty_label = 'Contractor status'

    contractor = forms.ModelChoiceField(
        queryset=ContractorProfile.objects.filter(public=True),
        widget=forms.Select(attrs={'class': 'c-select', 'id': 'affiliation-contractor'}),
        required=True,
    )

    class Meta:
        model = OrganizationContractorAffiliation

        fields = [
            'contractor',
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
            'strengths': TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Strengths'}),
            'conflicts': TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Conflicts'}),
            'editor_notes': Textarea(
                attrs={'class': 'form-control', 'rows': 12, 'placeholder': 'Editor Notes'}),
        }


class ContractorSubscriptionForm(forms.ModelForm):
    """ Form to edit a contractor subscription."""

    class Meta:
        model = ContractorSubscription
        fields = ['standard']


class CallForm(forms.ModelForm):
    """Handles creation and editing of a call."""

    def __init__(self, *args, **kwargs):
        org = kwargs.pop("organization")
        super(CallForm, self).__init__(*args, **kwargs)
        # set empty label
        self.fields['status'].empty_label = 'Call status'

    expiration_date = forms.DateTimeField(
        required=False,
        widget=DateTimePicker(
            options={'format': 'YYYY-MM-DD HH:mm'},
            attrs={'id': 'story-embargo-picker'})
    )

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
            'timeframe': TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Timeframe'}),
            'status': Select(attrs={'class': 'c-select', 'id': 'call-status'}),
        }


class PitchForm(forms.ModelForm):
    """Handles creation and editing of a pitch."""

    recipient = forms.ModelChoiceField(
        queryset=TalentEditorProfile.objects.filter(public=True),
        widget=forms.Select(attrs={'class': 'c-select', 'id': 'pitch-recipient'}),
        required=True,
    )

    class Meta:
        model = Pitch

        fields = [
            'name',
            'text',
            'status',
            'exclusive',
            'recipient',
        ]

        widgets = {
            'name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}),
            'text': Textarea(attrs={'class': 'form-control', 'placeholder': 'Text'}),
            'status': Select(attrs={'class': 'c-select', 'id': 'pitch-status'}),
        }


class AssignmentForm(forms.ModelForm):
    """Handles creation and editing of a assignment."""

    def __init__(self, *args, **kwargs):
        org = kwargs.pop("organization")
        super(AssignmentForm, self).__init__(*args, **kwargs)
        # limit to stories or facets owned by an organization or that an org is a collaborator on
        self.fields['story'].queryset = Story.objects.filter(
            Q(organization=org) | Q(collaborate_with=org))
        self.fields['facet'].queryset = Facet.objects.filter(Q(organization=org))
        # set empty labels
        self.fields['contractor'].empty_label = "Select a contractor"
        self.fields['story'].empty_label = 'Select a story'
        self.fields['facet'].empty_label = 'Select a facet'

    contractor = forms.ModelChoiceField(
        queryset=ContractorProfile.objects.filter(public=True),
        widget=forms.Select(attrs={'class': 'c-select', 'id': 'assignment-contractor'}),
        required=True,
    )

    class Meta:
        model = Assignment

        fields = [
            'name',
            'text',
            'rate',
            'contractor',
            'complete',
            'story',
            'facet',
        ]

        widgets = {
            'name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}),
            'text': Textarea(attrs={'class': 'form-control', 'placeholder': 'Text'}),
            'rate': TextInput(attrs={'class': 'form-control', 'placeholder': 'Rate'}),
            'story': Select(attrs={'class': 'c-select', 'id': 'assignment-story'}),
            'facet': Select(attrs={'class': 'c-select', 'id': 'assignment-facet'}),
        }
