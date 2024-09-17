from polls2.models import ReporteAvances, DatosQuienReporta, DatosCooperante, LogrosAvances, ApoyoEventos
from  polls2.forms import ReporteAvancesForm, DatosQuienReportaForm, DatosCooperanteForm, LogrosAvancesForm, ApoyoEventosForm
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.db.utils import IntegrityError
from django.http import HttpResponse
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT



class ReporteAvancesCreateView(CreateView):
    model = ReporteAvances
    form_class = ReporteAvancesForm
    template_name = 'polls2/crear_reporte_avances.html'
    def form_valid(self, form):
        response = super().form_valid(form)
        return redirect('polls2:crear_datos_quien_reporta', reporte_id=self.object.id)
    def get_success_url(self):
        return reverse_lazy('polls2:crear_datos_quien_reporta', kwargs={'reporte_id': self.object.id})

class DatosQuienReportaCreateView(CreateView):
    model = DatosQuienReporta
    form_class = DatosQuienReportaForm
    template_name = 'polls2/crear_datos_quien_reporta.html'
    
    def dispatch(self, request, *args, **kwargs):
        reporte = get_object_or_404(ReporteAvances, id=self.kwargs['reporte_id'])
       
        if reporte.estado == ReporteAvances.ESTADO_DATOS_COOPERANTE:
            return redirect('polls2:crear_datos_cooperante', reporte_id=reporte.id)
        elif reporte.estado == ReporteAvances.ESTADO_LOGROS_AVANCES:
            return redirect('polls2:crear_logros_avances', reporte_id=reporte.id)
        elif reporte.estado == ReporteAvances.ESTADO_FINALIZADO:
            return redirect('polls2:index')
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        form.instance.reporte = get_object_or_404(ReporteAvances, id=self.kwargs['reporte_id'])
        
        try:
            response = super().form_valid(form)
        except IntegrityError:
            form.add_error(None, "Error: El ID ya está en uso.")
            return self.form_invalid(form)
        
        reporte = form.instance.reporte
        reporte.estado = ReporteAvances.ESTADO_DATOS_COOPERANTE
        reporte.save()
        
        return redirect('polls2:crear_datos_cooperante', reporte_id=self.kwargs['reporte_id'])

    def get_success_url(self):
        return reverse_lazy('polls2:crear_datos_cooperante', kwargs={'reporte_id': self.kwargs['reporte_id']})
    
class DatosCooperanteCreateView(CreateView):
    model = DatosCooperante
    form_class = DatosCooperanteForm
    template_name = 'polls2/crear_datos_cooperante.html'
    
    def dispatch(self, request, *args, **kwargs):
        reporte = get_object_or_404(ReporteAvances, id=self.kwargs['reporte_id'])
       
        if reporte.estado == ReporteAvances.ESTADO_DATOS_QUIEN_REPORTA:
            return redirect('polls2:crear_datos_quien_reporta', reporte_id=reporte.id)
        elif reporte.estado == ReporteAvances.ESTADO_LOGROS_AVANCES:
            return redirect('polls2:crear_logros_avances', reporte_id=reporte.id)
        elif reporte.estado == ReporteAvances.ESTADO_FINALIZADO:
            return redirect('polls2:index')
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        form.instance.reporte = get_object_or_404(ReporteAvances, id=self.kwargs['reporte_id'])
        response = super().form_valid(form)
        reporte = form.instance.reporte
        reporte.estado = ReporteAvances.ESTADO_LOGROS_AVANCES
        reporte.save()
        
        return redirect('polls2:crear_logros_avances', reporte_id=self.kwargs['reporte_id'])
    
    def get_success_url(self):
        return reverse_lazy('polls2:crear_logros_avances', kwargs={'reporte_id': self.kwargs['reporte_id']})
    

class LogrosAvancesCreateView(CreateView):
    model = LogrosAvances
    form_class = LogrosAvancesForm  # Usa form_class en lugar de fields
    template_name = 'polls2/crear_logros_avances.html'
    
    def dispatch(self, request, *args, **kwargs):
        reporte = get_object_or_404(ReporteAvances, id=self.kwargs['reporte_id'])
       
        if reporte.estado == ReporteAvances.ESTADO_DATOS_QUIEN_REPORTA:
            return redirect('polls2:crear_datos_quien_reporta', reporte_id=reporte.id)
        elif reporte.estado == ReporteAvances.ESTADO_DATOS_COOPERANTE:
            return redirect('polls2:crear_datos_cooperante', reporte_id=reporte.id)
        elif reporte.estado == ReporteAvances.ESTADO_FINALIZADO:
            return redirect('polls2:index')
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        form.instance.reporte = get_object_or_404(ReporteAvances, id=self.kwargs['reporte_id'])
        response = super().form_valid(form)
        reporte = form.instance.reporte
        reporte.estado = ReporteAvances.ESTADO_FINALIZADO
        reporte.save()
        
        return redirect('polls2:index')
    
    def get_success_url(self):
        return reverse_lazy('polls2:index')
    

class ApoyoEventosCreateView(CreateView):
    model = ApoyoEventos
    form_class = ApoyoEventosForm
    template_name = 'polls2/crear_apoyo_eventos.html'
    
    def form_valid(self, form):
        form.instance.reporte = get_object_or_404(ReporteAvances, id=self.kwargs['reporte_id'])
        response = super().form_valid(form)
        reporte = form.instance.reporte
        reporte.save()
        
        return redirect('polls2:crear_datos_quien_reporta', reporte_id=self.kwargs['reporte_id'])
    
    def get_success_url(self):
        return reverse_lazy('polls2:crear_datos_quien_reporta', kwargs={'reporte_id': self.kwargs['reporte_id']})


class ListarReportesView(ListView):
    model = ReporteAvances
    template_name = 'polls2/listar_reportes_avances.html'
    context_object_name = 'reportes'
    paginate_by = 10
    
    
# Vistas para ver la información de los informes

from django.views.generic.detail import DetailView

class DatosQuienReportaDetailView(DetailView):
    model = DatosQuienReporta
    template_name = 'polls2/ver_datos_quien_reporta.html'
    context_object_name = 'datos_quien_reporta'

    def get_object(self):
        
        reporte = get_object_or_404(ReporteAvances, id=self.kwargs['reporte_id'])
        return get_object_or_404(DatosQuienReporta, reporte=reporte)

    
class DatosCooperanteDetailView(DetailView):
    model = DatosCooperante
    template_name = 'polls2/ver_datos_cooperante.html'
    context_object_name = 'datos_cooperante'
    def get_object(self):
        reporte = get_object_or_404(ReporteAvances, id=self.kwargs['reporte_id'])
        return get_object_or_404(DatosCooperante, reporte=reporte)

class LogrosAvancesDetailView(DetailView):
    model = LogrosAvances
    template_name = 'polls2/ver_logros_avances.html'
    context_object_name = 'logros_avances'
    def get_object(self):
        reporte = get_object_or_404(ReporteAvances, id=self.kwargs['reporte_id'])
        return get_object_or_404(LogrosAvances, reporte=reporte)    
    
    
    
    

def generar_pdf_reporte_avances(request, reporte_id):
    # Obtener el reporte
    reporte = get_object_or_404(ReporteAvances, id=reporte_id)
    usuario = reporte.datosquienreporta
    cooperante = reporte.datoscooperante
    logros = reporte.logrosavances
    reporte_fecha = reporte.fecha_elaboracion.strftime('%Y-%m-%d')
    reporte_hasta = reporte.hasta.strftime('%Y-%m-%d')
    reporte_desde = reporte.desde.strftime('%Y-%m-%d')
    
    # Crear buffer
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=30, bottomMargin=30, leftMargin=40, rightMargin=40)
    
    # Definir estilos
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='CenteredHeading', parent=styles['Heading3'], alignment=TA_CENTER, fontSize=10))
    styles.add(ParagraphStyle(name='LeftAligned', parent=styles['Normal'], alignment=TA_LEFT, fontSize=10))
    styles.add(ParagraphStyle(name='TableHeader', fontSize=10, alignment=TA_CENTER, fontName='Helvetica-Bold'))
    styles.add(ParagraphStyle(name='TableContent', fontSize=9, alignment=TA_CENTER, fontName='Helvetica'))
    styles.add(ParagraphStyle(name='ObjectiveContent', alignment=TA_LEFT, fontSize=9))  # Estilo para el objetivo
    styles.add(ParagraphStyle(name='RightAligned', parent=styles['Normal'], alignment=TA_RIGHT, fontSize=9))  # Estilo alineado a la derecha
    styles.add(ParagraphStyle(name='Bold', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=9))  # Estilo para texto en negrita

    # Definir los datos de la tabla
    data = [
        [Paragraph("1. OBJETIVO", styles['TableHeader'])], 
        [Paragraph('''Informar los avances y actividades realizadas en el trimestre, del proyecto de cooperación que se ejecuta entre la Unidad Administrativa Especial de Gestión de Restitución de Tierras''', styles['ObjectiveContent'])],
        [Paragraph("2. DATOS DEL INFORME", styles['TableHeader'])],
        [Paragraph("Fecha de elaboración del reporte:", styles['TableContent']), Paragraph(reporte_fecha, styles['TableContent'])],
        [Paragraph("Periodo", styles['TableContent']), Paragraph(reporte.periodo, styles['TableContent'])],
        [Paragraph("Desde:", styles['RightAligned']), Paragraph(reporte_desde, styles['TableContent']), Paragraph("Hasta:", styles['RightAligned']), Paragraph(reporte_hasta, styles['TableContent'])],
        [Paragraph("3. DATOS DE QUIÉN REPORTA", styles['TableHeader'])],
        [Paragraph("Nombre y apellidos"), Paragraph(usuario.nombre_completo)],
        [Paragraph("Rol"), Paragraph(usuario.rol)],
        [Paragraph("Dependencia"), Paragraph(usuario.dependencia)],
        [Paragraph("Correo Electrónico"), Paragraph(usuario.correo_electronico)],
        [Paragraph("4. DATOS DEL COOPERANTE Y PROGRAMA, PROYECTO O PLAN", styles['TableHeader'])],
        [Paragraph("NOMBRE DEL COOPERANTE"), Paragraph(cooperante.nombre_cooperante)],
        [Paragraph("IDENTIFICACIÓN:"), Paragraph( cooperante.identificacion)],
        [Paragraph("NOMBRE DEL IMPLEMENTADOR U OPERADOR: "), Paragraph(cooperante.nombre_implementador)],
        [Paragraph("LÍNEA DE ACCIÓN / COMPONENTE: "), Paragraph(cooperante.linea_accion)],
        [Paragraph("ROL DE QUIEN REPORTA: "), Paragraph(cooperante.rol_quien_reporta)],
        [Paragraph("5. RESULTADOS, LOGROS Y/O AVANCES Y ADJUNTOS", styles['TableHeader'])],
        [Paragraph("Resultados/Productos Esperados"), Paragraph("Logros y/o avances"), Paragraph("Adjunto")],
        [Paragraph(logros.resultado_1), Paragraph(logros.logros_avances_1), Paragraph(logros.adjunto_1.url) ],
        [Paragraph(logros.resultado_2), Paragraph(logros.logros_avances_2), Paragraph(logros.adjunto_2.url) ],
        [Paragraph(logros.resultado_3), Paragraph(logros.logros_avances_3), Paragraph(logros.adjunto_3.url) ],
        [Paragraph("", styles['TableHeader'])],
        [Paragraph("¿Algún aspecto a resaltar como un logro significativo en este período?"), Paragraph(logros.logros_significativos)],
        [Paragraph("Comente en caso haya habido inconvenientes o dificultades presentadas en relación a este proyecto:"), Paragraph(logros.dificultades)],
        [Paragraph("¿Se ha presentado alguna situación que ponga en riesgo el buen relacionamiento con el cooperante?"), Paragraph('SI' if logros.detalle_riesgo else 'NO'), Paragraph("Explique detalladamente"), Paragraph(logros.detalle_riesgo)],
        [Paragraph("Observaciones y comentarios generales: otros aspectos respecto al desarrollo de este proyecto (sugerencias, inquietudes, etc.)"), Paragraph(logros.observaciones_generales)],
       
    ]
    
    

    # Definir estilo de la tabla
    table_style = TableStyle([
        ('SPAN', (0, 0), (-1, 0)), 
        ('SPAN', (0, 1), (-1, 1)),  
        ('SPAN', (0, 2), (-1, 2)),
        ('SPAN', (1, 3), (-1, 3)),  # Combinar solo las celdas de contenido en la fila "Fecha"
        ('SPAN', (1, 4), (-1, 4)),
        ('SPAN', (0, 6), (-1, 6)),
        ('SPAN', (1, 7), (-1, 7)),
        ('SPAN', (1, 8), (-1, 8)),
        ('SPAN', (1, 9), (-1, 9)),
        ('SPAN', (1, 10), (-1, 10)),
        ('SPAN', (0, 11), (-1, 11)),
        ('SPAN', (1, 12), (-1, 12)),
        ('SPAN', (1, 13), (-1, 13)),
        ('SPAN', (1, 14), (-1, 14)),
        ('SPAN', (1, 15), (-1, 15)),
        ('SPAN', (1, 16), (-1, 16)),
        ('SPAN', (0, 17), (-1, 17)),
        ('SPAN', (2, 18), (-1, 18)),
        ('SPAN', (2, 19), (-1, 19)),
        ('SPAN', (2, 20), (-1, 20)),
        ('SPAN', (2, 21), (-1, 21)),
        ('SPAN', (0, 22), (-1, 22)),
        ('SPAN', (1, 23), (-1, 23)),
        ('SPAN', (1, 24), (-1, 24)),
        ('SPAN', (1, 26), (-1, 26)),
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey), 
        ('BACKGROUND', (0, 2), (-1, 2), colors.lightgrey),
        ('BACKGROUND', (0, 6), (-1, 6), colors.lightgrey),
        ('BACKGROUND', (0, 11), (-1, 11), colors.lightgrey),
        ('BACKGROUND', (0, 17), (-1, 17), colors.lightgrey),
        ('BACKGROUND', (0, 22), (-1, 22), colors.lightgrey),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),  
        ('ALIGN', (0, 2), (-1, 2), 'CENTER'),  
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),  
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  
        ('FONTNAME', (0, 2), (-1, 2), 'Helvetica-Bold'),  
        ('FONTNAME', (0, 3), (-1, -1), 'Helvetica'), 
        ('FONTSIZE', (0, 0), (-1, -1), 9),  
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'), 
    ])

    
    table = Table(data, colWidths=[doc.width * 0.25, doc.width * 0.25, doc.width * 0.25, doc.width * 0.25])
    table.setStyle(table_style)
    # Construir el documento
    elements = [
        Paragraph("UNIDAD ADMINISTRATIVA ESPECIAL DE GESTIÓN DE RESTITUCIÓN DE TIERRAS DESPOJADAS", styles['CenteredHeading']),
        Spacer(1, 12),
        Paragraph("PROCESO: GESTIÓN DE TI", styles['CenteredHeading']),
        Spacer(1, 12),
        Paragraph("REPORTE DE COOPERACIÓN INTERNACIONAL", styles['CenteredHeading']),
        Spacer(1, 20),
        table,
        Spacer(1, 25),  # Espacio después de la tabla
        Paragraph("______________________________", styles['LeftAligned']),
        Paragraph("Firma", styles['LeftAligned']),
        Spacer(1, 12),
        Paragraph(usuario.nombre_completo.upper(), styles['Bold']),
        Paragraph(usuario.get_rol_display(), styles['LeftAligned']),
        Paragraph(usuario.dependencia, styles['LeftAligned'])]
    
    doc.build(elements)

    # Obtener el PDF
    pdf = buffer.getvalue()
    buffer.close()

    # Crear la respuesta HTTP con el PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="reporteDeAvances_{reporte.id}.pdf"'
    response.write(pdf)

    return response