from django.contrib import admin

# Register your models here.
from models import (
    User,
    ContractorProfile,
    TalentEditorProfile,
    OrganizationContractorAffiliation,
    OrganizationSubscription,
    ContractorSubscription,
    Organization,
    Network,
    Platform,
    PlatformAccount,
    Pitch,
    Call,
    Assignment,
    Project,
    Series,
    Story,
    Facet,
    Task,
    Event,
    ContentLicense,
    Note,
    ImageAsset,
    DocumentAsset,
    AudioAsset,
    VideoAsset,
    SimpleImage,
    SimpleDocument,
    SimpleAudio,
    SimpleVideo,
    Comment,
    Discussion,
    PrivateMessage,
    FacetTemplate,
)

from .forms import FacetTemplateForm


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email']


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
admin.site.register(Series)
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
