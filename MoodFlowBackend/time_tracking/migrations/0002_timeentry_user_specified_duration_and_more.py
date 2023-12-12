# Generated by Django 4.2.7 on 2023-12-05 22:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('time_tracking', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='timeentry',
            name='user_specified_duration',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='timeentry',
            name='end_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
