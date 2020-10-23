from django.utils.crypto import get_random_string
from django.utils import timezone
from django.contrib.auth import get_user_model

from .conf import VERIFICATION_CODE_FIELD
from .models import Verification, VerificationRecord
from . import conf
from . import exceptions

User = get_user_model()


def generate_verification(user, verification_type) -> str:

    if is_verified(user, verification_type):
        print("IS VERIFIEDDDDDD")
        raise exceptions.UserIsVerified()
        # raise Exception
    else:

        try:
            expired_verification = not_have_active_verification(user, verification_type)

            if expired_verification is not None:
                change_to_unverified_record(expired_verification)

            verification_code = generate_unique_code(verification_type)
            new_verification = Verification.objects.create(user=user,
                                                           verification_type=verification_type,
                                                           verification_code=verification_code)
        except Verification.DoesNotExist:
            verification_code = generate_unique_code(verification_type)
            new_verification = Verification.objects.create(user=user,
                                                           verification_type=verification_type,
                                                           verification_code=verification_code)

    return new_verification


# verify_by_verification()


def verify(*args, **kwargs):
    user = kwargs.get('user')
    # user = User.objects.get(id=user_id)
    code = kwargs.get(VERIFICATION_CODE_FIELD)
    verification_type = kwargs.get('verification_type')
    return verify_code(user, verification_type, code)


def verify_code(user, verification_type, code) -> (bool, str):
    verified = False
    try:
        verification = Verification.objects.get(user=user,
                                                verification_type=verification_type)

        if verification.verification_code == code and timezone.now() < verification.created + conf.CODE_LIEF_TIME:
            change_to_verified_user(user, verification.verification_type)
            change_to_verified_record(verification)
            verified = True
        else:
            verified = False
    except Verification.DoesNotExist:
        verified = False

    return verified


def is_verified(user, verification_type):
    # last_verification_record = \
    #     VerificationRecord.objects.filter(user=user,
    #                                       verification_type=verification_type).order_by('created').last()
    # return last_verification_record.is_verified if last_verification_record is not None else False
    return getattr(user, conf.get_user_model_field(verification_type), False)


def not_have_active_verification(user, verification_type):
    """
    if user has active code exception will arise, else the expired verification will return
    :param user:
    :param verification_type:
    :return:
    """
    try:
        verification = Verification.objects.get(user=user,
                                                verification_type=verification_type)
        if timezone.now() < verification.created + conf.CODE_LIEF_TIME:
            raise exceptions.UserHasActiveVerification

        return verification
    except Verification.DoesNotExist:
        return None


def change_to_verified_record(verification: Verification):
    VerificationRecord.objects.create(
        user=verification.user,
        verification_type=verification.verification_type,
        verification_code=verification.verification_code,
        is_verified=True,
    )

    verification.delete()


def change_to_unverified_record(verification: Verification):
    VerificationRecord.objects.create(
        user=verification.user,
        verification_type=verification.verification_type,
        verification_code=verification.verification_code,
        is_verified=False,
    )

    verification.delete()


def change_to_verified_user(user, verification_type):
    update_data = {conf.get_user_model_field(verification_type): True}
    User.objects.filter(pk=user.pk).update(**update_data)


def generate_unique_code(verification_type):
    code = get_random_string(length=conf.CODE_LENGTH, allowed_chars=conf.ALLOWED_CODE_LETTERS)
    qs_exists = Verification.objects.filter(verification_type=verification_type, verification_code=code).exists()
    if qs_exists:
        return generate_unique_code(verification_type)
    return code
