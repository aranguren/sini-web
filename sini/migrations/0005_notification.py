# Generated by Django 3.2.6 on 2023-07-26 20:22

import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sini', '0004_auto_20230710_1759'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('send_to', models.CharField(choices=[('todos', 'Todos'), ('grupo', 'Grupo'), ('uno', 'Uno')], max_length=254, verbose_name='Enviar a')),
                ('subject', models.CharField(max_length=254, verbose_name='Asunto')),
                ('message', models.TextField(verbose_name='Mensaje')),
                ('url_noticia', models.URLField(verbose_name='URL noticia')),
                ('url_imagen', models.URLField(verbose_name='URL imagen')),
                ('geom', django.contrib.gis.db.models.fields.PointField(blank=True, null=True, srid=4326, verbose_name='Localización')),
                ('api_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to='sini.apigroup', verbose_name='Grupo')),
                ('api_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to='sini.apiuser', verbose_name='Usuario')),
            ],
            options={
                'verbose_name': 'Notification',
                'verbose_name_plural': 'Notifications',
                'db_table': 'sini_notificacion',
                'managed': True,
            },
        ),
    ]
