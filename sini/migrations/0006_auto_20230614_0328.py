# Generated by Django 3.2.6 on 2023-06-14 03:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sini', '0005_auto_20230614_0328'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='apiuser',
            options={'managed': True, 'verbose_name': 'Usuario API', 'verbose_name_plural': 'Usuarios API'},
        ),
        migrations.AlterModelTable(
            name='apiuser',
            table='sini_api_user',
        ),
    ]
