from django.conf import settings
from django.utils import timezone
from .base import default_config, numeric, lowercase_alphabetic, uppercase_alphabetic

config = default_config
config.update(settings.VERIFICATION)

VERIFICATION_CODE_FIELD = 'verification_code'
VERIFICATIONS = config.get('VERIFICATIONS')
CODE_LENGTH = config.get('CODE_LENGTH')
LIFE_TIME_SECOND = config.get('LIFE_TIME_SECOND')
LIFE_TIME_MINUTE = config.get('LIFE_TIME_MINUTE')
LIFE_TIME_HOUR = config.get('LIFE_TIME_HOUR')
LIFE_TIME_DAY = config.get('LIFE_TIME_DAY')
LIFE_TIME_PENALTY_SECOND = config.get('LIFE_TIME_PENALTY_SECOND')

CODE_LIEF_TIME = timezone.timedelta(
    seconds=LIFE_TIME_SECOND + LIFE_TIME_PENALTY_SECOND,
    minutes=LIFE_TIME_MINUTE,
    hours=LIFE_TIME_HOUR,
    days=LIFE_TIME_DAY,
)

ALLOWED_CODE_LETTERS = ''
if config.get('CONTAINS_NUMERIC'):
    ALLOWED_CODE_LETTERS += numeric
if config.get('CONTAINS_UPPER_ALPHABETIC'):
    ALLOWED_CODE_LETTERS += uppercase_alphabetic
if config.get('CONTAINS_LOWER_ALPHABETIC'):
    ALLOWED_CODE_LETTERS += lowercase_alphabetic

if len(ALLOWED_CODE_LETTERS) == 0:
    raise Exception("No letters are allowed for code generation")


VERIFICATIONS_DICT = {}
VERIFICATIONS_TYPES = []
VERIFICATIONS_USER_MODEL_FIELDS = []
for verification in VERIFICATIONS:
    VERIFICATIONS_TYPES.append(verification.get('type'))
    VERIFICATIONS_USER_MODEL_FIELDS.append(verification.get('user_model_field'))
    VERIFICATIONS_DICT[verification.get('type')] = verification


def get_user_model_field(verification_type):
    return VERIFICATIONS_DICT.get(verification_type, None).get('user_model_field')

