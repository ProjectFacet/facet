import factory
from datetime import datetime
from django.utils.text import slugify
from django.utils.timezone import make_aware

from .. import models


class UserFactory(factory.DjangoModelFactory):
    """Factory for making demo users."""

    class Meta:
        model = models.User
        # This next line is actually performed in _create, below, but it shown here for
        # declarative documentation.
        django_get_or_create = ['username']

    first_name = "Gwen"
    last_name = "Ifill"
    username = factory.LazyAttribute(lambda u: slugify(u.first_name))
    email = factory.LazyAttribute(
        lambda u: "%s@%s.om" % (slugify(u.first_name), slugify(u.first_name)))
    password = "secret"

    # There's is a circular dependency on users/organizations, so we can't create an
    # org when we create the first user for the org. To create a user with an organization,
    # do this:
    #   u = UserFactory()
    #   o = OrganizationFactory()
    #   u.organization = o
    #
    # organization = factory.SubFactory('editorial.tests.factories.OrganizationFactory')

    user_type = "Editor"
    credit_name = factory.LazyAttribute(lambda c: "Credit %s %s" % (c.first_name, c.last_name))
    title = "Managing Editor"
    phone = "415-555-1212"
    bio = factory.LazyAttribute(lambda c: "Bio for %s." % c.first_name)
    location = "Baltimore, Maryland"
    expertise = ["Writing", "Editing"]
    # notes = []   # FIXME
    photo = factory.django.ImageField()
    facebook = factory.LazyAttribute(
        lambda c: "http://facebook.com/%s" % slugify(c.first_name))
    twitter = factory.LazyAttribute(lambda c: "http://twitter.com/%s" % slugify(c.first_name))
    github = factory.LazyAttribute(lambda c: "http://github.com/%s" % slugify(c.first_name))
    linkedin = factory.LazyAttribute(
        lambda c: "http://linkedin.com/%s" % slugify(c.first_name))
    instagram = factory.LazyAttribute(
        lambda c: "http://instagram.com/%s" % slugify(c.first_name))
    snapchat = factory.LazyAttribute(
        lambda c: "http://snapchat.com/%s" % slugify(c.first_name))
    vine = factory.LazyAttribute(lambda c: "http://vine.com/%s" % slugify(c.first_name))
    website = factory.LazyAttribute(lambda c: "http://www.%s.com/" % slugify(c.first_name))

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """Override the default ``_create`` with our custom call."""

        try:
            return models.User.objects.get(username=kwargs['username'])
        except models.User.DoesNotExist:
            manager = cls._get_manager(model_class)
            return manager.create_user(*args, **kwargs)


class DiscussionFactory(factory.DjangoModelFactory):
    """Factory for making demo discussions."""

    class Meta:
        model = models.Discussion

    discussion_type = "???"


class OrganizationFactory(factory.DjangoModelFactory):
    """Factory for making demo organizations."""

    class Meta:
        model = models.Organization
        django_get_or_create = ['name']

    name = "Baltimore Sun"
    owner = factory.SubFactory(UserFactory)
    org_description = factory.LazyAttribute(lambda c: "Description for " + c.name)
    logo = factory.django.ImageField()
    location = "Baltimore, Maryland"
    creation_date = make_aware(datetime(2017, 1, 1))
    facebook = factory.LazyAttribute(lambda c: "http://facebook.com/%s" % slugify(c.name))
    twitter = factory.LazyAttribute(lambda c: "http://twitter.com/%s" % slugify(c.name))
    website = factory.LazyAttribute(lambda c: "http://www.%s.com/" % slugify(c.name))
    discussion = factory.SubFactory(DiscussionFactory, discussion_type="ORG")

    @factory.post_generation
    def add_owner_to_org(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return
        self.owner.organization = self
        self.owner.save()


class NetworkFactory(factory.DjangoModelFactory):
    """Factory for making network."""

    class Meta:
        model = models.Network
        django_get_or_create = ['name']

    name = "Baltimore Co-Op"
    owner_organization = factory.SubFactory(OrganizationFactory)
    creation_date = make_aware(datetime(2017, 1, 1))
    network_description = "Description of network."
    logo = factory.django.ImageField()
    # organizations = [] ...
    discussion = factory.SubFactory(DiscussionFactory, discussion_type='NET')

    @factory.post_generation
    def organizations(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for org in extracted:
                self.organizations.add(org)


class SeriesFactory(factory.DjangoModelFactory):
    """Factory for making series."""

    class Meta:
        model = models.Series
        django_get_or_create = ['name']

    name = "American Pets"
    series_description = "Description of series."
    owner = factory.SubFactory(UserFactory)
    organization = factory.SubFactory(OrganizationFactory)
    # team ...
    creation_date = make_aware(datetime(2017, 1, 1))
    sensitivity = False
    share = False
    # share_with = ...
    share_with_date = None
    collaborate = False
    # collaborate_with = ...
    archived = False
    discussion = factory.SubFactory(DiscussionFactory, discussion_type='SER')

    @factory.post_generation
    def team(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for user in extracted:
                self.team.add(user)

    @factory.post_generation
    def share_with(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for network in extracted:
                self.share_with.add(network)

    @factory.post_generation
    def collaborate_with(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for org in extracted:
                self.collaborate_with.add(org)


class StoryFactory(factory.DjangoModelFactory):
    """Factory for making stories."""

    class Meta:
        model = models.Story
        django_get_or_create = ['name']

    series = factory.SubFactory(SeriesFactory)
    owner = factory.SubFactory(UserFactory)
    organization = factory.SubFactory(OrganizationFactory)
    original_story = True
    name = "Cute Kitten Rescued"
    story_description = "Description of story."
    embargo = False
    embargo_datetime = None
    creation_date = make_aware(datetime(2017, 1, 1))
    # team = ...
    sensitive = False
    share = False
    share_with_date = None
    ready_to_share = False
    # share_with = ...
    collaborate = False
    # collaborate_with = ...
    archived = False
    discussion = factory.SubFactory(DiscussionFactory, discussion_type='STO')
