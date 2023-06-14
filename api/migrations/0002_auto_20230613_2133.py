# Generated by Django 3.2.6 on 2023-06-13 21:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='apiuser',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='apiuser',
            name='group',
        ),
        migrations.RemoveField(
            model_name='apiuser',
            name='modified_by',
        ),
        migrations.DeleteModel(
            name='BlacklistedToken',
        ),
        migrations.DeleteModel(
            name='ApiGroup',
        ),
        migrations.DeleteModel(
            name='ApiUser',
        ),
    ]
