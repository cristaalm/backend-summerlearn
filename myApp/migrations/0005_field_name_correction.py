# Generated by Django 5.1 on 2024-09-19 18:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myApp', '0004_change_foreing_key_days_activities'),
    ]

    operations = [
        migrations.RenameField(
            model_name='activities',
            old_name='areas_status',
            new_name='activities_status',
        ),
    ]
