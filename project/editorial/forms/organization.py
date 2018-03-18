"""Forms for Users and related entities."""

from django import forms
from django.forms import Textarea, TextInput, Select, CheckboxInput

from editorial.models import (
    User,
    Organization,
    Network,
    OrganizationSubscription,
)


class OrganizationForm(forms.ModelForm):
    """Create an Organization."""

    class Meta:
        model = Organization
        fields = ['name', 'org_description', 'location', 'logo']
        widgets = {
            'name': TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Organization Name'}),
            'location': TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Organization Location'}),
            'org_description': Textarea(
                attrs={'class': 'form-control', 'placeholder': 'Organization Description'}),
        }


class OrganizationSubscriptionForm(forms.ModelForm):
    """ Form to edit an organization subscription."""

    class Meta:
        model = OrganizationSubscription
        fields = ['collaborations', 'contractors', ]
