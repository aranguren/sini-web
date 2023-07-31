# Generated by Django 3.2.6 on 2023-07-31 12:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fcm_django', '0011_fcmdevice_fcm_django_registration_id_user_id_idx'),
        ('sini', '0010_apiuser_device'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apiuser',
            name='device',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='api_user', to='fcm_django.fcmdevice', verbose_name='Dispositivo'),
        ),
    ]
