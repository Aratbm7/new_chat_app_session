# Generated by Django 4.1.7 on 2023-03-13 15:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_alter_profile_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='is_owner',
        ),
    ]
