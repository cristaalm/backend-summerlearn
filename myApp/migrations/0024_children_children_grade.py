# Generated by Django 5.1 on 2024-11-18 02:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myApp', '0023_alter_performancebeneficiaries_performance_beneficiaries_value'),
    ]

    operations = [
        migrations.AddField(
            model_name='children',
            name='children_grade',
            field=models.ForeignKey(db_column='children_grade', default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='myApp.grades'),
            preserve_default=False,
        ),
    ]
