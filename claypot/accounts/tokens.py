from django.contrib.auth.tokens import PasswordResetTokenGenerator


class SignupTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        # Propably not a good idea. user.is_active could be altered to "block" a user.
        # If he tries to use the signup link again, reactivation could be successfull.
        return super()._make_hash_value(user, timestamp) + str(user.is_active)


signup_token_generator = SignupTokenGenerator()
