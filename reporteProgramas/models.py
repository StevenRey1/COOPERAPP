from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User
from reporteAcercamientos.models import Reporte



class DatosCooperante(models.Model):
    # Opciones para campos de selección
    IDENTIFICACION_CHOICES = [
        ('Acuerdo/Convenio', 'Acuerdo/Convenio'),
        ('Otro', 'Otro'),
    ]

    # Campos del formulario
    reporte = models.OneToOneField(Reporte, on_delete=models.CASCADE)
    nombre_cooperante = models.CharField(max_length=255, verbose_name="Nombre del cooperante")
    cual_cooperante = models.CharField(max_length=255, blank=True, null=True, verbose_name="Cual (cooperante)")
    
    identificacion = models.CharField(max_length=50, verbose_name="Identificación")
    
    nombre_implementador = models.CharField(max_length=255, default='Automático', verbose_name="Nombre del implementador u operador")

    programa_proyecto_plan = models.CharField(max_length=255, verbose_name="Programa/proyecto o plan")
    cual_programa = models.CharField(max_length=255, blank=True, null=True, verbose_name="Cual (programa/proyecto o plan)")

    linea_accion = models.CharField(max_length=255, verbose_name="Línea de acción/componente")
    cual_linea_accion = models.CharField(max_length=255, blank=True, null=True, verbose_name="Cual (línea de acción)")

    rol_quien_reporta = models.CharField(max_length=255, verbose_name="Rol de quien reporta")
    cual_rol_reporta = models.CharField(max_length=255, blank=True, null=True, verbose_name="Cual (rol quien reporta)")
    
    class Meta:
        db_table = "datos_cooperante"
        
    def __str__(self):
        return f"Reporte de {self.nombre_cooperante}"
    




class Departamento(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = "departamento"
        verbose_name = "Departamento"
        verbose_name_plural = "Departamentos"

    def __str__(self):
        return self.nombre

class Municipio(models.Model):
    nombre = models.CharField(max_length=100, unique=True )
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE)

    class Meta:
        db_table = "municipio"
        verbose_name = "Municipio"
        verbose_name_plural = "Municipios"

    def __str__(self):
        return self.nombre

class Resultado(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = "resultado"
        verbose_name = "Resultado"
        verbose_name_plural = "Resultados"

    def __str__(self):
        return self.nombre

class LogrosAvances(models.Model):
    # Relación con el reporte
    reporte = models.OneToOneField(Reporte, on_delete=models.CASCADE)

    # Campos adicionales
    riesgo_relacionamiento = models.BooleanField(default=False,verbose_name="¿Se presentó alguna situación de riesgo en el relacionamiento con el cooperante?")
    logros_significativos = models.CharField(max_length=200, verbose_name="Logros significativos en este periodo")
    dificultades = models.CharField(max_length=200,  verbose_name="Dificultades presentadas")
    detalle_riesgo = models.CharField(max_length=200, blank=True, null=True, verbose_name="Detalle situación de riesgo", help_text="Solo si la respuesta es 'Sí'")
    observaciones_generales = models.CharField(max_length=200, verbose_name="Observaciones o comentarios generales")

    class Meta:
        db_table = "logros_avances"

    def __str__(self):
        return "Reporte de Logros y Avances"

class Logro(models.Model):
    logros_avances = models.ForeignKey(LogrosAvances, on_delete=models.CASCADE, related_name='logros')
    resultado = models.ForeignKey(Resultado, on_delete=models.CASCADE)
    logros_avances_texto = models.CharField(max_length=200, verbose_name="Logros y/o avances")
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE)
    municipio = models.ForeignKey(Municipio, on_delete=models.CASCADE)
    adjunto = models.FileField(upload_to='adjuntos/', verbose_name="Adjunto")

    class Meta:
        db_table = "logro"

    def __str__(self):
        return f"Logro para {self.resultado.nombre}"

