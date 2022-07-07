from .settings import *

GRAPHQL_AUTH = {
    "LOGIN_REQUIRE_RECAPTCHA": True,
    "RECAPTCHA_MIN_SCORE": 0.7
}

INSTALLED_APPS += ["tests"]

AUTH_USER_MODEL = "tests.CustomUser"
