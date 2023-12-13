# Generated by Django 4.2.7 on 2023-12-12 05:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('guild', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='category',
            name='subscribes',
            field=models.ManyToManyField(related_name='categories', through='guild.Subscription', to='guild.profile'),
        ),
        migrations.AddField(
            model_name='subscription',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subscriptions', to='guild.category'),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscriptions', to='guild.profile'),
        ),
    ]