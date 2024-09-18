# Generated by Django 5.1.1 on 2024-09-18 18:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ReporteAcercamiento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_elaboracion', models.DateField()),
                ('periodo', models.CharField(choices=[('1', 'Periodo 1'), ('2', 'Periodo 2'), ('3', 'Periodo 3')], max_length=1)),
                ('desde', models.DateField()),
                ('hasta', models.DateField()),
                ('estado', models.IntegerField(choices=[(0, 'Datos Quien Informa'), (1, 'Acercamiento de Cooperación'), (2, 'Necesidades de Cooperación'), (3, 'Finalizado')], default=0)),
            ],
        ),
        migrations.CreateModel(
            name='NecesidadesCooperacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('necesidad_identificado', models.BooleanField(default=False)),
                ('necesidades_identificadas', models.TextField(blank=True, null=True)),
                ('cooperante_identificado', models.BooleanField(default=False)),
                ('cooperante', models.CharField(blank=True, max_length=100, null=True)),
                ('reporte', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='polls.reporteacercamiento')),
            ],
        ),
        migrations.CreateModel(
            name='DatosQuienReporta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_completo', models.CharField(max_length=255)),
                ('rol', models.CharField(choices=[('Director de dependencia a nivel nacional', 'Director de dependencia a nivel nacional'), ('Director territorial', 'Director territorial'), ('Enlace de cooperación', 'Enlace de cooperación')], max_length=100)),
                ('dependencia', models.CharField(max_length=100)),
                ('correo_electronico', models.EmailField(max_length=254)),
                ('correo_electronico_institucional', models.EmailField(blank=True, max_length=254, null=True)),
                ('reporte', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='polls.reporteacercamiento')),
            ],
        ),
        migrations.CreateModel(
            name='AcercamientoCooperacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('entidad', models.CharField(max_length=200)),
                ('temas_perspectivas', models.TextField()),
                ('reporte', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.reporteacercamiento')),
            ],
        ),
    ]
