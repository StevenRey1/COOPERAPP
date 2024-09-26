# Generated by Django 5.1.1 on 2024-09-24 20:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('reporteAcercamientos', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Acuerdo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('identificacion', models.CharField(max_length=100, unique=True)),
                ('pais', models.CharField(max_length=100)),
                ('tipo_cooperacion', models.CharField(max_length=100)),
                ('fecha_inicio', models.DateField()),
                ('fecha_finalizacion', models.DateField()),
                ('objetivo', models.TextField()),
            ],
            options={
                'db_table': 'acuerdo',
            },
        ),
        migrations.CreateModel(
            name='Cooperante',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('nombre_corto', models.CharField(max_length=10)),
                ('tipo', models.CharField(max_length=10)),
            ],
            options={
                'db_table': 'cooperante',
            },
        ),
        migrations.CreateModel(
            name='Departamento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100, unique=True)),
            ],
            options={
                'verbose_name': 'Departamento',
                'verbose_name_plural': 'Departamentos',
                'db_table': 'departamento',
            },
        ),
        migrations.CreateModel(
            name='LineaAccion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100, unique=True)),
                ('responsable', models.CharField(max_length=100)),
                ('nombre_supervisor', models.CharField(max_length=100)),
                ('formularios', models.TextField()),
                ('observaciones', models.TextField()),
            ],
            options={
                'db_table': 'linea_accion',
            },
        ),
        migrations.CreateModel(
            name='Operador',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('nombre_corto', models.CharField(max_length=10)),
            ],
            options={
                'db_table': 'operador',
            },
        ),
        migrations.CreateModel(
            name='ProyectoPlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100, unique=True)),
                ('cobertura_geografica', models.CharField(max_length=100)),
                ('fecha_inicio', models.DateField()),
                ('fecha_finalizacion', models.DateField()),
                ('valor_aporte', models.DecimalField(decimal_places=2, max_digits=10)),
                ('valor_contrapartida', models.DecimalField(decimal_places=2, max_digits=10)),
                ('valor_total', models.DecimalField(decimal_places=2, max_digits=10)),
                ('observaciones_valor_economico', models.TextField()),
            ],
            options={
                'db_table': 'proyecto_plan',
            },
        ),
        migrations.CreateModel(
            name='rol_linea_accion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'rol_linea_accion',
            },
        ),
        migrations.CreateModel(
            name='DatosCooperante',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cooperante', models.CharField(max_length=100)),
                ('identificacion', models.CharField(max_length=100)),
                ('operador', models.CharField(max_length=100)),
                ('proyecto_plan', models.CharField(max_length=100)),
                ('linea_accion', models.CharField(max_length=100)),
                ('reporte', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='reporteAcercamientos.reporte')),
            ],
            options={
                'db_table': 'datos_cooperante',
            },
        ),
        migrations.CreateModel(
            name='LogrosAvances',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('riesgo_relacionamiento', models.BooleanField(default=False, verbose_name='¿Se presentó alguna situación de riesgo en el relacionamiento con el cooperante?')),
                ('logros_significativos', models.CharField(max_length=200, verbose_name='Logros significativos en este periodo')),
                ('dificultades', models.CharField(max_length=200, verbose_name='Dificultades presentadas')),
                ('detalle_riesgo', models.CharField(blank=True, help_text="Solo si la respuesta es 'Sí'", max_length=200, null=True, verbose_name='Detalle situación de riesgo')),
                ('observaciones_generales', models.CharField(max_length=200, verbose_name='Observaciones o comentarios generales')),
                ('reporte', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='reporteAcercamientos.reporte')),
            ],
            options={
                'db_table': 'logros_avances',
            },
        ),
        migrations.CreateModel(
            name='Municipio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100, unique=True)),
                ('departamento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reporteProgramas.departamento')),
            ],
            options={
                'verbose_name': 'Municipio',
                'verbose_name_plural': 'Municipios',
                'db_table': 'municipio',
            },
        ),
        migrations.CreateModel(
            name='AcuerdoCooperacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('acuerdo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reporteProgramas.acuerdo')),
                ('cooperante', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reporteProgramas.cooperante')),
                ('lineas_accion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reporteProgramas.lineaaccion')),
                ('operador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reporteProgramas.operador')),
                ('proyecto_plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reporteProgramas.proyectoplan')),
            ],
            options={
                'db_table': 'acuerdo_cooperacion',
            },
        ),
        migrations.CreateModel(
            name='Resultado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('linea_accion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='resultados', to='reporteProgramas.lineaaccion')),
            ],
            options={
                'verbose_name': 'Resultado',
                'verbose_name_plural': 'Resultados',
                'db_table': 'resultado',
            },
        ),
        migrations.CreateModel(
            name='Logro',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('logros_avances_texto', models.CharField(max_length=200, verbose_name='Logros y/o avances')),
                ('adjunto', models.FileField(upload_to='adjuntos/', verbose_name='Adjunto')),
                ('departamento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reporteProgramas.departamento')),
                ('logros_avances', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='logros', to='reporteProgramas.logrosavances')),
                ('municipio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reporteProgramas.municipio')),
                ('resultado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reporteProgramas.resultado')),
            ],
            options={
                'db_table': 'logro',
            },
        ),
        migrations.AddField(
            model_name='lineaaccion',
            name='rol',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reporteProgramas.rol_linea_accion'),
        ),
    ]
