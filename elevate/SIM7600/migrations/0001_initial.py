# Generated by Django 4.2.10 on 2024-02-12 03:02

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('car_number', models.CharField(max_length=20)),
                ('parking_slot_number', models.CharField(max_length=10)),
                ('phone_number', models.CharField(max_length=15)),
            ],
        ),
    ]
