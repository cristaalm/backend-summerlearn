# Generated by Django 5.1 on 2024-09-11 05:19

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rol',
            fields=[
                ('rol_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('rol_name', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'rol',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('status_name', models.CharField(max_length=255)),
                ('status_id', models.BigAutoField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'status',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='UserData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('email', models.EmailField(max_length=100, unique=True)),
                ('users_photo', models.CharField(blank=True, max_length=255, null=True)),
                ('users_birthdate', models.DateField(blank=True, null=True)),
                ('users_phone', models.CharField(blank=True, max_length=20, null=True)),
                ('users_tour', models.BooleanField(default=False)),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
                ('users_rol', models.ForeignKey(blank=True, db_column='users_rol', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='myApp.rol')),
                ('users_status', models.ForeignKey(blank=True, db_column='users_status', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='myApp.status')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Areas',
            fields=[
                ('areas_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('areas_name', models.CharField(max_length=255)),
                ('areas_date', models.DateField()),
                ('areas_status', models.BooleanField()),
                ('areas_user', models.ForeignKey(db_column='areas_user', on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'areas',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Activities',
            fields=[
                ('activities_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('activities_name', models.CharField(max_length=255)),
                ('activities_description', models.CharField(max_length=255)),
                ('activities_date', models.DateField()),
                ('areas_status', models.BooleanField()),
                ('activities_user', models.ForeignKey(db_column='activities_user', on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ('activities_area', models.ForeignKey(db_column='activities_area', on_delete=django.db.models.deletion.DO_NOTHING, to='myApp.areas')),
            ],
            options={
                'db_table': 'activities',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Children',
            fields=[
                ('children_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('children_name', models.CharField(max_length=255)),
                ('children_photo', models.CharField(blank=True, max_length=255, null=True)),
                ('children_birthdate', models.DateField()),
                ('children_curp', models.CharField(blank=True, max_length=255, null=True)),
                ('children_user', models.ForeignKey(db_column='children_user', on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'children',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Days',
            fields=[
                ('days_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('days_description', models.CharField(max_length=255)),
                ('days_activity', models.ForeignKey(db_column='days_activity', on_delete=django.db.models.deletion.DO_NOTHING, to='myApp.activities')),
            ],
            options={
                'db_table': 'days',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Donations',
            fields=[
                ('donations_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('donations_concept', models.CharField(max_length=255)),
                ('donations_quantity', models.FloatField()),
                ('donations_date', models.DateField()),
                ('donations_user', models.ForeignKey(db_column='donations_user', on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'donations',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Bills',
            fields=[
                ('bills_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('bills_concept', models.CharField(max_length=255)),
                ('bills_date', models.DateField()),
                ('bills_donations', models.ForeignKey(db_column='bills_donations', on_delete=django.db.models.deletion.DO_NOTHING, to='myApp.donations')),
            ],
            options={
                'db_table': 'bills',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Logs',
            fields=[
                ('logs_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('logs_description', models.CharField(max_length=255)),
                ('logs_creation', models.DateField()),
                ('logs_user', models.ForeignKey(db_column='logs_user', on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'logs',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Objectives',
            fields=[
                ('objectives_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('objectives_description', models.CharField(max_length=255)),
                ('objectives_activity', models.ForeignKey(db_column='objectives_activity', on_delete=django.db.models.deletion.DO_NOTHING, to='myApp.activities')),
            ],
            options={
                'db_table': 'objectives',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='PerformanceBeneficiaries',
            fields=[
                ('performance_beneficiaries_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('performance_beneficiaries_value', models.FloatField()),
                ('performance_beneficiaries_activity', models.ForeignKey(db_column='performance_beneficiaries_activity', on_delete=django.db.models.deletion.DO_NOTHING, to='myApp.activities')),
                ('performance_beneficiaries_children', models.ForeignKey(db_column='performance_beneficiaries_children', on_delete=django.db.models.deletion.DO_NOTHING, to='myApp.children')),
            ],
            options={
                'db_table': 'performance_beneficiaries',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Programs',
            fields=[
                ('programs_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('programs_start', models.DateField()),
                ('programs_end', models.DateField()),
                ('programs_user', models.ForeignKey(db_column='programs_user', on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ('programs_status', models.ForeignKey(db_column='programs_status', on_delete=django.db.models.deletion.DO_NOTHING, to='myApp.status')),
            ],
            options={
                'db_table': 'programs',
                'managed': True,
            },
        ),
        migrations.AddField(
            model_name='activities',
            name='activities_program',
            field=models.ForeignKey(db_column='activities_program', on_delete=django.db.models.deletion.DO_NOTHING, to='myApp.programs'),
        ),
        migrations.CreateModel(
            name='Schedules',
            fields=[
                ('schedules_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('schedules_start', models.TimeField()),
                ('schedules_duration', models.TimeField()),
                ('schedules_day', models.ForeignKey(db_column='schedules_day', on_delete=django.db.models.deletion.DO_NOTHING, to='myApp.days')),
            ],
            options={
                'db_table': 'schedules',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Subscriptions',
            fields=[
                ('subscriptions_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('subscriptions_activity', models.ForeignKey(db_column='subscriptions_activity', on_delete=django.db.models.deletion.DO_NOTHING, to='myApp.activities')),
                ('subscriptions_user', models.ForeignKey(db_column='subscriptions_user', on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'subscriptions',
                'managed': True,
            },
        ),
    ]
