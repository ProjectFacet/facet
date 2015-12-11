from django.contrib import admin

# Register your models here.
from models import (
    User,
    Organization,
    Network,
    Series,
    Story,
    WebFacet,
    PrintFacet,
    AudioFacet,
    VideoFacet,
    SeriesPlan,
    StoryPlan,
    Asset,
    Comment,
    Discussion)



class UserAdmin(admin.ModelAdmin):
    model = User,
    list_display = ('name', 'email')


admin.site.register(User)
admin.site.register(Organization)
admin.site.register(Network)
admin.site.register(Series)
admin.site.register(Story)
admin.site.register(WebFacet)
admin.site.register(PrintFacet)
admin.site.register(AudioFacet)
admin.site.register(VideoFacet)
admin.site.register(SeriesPlan)
admin.site.register(StoryPlan)
admin.site.register(Asset)
admin.site.register(Comment)
admin.site.register(Discussion)
