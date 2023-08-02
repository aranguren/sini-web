# Generated by Django 3.2.6 on 2023-07-28 23:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fcm_django', '0011_fcmdevice_fcm_django_registration_id_user_id_idx'),
        ('sini', '0009_alter_notification_send_to'),
    ]

    operations = [
        migrations.AddField(
            model_name='apiuser',
            name='device',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='fcm_django.fcmdevice', verbose_name='Dispositivo'),
        ),
    ]