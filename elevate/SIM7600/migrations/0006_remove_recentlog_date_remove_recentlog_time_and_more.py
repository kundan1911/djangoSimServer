# Generated by Django 4.2.10 on 2024-03-23 07:01

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('SIM7600', '0005_alter_alllogs_date_alter_alllogs_time_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recentlog',
            name='date',
        ),
        migrations.RemoveField(
            model_name='recentlog',
            name='time',
        ),
        migrations.AddField(
            model_name='recentlog',
            name='datetime',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='recentlog',
            name='car_no',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='recentlog',
            name='slot_no',
            field=models.CharField(max_length=10),
        ),
    ]