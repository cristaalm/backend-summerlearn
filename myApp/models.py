from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class UserManager(BaseUserManager):

    use_in_migration = True

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('email is Required')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff = True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser = True')

        return self.create_user(email, password, **extra_fields)


class UserData(AbstractUser):
    username = None  # Disable the default username field
    name = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    users_photo = models.CharField(max_length=255, blank=True, null=True)
    users_birthdate = models.DateField(blank=True, null=True)
    users_phone = models.CharField(max_length=20, blank=True, null=True)
    users_rol = models.ForeignKey('Rol', models.DO_NOTHING, db_column='users_rol', null=True, blank=True)
    users_status = models.ForeignKey('Status', models.DO_NOTHING, db_column='users_status', null=True, blank=True)
    users_tour = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.name

class Status(models.Model):
    status_name = models.CharField(max_length=255)
    status_id = models.BigAutoField(primary_key=True)

    class Meta:
        managed = True
        db_table = 'status'

class Rol(models.Model):
    rol_id = models.BigAutoField(primary_key=True)
    rol_name = models.CharField(max_length=255)

    class Meta:
        managed = True
        db_table = 'rol'
        
class Areas(models.Model):
    areas_id = models.BigAutoField(primary_key=True)
    areas_name = models.CharField(max_length=255)
    areas_date = models.DateField()
    areas_user = models.ForeignKey('UserData', models.DO_NOTHING, db_column='areas_user', to_field='id')
    areas_status = models.BooleanField()

    class Meta:
        managed = True
        db_table = 'areas'

class Grades(models.Model):
    grades_id = models.BigAutoField(primary_key=True)
    grades_description = models.CharField(max_length=255)

    class Meta:
        managed = True
        db_table = 'grades'
            
class Programs(models.Model):
    programs_id = models.BigAutoField(primary_key=True)
    programs_name = models.CharField(max_length=255)
    programs_start = models.DateField()
    programs_end = models.DateField()
    programs_grade = models.ForeignKey('Grades', models.DO_NOTHING, db_column='programs_grade')
    programs_user = models.ForeignKey('UserData', models.DO_NOTHING, db_column='programs_user')
    programs_status = models.ForeignKey('Status', models.DO_NOTHING, db_column='programs_status')
    programs_area = models.ForeignKey('Areas', models.DO_NOTHING, db_column='programs_area')

    class Meta:
        managed = True
        db_table = 'programs'
        
class SubscriptionsVolunteer(models.Model):
    subscriptions_volunteer_id = models.BigAutoField(primary_key=True)
    subscriptions_volunteer_activity = models.ForeignKey('Activities', models.DO_NOTHING, db_column='subscriptions_volunteer_activity')
    subscriptions_volunteer_user = models.ForeignKey('UserData', models.DO_NOTHING, db_column='subscriptions_volunteer_user')

    class Meta:
        managed = True
        db_table = 'subscriptions_volunteer'

class SubscriptionsChildren(models.Model):
    subscriptions_children_id = models.BigAutoField(primary_key=True)
    subscriptions_children_activity = models.ForeignKey('Activities', models.DO_NOTHING, db_column='subscriptions_children_activity')
    subscriptions_children_child = models.ForeignKey('Children', models.DO_NOTHING, db_column='subscriptions_children_child')

    class Meta:
        managed = True
        db_table = 'subscriptions_children'
        
class Logs(models.Model):
    logs_id = models.BigAutoField(primary_key=True)
    logs_description = models.CharField(max_length=255)
    logs_creation = models.DateField()
    logs_user = models.ForeignKey('UserData', models.DO_NOTHING, db_column='logs_user')

    class Meta:
        managed = True
        db_table = 'logs'
        
class Donations(models.Model):
    donations_id = models.BigAutoField(primary_key=True)
    donations_concept = models.CharField(max_length=255)
    donations_quantity = models.FloatField()
    donations_spent = models.FloatField(null=True)
    donations_date = models.DateField()
    donations_user = models.ForeignKey('UserData', models.DO_NOTHING, db_column='donations_user')

    class Meta:
        managed = True
        db_table = 'donations'
        
class Children(models.Model):
    children_id = models.BigAutoField(primary_key=True)
    children_name = models.CharField(max_length=255)
    children_photo = models.CharField(blank=True, null=True, max_length=255)
    children_birthdate = models.DateField()
    children_curp = models.CharField(blank=True, null=True, max_length=255)
    children_user = models.ForeignKey('UserData', models.DO_NOTHING, db_column='children_user')

    class Meta:
        managed = True
        db_table = 'children'
        
class PerformanceBeneficiaries(models.Model):
    performance_beneficiaries_id = models.BigAutoField(primary_key=True)
    performance_beneficiaries_subscription = models.ForeignKey('SubscriptionsChildren', models.DO_NOTHING, db_column='performance_beneficiaries_subscription',null=True)
    performance_beneficiaries_value = models.FloatField()

    class Meta:
        managed = True
        db_table = 'performance_beneficiaries'
        
class Bills(models.Model):
    bills_id = models.BigAutoField(primary_key=True)
    bills_concept = models.CharField(max_length=255)
    bills_amount = models.FloatField(null=True)
    bills_date = models.DateField()
    bills_donations = models.ForeignKey('Donations', models.DO_NOTHING, db_column='bills_donations')
    bills_user = models.ForeignKey('UserData', models.DO_NOTHING, db_column='bills_user')

    class Meta:
        managed = True
        db_table = 'bills'

class Days(models.Model):
    day_id = models.BigAutoField(primary_key=True)
    day_description = models.CharField(max_length=255)

    class Meta:
        managed = True
        db_table = 'days'
        
class DaysActivities(models.Model):
    days_activities_id = models.BigAutoField(primary_key=True)
    days_activities_days = models.ForeignKey('Days', models.DO_NOTHING, db_column='days_activities_days')
    days_activities_activity = models.ForeignKey('Activities', models.DO_NOTHING, db_column='days_activities_activity')

    class Meta:
        managed = True
        db_table = 'days_activities'
        
class Schedules(models.Model):
    schedules_id = models.BigAutoField(primary_key=True)
    schedules_start = models.TimeField()
    schedules_duration = models.TimeField()
    schedules_day = models.ForeignKey('DaysActivities', models.DO_NOTHING, db_column='schedules_day')

    class Meta:
        managed = True
        db_table = 'schedules'


class Objectives(models.Model):
    objectives_id = models.BigAutoField(primary_key=True)
    objectives_description = models.CharField(max_length=255)
    objectives_activity = models.ForeignKey('Activities', models.DO_NOTHING, db_column='objectives_activity')

    class Meta:
        managed = True
        db_table = 'objectives'


class Activities(models.Model):
    activities_id = models.BigAutoField(primary_key=True)
    activities_name = models.CharField(max_length=255)
    activities_description = models.CharField(max_length=255)
    activities_program = models.ForeignKey('Programs', models.DO_NOTHING, db_column='activities_program')
    activities_date = models.DateField()
    activities_user = models.ForeignKey('UserData', models.DO_NOTHING, db_column='activities_user')
    activities_status = models.BooleanField()

    class Meta:
        managed = True
        db_table = 'activities'

class Chat(models.Model):
    chat_id = models.CharField(max_length=255, primary_key=True, unique=True)
    chat_date = models.DateField()
    chat_user1 = models.ForeignKey('UserData', models.DO_NOTHING, db_column='chat_user1', related_name='chats_as_user1')
    chat_user2 = models.ForeignKey('UserData', models.DO_NOTHING, db_column='chat_user2', related_name='chats_as_user2')

    class Meta:
        managed = True
        db_table = 'chat'

class Messages(models.Model):
    messages_id = models.BigAutoField(primary_key=True)
    messages_date = models.DateTimeField()
    messages_content = models.CharField(max_length=500)
    messages_chat = models.ForeignKey('Chat', models.DO_NOTHING, db_column='messages_chat')
    messages_user = models.ForeignKey('UserData', models.DO_NOTHING, db_column='messages_user')

    class Meta:
        managed = True
        db_table = 'messages'