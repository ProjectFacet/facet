"""Configuration for editorial application."""

from django.apps import AppConfig
from search import register_watson


class EditorialAppConfig(AppConfig):
    """Configure editorial app."""

    name = "editorial"

    def ready(self):
        """Add models to search. Add models to Activity Stream."""

        for model_name in [
            "Project",
            # "Series",
            "Story",
            "Facet",
            "Task",
            "Event",
            "Call",
            "Pitch",
            "Assignment",
            "ContractorProfile",
            "OrganizationContractorAffiliation",
            "FacetTemplate",
            "ImageAsset",
            "DocumentAsset",
            "AudioAsset",
            "VideoAsset",
            "SimpleImage",
            "SimpleDocument",
            "SimpleAudio",
            "SimpleVideo",
            "Note",
        ]:
            register_watson(self, model_name)

            # TODO register keywords fields for facet and all kinds of assets
            # image_asset = self.get_model("ImageAsset")
            # register_watson(image_asset, "keywords")


        # register models for activity
        from actstream import registry

        registry.register(self.get_model('User'))
        registry.register(self.get_model('ContractorProfile'))
        registry.register(self.get_model('OrganizationContractorAffiliation'))
        registry.register(self.get_model('Call'))
        registry.register(self.get_model('Pitch'))
        registry.register(self.get_model('Assignment'))
        registry.register(self.get_model('Organization'))
        registry.register(self.get_model('Network'))
        registry.register(self.get_model('Project'))
        # registry.register(self.get_model('Series'))
        registry.register(self.get_model('Story'))
        registry.register(self.get_model('Facet'))
        registry.register(self.get_model('FacetTemplate'))
        registry.register(self.get_model('Task'))
        registry.register(self.get_model('Event'))
        registry.register(self.get_model('ImageAsset'))
        registry.register(self.get_model('DocumentAsset'))
        registry.register(self.get_model('AudioAsset'))
        registry.register(self.get_model('VideoAsset'))
        registry.register(self.get_model('SimpleImage'))
        registry.register(self.get_model('SimpleDocument'))
        registry.register(self.get_model('SimpleAudio'))
        registry.register(self.get_model('SimpleVideo'))
        registry.register(self.get_model('Note'))
        registry.register(self.get_model('Comment'))
