"""Forms for Users and related entities."""

from django import forms
from django.forms import Textarea, TextInput, Select, CheckboxInput

from editorial.models import (
    User,
    Organization,
    Network,
    OrganizationSubscription,
)



class NetworkForm(forms.ModelForm):
    """Create a new network."""

    class Meta:
        model = Network

        fields = ['name', 'network_description', 'logo']

        widgets = {
            'name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Network Name'}),
            'network_description': Textarea(
                attrs={'class': 'form-control', 'placeholder': 'Description'}),
        }


class AddToNetworkForm(forms.Form):
    """Add an organization to a network."""


class InviteToNetworkForm(forms.Form):
    """Send private message inviting an organization to a network."""

    invited_user = forms.CharField(max_length=100)
