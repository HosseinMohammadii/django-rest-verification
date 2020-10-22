from celery import shared_task

from django.utils import timezone

from .models import Verification
from .conf import CODE_LIEF_TIME
from .verification import change_to_unverified_record


@shared_task()
def archive_expired_verifications():
    expired_verifications_qs = Verification.objects.filter(created__lt=timezone.now() - CODE_LIEF_TIME)
    for verification in expired_verifications_qs:
        change_to_unverified_record(verification=verification)
