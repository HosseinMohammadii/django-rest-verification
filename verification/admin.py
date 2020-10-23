from django.contrib import admin

from .models import Verification, VerificationRecord


@admin.register(Verification)
class VerificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'verification_type', 'created']
    list_filter = ['user']


@admin.register(VerificationRecord)
class VerificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'verification_type', 'created']
    list_filter = ['user']
