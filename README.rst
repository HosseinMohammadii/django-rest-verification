============
Verification
============

Verification is a Django app to conduct code-based verifications. For any verification,
email or phone, it can be used.

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "verification" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'verification',
    ]

2. Write yuor preferred settings in settings file::
   
    VERIFICATION = {
        'VERIFICATIONS': [
            {'type': 'email', 'user_model_field': 'is_email_verified'},],

        'CODE_LENGTH': 6,
        'CONTAINS_NUMERIC': True,
        'CONTAINS_UPPER_ALPHABETIC': False,
        'CONTAINS_LOWER_ALPHABETIC': False,
        'LIFE_TIME_SECOND': 0,
        'LIFE_TIME_MINUTE': 3,
        'LIFE_TIME_HOUR': 0,
        'LIFE_TIME_DAY': 0,
        'LIFE_TIME_PENALTY_SECOND': 60,
        
    }
    

2. Inherit from verification.views "BaseGenerateVerificationAPIView" and
"BaseVerifyVerificationAPIView" classes.

3. Write your preferred function for sending code and In class that inherits
from "BaseGenerateVerificationAPIView" set it to "send_code_function" variable.


4. Connect your urls to your views.


5. Run ``python manage.py migrate`` to create the verification models.

