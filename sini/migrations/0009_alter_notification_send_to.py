# Generated by Django 3.2.6 on 2023-07-27 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sini', '0008_auto_20230726_2211'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='send_to',
            field=models.CharField(choices=[('todos', 'Todos'), ('grupo', 'Grupo'), ('uno', 'Uno')], default='todos', max_length=254, verbose_name='Enviar a'),
        ),
    ]
