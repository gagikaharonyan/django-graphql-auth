from unittest import mock

from pytest import mark

from graphql_auth.constants import Messages
from .testCases import RelayTestCase, DefaultTestCase


class LoginWithRecaptchaTestCaseMixin:
    VALID_RESULT = {'success': True,
                    'challenge_ts': '2022-07-06T07:37:37Z',
                    'hostname': 'localhost',
                    'score': 0.9,
                    'action': 'yourAction'}

    VALID_RESULT_LOW_SCORE = {'success': True,
                              'challenge_ts': '2022-07-06T07:37:37Z',
                              'hostname': 'localhost',
                              'score': 0.4,
                              'action': 'yourAction'}

    FAILED_RESULT = {
        'success': False,
    }

    def setUp(self):
        self.user = self.register_user(
            email="foo@email.com",
            username="foo",
            verified=True,
        )

    def test_to_pass_default_settings(self):
        self.assertTrue(True)

    @mark.settings_b
    def test_to_pass_settings_b(self):
        self.assertTrue(True)

    @mark.settings_recaptcha
    @mock.patch("graphql_auth.providers.validate_recaptcha",
                mock.Mock(return_value=VALID_RESULT))
    def test_success_login_with_recaptcha(self):
        query = self.get_query("username", self.user.username,
                               password=None, recaptcha_token='example_token')
        executed = self.make_request(query)
        self.assertTrue(executed["success"])
        self.assertFalse(executed["errors"])
        self.assertTrue(executed["token"])
        self.assertTrue(executed["refreshToken"])

    @mark.settings_recaptcha
    @mock.patch("graphql_auth.providers.validate_recaptcha",
                mock.Mock(return_value=FAILED_RESULT))
    def test_failed_login_with_recaptcha(self):
        query = self.get_query("username", self.user.username,
                               password=None, recaptcha_token='example_token')
        executed = self.make_request(query)
        self.assertFalse(executed["success"])
        self.assertEqual(executed["errors"]["nonFieldErrors"], Messages.RECAPTCHA_FAILED)
        self.assertFalse(executed["token"])
        self.assertFalse(executed["refreshToken"])

    @mark.settings_recaptcha
    @mock.patch("graphql_auth.providers.validate_recaptcha",
                mock.Mock(return_value=VALID_RESULT_LOW_SCORE))
    def test_failed_login_with_recaptcha(self):
        query = self.get_query("username", self.user.username,
                               password=None, recaptcha_token='example_token')
        executed = self.make_request(query)
        self.assertFalse(executed["success"])
        self.assertEqual(executed["errors"]["nonFieldErrors"], Messages.RECAPTCHA_FAILED)
        self.assertFalse(executed["token"])
        self.assertFalse(executed["refreshToken"])


class LoginTestCase(LoginWithRecaptchaTestCaseMixin, DefaultTestCase):
    def get_query(self, field, username, password=None, recaptcha_token=None):
        return """
            mutation {
            tokenAuth(%s: "%s", password: "%s", recaptchaToken: "%s" )
                { token, refreshToken, success, errors  }
            }
            """ % (
            field,
            username,
            password or self.default_password,
            recaptcha_token,
        )


class LoginRelayTestCase(LoginWithRecaptchaTestCaseMixin, RelayTestCase):
    def get_query(self, field, username, password=None, recaptcha_token=None):
        return """
           mutation {
           tokenAuth(input:{ %s: "%s", password: "%s", recaptchaToken: "%s"})
               { token, refreshToken, success, errors  }
           }
           """ % (
            field,
            username,
            password or self.default_password,
            recaptcha_token,
        )
