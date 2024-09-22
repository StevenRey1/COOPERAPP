from django.db import models
from django.contrib.auth.models import User


class ReporteAcercamiento(models.Model):
    PERIODOS = [
        (1, 'Periodo 1'),
        (2, 'Periodo 2'),
        (3, 'Periodo 3'),
    ]
    ESTADO_DATOS = 0
    ESTADO_ACERCAMIENTO = 1
    ESTADO_NECESIDADES = 2
    ESTADO_FINALIZADO = 3

    ESTADOS = [
        (ESTADO_DATOS, 'Datos Quien Informa'),
        (ESTADO_ACERCAMIENTO, 'Acercamiento de Cooperación'),
        (ESTADO_NECESIDADES, 'Necesidades de Cooperación'),
        (ESTADO_FINALIZADO, 'Finalizado'),
    ]
    
    fecha_elaboracion = models.DateField()
    periodo = models.IntegerField(choices=PERIODOS)
    desde = models.DateField()
    hasta = models.DateField()
    estado = models.IntegerField(choices=ESTADOS, default=ESTADO_DATOS)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    
    class Meta:
        db_table = "reporte_acercamiento"
        unique_together = ('usuario', 'periodo')
        constraints = [
            models.UniqueConstraint(fields=['usuario', 'periodo'], name='unique_reporteAcercamiento_per_user_periodo')
        ]

    def __str__(self):
        return f"Informe {self.fecha_elaboracion} - {self.get_periodo_display()}"
    
class Rol(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = "rol"
        verbose_name = "Rol"
        verbose_name_plural = "Roles"
        

    def __str__(self):
        return self.nombre

class Dependencia(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = "dependencia"
        verbose_name = "Dependencia"
        verbose_name_plural = "Dependencias"

    def __str__(self):
        return self.nombre

class DatosQuienReporta(models.Model):
    reporte = models.OneToOneField(ReporteAcercamiento, on_delete=models.CASCADE)
    nombre_completo = models.CharField(max_length=255)
    rol = models.ForeignKey(Rol, on_delete=models.SET_NULL, null=True)
    dependencia = models.ForeignKey(Dependencia, on_delete=models.SET_NULL, null=True)
    correo_electronico = models.EmailField(max_length=254)
    correo_electronico_institucional = models.EmailField(max_length=254, blank=True, null=True)
    
    class Meta:
        db_table = "datos_quien_reporta"
        verbose_name = "Datos Quien Reporta"
        verbose_name_plural = "Datos Quien Reporta"

    def __str__(self):
        return self.nombre_completo

    
class AcercamientoCooperacion(models.Model):
    reporte = models.ForeignKey(ReporteAcercamiento, on_delete=models.CASCADE)
    entidad = models.CharField(max_length=200, blank=True, null=True)
    temas_perspectivas = models.TextField(max_length=500, blank=True, null=True)
    
    class Meta:
        db_table = "acercamiento_cooperacion"
        verbose_name = "Acercamiento de Cooperación"
        verbose_name_plural = "Acercamientos de Cooperación"

    def __str__(self):
        return f"Acercamiento {self.id} del Reporte {self.reporte.id}"

class NecesidadesCooperacion(models.Model):
    reporte = models.OneToOneField(ReporteAcercamiento, on_delete=models.CASCADE)
    necesidad_identificado = models.BooleanField(default=False)
    necesidades_identificadas = models.TextField(blank=True, null=True)
    cooperante_identificado = models.BooleanField(default=False)
    cooperante = models.CharField(max_length=100, blank=True, null=True)
    
    class Meta:
        db_table = "necesidades_cooperacion"
        verbose_name = "Necesidades de Cooperación"
        verbose_name_plural = "Necesidades de Cooperación"

    def __str__(self):
        return f"Necesidad {self.id} del Reporte {self.reporte.id}"


