"""Forms for Platform Accounts and related entities."""

from django.db.models import Q

from editorial.widgets import ArrayFieldSelectMultiple
from django import forms
from django.forms import TextInput, Select, HiddenInput
from django.forms import modelformset_factory

from editorial.models import (
    Project,
    PlatformAccount,
)


# ------------------------------ #
#             Forms              #
# ------------------------------ #


class PlatformAccountForm(forms.ModelForm):
    """Form to create social accounts associated with a user."""

    def __init__(self, *args, **kwargs):
        """Handle passing of org/user info into form."""

        super(PlatformAccountForm, self).__init__(*args, **kwargs)

        # Handle case of existing record (get from instance) or new, blank record

        if 'instance' in kwargs:
            org = kwargs['instance'].organization
        else:
            org = kwargs['initial']['organization']

        if org:
            # limit team to org users
            self.fields['team'].queryset = org.get_org_users()
            # limit project to org projects or projects on which an org is a collaborator
            self.fields['project'].queryset = Project.objects.filter(
                Q(organization=org) | Q(collaborate_with=org))

    class Meta:
        model = PlatformAccount
        fields = [
            'id',
            'user',
            'name',
            'platform',
            'url',
            'description',
            'team',
            'organization',
            'project',
        ]
        widgets = {
            'id': HiddenInput(),
            'name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}),
            'platform': Select(attrs={'class': 'c-select', 'id': 'account-platform'}),
            'url': TextInput(attrs={'class': 'form-control', 'placeholder': 'URL'}),
            'description': TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Description'}),
            'team': ArrayFieldSelectMultiple(
                attrs={'class': 'chosen-select', 'id': 'share-with',
                       'data-placeholder': 'Select Team'}),
            'user': HiddenInput(),
            'organization': HiddenInput(),
            'project': Select(attrs={'class': 'c-select', 'id': 'account-project'}),
        }


PlatformAccountFormSet = modelformset_factory(PlatformAccount, form=PlatformAccountForm)
