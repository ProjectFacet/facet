from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm


from models import (
    Assignment,
    AudioAsset,
    Call,
    Comment,
    ContentLicense,
    ContractorProfile,
    ContractorSubscription,
    Discussion,
    DocumentAsset,
    Event,
    Facet,
    FacetTemplate,
    ImageAsset,
    Network,
    Note,
    Organization,
    OrganizationContractorAffiliation,
    OrganizationSubscription,
    Pitch,
    Platform,
    PlatformAccount,
    PrivateMessage,
    Project,
    # Series,
    SimpleAudio,
    SimpleDocument,
    SimpleImage,
    SimpleVideo,
    Story,
    TalentEditorProfile,
    Task,
    User,
    VideoAsset,
)

from .forms import FacetTemplateForm

class FacetUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User
        fields = "__all__"

@admin.register(User)
class FacetUserAdmin(UserAdmin):
    form = FacetUserChangeForm
    fieldsets = UserAdmin.fieldsets + (("Facet", {'fields': ('organization',
      'user_type', 'credit_name', 'title', 'phone', 'bio', 'location', 'expertise',
      'notes', 'photo'
    )}), )


@admin.register(FacetTemplate)
class FacetTemplateAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'organization']
    form = FacetTemplateForm


admin.site.register(ContractorProfile)
admin.site.register(TalentEditorProfile)
admin.site.register(OrganizationContractorAffiliation)
admin.site.register(Organization)
admin.site.register(OrganizationSubscription)
admin.site.register(ContractorSubscription)
admin.site.register(Network)
admin.site.register(Platform)
admin.site.register(PlatformAccount)
admin.site.register(Project)
# admin.site.register(Series)
admin.site.register(Story)
admin.site.register(Facet)
admin.site.register(Task)
admin.site.register(Event)
admin.site.register(Pitch)
admin.site.register(Call)
admin.site.register(Assignment)
admin.site.register(ContentLicense)
admin.site.register(Note)
admin.site.register(ImageAsset)
admin.site.register(DocumentAsset)
admin.site.register(AudioAsset)
admin.site.register(VideoAsset)
admin.site.register(SimpleImage)
admin.site.register(SimpleDocument)
admin.site.register(SimpleAudio)
admin.site.register(SimpleVideo)
admin.site.register(Comment)
admin.site.register(Discussion)
admin.site.register(PrivateMessage)
