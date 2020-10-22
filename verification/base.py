from django.utils import timezone

default_config = {
    'VERIFICATIONS': [],
    'CONTAINS_NUMERIC': True,
    'CONTAINS_UPPER_ALPHABETIC': False,
    'CONTAINS_LOWER_ALPHABETIC': False,
    'CUSTOM_CODE_LETTERS': '',
    'CODE_LENGTH': 6,
    'LIFE_TIME_SECOND': 0,
    'LIFE_TIME_MINUTE': 3,
    'LIFE_TIME_HOUR': 0,
    'LIFE_TIME_DAY': 0,
    'LIFE_TIME_PENALTY_SECOND': 60,
}


CELERY_BEAT_SCHEDULE = {
    'archive-expired-verifications': {
        'task': 'verification.tasks.archive_expired_verifications',
        'schedule': timezone.timedelta(minutes=3),
    },
}

numeric = '0123456789'
lowercase_alphabetic = 'abcdefghijklmnopqrstuvwxyz'
uppercase_alphabetic = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
