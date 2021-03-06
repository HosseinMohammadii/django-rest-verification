# Generated by Django 3.1.1 on 2020-10-23 18:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='VerificationRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated', models.DateTimeField(auto_created=True, auto_now=True)),
                ('created', models.DateTimeField(auto_created=True, auto_now=True)),
                ('verification_type', models.CharField(max_length=128)),
                ('verification_code', models.CharField(max_length=32)),
                ('is_verified', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='verification_verificationrecord_related', related_query_name='verification_verificationrecords', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='Verification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated', models.DateTimeField(auto_created=True, auto_now=True)),
                ('created', models.DateTimeField(auto_created=True, auto_now=True)),
                ('verification_type', models.CharField(max_length=128)),
                ('verification_code', models.CharField(max_length=32, unique=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='verification_verification_related', related_query_name='verification_verifications', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created'],
                'unique_together': {('user', 'verification_type')},
            },
        ),
    ]
