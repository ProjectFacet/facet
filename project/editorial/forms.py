import datetime

from django import forms
from django.utils.safestring import mark_safe
from django.contrib.auth import get_user_model

from editorial.models import User, Organization, Network, Story


# class EditUserProfile(forms.ModelForm):
#     """ Handle a user completing their profile."""
#
#     class Meta:
#         model = User
#         fields = ['first_name', 'last_name', 'credit_name', 'title', 'phone', 'bio',
#                  'expertise', 'facebook', 'twitter', 'linkedin', 'instagram', 'snapchat', 'vine',]
#
#         widgets = {}


class StoryForm(forms.ModelForm):
    class Meta:
        model = Story
        fields =
        exclude = ['series_id', 'owner', 'creation_date', 'team', 'share_with','collaborate_with', 'embargo', 'embargo_datetime']
