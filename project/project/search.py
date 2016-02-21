"""Search feature via watson."""

from watson import search as watson

class SearchAdapter(watson.SearchAdapter):
    """Watson search adapter."""

    def get_title(self, obj):
        """ Returns search_title of the search result."""

        return obj.search_title

    def get_description(self, obj):
        """ Returns description of the search result."""

        return obj.description

    def get_absolute_url(self, obj):
        """ Detail url for object or normal display location."""


class register_watson(app, model_name):
    """Register a model with the search."""
