# Generated by Django 4.2.6 on 2025-07-19 15:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('monitoring', '0002_uptimecheck_description_uptimestats_description_and_more'),
    ]

    operations = [
        migrations.RenameIndex(
            model_name='website',
            new_name='websites_user_id_c3b78e_idx',
            old_name='website_user_id_1c5543_idx',
        ),
        migrations.RenameIndex(
            model_name='website',
            new_name='websites_status_d86451_idx',
            old_name='website_status_f9439e_idx',
        ),
        migrations.AlterField(
            model_name='website',
            name='check_security',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='website',
            name='status',
            field=models.CharField(choices=[('active', 'Active'), ('paused', 'Paused'), ('deleted', 'Deleted')], default='active', max_length=20),
        ),
        migrations.AlterField(
            model_name='website',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='websites', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterModelTable(
            name='website',
            table='websites',
        ),
    ]
