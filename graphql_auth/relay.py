import graphene
import graphql_jwt

from .bases import RelayMutationMixin, DynamicInputMixin
from .mixins import (
    RegisterMixin,
    VerifyAccountMixin,
    ResendActivationEmailMixin,
    SendPasswordResetEmailMixin,
    PasswordSetMixin,
    PasswordResetMixin,
    ObtainJSONWebTokenMixin,
    ArchiveAccountMixin,
    DeleteAccountMixin,
    PasswordChangeMixin,
    UpdateAccountMixin,
    RefreshTokenMixin,
    RevokeTokenMixin,
    VerifyTokenMixin,
    SendSecondaryEmailActivationMixin,
    VerifySecondaryEmailMixin,
    SwapEmailsMixin,
    RemoveSecondaryEmailMixin,
    BlockUserMixin
)
from .schema import UserNode
from .settings import graphql_auth_settings as app_settings
from .utils import normalize_fields


class Register(
    RelayMutationMixin, DynamicInputMixin, RegisterMixin, graphene.ClientIDMutation
):
    __doc__ = RegisterMixin.__doc__

    password_fields = (
        []
        if app_settings.ALLOW_PASSWORDLESS_REGISTRATION
        else ["password1", "password2"]
    )

    _required_inputs = normalize_fields(
        app_settings.REGISTER_MUTATION_FIELDS, password_fields
    )
    _inputs = app_settings.REGISTER_MUTATION_FIELDS_OPTIONAL


class VerifyAccount(
    RelayMutationMixin, DynamicInputMixin, VerifyAccountMixin, graphene.ClientIDMutation
):
    __doc__ = VerifyAccountMixin.__doc__
    _required_inputs = ["token"]


class ResendActivationEmail(
    RelayMutationMixin,
    DynamicInputMixin,
    ResendActivationEmailMixin,
    graphene.ClientIDMutation,
):
    __doc__ = ResendActivationEmailMixin.__doc__
    _required_inputs = ["email"]


class SendPasswordResetEmail(
    RelayMutationMixin,
    DynamicInputMixin,
    SendPasswordResetEmailMixin,
    graphene.ClientIDMutation,
):
    __doc__ = SendPasswordResetEmailMixin.__doc__
    _required_inputs = ["email"]


class SendSecondaryEmailActivation(
    RelayMutationMixin,
    DynamicInputMixin,
    SendSecondaryEmailActivationMixin,
    graphene.ClientIDMutation,
):
    __doc__ = SendSecondaryEmailActivationMixin.__doc__
    _required_inputs = ["email", "password"]


class VerifySecondaryEmail(
    RelayMutationMixin,
    DynamicInputMixin,
    VerifySecondaryEmailMixin,
    graphene.ClientIDMutation,
):
    __doc__ = VerifySecondaryEmailMixin.__doc__
    _required_inputs = ["token"]


class SwapEmails(
    RelayMutationMixin, DynamicInputMixin, SwapEmailsMixin, graphene.ClientIDMutation
):
    __doc__ = SwapEmailsMixin.__doc__
    _required_inputs = ["password"]


class RemoveSecondaryEmail(
    RelayMutationMixin,
    DynamicInputMixin,
    RemoveSecondaryEmailMixin,
    graphene.ClientIDMutation,
):
    __doc__ = RemoveSecondaryEmailMixin.__doc__
    _required_inputs = ["password"]


class PasswordSet(
    RelayMutationMixin, DynamicInputMixin, PasswordSetMixin, graphene.ClientIDMutation
):
    __doc__ = PasswordSetMixin.__doc__
    _required_inputs = ["token", "new_password1", "new_password2"]


class PasswordReset(
    RelayMutationMixin, DynamicInputMixin, PasswordResetMixin, graphene.ClientIDMutation
):
    __doc__ = PasswordResetMixin.__doc__
    _required_inputs = ["token", "new_password1", "new_password2"]


class ObtainJSONWebToken(
    RelayMutationMixin, ObtainJSONWebTokenMixin, graphql_jwt.relay.JSONWebTokenMutation
):
    __doc__ = ObtainJSONWebTokenMixin.__doc__
    user = graphene.Field(UserNode)
    unarchiving = graphene.Boolean(default_value=False)

    @classmethod
    def Field(cls, *args, **kwargs):
        cls._meta.arguments["input"]._meta.fields.update(
            {"password": graphene.InputField(graphene.String, required=True)}
        )

        if app_settings.LOGIN_REQUIRE_RECAPTCHA is True:
            cls._meta.arguments["input"]._meta.fields.update(
                {"recaptcha_token": graphene.InputField(graphene.String, required=True)}
            )

        for field in app_settings.LOGIN_ALLOWED_FIELDS:
            cls._meta.arguments["input"]._meta.fields.update(
                {field: graphene.InputField(graphene.String)}
            )
        return super(graphql_jwt.relay.JSONWebTokenMutation, cls).Field(*args, **kwargs)


class ArchiveAccount(
    RelayMutationMixin,
    ArchiveAccountMixin,
    DynamicInputMixin,
    graphene.ClientIDMutation,
):
    __doc__ = ArchiveAccountMixin.__doc__
    _required_inputs = ["password"]


class DeleteAccount(
    RelayMutationMixin, DeleteAccountMixin, DynamicInputMixin, graphene.ClientIDMutation
):
    __doc__ = DeleteAccountMixin.__doc__
    _required_inputs = ["password"]


class PasswordChange(
    RelayMutationMixin,
    PasswordChangeMixin,
    DynamicInputMixin,
    graphene.ClientIDMutation,
):
    __doc__ = PasswordChangeMixin.__doc__
    _required_inputs = ["old_password", "new_password1", "new_password2"]


class UpdateAccount(
    RelayMutationMixin, DynamicInputMixin, UpdateAccountMixin, graphene.ClientIDMutation
):
    __doc__ = UpdateAccountMixin.__doc__
    _inputs = app_settings.UPDATE_MUTATION_FIELDS


class VerifyToken(
    RelayMutationMixin, VerifyTokenMixin, graphql_jwt.relay.Verify
):
    __doc__ = VerifyTokenMixin.__doc__

    class Input:
        token = graphene.String(required=True)


class RefreshToken(
    RelayMutationMixin, RefreshTokenMixin, graphql_jwt.relay.Refresh
):
    __doc__ = RefreshTokenMixin.__doc__

    class Input(graphql_jwt.mixins.RefreshMixin.Fields):
        """Refresh Input"""


class RevokeToken(
    RelayMutationMixin, RevokeTokenMixin, graphql_jwt.relay.Revoke
):
    __doc__ = RevokeTokenMixin.__doc__

    class Input:
        refresh_token = graphene.String(required=True)


class BlockUser(
    RelayMutationMixin, BlockUserMixin, graphene.ClientIDMutation
):
    __doc__ = BlockUserMixin.__doc__

    class Input:
        user_id = graphene.Int(required=True)
        unblocking = graphene.Boolean()
