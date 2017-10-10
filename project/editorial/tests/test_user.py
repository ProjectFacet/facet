"""Tests for users."""

from django.test import TestCase

from .factories import UserFactory


class UserModelTestCase(TestCase):
    """Test basic features of `User` model."""

    def test_model(self):
        """Test instantiation."""

        u = UserFactory()
        u.full_clean()

    def test_str(self):
        """Test str()."""

        u = UserFactory()
        self.assertEqual(str(u), "Credit Gwen Ifill")

    def test_basic(self):
        """Basic info."""

        u = UserFactory()
        self.assertEqual(u.description, "Gwen Ifill, Baltimore Sun")
        self.assertEqual(u.search_title, "Credit Gwen Ifill")
        self.assertEqual(u.type, "User")

    def test_get_user_content(self):
        """Test for matching content."""

        # FIXME

    def test_get_user_stories(self):
        """Test for matching content."""

        # FIXME

    def test_inbox_comments(self):
        """Test for matching content."""

        # FIXME

    def test_get_recent_comments(self):
        """Test for matching content."""

        # FIXME

    def test_get_user_contact_list(self):
        """Test for matching content."""

        # FIXME

    def test_private_messages_received(self):
        """Test for matching content."""

        # FIXME

    def test_private_messages_sent(self):
        """Test for matching content."""

        # FIXME

    def test_get_user_searchable_content(self):
        """Test for matching content."""

        # FIXME

