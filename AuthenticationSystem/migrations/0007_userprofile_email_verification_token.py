# Generated by Django 3.2.25 on 2024-03-27 03:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AuthenticationSystem', '0006_userprofile_email_verified'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='email_verification_token',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
