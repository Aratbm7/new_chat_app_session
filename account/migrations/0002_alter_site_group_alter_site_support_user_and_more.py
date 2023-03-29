# Generated by Django 4.1.7 on 2023-03-29 14:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='site',
            name='group',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='group_sites', to='account.customgroup'),
        ),
        migrations.AlterField(
            model_name='site',
            name='support_user',
            field=models.ManyToManyField(null=True, related_name='supported_sites', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='site',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sites', to=settings.AUTH_USER_MODEL),
        ),
    ]
