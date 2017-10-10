"""Tests for users."""

from django.test import TestCase

from .factories import UserFactory, OrganizationFactory, NetworkFactory


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
        self.assertEqual(u.description, "Credit Gwen Ifill, Managing Editor, (No org)")
        self.assertEqual(u.search_title, "Credit Gwen Ifill")
        self.assertEqual(u.type, "User")

    def test_with_org(self):
        """Test with an organization."""

        u = UserFactory()
        o = OrganizationFactory()
        u.organization = o

        self.assertEqual(u.description, "Credit Gwen Ifill, Managing Editor, Baltimore Sun")

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


class OrganizationModelTestCase(TestCase):
    """Test basic features of `Organization` model."""

    def setUp(self):
        """Make a owner for the org."""

        self.u = UserFactory()

    def test_model(self):
        """Test instantiation."""

        o = OrganizationFactory()
        o.full_clean()

    def test_str(self):
        """Test str()."""

        o = OrganizationFactory()
        self.assertEqual(str(o), "Baltimore Sun")

    def test_basic(self):
        """Basic info."""

        o = OrganizationFactory()
        self.assertEqual(o.description, "Description for Baltimore Sun")
        self.assertEqual(o.search_title, "Baltimore Sun")
        self.assertEqual(o.type, "Organization")

    def test_get_org_users(self):
        """Test org users."""

        u2 = UserFactory(first_name="Bob", last_name="Woodward")
        o = OrganizationFactory()
        u2.organization = o
        u2.save()

        # User not in org
        u3 = UserFactory(first_name="Nope", last_name="Nope")

        orgs = o.get_org_users()
        self.assertIn(self.u, orgs)
        self.assertIn(u2, orgs)
        self.assertEqual(len(orgs), 2)

    def test_get_org_networks(self):
        """Test network memberships."""

        o = OrganizationFactory()

        # Network we own
        n1 = NetworkFactory()

        # Network we're in, but owned by someone else
        o2 = OrganizationFactory(name="New Zork Times")
        n2 = NetworkFactory(name="Chicago Co-Op", owner_organization=o2, organizations=[o])

        # Network we're in *and* own (catch case where we're in both)
        n3 = NetworkFactory(name="LA Co-Op", organizations=[o])

        # Network we're not in & don't own
        n4 = NetworkFactory(name="LA Co-Op", owner_organization=o2, organizations=[])

        nets = o.get_org_networks()

        self.assertIn(n1, nets)
        self.assertIn(n2, nets)
        self.assertIn(n3, nets)
        self.assertEqual(len(nets), 3)

    def test_get_org_collaborators(self):
        """Test collaborators."""

        o = OrganizationFactory()
        o2 = OrganizationFactory(name="New Zork Times")

        # should not be a collaborator for us
        o3 = OrganizationFactory(name="Trump Media")

        n1 = NetworkFactory(organizations=[o2])

        collabs = o.get_org_collaborators()
        self.assertSequenceEqual(collabs, [o2])

    def test_libraries(self):
        """Test libraries."""

        # FIXME

    def test_comments(self):
        """Test comments."""

        # FIXME

    def test_collaborative_content(self):
        """ Return list of all content that an org is a collaborator on."""

        # FIXME

    def test_stories_running_today(self):
        """Return list of content scheduled to run today."""

        # FIXME

    def test_stories_due_for_edit_today(self):
        """Return list of content scheduled for edit today."""

        # FIXME

    def test_org_searchable_content(self):
        """ Return queryset of all objects that can be searched by a user."""

        # FIXME


class NetworkModelTestCase(TestCase):
    """Test basic features of `Network` model."""

    def setUp(self):
        """Make an owner org for the network."""

        self.u = UserFactory()
        self.o = OrganizationFactory()
        self.u.organization = self.o
        self.u.save()

    def test_model(self):
        """Test instantiation."""

        n = NetworkFactory()
        n.full_clean()

    def test_str(self):
        """Test str()."""

        n = NetworkFactory()
        self.assertEqual(str(n), "Baltimore Co-Op")

    def test_basic(self):
        """Basic info."""

        n = NetworkFactory()
        self.assertEqual(n.description, "Description of network.")
        self.assertEqual(n.search_title, "Baltimore Co-Op")
        self.assertEqual(n.type, "Network")

    def test_network_shared_stories(self):
        """Test shared stories."""

        # FIXME