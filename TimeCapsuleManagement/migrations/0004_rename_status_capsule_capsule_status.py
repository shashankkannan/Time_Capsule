# Generated by Django 5.0.1 on 2024-03-17 01:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('TimeCapsuleManagement', '0003_rename_seal_capsule_capsule_status'),
    ]

    operations = [
        migrations.RenameField(
            model_name='capsule',
            old_name='status',
            new_name='capsule_status',
        ),
    ]