"""Search feature via watson."""

from watson import search as watson

class SearchAdapter(watson.SearchAdapter):

    def get_title(self, obj):
        """ Returns search_title of the search result."""

        return obj.search_title

    def get_description(self, obj):
        """ Returns description of the search result."""

        return obj.description

    def get_absolute_url(self, obj):
        """ Returns url of instance or instance container."""

        return obj.get_absolute_url

    def get_type(self, obj):
        """ Returns type of object."""

        return obj.type


def register_watson(app, model_name):
    """Register a model with the search."""

    watson.register(app.get_model(model_name),
        SearchAdapter,
        store=['get_type'])
