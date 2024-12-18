# Generated by Django 5.1.4 on 2024-12-18 17:29

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0006_project_completed_tasks_project_remaining_tasks_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignment',
            name='completed_tasks',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='assignment',
            name='score',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='task',
            name='assigned_to',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]