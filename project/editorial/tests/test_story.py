"""Tests for stories."""
from datetime import datetime
from django.test import TestCase
from django.utils.timezone import make_aware

from .factories import UserFactory, OrganizationFactory, NetworkFactory, StoryFactory, \
    SeriesFactory


class SeriesModelTestCase(TestCase):
    """Test basic features of `Series` model."""

    def test_model(self):
        """Test instantiation."""

        sr = SeriesFactory()
        sr.full_clean()

    def test_str(self):
        """Test str()."""

        sr = SeriesFactory()
        self.assertEqual(str(sr), "American Pets")

    def test_basic(self):
        """Basic info."""

        sr = SeriesFactory()
        self.assertEqual(sr.description, "Description of series.")
        self.assertEqual(sr.search_title, "American Pets")
        self.assertEqual(sr.type, "Series")

    def test_team(self):
        """Test team."""

        sr = SeriesFactory()
        team = sr.get_series_team()

        # FIXME

        # self.assertEqual(sr.organization, "")


class StoryModelTestCase(TestCase):
    """Test basic features of `Story` model."""

    def test_model(self):
        """Test instantiation."""

        s = StoryFactory()
        s.full_clean()

    def test_str(self):
        """Test str()."""

        s = StoryFactory()
        self.assertEqual(str(s), "Cute Kitten Rescued")

    def test_basic(self):
        """Basic info."""

        s = StoryFactory()
        self.assertEqual(s.description, "Description of story.")
        self.assertEqual(s.search_title, "Cute Kitten Rescued")
        self.assertEqual(s.type, "Story")

    def test_copy_story(self):
        """Test cloning of stories."""

        # FIXME

    def test_story_download(self):
        """Test story download."""

        s = StoryFactory()
        s.creation_date = make_aware(datetime(2017, 1, 1))

        self.assertEqual(s.get_story_download(),
                         """
        Story
        ========
        Cute Kitten Rescued
        --------------
        Description: Description of story.
        Series: American Pets
        Owner: Credit Gwen Ifill
        Organization: Baltimore Sun
        Original: True
        Team: 
        Created: 2017-01-01 00:00:00-08:00
        Sensitive: False
        Embargo Status: False
        Embargo Date/Time: None
        Share: False
        Share Date: None
        Shared With: 
        Ready for Sharing: False
        Collaborate: False
        Collaborate With: 
        Archived: False
        """)

        # FIXME should add sharing/collaboring and test for these, too

    def test_story_team(self):
        """Test story team."""

        # FIXME

    def test_story_assets(self):
        """Test images, documents, audio for story."""

        # FIXME

    def test_facets(self):
        """Return all existing facets associated with a story."""

        # FIXME
