from django.contrib import admin

# Register your models here.
from models import (
    User,
    ContractorInfo,
    OrganizationContractorInfo,
    Organization,
    OrganizationNote,
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
    ProjectNote,
    SeriesNote,
    StoryNote,
    TaskNote,
    EventNote,
    ImageAsset,
    DocumentAsset,
    AudioAsset,
    VideoAsset,
    Comment,
    Discussion,
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


admin.site.register(ContractorInfo)
admin.site.register(OrganizationContractorInfo)
admin.site.register(Organization)
admin.site.register(OrganizationNote)
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
admin.site.register(ProjectNote)
admin.site.register(SeriesNote)
admin.site.register(StoryNote)
admin.site.register(TaskNote)
admin.site.register(EventNote)
admin.site.register(ImageAsset)
admin.site.register(DocumentAsset)
admin.site.register(AudioAsset)
admin.site.register(VideoAsset)
admin.site.register(Comment)
admin.site.register(Discussion)
