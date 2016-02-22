"""Configuration for editorial application."""

from django.apps import AppConfig

class EditorialAppConfig(AppConfig):
    """Configure editorial app."""

    name = 'editorial'

    def ready(self):
        """Add models to search."""

        from facet.search import register_watson

        for model_name in [
            "Series",
            "Story",
            "WebFacet",
            "PrintFacet",
            "AudioFacet",
            "VideoFacet",
            "ImageAsset",
            "NetworkNote",
            "OrgNote",
            "UserNote",
            "SeriesNote",
            "StoryNote",
        ]:
            register_watson(self, model_name)
