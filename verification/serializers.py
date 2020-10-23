from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers
from rest_framework.exceptions import ValidationError, NotAuthenticated

from .models import (BaseVerification,
                     Verification, VerificationRecord)
from .validators import validate_verification_type

from .verification import generate_verification
from .conf import VERIFICATION_CODE_FIELD, VERIFICATIONS_TYPES


class BaseVerificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = BaseVerification
        fields = [
            'id', 'user', 'verification_type', 'verification_code', 'created', 'updated', VERIFICATION_CODE_FIELD
        ]

    def validate_verification_type(self, value):
        return validate_verification_type(value)

    def validate_user(self, value):
        request = self.context.get('request')
        user = request.user
        if not user:
            raise NotAuthenticated
        if user != value:
            raise ValidationError(_("The user should send request himself."))
        return value

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class VerificationGenerateRequestSerializer(BaseVerificationSerializer):

    verification_type = serializers.ChoiceField(
        choices=VERIFICATIONS_TYPES
    )

    class Meta(BaseVerificationSerializer.Meta):
        model = Verification
        fields = [
            'user', 'verification_type',
        ]
        validators = []

    def create(self, validated_data):
        return generate_verification(validated_data['user'], validated_data['verification_type'])


class VerificationGenerateSerializer(BaseVerificationSerializer):

    verification_type = serializers.ChoiceField(
        choices=VERIFICATIONS_TYPES
    )

    class Meta(BaseVerificationSerializer.Meta):
        model = Verification
        fields = [
            'id', 'user', 'verification_type', 'created', 'updated',
        ]

        validators = []


class VerificationVerifySerializer(BaseVerificationSerializer):

    verification_type = serializers.ChoiceField(
        choices=VERIFICATIONS_TYPES
    )

    verification_code = serializers.CharField(
        validators=[],
    )

    class Meta(BaseVerificationSerializer.Meta):
        model = Verification
        fields = [
            'id', 'user', 'verification_type', 'created', 'updated', VERIFICATION_CODE_FIELD,
        ]

        extra_kwargs = {
            VERIFICATION_CODE_FIELD: {'write_only': True, 'validators': []},
        }

        validators = []

    def validate_verification_code(self, value):
        pass

    def create(self, validated_data):
        return Verification.objects.get(user=validated_data['user'], verification_type=validated_data['verification_type'])


# class VerificationVerifySerializer(BaseVerificationSerializer):
#
#     verification_type = serializers.ChoiceField(
#         choices=VERIFICATIONS_TYPES
#     )
#
#     verification_code = serializers.CharField(
#         validators=[],
#     )
#
#     class Meta(BaseVerificationSerializer.Meta):
#         model = Verification
#         fields = [
#             'id', 'user', 'verification_type', 'created', 'updated', 'verified'
#         ]
#
#         extra_kwargs = {
#         }
#
#         validators = []
#
#     def validate_verification_code(self, value):
#         pass
#
#     def create(self, validated_data):
#         return Verification.objects.get(user=validated_data['user'], verification_type=validated_data['verification_type'])