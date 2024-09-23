from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


""" class ApoyoEventos(models.Model):
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
    
    class Meta:
        db_table = "apoyo_eventos"

    def __str__(self):
        return f"Apoyo a eventos - Reporte {self.reporte.id}"  # Ajusta según tu modelo Reporte """