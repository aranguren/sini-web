# Generated by Django 3.2.6 on 2023-07-31 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sini', '0012_auto_20230731_1355'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='status_description',
            field=models.TextField(blank=True, null=True, verbose_name='Descripción'),
        ),
    ]
