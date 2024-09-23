# Generated by Django 5.1.1 on 2024-09-22 22:40

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reporteAcercamientos', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='reporte',
            name='unique_reporteAcercamiento_per_user_periodo',
        ),
        migrations.AddConstraint(
            model_name='reporte',
            constraint=models.UniqueConstraint(fields=('tipo', 'usuario', 'periodo'), name='unique_reporteAcercamiento_per_user_periodo'),
        ),
    ]
