# Generated by Django 5.1 on 2024-10-25 14:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myApp', '0019_fix_daysactivities'),
    ]

    operations = [
        migrations.AlterField(
            model_name='daysactivities',
            name='days_activities_schedules',
            field=models.ForeignKey(db_column='days_activities_schedules', on_delete=django.db.models.deletion.DO_NOTHING, to='myApp.schedules'),
        ),
    ]
