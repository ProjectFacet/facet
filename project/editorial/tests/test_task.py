"""Tests for tasks."""
from datetime import datetime
from django.test import TestCase
from django.utils.timezone import make_aware
from django.core.exceptions import ValidationError

from .factories import UserFactory, OrganizationFactory, NetworkFactory, StoryFactory, \
    SeriesFactory, ProjectFactory, TaskFactory


class TaskModelTestCase(TestCase):
    """Test basic features of `Task` model."""

    def test_model(self):
        """Test instantiation."""

        p = ProjectFactory()
        tk = TaskFactory(project=p)
        tk.full_clean()

    def test_str(self):
        """Test str()."""

        tk = TaskFactory()
        self.assertEqual(str(tk), "Get photos")

    def test_relationship(self):
        """Test that a task is assigned to only 1 thing."""

        tk = TaskFactory()
        with self.assertRaises(ValidationError):
            tk.full_clean()

        p = ProjectFactory()
        sr = SeriesFactory()
        tk = TaskFactory(project=p, series=sr)
        with self.assertRaises(ValidationError):
            tk.full_clean()
