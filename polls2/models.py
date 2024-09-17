from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class ReporteAvances(models.Model):
    PERIODOS = [
        ('1', 'Periodo 1'),
        ('2', 'Periodo 2'),
        ('3', 'Periodo 3'),
    ]
    
    ESTADO_DATOS_QUIEN_REPORTA = 0
    ESTADO_DATOS_COOPERANTE = 1
    ESTADO_LOGROS_AVANCES = 2
    ESTADO_FINALIZADO = 3
    
    ESTADOS = [(ESTADO_DATOS_QUIEN_REPORTA, 'Datos Quien Reporta'),
               (ESTADO_DATOS_COOPERANTE, 'Datos Cooperante'),
               (ESTADO_LOGROS_AVANCES, 'Logros y Avances')]
    
    fecha_elaboracion = models.DateField()
    periodo = models.CharField(max_length=1, choices=PERIODOS)
    desde = models.DateField()
    hasta = models.DateField()
    estado = models.IntegerField(choices=ESTADOS, default=ESTADO_DATOS_QUIEN_REPORTA)
    
    def __str__(self):
        return f"Informe {self.fecha_elaboracion} - {self.get_periodo_display()}"

class DatosQuienReporta(models.Model):
    reporte = models.OneToOneField(ReporteAvances, on_delete=models.CASCADE)
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
    
    
class DatosCooperante(models.Model):
    # Opciones para campos de selección
    IDENTIFICACION_CHOICES = [
        ('Acuerdo/Convenio', 'Acuerdo/Convenio'),
        ('Otro', 'Otro'),
    ]

    # Campos del formulario
    reporte = models.OneToOneField(ReporteAvances, on_delete=models.CASCADE)
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

    def __str__(self):
        return f"Reporte de {self.nombre_cooperante}"
    


class LogrosAvances(models.Model):
    # Campos para los resultados/productos esperados
    reporte = models.OneToOneField(ReporteAvances, on_delete=models.CASCADE)
    resultado_1 = models.CharField(max_length=255, default="Automático", verbose_name="Resultado 1")
    logros_avances_1 = models.CharField(max_length=50, verbose_name="Logros y/o avances 1")
    departamento_1 = models.CharField(max_length=255, verbose_name="Departamento 1")
    municipio_1 = models.CharField(max_length=255,  verbose_name="Municipio 1")
    adjunto_1 = models.FileField(upload_to='adjuntos/', blank=True, null=True, verbose_name="Adjunto 1")

    resultado_2 = models.CharField(max_length=255, default="Automático", verbose_name="Resultado 2")
    logros_avances_2 = models.CharField(max_length=50, blank=True, verbose_name="Logros y/o avances 2")
    departamento_2 = models.CharField(max_length=255, verbose_name="Departamento 2")
    municipio_2 = models.CharField(max_length=255, verbose_name="Municipio 2")
    adjunto_2 = models.FileField(upload_to='adjuntos/', blank=True, null=True, verbose_name="Adjunto 2")

    resultado_3 = models.CharField(max_length=255, default="Automático", verbose_name="Resultado 3")
    logros_avances_3 = models.CharField(max_length=50,  verbose_name="Logros y/o avances 3")
    departamento_3 = models.CharField(max_length=255, verbose_name="Departamento 3")
    municipio_3 = models.CharField(max_length=255, verbose_name="Municipio 3")
    adjunto_3 = models.FileField(upload_to='adjuntos/', blank=True, null=True, verbose_name="Adjunto 3")

    # Campos adicionales
    logros_significativos = models.CharField(max_length=50,  verbose_name="Logros significativos en este periodo")
    dificultades = models.CharField(max_length=50,  verbose_name="Dificultades presentadas")
    
    detalle_riesgo = models.CharField(max_length=50, blank=True, null=True, verbose_name="Detalle situación de riesgo", help_text="Solo si la respuesta es 'Sí'")

    observaciones_generales = models.CharField(max_length=50, blank=True, verbose_name="Observaciones o comentarios generales")

    def __str__(self):
        return f"Reporte de Logros y Avances"
    

class ApoyoEventos(models.Model):
    reporte = models.OneToOneField(ReporteAvances, on_delete=models.CASCADE)

    cantidad_eventos = models.PositiveIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(999)],
        verbose_name="Cantidad de eventos apoyados en el periodo reportado"
    )

    # Tipos de eventos (campos booleanos)
    eventos_seleccionados = models.CharField(max_length=200, blank=True)
    otros_eventos = models.CharField(max_length=255, blank=True, null=True, verbose_name="Cuales")

    objetivo_principal = models.TextField(max_length=120, verbose_name="Objetivo principal de los eventos apoyados")

    # Público objetivo (campos booleanos)
    publico_seleccionados = models.CharField(max_length=200, blank=True )
    otros_publicos = models.CharField(max_length=255, blank=True, null=True, verbose_name="Cuales")

    cantidad_participantes = models.PositiveIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(9999)],
        verbose_name="Cantidad total de participantes en los eventos en este periodo"
    )

    def __str__(self):
        return f"Apoyo a eventos - Reporte {self.reporte.id}"  # Ajusta según tu modelo Reporte
    
    

