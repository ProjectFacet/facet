import datetime

from django import forms
from django.utils.safestring import mark_safe
from django.contrib.auth import get_user_model

from editorial.models import User, Organization, Network


class UserProfile(forms.ModelForm):
    """ Handle a user completing their profile."""

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'credit_name', 'title', 'phone', 'bio', 'expertise', 'facebook', 'twitter', 'linkedin', 'instagram', 'snapchat', 'vine',]
        widgets = {}
