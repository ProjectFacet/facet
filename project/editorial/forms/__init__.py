""" Forms for editorial application.

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


from .peopleforms import AddUserForm, UserProfileForm, OrganizationForm, OrganizationSubscriptionForm, NetworkForm, AddToNetworkForm, InviteToNetworkForm
from .contractorforms import ContractorProfileForm, ContractorSubscriptionForm, OrganizationContractorAffiliationForm, CallForm, PitchForm, AssignmentForm
from .projectforms import ProjectForm
from .seriesforms import SeriesForm
from .storyforms import StoryForm
from .facetforms import FacetTemplateForm, get_facet_form_for_template, FacetPreCreateForm
from .assetforms import ImageAssetForm, DocumentAssetForm, AudioAssetForm, VideoAssetForm, SimpleImageForm, SimpleDocumentForm, SimpleAudioForm, SimpleVideoForm, LibraryImageAssociateForm, LibraryDocumentAssociateForm
from .taskforms import TaskForm
from .eventforms import EventForm
from .discussionforms import PrivateMessageForm, CommentForm
from .noteforms import NetworkNoteForm, OrganizationNoteForm, ProjectNoteForm, SeriesNoteForm, StoryNoteForm, UserNoteForm
from .platformaccountsforms import PlatformAccountForm, PlatformAccountFormSet

from editorial.models.facets import COMMON_FIELDS
