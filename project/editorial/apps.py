"""Configuration for editorial application."""

from django.apps import AppConfig
from watson import search as watson

class EditorialAppConfig(AppConfig):
    """Configure editorial app."""

    name = "editorial"

    def ready(self):
        """Add models to search."""

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
