# Generated by Django 4.2.10 on 2024-03-23 06:45

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SIM7600', '0003_receivedcall'),
    ]

    operations = [
        migrations.CreateModel(
            name='AllLogs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('slot_no', models.CharField(max_length=100)),
                ('car_no', models.CharField(max_length=100)),
                ('date', models.DateField(default=datetime.date(2024, 3, 23))),
                ('time', models.TimeField(default=datetime.time(6, 45, 36, 18857))),
            ],
        ),
        migrations.CreateModel(
            name='RecentLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('slot_no', models.CharField(max_length=100)),
                ('car_no', models.CharField(max_length=100)),
                ('date', models.DateField(default=datetime.date(2024, 3, 23))),
                ('time', models.TimeField(default=datetime.time(6, 45, 36, 18730))),
            ],
        ),
        migrations.CreateModel(
            name='SMSTask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(max_length=20)),
                ('message', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
