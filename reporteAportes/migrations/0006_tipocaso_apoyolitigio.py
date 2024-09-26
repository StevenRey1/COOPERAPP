# Generated by Django 5.1.1 on 2024-09-25 18:32

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reporteAportes', '0005_tipoherramienta_remove_apoyoeventos_reporte_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='TipoCaso',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255, verbose_name='Tipo de Caso')),
            ],
        ),
        migrations.CreateModel(
            name='ApoyoLitigio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_caso', models.CharField(blank=True, max_length=255, verbose_name='Nombre de los casos')),
                ('cantidad_ids', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(999)], verbose_name='Cantidad de IDs')),
                ('otro_tipo', models.CharField(blank=True, max_length=255, null=True, verbose_name='Otro, ¿Cúales?')),
                ('resaltar_apoyo', models.TextField(max_length=255, verbose_name='¿Qué resaltaría de este apoyo relacionado con el litigio de casos por parte de este cooperante o, alguna observación al respecto de este tipo de apoyo recibido?')),
                ('tipo_caso', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reporteAportes.tipocaso')),
            ],
            options={
                'verbose_name': 'Apoyo en Litigio de Casos',
                'verbose_name_plural': 'Apoyo en Litigio de Casos',
            },
        ),
    ]
