# Generated by Django 3.2.6 on 2023-08-03 15:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sini', '0017_remove_apiuser_token_fcm'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='incidence',
            name='incidence_type',
        ),
        migrations.RemoveField(
            model_name='mobilewarning',
            name='incidence_type',
        ),
        migrations.CreateModel(
            name='IncidenceType',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Fecha creado')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='Fecha modificado')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='Nombre')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Creado por')),
                ('modified_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Modificado por')),
            ],
            options={
                'verbose_name': 'Contacto',
                'verbose_name_plural': 'Contactos',
                'db_table': 'arbolsaf_type_incidence',
                'ordering': ['name'],
                'managed': True,
            },
        ),
        migrations.AddField(
            model_name='incidence',
            name='type_incidence',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.RESTRICT, to='sini.incidencetype', verbose_name='Tipo incidente'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='mobilewarning',
            name='type_incidence',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.RESTRICT, to='sini.incidencetype', verbose_name='Tipo incidente'),
            preserve_default=False,
        ),
    ]