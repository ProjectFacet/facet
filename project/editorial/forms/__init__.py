""" Forms for editorial application."""

from .assets import (
    ImageAssetForm,
    DocumentAssetForm,
    AudioAssetForm,
    VideoAssetForm,
    SimpleImageForm,
    SimpleDocumentForm,
    SimpleAudioForm,
    SimpleVideoForm,
    LibraryImageAssociateForm,
    LibraryDocumentAssociateForm,
    LibraryAudioAssociateForm,
    LibraryVideoAssociateForm,
)

from .contractors import (
    ContractorProfileForm,
    ContractorSubscriptionForm,
    OrganizationContractorAffiliationForm,
    CallForm,
    PitchForm,
    AssignmentForm,
)

from .discussion import (
    PrivateMessageForm,
    CommentForm,
)

from .events import (
    EventForm,
)

from .facets import (
    FacetTemplateForm,
    get_facet_form_for_template,
    FacetPreCreateForm,
)

from .notes import (
    NoteForm,
)

from .people import (
    AddUserForm,
    UserProfileForm,
    OrganizationForm,
    OrganizationSubscriptionForm,
    NetworkForm,
    AddToNetworkForm,
    InviteToNetworkForm,
)

# from .noteforms import NetworkNoteForm, OrganizationNoteForm, ProjectNoteForm, SeriesNoteForm, StoryNoteForm, UserNoteForm, TaskNoteForm, EventNoteForm

from .platforms import (
    PlatformAccountForm,
    PlatformAccountFormSet,
)

from .projects import (
    ProjectForm,
)

from .series import (
    SeriesForm,
)

from .story import (
    StoryForm,
)

from .tasks import (
    TaskForm,
)
