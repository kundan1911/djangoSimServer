# Generated by Django 4.2.10 on 2024-04-25 02:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SIM7600', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='alllogs',
            name='user',
        ),
        migrations.RemoveField(
            model_name='recentlog',
            name='user',
        ),
        migrations.AddField(
            model_name='alllogs',
            name='ownerId',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='recentlog',
            name='ownerId',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]