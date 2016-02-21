"""Search feature via watson."""

from watson import search as watson

class SearchAdapter(watson.SearchAdapter):

    def get_title(self, obj):
        """ Returns search_title of the search result."""

        return obj.search_title

    def get_description(self, obj):
        """ Returns description of the search result."""

        return obj.description

# class register_watson(app, model_name):
#     """Register a model with the search."""
