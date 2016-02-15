from django.contrib import admin

# Register your models here.
from models import (
    User,
    Organization,
    OrganizationNote,
    Network,
    Series,
    Story,
    WebFacet,
    PrintFacet,
    AudioFacet,
    VideoFacet,
    SeriesNote,
    StoryNote,
    ImageAsset,
    Comment,
    Discussion)



class UserAdmin(admin.ModelAdmin):
    model = User,
    list_display = ('name', 'email')


admin.site.register(User)
admin.site.register(Organization)
admin.site.register(OrganizationNote)
admin.site.register(Network)
admin.site.register(Series)
admin.site.register(Story)
admin.site.register(WebFacet)
admin.site.register(PrintFacet)
admin.site.register(AudioFacet)
admin.site.register(VideoFacet)
admin.site.register(SeriesNote)
admin.site.register(StoryNote)
admin.site.register(ImageAsset)
admin.site.register(Comment)
admin.site.register(Discussion)
