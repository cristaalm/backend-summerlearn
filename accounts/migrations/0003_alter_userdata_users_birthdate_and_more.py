# Generated by Django 5.1 on 2024-09-09 19:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_userdata_users_birthdate_userdata_users_phone_and_more'),
        ('myApp', '__first__'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdata',
            name='users_birthdate',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='userdata',
            name='users_rol',
            field=models.ForeignKey(blank=True, db_column='users_rol', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='myApp.rol'),
        ),
        migrations.AlterField(
            model_name='userdata',
            name='users_status',
            field=models.ForeignKey(blank=True, db_column='users_status', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='myApp.status'),
        ),
        migrations.AlterField(
            model_name='userdata',
            name='users_tour',
            field=models.BooleanField(default=False),
        ),
    ]