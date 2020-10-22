from . import conf
from .exceptions import VerificationTypeNotValid


def validate_verification_type(value):
    if value not in conf.VERIFICATIONS_TYPES:
        raise VerificationTypeNotValid
    return value

