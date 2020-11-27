from django.apps import AppConfig


class EmailVerificationConfig(AppConfig):
    name = 'verification'

#    def ready(self):
#        from .signals import handlers
