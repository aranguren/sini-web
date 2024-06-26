# Generated by Django 3.2.6 on 2023-07-31 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sini', '0011_alter_apiuser_device'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='status',
            field=models.CharField(blank=True, choices=[('enviado', 'Enviado'), ('fallido', 'Fallido'), ('enviado_parcialmente', 'Enviado (Parcialmente)')], max_length=50, null=True, verbose_name='Status'),
        ),
        migrations.AddField(
            model_name='notification',
            name='status_description',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Descripción'),
        ),
    ]
