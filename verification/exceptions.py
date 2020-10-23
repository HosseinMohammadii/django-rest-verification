from django.utils.translation import ugettext_lazy as _
from rest_framework import status
from rest_framework.exceptions import APIException, ValidationError, PermissionDenied


# class UserIsVerified(Exception):
#     """The user already has been verified"""
#     pass


class UserIsVerified(PermissionDenied):
    # status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _('The user has been already verified')
    # default_code = 'invalid'


class VerificationTypeNotValid(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _('Verification_field is not valid')
    default_code = 'invalid'


class UserHasActiveVerification(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = _('User has unexpired verification code')
    default_code = 'permission_denied'


class VerificationFailed(ValidationError):
    default_detail = _('Verification failed.')
