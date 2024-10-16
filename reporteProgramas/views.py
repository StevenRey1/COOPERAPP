from reporteProgramas.models import  Logro, Cooperante, AcuerdoCooperacion, Acuerdo, Operador, LineaAccion, LogrosAvances
from  reporteProgramas.forms import   LogrosAvancesForm, LogroFormSet, DatosCooperanteForm
from django.views.generic.edit import CreateView, UpdateView
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.urls import reverse_lazy
from django.db.utils import IntegrityError
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from reporteAcercamientos.models import Reporte, DatosQuienReporta
from reporteAcercamientos.forms import ReporteForm, DatosQuienReportaForm
from reporteProgramas.models import Resultado, DatosCooperante, Municipio



class ReporteProgramaCreateView(LoginRequiredMixin,CreateView):
    model = Reporte
    form_class = ReporteForm
    template_name = 'reporteProgramas/crear_reporte_avances.html'
    def form_valid(self, form):
        form.instance.usuario = self.request.user
        form.instance.tipo = 2
        try:
            # Intentar guardar el formulario
            response = super().form_valid(form)
            return redirect('reporteProgramas:crear_datos_quien_reporta', reporte_id=self.object.id)
        except IntegrityError:
            # Mensaje flash de error si ya existe un reporte para ese período
            messages.error(self.request, 'Ya has creado un reporte para este período.')
            return self.form_invalid(form)
    def get_success_url(self):
        return reverse_lazy('reporteProgramas:crear_datos_quien_reporta', kwargs={'reporte_id': self.object.id})


class DatosQuienReportaCreateView(LoginRequiredMixin,CreateView):
    model = DatosQuienReporta
    form_class = DatosQuienReportaForm
    template_name = 'reporteProgramas/crear_datos_quien_reporta.html'
    
    def get_initial(self):
        # Aquí puedes establecer los valores iniciales del formulario
        initial = super().get_initial()
        initial['nombre_completo'] = self.request.user.first_name + ' ' + self.request.user.last_name
        initial['correo_electronico_sesion'] = self.request.user.email
        return initial

    def form_valid(self, form):
        form.instance.reporte = get_object_or_404(Reporte, id=self.kwargs['reporte_id'])
        
        try:
            response = super().form_valid(form)
        except IntegrityError:
            form.add_error(None, "Error: El ID ya está en uso.")
            return self.form_invalid(form)
        
        reporte = form.instance.reporte
        reporte.avance = 1
        reporte.save()
        
        return redirect('reporteProgramas:crear_datos_cooperante', reporte_id=self.kwargs['reporte_id'])

    def get_success_url(self):
        return reverse_lazy('reporteProgramas:crear_datos_cooperante', kwargs={'reporte_id': self.kwargs['reporte_id']})
 
class DatosQuienReportaUpdateView(LoginRequiredMixin, UpdateView):
    model = DatosQuienReporta
    form_class = DatosQuienReportaForm
    template_name = 'reporteProgramas/editar_datos_quien_reporta.html'

    def get_object(self, queryset=None):
        # Buscamos el objeto DatosQuienReporta relacionado al reporte_id
        reporte_id = self.kwargs.get('reporte_id')
        return get_object_or_404(DatosQuienReporta, reporte_id=reporte_id)
    
    def get_success_url(self):
        return reverse_lazy('reporteAportes:editar_reporte', kwargs={'reporte_id': self.object.reporte.id}) 
    
@login_required
def obtener_cooperantes(request):
    if request.method == 'GET':
        cooperantes = list(Cooperante.objects.values('id', 'nombre'))
        return JsonResponse({'cooperantes': cooperantes})

@login_required
def obtener_identificaciones_por_cooperante(request, cooperante_id):
    if request.method == 'GET':
       
        # Filtrar las identificaciones según el cooperante seleccionado
        acuerdos = AcuerdoCooperacion.objects.filter(cooperante=cooperante_id)
        

      
        identificaciones = [
            {'id': acuerdo.acuerdo.id, 'identificacion': acuerdo.acuerdo.identificacion}
            for acuerdo in acuerdos
        ]

        
        return JsonResponse({'identificaciones': identificaciones})

@login_required    
def obtener_operadores_por_identificacion(request, identificacion_id):
    if request.method == 'GET':
        # Filtrar los acuerdos que coinciden con la identificación seleccionada
        acuerdos = Acuerdo.objects.filter(id=identificacion_id).distinct()
    
        print(identificacion_id)
        
        # Obtener los operadores relacionados a esos acuerdos a través del modelo AcuerdoCooperacion
        acuerdos_cooperacion = AcuerdoCooperacion.objects.filter(acuerdo__in=acuerdos).distinct()

        # Extraer los operadores de los acuerdos de cooperación
        operadores = [acuerdo_cooperacion.operador for acuerdo_cooperacion in acuerdos_cooperacion]

        # Construir la respuesta en formato JSON
        operadores_data = [
            {'id': operador.id, 'nombre': operador.nombre}
            for operador in operadores
        ]
        
        return JsonResponse({'operadores': operadores_data})

@login_required   
def obtener_proyectos_plan(request, cooperante_id, identificacion_id, operador_id):
    if request.method == 'GET':
        # Filtrar acuerdos por la identificación seleccionada
        acuerdos = Acuerdo.objects.filter(id=identificacion_id).distinct()

        # Filtrar los acuerdos de cooperación que coinciden con el cooperante, identificación y operador
        acuerdos_cooperacion = AcuerdoCooperacion.objects.filter(
            acuerdo__in=acuerdos,
            cooperante_id=cooperante_id,
            operador_id=operador_id
        ).distinct()

        # Extraer los proyectos plan relacionados a los acuerdos de cooperación
        proyectos_plan = [acuerdo_cooperacion.proyecto_plan for acuerdo_cooperacion in acuerdos_cooperacion]

        # Construir la respuesta en formato JSON
        proyectos_plan_data = [
            {'id': proyecto_plan.id, 'nombre': proyecto_plan.nombre}
            for proyecto_plan in proyectos_plan
        ]
        
        return JsonResponse({'proyectos_plan': proyectos_plan_data})

@login_required
def obtener_lineas_accion(request, cooperante_id, identificacion_id, operador_id, proyecto_plan_id):
    if request.method == 'GET':
        # Filtrar acuerdos por la identificación seleccionada
        acuerdos = Acuerdo.objects.filter(id=identificacion_id).distinct()

        # Filtrar los acuerdos de cooperación que coinciden con el cooperante, identificación y operador
        acuerdos_cooperacion = AcuerdoCooperacion.objects.filter(
            acuerdo__in=acuerdos,
            cooperante_id=cooperante_id,
            operador_id=operador_id,
            proyecto_plan_id=proyecto_plan_id
        ).distinct()

        # Obtener las líneas de acción relacionadas a los acuerdos de cooperación
        lineas_accion_data = []
        for acuerdo_cooperacion in acuerdos_cooperacion:
            # Como lineas_accion es un ForeignKey, podemos acceder directamente
            linea_accion = acuerdo_cooperacion.lineas_accion
            lineas_accion_data.append({
                'id': linea_accion.id,
                'nombre': linea_accion.nombre
            })

        # Retornar la respuesta en formato JSON
        return JsonResponse({'lineas_accion': lineas_accion_data})

# DATOS COOPERANTE
@login_required
def crear_datos_cooperante(request,reporte_id):

    reporte = get_object_or_404(Reporte, id=reporte_id)
    if request.method == 'POST':
        form = DatosCooperanteForm(request.POST)
        if form.is_valid():
            datos_cooperante = form.save(commit=False)
            datos_cooperante.reporte = reporte
            datos_cooperante.save()
            reporte.avance = 2
            reporte.save()
            return redirect('reporteProgramas:crear_logros_avances', reporte_id=reporte_id, linea_accion_id=datos_cooperante.linea_accion.id)
    else:
        form = DatosCooperanteForm()
    return render(request, 'reporteProgramas/crear_datos_cooperante.html', {'form': form, 'reporte': reporte})

@login_required
def editar_datos_cooperante(request, reporte_id):
    reporte = get_object_or_404(Reporte, id=reporte_id)
    datos_cooperante = get_object_or_404(DatosCooperante, reporte=reporte_id)
    if request.method == 'POST':
        form = DatosCooperanteForm(request.POST, instance=datos_cooperante)
        if form.is_valid():
            form.save()
            return redirect('accounts:listar_reportes')
    else:
        form = DatosCooperanteForm(instance=datos_cooperante)
    return render(request, 'reporteProgramas/editar_datos_cooperante.html', {'form': form, 'reporte': reporte})

# REPORTE LOGROS Y AVANCES
@login_required
def crear_reporte_logros(request, reporte_id, linea_accion_id):
    # Obtén el reporte basado en el ID
    reporte = get_object_or_404(Reporte, id=reporte_id)


    # Filtrar resultados según la línea de acción
    resultados = Resultado.objects.filter(linea_accion=linea_accion_id)
    extra_forms = resultados.count()

    if request.method == 'POST':
        print(request.POST)
        form_logros_avances = LogrosAvancesForm(request.POST)
        formset_logro = LogroFormSet(request.POST, request.FILES )

        if form_logros_avances.is_valid() and formset_logro.is_valid():
             logros_avances = form_logros_avances.save(commit=False)
             logros_avances.reporte = reporte
             logros_avances.save()
             
             formset_logro.instance = logros_avances
             formset_logro.save()
     
             reporte.avance = 3  
             reporte.save()

             return redirect('reporteAportes:crear_apoyo_eventos', reporte_id=reporte_id)

        else:
            print("Form errors:", form_logros_avances.errors)       
            print("Formset errors:", formset_logro.errors)

    else:
        form_logros_avances = LogrosAvancesForm()
        formset_logro = LogroFormSet(queryset=Logro.objects.none(), initial=[{'resultado': resultado.id} for resultado in resultados])
        formset_logro.extra = extra_forms
        

    context = {
        'form_logros_avances': form_logros_avances,
        'formset_logro': formset_logro,
        'reporte': reporte,
        'resultados': resultados,
    }

    return render(request, 'reporteProgramas/crear_logros_avances.html', context)

@login_required
def editar_reporte_logros(request, reporte_id):
    reporte = get_object_or_404(Reporte, id=reporte_id)
    logros_avances = get_object_or_404(LogrosAvances, reporte=reporte_id)
    resultados = Resultado.objects.filter(linea_accion=logros_avances.reporte.datoscooperante.linea_accion)
    urls = [logro.adjunto.url for logro in logros_avances.logros.all()]
 

    if request.method == 'POST':
        form_logros_avances = LogrosAvancesForm(request.POST, instance=logros_avances)
        formset_logro = LogroFormSet(request.POST, request.FILES, instance=logros_avances)

        if form_logros_avances.is_valid() and formset_logro.is_valid():
            form_logros_avances.save()
            formset_logro.save()
            return redirect('accounts:listar_reportes')
    else:
        form_logros_avances = LogrosAvancesForm(instance=logros_avances)
        # No pasar queryset ni initial al editar
        formset_logro = LogroFormSet(instance=logros_avances)  
        formset_logro.extra = 0

    context = {
        'form_logros_avances': form_logros_avances,
        'formset_logro': formset_logro,
        'reporte': reporte,
        'resultados': resultados,
        'urls': urls
    }

    return render(request, 'reporteProgramas/editar_logros_avances.html', context)
   

@login_required
def get_municipios(request, departamento_id):
    municipios = Municipio.objects.filter(departamento_id=departamento_id).values('id', 'nombre')
    return JsonResponse({'municipios': list(municipios)})

    
@login_required
def generar_pdf_reporte_avances(request, reporte_id):
    # Obtener el reporte
    reporte = get_object_or_404(Reporte, id=reporte_id)
    usuario = get_object_or_404(DatosQuienReporta,reporte=reporte_id)
    acuerdo = get_object_or_404(Acuerdo, id=reporte.datoscooperante.identificacion.id)
    cooperante = get_object_or_404(Cooperante, id=reporte.datoscooperante.cooperante.id)
    operante = get_object_or_404(Operador, id=reporte.datoscooperante.operador.id)
    linea_accion = get_object_or_404(LineaAccion, id = reporte.datoscooperante.linea_accion.id) 
    
    logros_avances = reporte.logrosavances  # Acceder al objeto LogrosAvances
    reporte_fecha = reporte.fecha_elaboracion.strftime('%Y-%m-%d')
    reporte_hasta = reporte.hasta.strftime('%Y-%m-%d')
    reporte_desde = reporte.desde.strftime('%Y-%m-%d')
    
    # Crear buffer
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=30, bottomMargin=30, leftMargin=40, rightMargin=40)
    logo = Image('static/img/image.png', width=0.6*inch, height=1.2*inch) # Ajusta altura
    
    styles = getSampleStyleSheet()
    style_title = ParagraphStyle('CustomTitle', textColor=colors.black, parent=styles['Normal'], alignment=1, spaceAfter=6, fontSize=8)
   
    
    # Definir estilos
    
    styles.add(ParagraphStyle(name='CenteredHeading', parent=styles['Heading3'], alignment=TA_CENTER, fontSize=10))
    styles.add(ParagraphStyle(name='LeftAligned', parent=styles['Normal'], alignment=TA_LEFT, fontSize=10))
    styles.add(ParagraphStyle(name='TableHeader', fontSize=10, alignment=TA_CENTER, fontName='Helvetica-Bold'))
    styles.add(ParagraphStyle(name='TableContent', fontSize=9, alignment=TA_CENTER, fontName='Helvetica'))
    styles.add(ParagraphStyle(name='ObjectiveContent', alignment=TA_LEFT, fontSize=9))  # Estilo para el objetivo
    styles.add(ParagraphStyle(name='RightAligned', parent=styles['Normal'], alignment=TA_RIGHT, fontSize=9))  # Estilo alineado a la derecha
    styles.add(ParagraphStyle(name='Bold', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=9))  # Estilo para texto en negrita
    styles.add(ParagraphStyle(name='Normal-gray', parent=styles['Normal'], textColor=colors.gray, fontSize=9))
    
    # Definir los datos de la tabla
    data = [
        [Paragraph("1. OBJETIVO", styles['TableHeader'])], 
        [Paragraph('''Informar los avances y actividades realizadas en el trimestre, del proyecto de cooperación que se ejecuta entre la Unidad Administrativa Especial de Gestión de Restitución de Tierras''', styles['ObjectiveContent'])],
        [Paragraph("2. DATOS DEL INFORME", styles['TableHeader'])],
        [Paragraph("Fecha de elaboración del reporte:", styles['TableContent']), Paragraph(reporte_fecha, styles['TableContent'])],
        [Paragraph("Periodo", styles['TableContent']), Paragraph(str(reporte.periodo), styles['TableContent'])],
        [Paragraph("Desde:", styles['RightAligned']), Paragraph(reporte_desde, styles['TableContent']), Paragraph("Hasta:", styles['RightAligned']), Paragraph(reporte_hasta, styles['TableContent'])],
        [Paragraph("3. DATOS DE QUIÉN REPORTA", styles['TableHeader'])],
        [Paragraph("Nombre y apellidos"), Paragraph(usuario.nombre_completo)],
        [Paragraph("Rol"), Paragraph(usuario.rol.nombre)],
        [Paragraph("Dependencia"), Paragraph(usuario.dependencia.nombre)],
        [Paragraph("Correo Electrónico"), Paragraph(usuario.correo_electronico_sesion)],
        [Paragraph("4. DATOS DEL COOPERANTE Y PROGRAMA, PROYECTO O PLAN", styles['TableHeader'])],
        [Paragraph("NOMBRE DEL COOPERANTE"), Paragraph(cooperante.nombre)],
        [Paragraph("IDENTIFICACIÓN:"), Paragraph(acuerdo.identificacion )],
        [Paragraph("NOMBRE DEL IMPLEMENTADOR U OPERADOR: "), Paragraph(operante.nombre)],
        [Paragraph("LÍNEA DE ACCIÓN / COMPONENTE: "), Paragraph(linea_accion.nombre)],
        [Paragraph("ROL DE QUIEN REPORTA: "), Paragraph(reporte.datosquienreporta.rol.nombre)],
        [Paragraph("5. RESULTADOS, LOGROS Y/O AVANCES Y ADJUNTOS", styles['TableHeader'])],
        [Paragraph("Resultados/Productos Esperados"), Paragraph("Logros y/o avances"), Paragraph("Adjunto")]
    ]
    
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
    
    # Crear una tabla con dos celdas: una para el texto de clasificación y otra para la fecha
    data_foot_header = [
        [Paragraph("Clasificación de la Información: Pública <b>■</b> Reservada  Clasificada  ", styles['Normal-gray']),
         Paragraph("Fecha de aprobación: 12/03/2024", styles['Normal-gray'])]
    ]
    
    # Agregar la tabla a 'elements'
    table_foot_header = Table(data_foot_header, colWidths=[300, 200])  # Puedes ajustar los anchos de columna según sea necesario
    
   

    for logro in logros_avances.logros.all():  # Usamos related_name 'logros'
        data.append([
            Paragraph(logro.resultado.nombre, styles['TableContent']), 
            Paragraph(logro.logros_avances_texto, styles['TableContent']), 
            Paragraph(logro.adjunto.url if logro.adjunto else "", styles['TableContent'])
        ])
    
    data2 =[
        [Paragraph("", styles['TableHeader'])],
        [Paragraph("¿Algún aspecto a resaltar como un logro significativo en este período?"), Paragraph(logros_avances.logros_significativos)],
        [Paragraph("Comente en caso haya habido inconvenientes o dificultades presentadas en relación a este proyecto:"), Paragraph(logros_avances.dificultades)],
        [Paragraph("¿Se ha presentado alguna situación que ponga en riesgo el buen relacionamiento con el cooperante?"), Paragraph('SI' if logros_avances.detalle_riesgo else 'NO'), Paragraph("Explique detalladamente"), Paragraph(logros_avances.detalle_riesgo if logros_avances.detalle_riesgo else '')],
        [Paragraph("Observaciones y comentarios generales: otros aspectos respecto al desarrollo de este proyecto (sugerencias, inquietudes, etc.)"), Paragraph(logros_avances.observaciones_generales)],
    ]
    
    # Definir estilo de la tabla
    table_style = TableStyle([
        ('SPAN', (0, 0), (-1, 0)), 
        ('SPAN', (0, 1), (-1, 1)),  
        ('SPAN', (0, 2), (-1, 2)),
        ('SPAN', (1, 3), (-1, 3)),  
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
        
     
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey), 
        ('BACKGROUND', (0, 2), (-1, 2), colors.lightgrey),
        ('BACKGROUND', (0, 6), (-1, 6), colors.lightgrey),
        ('BACKGROUND', (0, 11), (-1, 11), colors.lightgrey),
        ('BACKGROUND', (0, 17), (-1, 17), colors.lightgrey),
       
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),  
        ('ALIGN', (0, 2), (-1, 2), 'CENTER'),  
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),  
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  
        ('FONTNAME', (0, 2), (-1, 2), 'Helvetica-Bold'),  
        ('FONTNAME', (0, 3), (-1, -1), 'Helvetica'), 
        ('FONTSIZE', (0, 0), (-1, -1), 9),  
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'), 
    ])

    table2_style = TableStyle([
        ('SPAN', (0, 0), (-1, 0)),
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('SPAN', (1, 1), (-1, 1)) ,
        ('SPAN', (1, 2), (-1, 2)) ,
        ('SPAN', (1, 4), (-1, 4)) ,
        ('SPAN', (1, 1), (-1, 1)),
        ('SPAN', (1, 2), (-1, 2)),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),  # Agrega esta línea para las líneas de la tabla
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),     

    ])

    
    table = Table(data, colWidths=[doc.width * 0.25, doc.width * 0.25, doc.width * 0.25])
    table2 = Table(data2,colWidths=[doc.width * 0.25, doc.width * 0.25, doc.width * 0.25] )
    table.setStyle(table_style)

    table2.setStyle(table2_style)
    # Construir el documento
    elements = [
        header_table,  # Encabezado
        table_foot_header,
        Spacer(1, 12),  # Espacio después del encabezado
        table,
        table2,
        Spacer(1, 25),  # Espacio después de la tabla
        Paragraph("______________________________", styles['LeftAligned']),
        Paragraph("Firma", styles['LeftAligned']),
        Spacer(1, 12),
        Paragraph(reporte.usuario.first_name +' '+ reporte.usuario.last_name , styles['Bold']),
        Paragraph(reporte.datosquienreporta.rol.nombre, styles['LeftAligned']),
        Paragraph(reporte.datosquienreporta.dependencia.nombre, styles['LeftAligned'])]
    
    doc.build(elements)

    # Obtener el PDF
    pdf = buffer.getvalue()
    buffer.close()
    
   #Guardar el pdf si no exite en media o reemplazarlo aún asi este creado
    with open(f'media/reportes2/reporte2_{reporte.usuario.identificacion}_periodo{reporte.periodo}.pdf', 'wb') as f:
        f.write(pdf)

    
    

    # Crear la respuesta HTTP con el PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="reporteDeAvances_{reporte.id}.pdf"'
    response.write(pdf)

    return response