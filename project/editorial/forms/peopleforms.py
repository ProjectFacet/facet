"""Forms for Users and related entities.

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
    Network,
    Platform,
    PlatformAccount,
)


# ------------------------------ #
#          User Forms            #
# ------------------------------ #

class AddUserForm(forms.ModelForm):
    """ Handles creating users for an organization."""

    class Meta:
        model = User
        fields = ['email', 'password', 'username', 'is_superuser', 'is_staff', 'user_type']
        widgets = {
            'email': TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'password': TextInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
            'username': TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'is_superuser': CheckboxInput(attrs={'class': 'c-indicator c-indicator-default'}),
            'is_staff': CheckboxInput(attrs={'class': 'c-indicator c-indicator-default'}),
            'user_type': Select(attrs={'class': 'c-select', 'id':'user-type'}),
            }


class UserProfileForm(forms.ModelForm):
    """ Handle a user completing their profile."""

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'credit_name', 'title', 'phone', 'email', 'bio', 'location',
                 'expertise', 'website', 'photo']
        widgets = {
            'first_name': TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'credit_name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Credit Name'}),
            'username': TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'title': TextInput(attrs={'class': 'form-control', 'placeholder': 'Title'}),
            'location': TextInput(attrs={'class': 'form-control', 'placeholder': 'Location'}),
            'email': TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'phone': TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone'}),
            'website': TextInput(attrs={'class': 'form-control', 'placeholder': 'Website'}),
            'bio': Textarea(attrs={'class': 'form-control', 'rows':2, 'placeholder': 'Professional Bio'}),
            'expertise': Textarea(attrs={'class': 'form-control', 'rows':2, 'placeholder': 'Expertise'}),
        }


# ------------------------------ #
#      Organization Forms        #
# ------------------------------ #

class OrganizationForm(forms.ModelForm):
    """ Create an Organization. """

    class Meta:
        model = Organization
        fields = ['name', 'org_description', 'location', 'logo']
        widgets = {
            'name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Organization Name'}),
            'location': TextInput(attrs={'class': 'form-control', 'placeholder': 'Organization Location'}),
            'org_description': Textarea(attrs={'class': 'form-control', 'placeholder': 'Organization Description'}),
            }

# ------------------------------ #
#         Network Forms          #
# ------------------------------ #

class NetworkForm(forms.ModelForm):
    """ Create a new network. """

    class Meta:
        model = Network
        fields = ['name', 'network_description', 'logo']
        widgets = {
            'name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Network Name'}),
            'network_description': Textarea(attrs={'class': 'form-control', 'placeholder': 'Description'}),
            }


class AddToNetworkForm(forms.Form):
    """ Add an organization to a network."""
    pass


class InviteToNetworkForm(forms.Form):
    """ Send private message inviting an organization to a network."""

    invited_user = forms.CharField(max_length=100)
