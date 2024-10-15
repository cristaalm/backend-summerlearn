# Generated by Django 5.1 on 2024-10-15 14:48

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myApp', '0011_add_field_programs_grade'),
    ]

    operations = [
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('chat_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('chat_date', models.DateField()),
                ('chat_user1', models.ForeignKey(db_column='chat_user1', on_delete=django.db.models.deletion.DO_NOTHING, related_name='chats_as_user1', to=settings.AUTH_USER_MODEL)),
                ('chat_user2', models.ForeignKey(db_column='chat_user2', on_delete=django.db.models.deletion.DO_NOTHING, related_name='chats_as_user2', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'chat',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Messages',
            fields=[
                ('messages_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('messages_date', models.DateField()),
                ('messages_content', models.CharField(max_length=500)),
                ('messages_chat', models.ForeignKey(db_column='messages_chat', on_delete=django.db.models.deletion.DO_NOTHING, to='myApp.chat')),
                ('messages_user', models.ForeignKey(db_column='messages_user', on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'messages',
                'managed': True,
            },
        ),
    ]
