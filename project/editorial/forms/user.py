"""Forms for Users and related entities."""

from django import forms
from django.forms import Textarea, TextInput, Select, CheckboxInput

from editorial.models import (
    User,
    Organization,
    Network,
    OrganizationSubscription,
)



class AddUserForm(forms.ModelForm):
    """Handles creating users for an organization."""

    class Meta:
        model = User
        fields = ['email', 'password', 'username', 'user_type']
        widgets = {
            'email': TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'password': TextInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
            'username': TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'user_type': Select(attrs={'class': 'c-select', 'id': 'user-type'}),
        }


class UserProfileForm(forms.ModelForm):
    """Handle a user completing their profile."""

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'credit_name',
            'title',
            'phone',
            'email',
            'bio',
            'location',
            'expertise',
            'website',
            'photo',
        ]
        widgets = {
            'first_name': TextInput(
                attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'credit_name': TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Credit Name'}),
            'title': TextInput(attrs={'class': 'form-control', 'placeholder': 'Title'}),
            'location': TextInput(attrs={'class': 'form-control', 'placeholder': 'Location'}),
            'email': TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'phone': TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone'}),
            'website': TextInput(attrs={'class': 'form-control', 'placeholder': 'Website'}),
            'bio': Textarea(
                attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Professional Bio'}),
            'expertise': Textarea(
                attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Expertise'}),
        }
