"""Forms for Users and related entities."""

from django import forms
from django.forms import Textarea, TextInput, Select, CheckboxInput, SelectMultiple

from editorial.models import (
    User,
    Organization,
    Network,
    OrganizationSubscription,
    OrganizationPublicProfile,
)


class OrganizationForm(forms.ModelForm):
    """Create an Organization."""

    class Meta:
        model = Organization
        fields = ['name', 'org_description', 'location', 'logo', 'cover_photo']
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
        fields = ['collaborations', 'contractors', 'partner_discovery', ]


class OrganizationPublicProfileForm(forms.ModelForm):
    """Form to edit organization public profile."""

    class Meta:
        model = OrganizationPublicProfile
        fields = [
            'org_structure',
            'primary_audience',
            'ownership',
            'business_model',
            'unionized_workforce',
            'diversity',
            'special_skills',
            'good_partner',
            'best_coverage',
            'collab_experience',
            'platform_print',
            'platform_online',
            'platform_social',
            'platform_network_tv',
            'platform_cable_tv',
            'platform_radio',
            'platform_podcast',
            'platform_newsletter',
            'platform_streaming_video',
        ]
        widgets = {
            'org_structure': Select(attrs={'class': 'custom-select', 'id': 'org_structure'}),
            'primary_audience': TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Audience'}),
            'ownership': TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Ownership Structure'}),
            'business_model': TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Business Model'}),
            'unionized_workforce': TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Unionization of workforce'}),
            'collab_experience': TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Experience with Collaboration'}),
            'diversity': Textarea(
                attrs={'class': 'form-control', 'placeholder': 'How does your organization foster diversity?'}),
            'special_skills': Textarea(
                attrs={'class': 'form-control', 'placeholder': 'Special skills or strengths in the newsroom'}),
            'good_partner': Textarea(
                attrs={'class': 'form-control', 'placeholder': 'What makes your organization a good partner'}),
            'best_coverage': Textarea(
                attrs={'class': 'form-control', 'placeholder': 'What coverage is your organizatino most proud of?'}),

        }
