"""Configuration for editorial application."""

from django.apps import AppConfig
from watson import search as watson

from django.apps import AppConfig


class EditorialAppConfig(AppConfig):
    """Configure editorial app."""

    name = "editorial"

    def ready(self):
        """Add models to search."""

        # Set up Watson Search
        from search import register_watson

        for model_name in [
            "Series",
            "Story",
            "WebFacet",
            "PrintFacet",
            "AudioFacet",
            "VideoFacet",
            "ImageAsset",
            "NetworkNote",
            "OrganizationNote",
            "UserNote",
            "SeriesNote",
            "StoryNote",
        ]:
            register_watson(self, model_name)


class MyAppConfig(AppConfig):
    name = 'myapp'

    def ready(self):

        # Set up Django Activity Strem
        from actstream import registry

        for model_name in [
            "User",
            "Organization",
            "Network",
            "Series",
            "Story",
            "WebFacet",
            "PrintFacet",
            "AudioFacet",
            "VideoFacet",
            "ImageAsset",
            "DocumentAsset",
            "AudioAsset",
            "OrganizationNote"
            "NetworkNote",
            "SeriesNote",
            "StoryNote",
            "Comment"
        ]:
            registry.register(self, model_name)

# myapp/__init__.py
default_app_config = 'editorial.apps.MyAppConfig'


        # registry.register(self.get_model('User'))
        # registry.register(self.get_model('Organization'))
        # registry.register(self.get_model('Network'))
        # registry.register(self.get_model('Series'))
        # registry.register(self.get_model('Story'))
        # registry.register(self.get_model('WebFacet'))
        # registry.register(self.get_model('PrintFacet'))
        # registry.register(self.get_model('AudioFacet'))
        # registry.register(self.get_model('VideoFacet'))
        # registry.register(self.get_model('ImageAsset'))
        # registry.register(self.get_model('DocumentAsset'))
        # registry.register(self.get_model('AudioAsset'))
        # registry.register(self.get_model('OrganizationNote'))
        # registry.register(self.get_model('NetworkNote'))
        # registry.register(self.get_model('SeriesNote'))
        # registry.register(self.get_model('StoryNote'))
        # registry.register(self.get_model('Comment'))
