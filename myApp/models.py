# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.hashers import check_password

class Activities(models.Model):
    activities_id = models.BigAutoField(primary_key=True)
    activities_name = models.CharField()
    activities_area = models.ForeignKey('Areas', models.DO_NOTHING, db_column='activities_area')
    activities_description = models.CharField()
    activities_program = models.ForeignKey('Programs', models.DO_NOTHING, db_column='activities_program')
    activities_date = models.DateField()
    activities_user = models.ForeignKey('Users', models.DO_NOTHING, db_column='activities_user')
    areas_status = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'activities'


class Areas(models.Model):
    areas_id = models.BigAutoField(primary_key=True)
    areas_name = models.CharField()
    areas_date = models.DateField()
    areas_user = models.ForeignKey('Users', models.DO_NOTHING, db_column='areas_user')
    areas_status = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'areas'


class Bills(models.Model):
    bills_id = models.BigAutoField(primary_key=True)
    bills_concept = models.CharField()
    bills_date = models.DateField()
    bills_donations = models.ForeignKey('Donations', models.DO_NOTHING, db_column='bills_donations')

    class Meta:
        managed = False
        db_table = 'bills'


class Children(models.Model):
    children_id = models.BigAutoField(primary_key=True)
    children_name = models.CharField()
    children_photo = models.CharField(blank=True, null=True)
    children_birthdate = models.DateField()
    children_curp = models.CharField(blank=True, null=True)
    children_user = models.ForeignKey('Users', models.DO_NOTHING, db_column='children_user')

    class Meta:
        managed = False
        db_table = 'children'


class Days(models.Model):
    days_id = models.BigAutoField(primary_key=True)
    days_description = models.CharField()
    days_activity = models.ForeignKey(Activities, models.DO_NOTHING, db_column='days_activity')

    class Meta:
        managed = False
        db_table = 'days'


class Donations(models.Model):
    donations_id = models.BigAutoField(primary_key=True)
    donations_concept = models.CharField()
    donations_quantity = models.FloatField()
    donations_date = models.DateField()
    donations_user = models.ForeignKey('Users', models.DO_NOTHING, db_column='donations_user')

    class Meta:
        managed = False
        db_table = 'donations'


class Logs(models.Model):
    logs_id = models.BigAutoField(primary_key=True)
    logs_description = models.CharField()
    logs_creation = models.DateField()
    logs_user = models.ForeignKey('Users', models.DO_NOTHING, db_column='logs_user')

    class Meta:
        managed = False
        db_table = 'logs'


class Objectives(models.Model):
    objectives_id = models.BigAutoField(primary_key=True)
    objectives_description = models.CharField()
    objectives_activity = models.ForeignKey(Activities, models.DO_NOTHING, db_column='objectives_activity')

    class Meta:
        managed = False
        db_table = 'objectives'


class PerformanceBeneficiaries(models.Model):
    performance_beneficiaries_id = models.BigAutoField(primary_key=True)
    performance_beneficiaries_activity = models.ForeignKey(Activities, models.DO_NOTHING, db_column='performance_beneficiaries_activity')
    performance_beneficiaries_children = models.ForeignKey(Children, models.DO_NOTHING, db_column='performance_beneficiaries_children')
    performance_beneficiaries_value = models.FloatField()

    class Meta:
        managed = False
        db_table = 'performance_beneficiaries'


class Programs(models.Model):
    programs_id = models.BigAutoField(primary_key=True)
    programs_start = models.DateField()
    programs_end = models.DateField()
    programs_user = models.ForeignKey('Users', models.DO_NOTHING, db_column='programs_user')
    programs_status = models.ForeignKey('Status', models.DO_NOTHING, db_column='programs_status')

    class Meta:
        managed = False
        db_table = 'programs'


class Rol(models.Model):
    rol_id = models.BigAutoField(primary_key=True)
    rol_name = models.CharField()

    class Meta:
        managed = False
        db_table = 'rol'


class Schedules(models.Model):
    schedules_id = models.BigAutoField(primary_key=True)
    schedules_start = models.TimeField()
    schedules_duration = models.TimeField()
    schedules_day = models.ForeignKey(Days, models.DO_NOTHING, db_column='schedules_day')

    class Meta:
        managed = False
        db_table = 'schedules'


class Status(models.Model):
    status_name = models.CharField()
    status_id = models.BigAutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'status'


class Subscriptions(models.Model):
    subscriptions_id = models.BigAutoField(primary_key=True)
    subscriptions_activity = models.ForeignKey(Activities, models.DO_NOTHING, db_column='subscriptions_activity')
    subscriptions_user = models.ForeignKey('Users', models.DO_NOTHING, db_column='subscriptions_user')

    class Meta:
        managed = False
        db_table = 'subscriptions'


class Users(models.Model):
    users_id = models.BigAutoField(primary_key=True)
    users_name = models.CharField(max_length=255)
    users_photo = models.CharField(max_length=255, blank=True, null=True)
    users_birthdate = models.DateField()
    users_mail = models.EmailField(unique=True)  
    users_password = models.CharField(max_length=128) 
    users_phone = models.CharField(max_length=20, blank=True, null=True)
    users_rol = models.ForeignKey(Rol, models.DO_NOTHING, db_column='users_rol')
    users_tour = models.BooleanField()
    users_status = models.ForeignKey(Status, models.DO_NOTHING, db_column='users_status')

    def check_password(self, raw_password):
        return check_password(raw_password, self.users_password)

    class Meta:
        managed = False
        db_table = 'users'