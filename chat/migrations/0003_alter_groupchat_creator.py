# Generated by Django 4.1.7 on 2023-02-28 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_groupchat_message_member'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groupchat',
            name='creator',
            field=models.CharField(db_index=True, max_length=32, unique=True),
        ),
    ]
