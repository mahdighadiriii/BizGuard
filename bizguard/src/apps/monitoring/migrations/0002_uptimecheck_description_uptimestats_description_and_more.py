# Generated by Django 4.2.6 on 2025-07-18 17:29

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('monitoring', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='uptimecheck',
            name='description',
            field=models.TextField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='uptimestats',
            name='description',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='website',
            name='description',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
    ]
