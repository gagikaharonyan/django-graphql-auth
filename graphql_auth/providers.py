import requests

from .exceptions import WrongUsage
from .settings import graphql_auth_settings as app_settings


def validate_recaptcha(token=''):
    if app_settings.RECAPTCHA_SECRET_KET is None:
        raise WrongUsage(
            "RECAPTCHA_SECRET_KET must be provided while using LOGIN_REQUIRE_RECAPTCHA"
        )

    payload = {"secret": app_settings.RECAPTCHA_SECRET_KET, "response": token}
    url = f'https://www.google.com/recaptcha/api/siteverify'
    res = requests.post(url, data=payload)
    return res.json()
