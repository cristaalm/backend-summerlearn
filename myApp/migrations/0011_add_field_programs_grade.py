# Generated by Django 5.1 on 2024-10-05 17:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myApp', '0010_add_grades'),
    ]

    operations = [
        migrations.AddField(
            model_name='programs',
            name='programs_grade',
            field=models.ForeignKey(db_column='programs_grade', default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='myApp.grades'),
            preserve_default=False,
        ),
    ]
