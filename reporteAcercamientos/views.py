from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from . models import *
from . forms import *
from django.shortcuts import render, get_object_or_404, redirect
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseForbidden
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib.units import inch
from django.views import View
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import formset_factory
from django.views.generic import FormView, UpdateView




class ReporteAcercamientosCreateView(LoginRequiredMixin, CreateView):
    model = Reporte
    form_class = ReporteForm
    template_name = 'reporteAcercamientos/crear_reporte_acercamiento.html'

    def form_valid(self, form):
        # Asignar el usuario autenticado
        form.instance.usuario = self.request.user
        form.instance.tipo = 1  # Reporte de Acercamientos
        try:
            # Intentar guardar el formulario
            response = super().form_valid(form)
            return redirect('reporteAcercamientos:crear_datos_quien_reporta', reporte_id=self.object.id)
        
        except IntegrityError:
            # Mensaje flash de error si ya existe un reporte para ese período
          
            messages.error(self.request, 'Ya has creado un reporte para este período.')
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('reporteAcercamientos:crear_datos_quien_reporta', kwargs={'reporte_id': self.object.id})
    
class DatosQuienReportaCreateView( LoginRequiredMixin, CreateView):
    model = DatosQuienReporta
    form_class = DatosQuienReportaForm
    template_name = 'reporteAcercamientos/crear_datos_quien_reporta.html'
    
    def get_initial(self):
        # Aquí puedes establecer los valores iniciales del formulario
        initial = super().get_initial()
        initial['nombre_completo'] = self.request.user.first_name + ' ' + self.request.user.last_name
        initial['correo_electronico_sesion'] = self.request.user.email
      

        return initial
    
    def dispatch(self, request, *args, **kwargs):
        reporte = get_object_or_404(Reporte, id=self.kwargs['reporte_id'])
       
        if reporte.avance == 1 and reporte.tipo == 1 :
            return redirect('reporteAcercamientos:crear_necesidades', reporte_id=reporte.id)
        elif reporte.avance == 2 and reporte.tipo == 1 :
            return redirect('reporteAcercamientos:crear_necesidades', reporte_id=reporte.id)
        elif reporte.avance == 3 and reporte.tipo == 1 :
            return redirect('accounts:listar_reportes')
        
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.reporte = get_object_or_404(Reporte, id=self.kwargs['reporte_id'])
        
        try:
            response = super().form_valid(form)
        except IntegrityError:
            form.add_error(None, "Error: El ID ya está en uso.")
            return self.form_invalid(form)
        
        # Actualizar el estado del reporte a 1 (Acercamientos)
        reporte = form.instance.reporte
        reporte.avance = 1
        reporte.save()
        
        return redirect('reporteAcercamientos:crear_acercamiento', reporte_id=self.kwargs['reporte_id'])

    def get_success_url(self):
        return reverse_lazy('reporteAcercamientos:crear_acercamiento', kwargs={'reporte_id': self.kwargs['reporte_id']})
    
""" class AcercamientoCreateView(LoginRequiredMixin, FormView):
    template_name = 'reporteAcercamientos/crear_acercamiento.html'
    form_class = AcercamientoForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reporte'] = get_object_or_404(Reporte, id=self.kwargs['reporte_id'])
        return context

    def dispatch(self, request, *args, **kwargs):
        reporte = get_object_or_404(Reporte, id=self.kwargs['reporte_id'])
        if reporte.avance == 0 and reporte.tipo == 1:
            return redirect('reporteAcercamientos:crear_datos_quien_reporta', reporte_id=reporte.id)
        elif reporte.avance == 2 and reporte.tipo == 1:
            return redirect('reporteAcercamientos:crear_necesidades', reporte_id=reporte.id)
        
        elif reporte.avance == 3 and reporte.tipo == 1 :
            return redirect('accounts:listar_reportes')
        
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        reporte = get_object_or_404(Reporte, id=self.kwargs['reporte_id'])
        entidades = self.request.POST.getlist('entidad')
        temas_perspectivas = self.request.POST.getlist('temas_perspectivas')

        for i in range(len(entidades)):
            AcercamientoCooperacion.objects.create(
                reporte=reporte,
                entidad=entidades[i],
                temas_perspectivas=temas_perspectivas[i]
            )

        # Actualizar el estado del reporte a 2 (Necesidades)
        reporte.avance = 2
        reporte.save()
        
        return redirect('reporteAcercamientos:crear_necesidades', reporte_id=self.kwargs['reporte_id'])

    def get_success_url(self):
        return reverse_lazy('reporteAcercamientos:crear_necesidades', kwargs={'reporte_id': self.kwargs['reporte_id']}) """
        


        
def crear_acercamiento(request, reporte_id):
    reporte = get_object_or_404(Reporte, id=reporte_id)
    formset = AcercamientoFormSet()

    if request.method == 'POST':
        formset = AcercamientoFormSet(request.POST)
        if formset.is_valid():
            # Guardar cada formulario del formset
            for form in formset:
                if form.cleaned_data: # Verificar si el formulario tiene datos
                    acercamiento = form.save(commit=False)
                    acercamiento.reporte = reporte
                    acercamiento.save()
            reporte.avance = 2
            reporte.save()
            return redirect('reporteAcercamientos:crear_necesidades', reporte_id=reporte.id)
        else:
            print(formset.errors)
            print(formset.non_form_errors())

            return redirect('reporteAcercamientos:crear_acercamiento', reporte_id=reporte_id)

    return render(request, 'reporteAcercamientos/crear_acercamiento.html', {'formset': formset, 'reporte': reporte})

class NecesidadesCreateView(LoginRequiredMixin, CreateView):
    model = NecesidadesCooperacion
    form_class = NecesidadesForm
    template_name = 'reporteAcercamientos/crear_necesidades.html'

    def dispatch(self, request, *args, **kwargs):
        reporte = get_object_or_404(Reporte, id=self.kwargs['reporte_id'])
        if reporte.avance == 0 and reporte.tipo == 1:
            return redirect('reporteAcercamientos:crear_datos_quien_reporta', reporte_id=reporte.id)
        elif reporte.avance == 1 and reporte.tipo == 1:
            return redirect('reporteAcercamientos:crear_acercamiento', reporte_id=reporte.id)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.reporte = get_object_or_404(Reporte, id=self.kwargs['reporte_id'])
        response = super().form_valid(form)

        # Actualizar el estado del reporte a 3 (Finalizado)
        reporte = form.instance.reporte
        reporte.avance = 3
        reporte.save()

        return redirect('accounts:listar_reportes')

    def get_success_url(self):
        return reverse_lazy('accounts:listar_reportes')
    
class ReporteAcercamientoListView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        reportes = Reporte.objects.filter(tipo=1)
        return render(request, 'reporteAcercamientos/listar_reportes_acercamiento.html', {'reportes': reportes})


     
@login_required
def generar_pdf_reporte(request, reporte_id):
    # generar encabezado 
    # Logo (You'll need to replace 'path_to_your_logo.png' with the actual path)
    logo = Image('static/img/image.png', width=0.6*inch, height=1.2*inch) # Ajusta altura

    # Container for the 'Flowable' objects
    elements = []
    
    # Styles
    styles = getSampleStyleSheet()
    style_normal = styles['Normal']
    style_title = ParagraphStyle('CustomTitle', textColor=colors.black, parent=styles['Normal'], alignment=1, spaceAfter=6, fontSize=8)
    
    
    # Header data
    header_data = [
        [logo, Paragraph('UNIDAD ADMINISTRATIVA ESPECIAL DE GESTIÓN DE RESTITUCIÓN DE TIERRAS<br/>DESPOJADAS', style_title), Paragraph('PÁGINA: 1 DE 1', style_title)],
        ['', Paragraph('PROCESO: GESTIÓN DE COOPERACIÓN INTERNACIONAL', style_title), Paragraph('CÓDIGO: CP-FO-04', style_title)],
        ['', Paragraph('REPORTE DE ACERCAMIENTOS, ACCIONES Y APORTES DE COOPERACIÓN INTERNACIONAL', style_title), Paragraph('VERSIÓN: 3', style_title)],
    ]
    
    # Create the header table
    header_table = Table(header_data, colWidths=[0.7*inch, 5*inch, 1.3*inch]) # Ajusta rowHeights
    header_table.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.black),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ALIGN', (1,0), (1,-1), 'CENTER'),
        ('ALIGN', (2,0), (2,-1), 'RIGHT'),
        ('SPAN', (0,0), (0,2)),  # Combina las celdas de la primera columna
    ]))
    
    elements.append(header_table)



    # Obtener el reporte
    reporte = get_object_or_404(Reporte, id=reporte_id)
    
    # Verificar si el estado del reporte es FINALIZADO
    if reporte.avance != 3:
        # Devolver un mensaje de error o redirigir al usuario
        return HttpResponseForbidden("No se puede generar el PDF hasta que el reporte esté finalizado.")


    usuario = reporte.datosquienreporta
    reporte_fecha = reporte.fecha_elaboracion.strftime('%Y-%m-%d')
    reporte_hasta = reporte.hasta.strftime('%Y-%m-%d')
    reporte_desde = reporte.desde.strftime('%Y-%m-%d')
    acercamientos = reporte.acercamientos.all()
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
        [Paragraph('''Informar sobre los aportes realizados por el cooperante / proyecto, de cooperación internacional realizados en el 
                      periodo por el/la Responsable Técnico correspondiente, en función de apoyar los procesos de restitución de tierras y 
                      territorios.  ''', styles['ObjectiveContent'])],
        [Paragraph("2. DATOS DEL INFORME", styles['TableHeader'])],
        [Paragraph("Fecha de elaboración del reporte:", styles['TableContent']), Paragraph(reporte_fecha, styles['TableContent'])],
        [Paragraph("Periodo", styles['TableContent']), Paragraph(str(reporte.periodo), styles['TableContent'])],
        [Paragraph("Desde:", styles['RightAligned']), Paragraph(reporte_desde, styles['TableContent']), Paragraph("Hasta:", styles['RightAligned']), Paragraph(reporte_hasta, styles['TableContent'])],
        [Paragraph("3. DATOS DE QUIÉN REPORTA", styles['TableHeader'])],
        [Paragraph("Nombre y apellidos"), Paragraph(usuario.nombre_completo)],
        [Paragraph("Rol"), Paragraph(usuario.rol.nombre)],
        [Paragraph("Dependencia"), Paragraph(usuario.dependencia.nombre)],
        [Paragraph("Correo Electrónico"), Paragraph(usuario.correo_electronico_sesion)],
        [Paragraph("4. REPORTE DE ACERCAMIENTOS DE COOPERACIÓN INTERNACIONAL", styles['TableHeader'])],
        [Paragraph("¿Ha realizado algún tipo de acercamiento con alguna entidad de cooperación internacional en este periodo?"), Paragraph("Sí" if "Ninguna" not in entidades_texto else "No")],
        [Paragraph("Mencione el nombre de la(s) entidad(es) con quien ha realizado los acercamientos:"), Paragraph( entidades_texto if "Ninguna" not in entidades_texto else "N/A")],
        [Paragraph("Mencione aquí los temas y perspectivas de trabajo colaborativo: "), Paragraph(temas_perspectivas_texto if "Ninguno" not in temas_perspectivas_texto else "N/A")],
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
        header_table,  # Encabezado
        Paragraph("Clasificación de la Información: Pública ☒ Reservada ☐ Clasificada ☐ Fecha de aprobación: 12/03/2024 ", styles['Normal'] ),
        Spacer(1, 12),  # Espacio después del encabezado
        table,
        Spacer(1, 25),  # Espacio después de la tabla
        Paragraph("______________________________", styles['LeftAligned']),
        Paragraph("Firma", styles['LeftAligned']),
        Spacer(1, 12),
        Paragraph(usuario.nombre_completo.upper(), styles['Bold']),
        Paragraph(usuario.rol.nombre, styles['LeftAligned']),
        Paragraph(usuario.dependencia.nombre, styles['LeftAligned'])]
    
    doc.build(elements)

    # Obtener el PDF
    pdf = buffer.getvalue()
    buffer.close()

    # Crear la respuesta HTTP con el PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="reporte_{reporte.id}.pdf"'
    response.write(pdf)

    return response


class SaltarAcercamientoView(View):
    def get(self, request, *args, **kwargs):
        # Obtén el reporte con el ID
        reporte = get_object_or_404(Reporte, id=self.kwargs['reporte_id'])
        
        # Crear un registro de AcercamientoCooperacion con datos predeterminados o vacíos
        AcercamientoCooperacion.objects.create(
            reporte=reporte,
            entidad="Ninguna",  # Puedes usar algún valor predeterminado o "Ninguna"
            temas_perspectivas="Ninguno"
        )
        
        # Cambia el estado del reporte para marcar que se ha saltado el acercamiento
        reporte.avance = 2  # Define el nuevo estado en el modelo
        reporte.save()

        # Redirige al paso de necesidades
        return redirect('reporteAcercamientos:crear_necesidades', reporte_id=reporte.id)
    
@login_required

def editar_reporte(request, reporte_id):
    reporte = get_object_or_404(Reporte, id=reporte_id)

    return render(request, 'reporteAcercamientos/editar_reporte.html', {'reporte_id': reporte_id, 'reporte': reporte})


# Vistar para editar 

class DatosQuienReportaUpdateView(LoginRequiredMixin, UpdateView):
    model = DatosQuienReporta
    form_class = DatosQuienReportaForm
    template_name = 'reporteAcercamientos/editar_datos_quien_reporta.html'

    def get_object(self, queryset=None):
        # Buscamos el objeto DatosQuienReporta relacionado al reporte_id
        reporte_id = self.kwargs.get('reporte_id')
        return get_object_or_404(DatosQuienReporta, reporte_id=reporte_id)
    
    def get_success_url(self):
        return reverse_lazy('reporteAcercamientos:editar_reporte', kwargs={'reporte_id': self.object.reporte.id})
    

def editar_acercamiento(request, reporte_id):
    reporte = Reporte.objects.get(id=reporte_id)
    acercamientos = AcercamientoCooperacion.objects.filter(reporte=reporte)

    if request.method == 'POST':
        formset = AcercamientoFormSet(request.POST)

        if formset.is_valid():
            # Guardar formularios y eliminar si corresponde
            for form in formset:
                acercamiento = form.save(commit=False)
                acercamiento.reporte = reporte
                if form.cleaned_data.get('DELETE'):
                    acercamiento.delete()  # Elimina la instancia si se marca el checkbox
                else:
                    acercamiento.save()  # Guarda la instancia si no se marca el checkbox

            return redirect('accounts:listar_reportes')
        else:
            print(formset.errors)
    else:
        formset = AcercamientoFormSet(queryset=acercamientos)
        formset.extra = 0  # No agregar formularios adicionales

    context = {
        'formset': formset,
        'reporte': reporte,
    }
    return render(request, 'reporteAcercamientos/editar_acercamiento.html', context)
    


class NecesidadesUpdateView(LoginRequiredMixin, UpdateView):
    model = NecesidadesCooperacion
    form_class = NecesidadesForm
    template_name = 'reporteAcercamientos/editar_necesidades.html'

    def get_object(self, queryset=None):
        # Buscamos el objeto NecesidadesCooperacion relacionado al reporte_id
        reporte_id = self.kwargs.get('reporte_id')
        return get_object_or_404(NecesidadesCooperacion, reporte_id=reporte_id)
    
    def get_success_url(self):
        return reverse_lazy('reporteAcercamientos:editar_reporte', kwargs={'reporte_id': self.object.reporte.id})

    

