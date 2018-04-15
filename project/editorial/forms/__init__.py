"""Forms for editorial application.

Because of the number of forms in this app, this is divided into submodules.
Please import forms from this file, rather than depending on the individual
module it appears in, as those may change as the codebase is refactored.
"""

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
    SimpleImageLibraryAssociateForm,
    SimpleDocumentLibraryAssociateForm,
    SimpleAudioLibraryAssociateForm,
    SimpleVideoLibraryAssociateForm,
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

from .user import (
    AddUserForm,
    UserProfileForm,
)

from .organization import (
    OrganizationForm,
    OrganizationSubscriptionForm,
)

from .network import (
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
    ProjectTeamForm,
)

from .series import (
    SeriesForm,
    SeriesTeamForm,
)

from .story import (
    StoryForm,
    StoryTeamForm,
)

from .tasks import (
    TaskForm,
)
