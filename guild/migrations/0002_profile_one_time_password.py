# Generated by Django 4.2.7 on 2023-12-18 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('guild', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='one_time_password',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
