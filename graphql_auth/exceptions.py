from django.utils.translation import gettext as _


class GraphQLAuthError(Exception):
    default_message = None

    def __init__(self, message=None):
        if message is None:
            message = self.default_message

        super().__init__(message)


class UserAlreadyVerified(GraphQLAuthError):
    default_message = _("User already verified.")


class InvalidCredentials(GraphQLAuthError):
    default_message = _("Invalid credentials.")


class UserNotVerified(GraphQLAuthError):
    default_message = _("User is not verified.")


class UserBlocked(GraphQLAuthError):
    default_message = _("User is blocked.")


class EmailAlreadyInUse(GraphQLAuthError):
    default_message = _("This email is already in use.")


class TokenScopeError(GraphQLAuthError):
    default_message = _("This token if for something else.")


class PasswordAlreadySetError(GraphQLAuthError):
    default_message = _("Password already set for account.")


class RecaptchaFailedError(GraphQLAuthError):
    default_message = _("Failed validation of recaptcha token")


class WrongUsage(GraphQLAuthError):
    """
    internal exception
    """

    default_message = _("Wrong usage, check your code!.")
