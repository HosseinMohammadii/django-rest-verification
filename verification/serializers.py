from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers
from rest_framework.exceptions import ValidationError, NotAuthenticated

from .models import (BaseVerification,
                     Verification, VerificationRecord)
from .validators import validate_verification_type

from .verification import generate_verification
from .conf import VERIFICATION_CODE_FIELD


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

    def validate(self, attrs):
        user = attrs
        is_verified(user, verification_type=self.verification_type)

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class VerificationSerializer(BaseVerificationSerializer):

    class Meta(BaseVerificationSerializer.Meta):
        model = Verification
        fields = [
            'id', 'user', 'verification_type', 'created', 'updated', VERIFICATION_CODE_FIELD
        ]

        extra_kwargs = {
            VERIFICATION_CODE_FIELD: {'write_only': True}
        }

    def create(self, validated_data):
        return generate_verification(validated_data['user'], validated_data['verification_type'])


# class VerificationSerializer(BaseVerificationSerializer):
#
#     class Meta(BaseVerificationSerializer.Meta):
#         model = Verification
#         fields = [
#             'id', 'user', 'verification_type', 'created', 'updated',
#         ]


class VerificationRecordSerializer(BaseVerificationSerializer):
    class Meta(BaseVerificationSerializer.Meta):
        model = VerificationRecord
        fields = [
            'id', 'user', 'verification_type', 'verification_code', 'created', 'updated', 'is_verified',
        ]

