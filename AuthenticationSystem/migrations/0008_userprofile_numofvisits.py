# Generated by Django 3.2.25 on 2024-04-03 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AuthenticationSystem', '0007_userprofile_email_verification_token'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='numofvisits',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
