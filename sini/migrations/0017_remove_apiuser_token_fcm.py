# Generated by Django 3.2.6 on 2023-08-02 15:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sini', '0016_alter_contact_address'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='apiuser',
            name='token_fcm',
        ),
    ]