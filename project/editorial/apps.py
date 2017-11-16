"""Configuration for editorial application."""

from django.apps import AppConfig
from watson import search as watson
from search import register_watson
from actstream import registry


class EditorialAppConfig(AppConfig):
    """Configure editorial app."""

    name = "editorial"

    def ready(self):
        """Add models to search. Add models to Activity Stream."""

        for model_name in [
            "Project",
            "Series",
            "Story",
            "Facet",
            "Task",
            "Event",
            "WebFacet",
            "PrintFacet",
            "AudioFacet",
            "VideoFacet",
            "ImageAsset",
            "DocumentAsset",
            "AudioAsset",
            "VideoAsset",
            "NetworkNote",
            "OrganizationNote",
            "UserNote",
            "ProjectNote",
            "SeriesNote",
            "StoryNote",
        ]:
            register_watson(self, model_name)

        registry.register(self.get_model('User'))
        registry.register(self.get_model('Organization'))
        registry.register(self.get_model('Network'))
        registry.register(self.get_model('Project'))
        registry.register(self.get_model('Series'))
        registry.register(self.get_model('Story'))
        registry.register(self.get_model('Facet'))
        registry.register(self.get_model('Task'))
        registry.register(self.get_model('Event'))
        registry.register(self.get_model('WebFacet'))
        registry.register(self.get_model('PrintFacet'))
        registry.register(self.get_model('AudioFacet'))
        registry.register(self.get_model('VideoFacet'))
        registry.register(self.get_model('ImageAsset'))
        registry.register(self.get_model('DocumentAsset'))
        registry.register(self.get_model('AudioAsset'))
        registry.register(self.get_model('VideoAsset'))
        registry.register(self.get_model('OrganizationNote'))
        registry.register(self.get_model('NetworkNote'))
        registry.register(self.get_model('ProjectNote'))
        registry.register(self.get_model('SeriesNote'))
        registry.register(self.get_model('StoryNote'))
        registry.register(self.get_model('Comment'))


# class MyAppConfig(AppConfig):
#     """configure editorial app for Django Activity Stream."""
#
#     name = "editorial"
#
#     def ready(self):
#         """Add models to Django Activity Stream."""
#
#         registry.register(self.get_model('User'))
#         registry.register(self.get_model('Organization'))
#         registry.register(self.get_model('Network'))
#         registry.register(self.get_model('Series'))
#         registry.register(self.get_model('Story'))
#         registry.register(self.get_model('WebFacet'))
#         registry.register(self.get_model('PrintFacet'))
#         registry.register(self.get_model('AudioFacet'))
#         registry.register(self.get_model('VideoFacet'))
#         registry.register(self.get_model('ImageAsset'))
#         registry.register(self.get_model('DocumentAsset'))
#         registry.register(self.get_model('AudioAsset'))
#         registry.register(self.get_model('OrganizationNote'))
#         registry.register(self.get_model('NetworkNote'))
#         registry.register(self.get_model('SeriesNote'))
#         registry.register(self.get_model('StoryNote'))
#         registry.register(self.get_model('Comment'))

        # for model_name in [
        #     "User",
        #     "Organization",
        #     "Network",
        #     "Series",
        #     "Story",
        #     "WebFacet",
        #     "PrintFacet",
        #     "AudioFacet",
        #     "VideoFacet",
        #     "ImageAsset",
        #     "DocumentAsset",
        #     "AudioAsset",
        #     "OrganizationNote"
        #     "NetworkNote",
        #     "SeriesNote",
        #     "StoryNote",
        #     "Comment"
        # ]:
        #     registry.register(self, model_name)
