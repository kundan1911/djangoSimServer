# Generated by Django 4.2.10 on 2024-03-25 03:18

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('SIM7600', '0006_remove_recentlog_date_remove_recentlog_time_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='alllogs',
            name='date',
        ),
        migrations.RemoveField(
            model_name='alllogs',
            name='time',
        ),
        migrations.AddField(
            model_name='alllogs',
            name='datetime',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
