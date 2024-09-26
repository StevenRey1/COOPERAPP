from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from reporteAcercamientos.models import Reporte

class Evento (models.Model):

    nombre = models.CharField(max_length=255, verbose_name="Nombre del evento")
    def __str__(self):
        return self.nombre
    
class PublicoObjetivo(models.Model):
    
    TIPO_PUBLICO = [
        ('Beneficiarios,solicitantes,comunidad en general', 'Beneficiarios,solicitantes,comunidad en general'),
        ('Funcionarios y/o contratistas de la URT', 'Funcionarios y/o contratistas de la URT'),
        ('Funcionarios y/o contratistas de otras entidades', 'Funcionarios y/o contratistas de otras entidades'),
    ]
    nombre = models.CharField(max_length=255,choices=TIPO_PUBLICO, verbose_name="Nombre del público objetivo")
    def __str__(self):
        return self.nombre

    
class ApoyoEventos(models.Model):

    reporte = models.OneToOneField(Reporte, on_delete=models.CASCADE, verbose_name="Reporte")
    cantidad_eventos = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(999)],
        verbose_name="Cantidad de eventos apoyados por este proyecto / cooperante en el período reportado"
    )
    eventos = models.ManyToManyField(Evento, verbose_name="Eventos apoyados")
    otros_eventos = models.BooleanField(default=False, verbose_name="Otros eventos")
    cuales_eventos = models.CharField(max_length=255, blank=True, null=True, verbose_name="Cuales")
    objetivo_principal = models.TextField(max_length=255, verbose_name="Objetivo principal de los eventos apoyados")
    publico_objetivo = models.ManyToManyField(PublicoObjetivo, verbose_name="Público objetivo")
    otro_publico = models.BooleanField(default=False, verbose_name="Otros públicos")
    cual_publico = models.CharField(max_length=255, blank=True, null=True, verbose_name="Cuales")
    cantidad_participantes = models.PositiveIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(9999)],
        verbose_name="Cantidad total de participantes en los eventos en este periodo"
    )


class ObjetivoViaje(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre
    
class ApoyoViajes(models.Model):
    
    cantidad_locales = models.PositiveIntegerField("Cantidad de viajes locales / regionales", default=0)
    cantidad_nacionales = models.PositiveIntegerField("Cantidad de viajes nacionales", default=0)
    cantidad_internacionales = models.PositiveIntegerField("Cantidad de viajes internacionales", default=0)
    suma_viajes = models.PositiveIntegerField("Cantidad total de viajes apoyados", blank=True, null=True)
    objetivo_viajes = models.ManyToManyField(ObjetivoViaje, blank=True)
    cuales_otros = models.CharField("Cuales (si selecciona otros)", max_length=255, blank=True, null=True)

    resaltado_apoyo = models.TextField("¿Qué resaltaría de este apoyo?", max_length=100, blank=True)

    def save(self, *args, **kwargs):
        self.suma_viajes = self.cantidad_locales + self.cantidad_nacionales + self.cantidad_internacionales
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Viajes Apoyados: {self.suma_viajes}"
    

class ApoyoTerritorios(models.Model):
    
    departamento = models.ForeignKey('reporteProgramas.Departamento', on_delete=models.CASCADE ,verbose_name="Departamento")
    municipio = models.ForeignKey('reporteProgramas.Municipio', on_delete=models.CASCADE, verbose_name="Municipio")
    vereda = models.CharField(max_length=255, verbose_name="Vereda / territorio / cabildo")
    apoyo_recibido = models.TextField(max_length=255, verbose_name="En qué consistió el apoyo recibido")
    tipo_visitas = models.TextField(max_length=255, verbose_name="Indique para qué tipo de visitas / actividades tuvo el acompañamiento o apoyo en cuanto al acceso")
    cantidad_visitas = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(999)], verbose_name="¿Para cuántas visitas obtuvo apoyo de este cooperante para el acceso a territorios en este periodo?")
    resaltar_apoyo = models.TextField(max_length=255, verbose_name="¿Qué resaltaría de este apoyo relacionado con acceso a los territorios por parte de este cooperante?")

    class Meta:
        verbose_name = "Apoyo a Territorios"
        verbose_name_plural = "Apoyo a Territorios"

    def __str__(self):
        return f"Apoyo a Territorios para el reporte {self.reporte}"
    

class TipoPersonal(models.Model):
    nombre = models.CharField(max_length=255, verbose_name="Tipo de Personal")

    def __str__(self):
        return self.nombre

class AreaProfesional(models.Model):
    nombre = models.CharField(max_length=255, verbose_name="Área Profesional")

    def __str__(self):
        return self.nombre

class ApoyoContratacion(models.Model):
    
    tipo_personal = models.ForeignKey(TipoPersonal, on_delete=models.CASCADE)
    cantidad_personas = models.PositiveIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(999)],
        verbose_name="Cantidad de personas"
    )
    tiempo_servicio = models.PositiveIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(99)],
        verbose_name="Tiempo de servicio en meses"
    )
    area_profesional = models.ForeignKey(AreaProfesional, on_delete=models.SET_NULL, null=True, blank=True)
    otro_tipo = models.CharField(max_length=255, blank=True, null=True, verbose_name="Otro, ¿Cúales?")
    objetivo_contratos = models.TextField(max_length=255, verbose_name="¿Cuál es el objetivo principal de los contratos del personal con el cual apoya este proyecto / cooperante?")
    resaltar_apoyo = models.TextField(max_length=255, verbose_name="¿Qué resaltaría de este apoyo relacionado con la contratación de personal por parte de este cooperante?")

    class Meta:
        verbose_name = "Apoyo de Contratación"
        verbose_name_plural = "Apoyo de Contratación"

    def __str__(self):
        return f"Apoyo de Contratación para el reporte {self.reporte}"
    

class TipoMaterial(models.Model):
    nombre = models.CharField(max_length=255, verbose_name="Tipo de Material")

    def __str__(self):
        return self.nombre

class ApoyoMaterial(models.Model):
    
    titulo_material = models.CharField(max_length=255, verbose_name="Título material")
    objetivo_principal = models.TextField(verbose_name="Objetivo principal")
    publico_destinatario = models.CharField(max_length=255, verbose_name="Público destinatario")
    tipo_material = models.ForeignKey(TipoMaterial, on_delete=models.SET_NULL, null=True, blank=True)
    cantidad_originales = models.PositiveIntegerField(verbose_name="Cantidad originales")
    cantidad_reproducciones = models.PositiveIntegerField(verbose_name="Cantidad reproducciones")
    resaltar_apoyo = models.TextField(max_length=255, verbose_name="Que resaltaría de este apoyo a través de la producción de materiales")

    class Meta:
        verbose_name = "Apoyo en Producción de Materiales"
        verbose_name_plural = "Apoyo en Producción de Materiales"

    def __str__(self):
        return f"Apoyo en materiales para el reporte {self.reporte}"


class TipoHerramienta(models.Model):
    nombre = models.CharField(max_length=255, verbose_name="Tipo de Herramienta / Equipo")

    def __str__(self):
        return self.nombre

class ApoyoHerramientas(models.Model):
    
    tipo_herramienta = models.ForeignKey(TipoHerramienta, on_delete=models.CASCADE)
    cantidad_recibida = models.PositiveIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(999)],
        verbose_name="Cantidad recibida"
    )
    descripcion = models.CharField(max_length=255, verbose_name="Descripción")
    observaciones = models.CharField(max_length=255, verbose_name="Observaciones / detalle")

    class Meta:
        verbose_name = "Apoyo de Herramientas"
        verbose_name_plural = "Apoyo de Herramientas"

    def __str__(self):
        return f"Apoyo de Herramientas para el reporte {self.reporte}"
    

class TipoCaso(models.Model):
    nombre = models.CharField(max_length=255, verbose_name="Tipo de Caso")

    def __str__(self):
        return self.nombre

class ApoyoLitigio(models.Model):
    
    tipo_caso = models.ForeignKey(TipoCaso, on_delete=models.CASCADE)
    nombre_caso = models.CharField(max_length=255, blank=True, verbose_name="Nombre de los casos")
    cantidad_ids = models.PositiveIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(999)],
        verbose_name="Cantidad de IDs"
    )
    otro_tipo = models.CharField(max_length=255, blank=True, null=True, verbose_name="Otro, ¿Cúales?")
    resaltar_apoyo = models.TextField(max_length=255, verbose_name="¿Qué resaltaría de este apoyo relacionado con el litigio de casos por parte de este cooperante o, alguna observación al respecto de este tipo de apoyo recibido?")

    class Meta:
        verbose_name = "Apoyo en Litigio de Casos"
        verbose_name_plural = "Apoyo en Litigio de Casos"

    def __str__(self):
        return f"Apoyo en Litigio para el reporte {self.reporte}"    
    
class TipoProyecto(models.Model):
    nombre = models.CharField(max_length=255, verbose_name="Tipo de Proyecto")

    def __str__(self):
        return self.nombre

class TipoApoyo(models.Model):
    nombre = models.CharField(max_length=255, verbose_name="Tipo de Apoyo")

    def __str__(self):
        return self.nombre

class ApoyoSeguridadAlimentaria(models.Model):
    
    tipo_proyecto = models.ForeignKey(TipoProyecto, on_delete=models.CASCADE)
    cantidad_proyectos = models.PositiveIntegerField(verbose_name="Cantidad proyectos")
    cantidad_familias = models.PositiveIntegerField(verbose_name="Cantidad familias beneficiarias")
    tipo_apoyo = models.ManyToManyField(TipoApoyo, verbose_name="Tipo de apoyo")
    otro_apoyo = models.CharField(max_length=255, blank=True, null=True, verbose_name="Cual")
    resaltar_apoyo = models.TextField(max_length=255, verbose_name="¿Qué resaltaría de este apoyo relacionado con seguridad alimentaria o proyectos productivos por parte de este proyecto / cooperante?")

    class Meta:
        verbose_name = "Apoyo a Seguridad Alimentaria"
        verbose_name_plural = "Apoyo a Seguridad Alimentaria"

    def __str__(self):
        return f"Apoyo a Seguridad Alimentaria para el reporte {self.reporte}"   
    
class ApoyoOrdenesJudiciales(models.Model):
    
    tipo_apoyo = models.TextField(max_length=255, verbose_name="Indique el tipo de apoyo que ha recibido de este proyecto / cooperante para el cumplimiento de órdenes judiciales")
    tipo_ordenes = models.TextField(max_length=255, verbose_name="¿Para qué tipo de órdenes judiciales recibió el apoyo?")
    cantidad_sentencias = models.PositiveIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(999)],
        verbose_name="Indique, si es posible, para cuántas sentencias ha contribuido el apoyo recibido de este proyecto / cooperante:",
        blank=True, null=True
    )
    cantidad_ordenes = models.PositiveIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(999)],
        verbose_name="Indique, si es posible, para cuántas órdenes ha contribuido el apoyo recibido de este proyecto / cooperante:",
        blank=True, null=True
    )

    class Meta:
        verbose_name = "Apoyo para el Cumplimiento de Órdenes Judiciales"
        verbose_name_plural = "Apoyo para el Cumplimiento de Órdenes Judiciales"

    def __str__(self):
        return f"Apoyo para Órdenes Judiciales del reporte {self.reporte}"
    

class AccionArchivo(models.Model):
    nombre = models.CharField(max_length=255, verbose_name="Acción")

    def __str__(self):
        return self.nombre

class ApoyoArchivoHistorico(models.Model):
    
    acciones = models.ManyToManyField(AccionArchivo, verbose_name="Indique el tipo de acciones para las cuales ha recibido apoyo")
    cuales_acciones = models.CharField(max_length=255, blank=True, null=True, verbose_name="Cuales")
    comentarios = models.TextField(max_length=255, verbose_name="¿Qué resaltaría o que comentarios tiene sobre el apoyo recibido para la gestión documental?")

    class Meta:
        verbose_name = "Apoyo en Gestión del Archivo Histórico"
        verbose_name_plural = "Apoyo en Gestión del Archivo Histórico"

    def __str__(self):
        return f"Apoyo en Gestión del Archivo Histórico para el reporte {self.reporte}"
    

class OtrosApoyos(models.Model):
    
    descripcion = models.TextField(max_length=255, verbose_name="Realice una breve descripción de algún otro tipo de apoyo recibido por este proyecto / cooperante, si no pudo registrarlo en las anteriores preguntas:")

    class Meta:
        verbose_name = "Otros Apoyos"
        verbose_name_plural = "Otros Apoyos"

    def __str__(self):
        return f"Otros Apoyos para el reporte {self.reporte}"
    
class EstimacionEconomica(models.Model):
    
    valor_economico = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True, verbose_name="Si tiene un valor económico del presupuesto destinado desde el proyecto / cooperante para el aporte a su dependencia durante este periodo, por favor indíquelo:")
    moneda = models.CharField(max_length=100, verbose_name="Moneda", blank=True, null=True)
    obtencion_valor = models.TextField(blank=True, null=True, verbose_name="Indique por favor como obtuvo este valor reportado: (Ej: presupuesto aprobado por cooperante, presupuesto ejecutado, costo de personal o materiales, etc.), estimativo según costos de lo entregado, cotizaciones, etc.")

    class Meta:
        verbose_name = "Estimación Económica"
        verbose_name_plural = "Estimaciones Económicas"

    def __str__(self):
        return f"Estimación Económica para el reporte {self.reporte}"    