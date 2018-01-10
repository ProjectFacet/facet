"""Custom search view for editorial app.

Subclasses watson's get_queryset to filter for only results
from a user's own organization.
"""

# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from watson import search as watson
from watson.views import SearchView as BaseWatsonSearchView


#----------------------------------------------------------------------#
#   Custom Search View
#----------------------------------------------------------------------#

# ACCESS: An org user should be able to search everything associated with an org
# except other users notes
# Contractors should only be able to search their own pitches, assignments.
class EditorialSearchView(BaseWatsonSearchView):
    """Search view that filters to only show results from user's org."""

    def get_queryset(self):
        """Returns list of querysets containing content a user is allowed to search.

        This is determined by a user's organization.
        """

        # FIXME Future Revise for both org users and contractors

        user_org = self.request.org
        user = self.request.user

        # retrieve all content a user is allowed to search
        searchable_org_objects = user_org.get_org_searchable_content()
        # FIXME searchable_user_objects = user.get_user_searchable_content()

        # unpack the querysets from the list of querysets returned
        projects, series, stories, facets, imageassets = searchable_org_objects
        # FIXME usernotes = searchable_user_objects

        # FIXME from joel: should usernotes be in the list below? it's not used anywhere

        # pass all querysets to search method
        return watson.search(
            self.query,
            models=[projects, series, stories, facets, imageassets]
        )
