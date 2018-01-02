from braces.views import UserPassesTestMixin


class CustomUserTest(UserPassesTestMixin):
    """User must be a member of this organization to view this content.

    This also requires that a user be logged in, so it's not needed to use this
    with LoginRequiredMixin.
    """

    def test_func(self, user):
        """"User must be a super"""

        if user.is_superuser:
            # Superuser can use all views
            return True

        if not user.is_authenticated():
            # No logged in user; this will redirect to login page
            return False

        return self.test_user(user)