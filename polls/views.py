from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from . models import *
from . forms import *
from django.shortcuts import render, get_object_or_404, redirect
from django.db import IntegrityError
from django.http import HttpResponse
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT



class ReporteAcercamientoCreateView(CreateView):
    model = ReporteAcercamiento
    form_class = ReporteAcercamientoForm
    template_name = 'polls/crear_reporte_acercamiento.html'
    def form_valid(self, form):
        response = super().form_valid(form)
        return redirect('crear_datos_quien_reporta', reporte_id=self.object.id)
    def get_success_url(self):
        return reverse_lazy('crear_datos_quien_reporta', kwargs={'reporte_id': self.object.id})

class DatosQuienReportaCreateView(CreateView):
    model = DatosQuienReporta
    form_class = DatosQuienReportaForm
    template_name = 'polls/crear_datos_quien_reporta.html'
    
    def dispatch(self, request, *args, **kwargs):
        reporte = get_object_or_404(ReporteAcercamiento, id=self.kwargs['reporte_id'])
       
        if reporte.estado == ReporteAcercamiento.ESTADO_ACERCAMIENTO:
            return redirect('crear_necesidades', reporte_id=reporte.id)
        elif reporte.estado == ReporteAcercamiento.ESTADO_NECESIDADES:
            return redirect('crear_necesidades', reporte_id=reporte.id)
        elif reporte.estado == ReporteAcercamiento.ESTADO_FINALIZADO:
            return redirect('listar_reportes_acercamiento')
        
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.reporte = get_object_or_404(ReporteAcercamiento, id=self.kwargs['reporte_id'])
        
        try:
            response = super().form_valid(form)
        except IntegrityError:
            form.add_error(None, "Error: El ID ya está en uso.")
            return self.form_invalid(form)
        
        # Actualizar el estado del reporte a 1 (Acercamientos)
        reporte = form.instance.reporte
        reporte.estado = ReporteAcercamiento.ESTADO_ACERCAMIENTO
        reporte.save()
        
        return redirect('crear_acercamiento', reporte_id=self.kwargs['reporte_id'])

    def get_success_url(self):
        return reverse_lazy('crear_acercamiento', kwargs={'reporte_id': self.kwargs['reporte_id']})
    
from django.forms import formset_factory    
from django.views.generic import FormView, UpdateView

class AcercamientoCreateView(FormView):
    template_name = 'polls/crear_acercamiento.html'
    form_class = AcercamientoForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reporte'] = get_object_or_404(ReporteAcercamiento, id=self.kwargs['reporte_id'])
        return context

    def dispatch(self, request, *args, **kwargs):
        reporte = get_object_or_404(ReporteAcercamiento, id=self.kwargs['reporte_id'])
        if reporte.estado == ReporteAcercamiento.ESTADO_DATOS:
            return redirect('crear_datos_quien_reporta', reporte_id=reporte.id)
        elif reporte.estado == ReporteAcercamiento.ESTADO_NECESIDADES:
            return redirect('crear_necesidades', reporte_id=reporte.id)
        
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        reporte = get_object_or_404(ReporteAcercamiento, id=self.kwargs['reporte_id'])
        entidades = self.request.POST.getlist('entidad')
        temas_perspectivas = self.request.POST.getlist('temas_perspectivas')

        for i in range(len(entidades)):
            AcercamientoCooperacion.objects.create(
                reporte=reporte,
                entidad=entidades[i],
                temas_perspectivas=temas_perspectivas[i]
            )

        # Actualizar el estado del reporte a 2 (Necesidades)
        reporte.estado = ReporteAcercamiento.ESTADO_NECESIDADES
        reporte.save()
        
        return redirect('crear_necesidades', reporte_id=self.kwargs['reporte_id'])

    def get_success_url(self):
        return reverse_lazy('crear_necesidades', kwargs={'reporte_id': self.kwargs['reporte_id']})

class NecesidadesCreateView(CreateView):
    model = NecesidadesCooperacion
    form_class = NecesidadesForm
    template_name = 'polls/crear_necesidades.html'

    def dispatch(self, request, *args, **kwargs):
        reporte = get_object_or_404(ReporteAcercamiento, id=self.kwargs['reporte_id'])
        if reporte.estado == ReporteAcercamiento.ESTADO_DATOS:
            return redirect('crear_datos_quien_reporta', reporte_id=reporte.id)
        elif reporte.estado == ReporteAcercamiento.ESTADO_ACERCAMIENTO:
            return redirect('crear_acercamiento', reporte_id=reporte.id)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.reporte = get_object_or_404(ReporteAcercamiento, id=self.kwargs['reporte_id'])
        response = super().form_valid(form)

        # Actualizar el estado del reporte a 3 (Finalizado)
        reporte = form.instance.reporte
        reporte.estado = ReporteAcercamiento.ESTADO_FINALIZADO
        reporte.save()

        return redirect('listar_reportes_acercamiento')

    def get_success_url(self):
        return reverse_lazy('listar_reportes_acercamiento')


from django.views.generic.list import ListView

class ReporteAcercamientoListView(ListView):
    model = ReporteAcercamiento
    template_name = 'polls/listar_reportes_acercamiento.html'
    context_object_name = 'reportes'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for reporte in context['reportes']:
            reporte.tiene_datos_quien_reporta = DatosQuienReporta.objects.filter(reporte=reporte).exists()
            reporte.tiene_acercamiento_cooperacion = AcercamientoCooperacion.objects.filter(reporte=reporte).exists()
            reporte.tiene_necesidades_cooperacion = NecesidadesCooperacion.objects.filter(reporte=reporte).exists()
        return context


from django.views.generic.detail import DetailView

class DatosQuienReportaDetailView(DetailView):
    model = DatosQuienReporta
    template_name = 'polls/ver_datos_quien_reporta.html'
    context_object_name = 'datos_quien_reporta'

    def get_object(self):
        # Aquí usamos `informe` en lugar de `reporte`
        reporte = get_object_or_404(ReporteAcercamiento, id=self.kwargs['reporte_id'])
        return get_object_or_404(DatosQuienReporta, reporte=reporte)


class AcercamientoDetailView(ListView):
    model = AcercamientoCooperacion
    template_name = 'polls/ver_acercamiento.html'
    context_object_name = 'acercamientos'  # Cambia el nombre a plural
    
    def get_queryset(self):
        # Aquí usamos `informe` en lugar de `reporte`
        reporte = get_object_or_404(ReporteAcercamiento, id=self.kwargs['reporte_id'])
        return AcercamientoCooperacion.objects.filter(reporte=reporte)

    


class NecesidadesDetailView(DetailView):
    model = NecesidadesCooperacion
    template_name = 'polls/ver_necesidades.html'
    context_object_name = 'necesidades'

    def get_object(self):
        # Aquí usamos `informe` en lugar de `reporte`
        reporte = get_object_or_404(ReporteAcercamiento, id=self.kwargs['reporte_id'])
        return get_object_or_404(NecesidadesCooperacion, reporte=reporte)






class DatosQuienReportaUpdateView(UpdateView):
    model = DatosQuienReporta
    form_class = DatosQuienReportaForm
    template_name = 'polls/editar_datos_quien_reporta.html'

    def get_object(self):
        reporte = get_object_or_404(ReporteAcercamiento, id=self.kwargs['reporte_id'])
        return get_object_or_404(DatosQuienReporta, reporte=reporte)

    def form_valid(self, form):
        try:
            response = super().form_valid(form)
        except IntegrityError:
            form.add_error(None, "Error: El ID ya está en uso.")
            return self.form_invalid(form)
        return redirect('ver_datos_quien_reporta', reporte_id=self.kwargs['reporte_id'])

    def get_success_url(self):
        return reverse_lazy('ver_datos_quien_reporta', kwargs={'reporte_id': self.kwargs['reporte_id']})
    
    

class AcercamientoUpdateView(UpdateView):
    model = AcercamientoCooperacion
    template_name = 'polls/editar_acercamiento.html'  # Ajusta la ruta del template
    form_class = AcercamientoForm

    def get_object(self, queryset=None):
        reporte = get_object_or_404(ReporteAcercamiento, id=self.kwargs['reporte_id'])
        return get_object_or_404(AcercamientoCooperacion, id=self.kwargs['pk'], reporte=reporte)

    def get_success_url(self):
        return reverse_lazy('crear_necesidades', kwargs={'reporte_id': self.kwargs['reporte_id']})
    


class NecesidadesCooperacionUpdateView(UpdateView):
    model = NecesidadesCooperacion
    form_class = NecesidadesForm
    template_name = 'polls/editar_necesidades.html'

    def get_object(self):
        reporte = get_object_or_404(ReporteAcercamiento, id=self.kwargs['reporte_id'])
        return get_object_or_404(NecesidadesCooperacion, reporte=reporte)

    def form_valid(self, form):
        try:
            response = super().form_valid(form)
        except IntegrityError:
            form.add_error(None, "Error: El ID ya está en uso.")
            return self.form_invalid(form)
        return redirect('ver_necesidades', reporte_id=self.kwargs['reporte_id'])

    def get_success_url(self):
        return reverse_lazy('ver_necesidades', kwargs={'reporte_id': self.kwargs['reporte_id']})
    
    
    
    
    
    
    
    
    
def generar_pdf_reporte(request, reporte_id):
    # Obtener el reporte
    reporte = get_object_or_404(ReporteAcercamiento, id=reporte_id)
    usuario = reporte.datosquienreporta
    reporte_fecha = reporte.fecha_elaboracion.strftime('%Y-%m-%d')
    reporte_hasta = reporte.hasta.strftime('%Y-%m-%d')
    reporte_desde = reporte.desde.strftime('%Y-%m-%d')
    acercamientos = reporte.acercamientocooperacion_set.all()
    # Crear una lista para almacenar los nombres de las entidades con índices
    entidades = [f'{i+1}. {acercamiento.entidad}' for i, acercamiento in enumerate(acercamientos)]
    temas_perspectivas = [f'{i+1}. {acercamiento.temas_perspectivas}' for i, acercamiento in enumerate(acercamientos)]
    
    # Unir las entidades en una cadena de texto, separadas por comas o saltos de línea
    entidades_texto = '\n'.join(entidades)
    temas_perspectivas_texto = '\n'.join(temas_perspectivas)
    
        
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
        [Paragraph('''Informar sobre los acercamientos y necesidades de cooperación internacional 
                      realizados e identificados en el periodo por la dependencia de la Unidad Administrativa Especial de Gestión de Restitución de Tierras.''', styles['ObjectiveContent'])],
        [Paragraph("2. DATOS DEL INFORME", styles['TableHeader'])],
        [Paragraph("Fecha de elaboración del reporte:", styles['TableContent']), Paragraph(reporte_fecha, styles['TableContent'])],
        [Paragraph("Periodo", styles['TableContent']), Paragraph(reporte.periodo, styles['TableContent'])],
        [Paragraph("Desde:", styles['RightAligned']), Paragraph(reporte_desde, styles['TableContent']), Paragraph("Hasta:", styles['RightAligned']), Paragraph(reporte_hasta, styles['TableContent'])],
        [Paragraph("3. DATOS DE QUIÉN REPORTA", styles['TableHeader'])],
        [Paragraph("Nombre y apellidos"), Paragraph(usuario.nombre_completo)],
        [Paragraph("Rol"), Paragraph(usuario.rol)],
        [Paragraph("Dependencia"), Paragraph(usuario.dependencia)],
        [Paragraph("Correo Electrónico"), Paragraph(usuario.correo_electronico)],
        [Paragraph("4. REPORTE DE ACERCAMIENTOS DE COOPERACIÓN INTERNACIONAL", styles['TableHeader'])],
        [Paragraph("¿Ha realizado algún tipo de acercamiento con alguna entidad de cooperación internacional en este periodo?"), Paragraph("Sí" if reporte.acercamientocooperacion_set.all() else "No")],
        [Paragraph("Mencione el nombre de la(s) entidad(es) con quien ha realizado los acercamientos:"), Paragraph( entidades_texto if entidades_texto else "N/A")],
        [Paragraph("Mencione aquí los temas y perspectivas de trabajo colaborativo: "), Paragraph(temas_perspectivas_texto if temas_perspectivas_texto else "N/A")],
        [Paragraph("5. NECESIDADES DE COOPERACIÓN INTERNACIONAL", styles['TableHeader'])],
        [Paragraph("¿Se identificaron necesidades de cooperación internacional en este periodo?"), Paragraph("Sí" if reporte.necesidadescooperacion.necesidad_identificado else "No")],
        [Paragraph("Mencione aquí las necesidades identificadas:"), Paragraph(reporte.necesidadescooperacion.necesidades_identificadas if reporte.necesidadescooperacion.necesidades_identificadas else "N/A")],
        [Paragraph("¿Se identificó algún cooperante en este periodo?"), Paragraph(reporte.necesidadescooperacion.cooperante if reporte.necesidadescooperacion.cooperante_identificado else "N/A")],
        [Paragraph("")]
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
        ('SPAN', (0, 15), (-1, 15)),
        ('SPAN', (1, 16), (-1, 16)),
        ('SPAN', (1, 17), (-1, 17)),
        ('SPAN', (1, 18), (-1, 18)),
        ('SPAN', (0, 19), (-1, 19)),
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey), 
        ('BACKGROUND', (0, 2), (-1, 2), colors.lightgrey),
        ('BACKGROUND', (0, 6), (-1, 6), colors.lightgrey),
        ('BACKGROUND', (0, 11), (-1, 11), colors.lightgrey),
        ('BACKGROUND', (0, 15), (-1, 15), colors.lightgrey),
        ('BACKGROUND', (0, 19), (-1, 19), colors.lightgrey),
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
    response['Content-Disposition'] = f'attachment; filename="reporte_{reporte.id}.pdf"'
    response.write(pdf)

    return response
