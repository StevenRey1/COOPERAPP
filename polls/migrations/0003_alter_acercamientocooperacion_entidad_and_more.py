# Generated by Django 5.1.1 on 2024-09-18 22:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_remove_reporteacercamiento_unique_reportea_per_user_periodo_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='acercamientocooperacion',
            name='entidad',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='acercamientocooperacion',
            name='temas_perspectivas',
            field=models.TextField(blank=True, max_length=500, null=True),
        ),
    ]
