from django.db import models

class ReporteAcercamiento(models.Model):
    PERIODOS = [
        ('1', 'Periodo 1'),
        ('2', 'Periodo 2'),
        ('3', 'Periodo 3'),
    ]
    
    fecha_elaboracion = models.DateField()
    periodo = models.CharField(max_length=1, choices=PERIODOS)
    desde = models.DateField()
    hasta = models.DateField()

    def __str__(self):
        return f"Informe {self.fecha_elaboracion} - {self.get_periodo_display()}"

class DatosQuienReporta(models.Model):
    reporte = models.ForeignKey(ReporteAcercamiento, on_delete=models.CASCADE)
    nombre_completo = models.CharField(max_length=255)
    rol = models.CharField(max_length=100, choices=[
        ('Director de dependencia a nivel nacional', 'Director de dependencia a nivel nacional'),
        ('Director territorial', 'Director territorial'),
        ('Enlace de cooperación', 'Enlace de cooperación'),
    ])
    dependencia = models.CharField(max_length=100)
    correo_electronico = models.EmailField(max_length=254)
    correo_electronico_institucional = models.EmailField(max_length=254, blank=True, null=True)

    def __str__(self):
        return self.nombre_completo

class AcercamientoCooperacion(models.Model):
    reporte = models.ForeignKey(ReporteAcercamiento, on_delete=models.CASCADE)
    entidad = models.CharField(max_length=200)
    temas_perspectivas = models.TextField()

    def __str__(self):
        return f"Acercamiento {self.id} del Reporte {self.reporte.id}"

class NecesidadesCooperacion(models.Model):
    reporte = models.ForeignKey(ReporteAcercamiento, on_delete=models.CASCADE)
    necesidad_identificado = models.BooleanField(default=False)
    necesidades_identificadas = models.TextField(blank=True, null=True)
    cooperante_identificado = models.BooleanField(default=False)
    cooperante = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"Necesidad {self.id} del Reporte {self.reporte.id}"


