# Generated by Django 4.2.10 on 2024-02-23 05:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SIM7600', '0002_rename_user_carowners'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReceivedCall',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(max_length=20)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
