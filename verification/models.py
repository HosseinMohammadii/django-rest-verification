from django.conf import settings
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class BaseVerification(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_related",
        related_query_name="%(app_label)s_%(class)ss",
    )

    verification_type = models.CharField(
        max_length=128,
    )

    verification_code = None

    created = models.DateTimeField(
        auto_created=True,
        auto_now=True,
    )

    updated = models.DateTimeField(
        auto_created=True,
        auto_now=True,
    )

    class Meta:
        abstract = True
        ordering = ['created']


class Verification(BaseVerification):

    verification_code = models.CharField(
        max_length=32,
        unique=True,
    )

    class Meta:
        unique_together = ['user', 'verification_type']
        ordering = ['-created']


class VerificationRecord(BaseVerification):
    verification_code = models.CharField(
        max_length=32,
    )

    is_verified = models.BooleanField(
        default=False,
    )

    class Meta:
        ordering = ['-created']
