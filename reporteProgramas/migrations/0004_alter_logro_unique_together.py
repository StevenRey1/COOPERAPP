# Generated by Django 5.1.1 on 2024-10-04 20:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reporteProgramas', '0003_alter_datoscooperante_cooperante_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='logro',
            unique_together={('resultado', 'logros_avances')},
        ),
    ]
