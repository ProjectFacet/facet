# import datetime
#
# from django import forms
# from django.utils.safestring import mark_safe
# from django.contrib.auth import get_user_model
#
# from editorial.models import User, Organization, Network
#
#
# class SignupForm(forms.Form):
#     # Field for allauth
#     email = forms.EmailField(
#         max_length=100,
#     )
#
#     def save(self, user):
#         editorial_user.email = data.get('email')
