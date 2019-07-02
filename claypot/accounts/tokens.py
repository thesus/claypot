from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import base36_to_int
from django.utils.crypto import constant_time_compare

from django.conf import settings


class TimeoutError(Exception):
    """Should be raised if a signup token is invalid due to it's age."""

    pass


class SignupTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        # Propably not a good idea. user.is_active could be altered to "block" a user.
        # If he tries to use the signup link again, reactivation could be successfull.
        return super()._make_hash_value(user, timestamp) + str(user.is_active)

    def check_token(self, user, token):
        """
        Check that a password reset token is correct for a given use.
        Derived from django.contrib.auth.tokens
        """

        # Parse token
        try:
            ts_b36, _ = token.split("-")
            ts = base36_to_int(ts_b36)
        except ValueError:
            return False

        # Check that the timestamp/uid has not been tampered with
        if not constant_time_compare(self._make_token_with_timestamp(user, ts), token):
            return False

        # Check the timestamp is within limit. Timestamps are rounded to
        # midnight (server time) providing a resolution of only 1 day. If a
        # link is generated 5 minutes before midnight and used 6 minutes later,
        # that counts as 1 day. Therefore, SIGNUP_TIMEOUT_DAYS = 1 means
        # "at least 1 day, could be up to 2."
        if (self._num_days(self._today()) - ts) > settings.SIGNUP_TIMEOUT_DAYS:
            raise TimeoutError()

        return True


signup_token_generator = SignupTokenGenerator()
