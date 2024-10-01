from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User
from reporteAcercamientos.models import Reporte


class Acuerdo(models.Model):
    nombre = models.CharField(max_length=100)
    identificacion = models.CharField(max_length=100, unique=True)
    pais = models.CharField(max_length=100)  # Nuevo atributo
    tipo_cooperacion = models.CharField(max_length=100)  # Nuevo atributo
    fecha_inicio = models.DateField()  # Nuevo atributo
    fecha_finalizacion = models.DateField()  # Nuevo atributo
    objetivo = models.TextField()  # Nuevo atributo

    class Meta:
        db_table = 'acuerdo'


class Cooperante(models.Model):
    nombre = models.CharField(max_length=100)
    nombre_corto = models.CharField(max_length=10)
    tipo = models.CharField(max_length=10)

    class Meta:
        db_table = 'cooperante'


class Operador(models.Model):
    nombre = models.CharField(max_length=100)
    nombre_corto = models.CharField(max_length=10)

    class Meta:
        db_table = 'operador'


class ProyectoPlan(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    cobertura_geografica = models.CharField(max_length=100)  # Nuevo atributo
    fecha_inicio = models.DateField()  # Nuevo atributo
    fecha_finalizacion = models.DateField()  # Nuevo atributo
    valor_aporte = models.DecimalField(max_digits=10, decimal_places=2)  # Nuevo atributo
    valor_contrapartida = models.DecimalField(max_digits=10, decimal_places=2)  # Nuevo atributo
    valor_total = models.DecimalField(max_digits=10, decimal_places=2)  # Nuevo atributo
    observaciones_valor_economico = models.TextField()  # Nuevo atributo

    class Meta:
        db_table = 'proyecto_plan'

class rol_linea_accion(models.Model):
    nombre = models.CharField(max_length=100)
    
    class Meta:
        db_table = 'rol_linea_accion'

class LineaAccion(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    responsable = models.CharField(max_length=100)  # Nuevo atributo
    rol = models.ForeignKey(rol_linea_accion, on_delete=models.CASCADE)  # Nuevo atributo
    nombre_supervisor = models.CharField(max_length=100)  # Nuevo atributo
    formularios = models.TextField()  # Nuevo atributo
    observaciones = models.TextField()  # Nuevo atributo

    class Meta:
        db_table = 'linea_accion'


class AcuerdoCooperacion(models.Model):
    acuerdo = models.ForeignKey(Acuerdo, on_delete=models.CASCADE)
    cooperante = models.ForeignKey(Cooperante, on_delete=models.CASCADE)
    operador = models.ForeignKey(Operador, on_delete=models.CASCADE)
    proyecto_plan = models.ForeignKey(ProyectoPlan, on_delete=models.CASCADE)
    lineas_accion = models.ForeignKey(LineaAccion, on_delete=models.CASCADE)

    class Meta:
        db_table = 'acuerdo_cooperacion'



class DatosCooperante(models.Model):
    
    reporte = models.OneToOneField(Reporte, on_delete=models.CASCADE)
    cooperante = models.CharField(max_length=100)
    identificacion = models.CharField(max_length=100)
    operador = models.CharField(max_length=100)
    proyecto_plan = models.CharField(max_length=100)
    linea_accion = models.CharField(max_length=100)
    rol = models.CharField(max_length=100)

    class Meta:
        db_table = 'datos_cooperante'





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
    nombre = models.CharField(max_length=100)
    linea_accion = models.ForeignKey(LineaAccion, related_name='resultados', on_delete=models.CASCADE)  # Relación muchos a uno

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

