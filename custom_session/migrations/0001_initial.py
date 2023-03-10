# Generated by Django 4.1.7 on 2023-02-20 15:29

import django.contrib.sessions.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('sessions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomSession',
            fields=[
                ('session_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='sessions.session')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'session',
                'verbose_name_plural': 'sessions',
                'abstract': False,
            },
            bases=('sessions.session',),
            managers=[
                ('objects', django.contrib.sessions.models.SessionManager()),
            ],
        ),
    ]
