from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.exceptions import NotAuthenticated

from .verification import is_verified, not_have_active_verification
from .validators import validate_verification_type


class IsAuthenticatedOrOptions(IsAuthenticated):
    message = 'User Should be Authenticated'

    def has_permission(self, request, view):
        if request.method == 'OPTIONS':
            return True
        return super(IsAuthenticatedOrOptions, self).has_permission(request, view)


class IsNotVerified(BasePermission):
    message = 'The user is already verified'

    def has_permission(self, request, view):
        if request.method != 'POST':
            return True
        user = request.user
        verification_type = validate_verification_type(request.data.get('verification_type', None))
        if user and user.is_authenticated:
            return not is_verified(user, verification_type=verification_type)
        return False

    def has_object_permission(self, request, view, obj):
        if request.method != 'POST':
            return True
        user = request.user
        verification_type = validate_verification_type(request.data.get('verification_type', None))
        if user and user.is_authenticated:
            return not is_verified(user, verification_type=verification_type)
        return False


class HasNotActiveVerification(BasePermission):
    message = 'The user has active verification.'

    def has_permission(self, request, view):
        if request.method != 'POST':
            return True
        user = request.user
        verification_type = validate_verification_type(request.data.get('verification_type', None))
        if user and user.is_authenticated:
            # This line may raise exception if user has active verification
            not_have_active_verification(user, verification_type=verification_type)
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.method != 'POST':
            return True
        user = request.user
        verification_type = validate_verification_type(request.data.get('verification_type', None))
        if user and user.is_authenticated:
            # This line may raise exception if user has active verification
            not_have_active_verification(user, verification_type=verification_type)
            return True
        return False
