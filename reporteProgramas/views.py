from reporteProgramas.models import  Logro, Cooperante, AcuerdoCooperacion, Acuerdo, Operador
from  reporteProgramas.forms import   LogrosAvancesForm, LogroFormSet
from django.views.generic.edit import CreateView
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.urls import reverse_lazy
from django.db.utils import IntegrityError
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
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
    
    def dispatch(self, request, *args, **kwargs):
        reporte = get_object_or_404(Reporte, id=self.kwargs['reporte_id'])
       
        if reporte.avance == 1:
            return redirect('reporteProgramas:crear_datos_cooperante', reporte_id=reporte.id)
        elif reporte.avance == 2:
            return redirect('reporteProgramas:crear_logros_avances', reporte_id=reporte.id)
        elif reporte.avance == 3:
            return redirect('accounts:listar_reportes')
        return super().dispatch(request, *args, **kwargs)
    
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
    



def obtener_cooperantes(request):
    if request.method == 'GET':
        cooperantes = list(Cooperante.objects.values('id', 'nombre'))
        return JsonResponse({'cooperantes': cooperantes})


def obtener_identificaciones_por_cooperante(request, cooperante_id):
    if request.method == 'GET':
        # Filtrar las identificaciones según el cooperante seleccionado
        acuerdos = AcuerdoCooperacion.objects.filter(cooperante_id=cooperante_id)
      
        identificaciones = [
            {'id': acuerdo.acuerdo.id, 'identificacion': acuerdo.acuerdo.identificacion}
            for acuerdo in acuerdos
        ]
        return JsonResponse({'identificaciones': identificaciones})
    
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

        # Iterar sobre los acuerdos de cooperación y obtener las líneas de acción relacionadas
        lineas_accion_data = []
        for acuerdo_cooperacion in acuerdos_cooperacion:
            # Asumimos que lineas_accion es un ManyToManyField
            for linea_accion in acuerdo_cooperacion.lineas_accion.all():
                lineas_accion_data.append({
                    'id': linea_accion.id,
                    'nombre': linea_accion.nombre
                })

        # Retornar la respuesta en formato JSON
        return JsonResponse({'lineas_accion': lineas_accion_data})

def crear_datos_cooperante(request,reporte_id):

    reporte = get_object_or_404(Reporte, id=reporte_id)

    if request.method == 'POST':
        cooperante = request.POST.get('cooperante')
        identificacion = request.POST.get('identificacion')
        operador = request.POST.get('operador')
        proyecto_plan = request.POST.get('proyecto_plan')
        linea_accion = request.POST.get('linea_accion')
        rol = request.POST.get('rol')
        
        # Validaciones adicionales (si es necesario)

        try:
            # Guardar los datos en la base de datos
            DatosCooperante.objects.create(
                reporte = reporte,
                cooperante=cooperante,
                identificacion=identificacion,
                operador=operador,
                proyecto_plan=proyecto_plan,
                linea_accion=linea_accion,
                rol=rol
            )
            reporte.avance = 2
            reporte.save()
            messages.success(request, 'Datos guardados correctamente.')
            return redirect('reporteProgramas:crear_logros_avances', reporte_id=reporte_id)
        except Exception as e:
            messages.error(request, f'Ocurrió un error al guardar los datos: {str(e)}')

    return render(request, 'reporteProgramas/crear_datos_cooperante.html', {'reporte': reporte})


@login_required
def crear_reporte_logros(request, reporte_id):
    # Obtén el reporte basado en el ID
    reporte = get_object_or_404(Reporte, id=reporte_id)
    resultados = Resultado.objects.all()  # Obtén todos los resultados

    if request.method == 'POST':
        form_logros_avances = LogrosAvancesForm(request.POST)
        formset_logro = LogroFormSet(request.POST, request.FILES)

        if form_logros_avances.is_valid() and formset_logro.is_valid():
            logros_avances = form_logros_avances.save(commit=False)
            logros_avances.reporte = reporte  # Asociar el reporte
            logros_avances.save()
            reporte.avance = 3  # Marcar el reporte como completado
            reporte.save()  # No olvides guardar el reporte después de actualizar

            for logro in formset_logro:
                if logro.cleaned_data:  # Solo guarda si hay datos limpios
                    nuevo_logro = logro.save(commit=False)
                    nuevo_logro.logros_avances = logros_avances  # Asociar el logro
                    nuevo_logro.save()

            return redirect('accounts:listar_reportes')  # Redirige a donde desees
        
        if not form_logros_avances.is_valid():
          print(form_logros_avances.errors)  # Para depuración

        if not formset_logro.is_valid():
          print(formset_logro.errors)  # Para depuración

    else:
        form_logros_avances = LogrosAvancesForm()
        formset_logro = LogroFormSet(queryset=Logro.objects.none())

    context = {
        'form_logros_avances': form_logros_avances,
        'formset_logro': formset_logro,
        'reporte': reporte,  # Pasa el reporte al contexto si lo necesitas
        'resultados': resultados,  # Pasa los resultados al contexto
    }
    
    return render(request, 'reporteProgramas/crear_logros_avances.html', context)



    

@login_required
def get_municipios(request, departamento_id):
    municipios = Municipio.objects.filter(departamento_id=departamento_id).values('id', 'nombre')
    return JsonResponse({'municipios': list(municipios)})


class ReporteProgramasListView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        reportes = Reporte.objects.filter(tipo=2)
        return render(request, 'reporteProgramas/listar_reportes_avances.html', {'reportes': reportes})
    
    

@login_required
def generar_pdf_reporte_avances(request, reporte_id):
    # Obtener el reporte
    reporte = get_object_or_404(Reporte, id=reporte_id)
    usuario = reporte.datosquienreporta
    cooperante = reporte.datoscooperante
    logros_avances = reporte.logrosavances  # Acceder al objeto LogrosAvances
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
        [Paragraph("Periodo", styles['TableContent']), Paragraph(str(reporte.periodo), styles['TableContent'])],
        [Paragraph("Desde:", styles['RightAligned']), Paragraph(reporte_desde, styles['TableContent']), Paragraph("Hasta:", styles['RightAligned']), Paragraph(reporte_hasta, styles['TableContent'])],
        [Paragraph("3. DATOS DE QUIÉN REPORTA", styles['TableHeader'])],
        [Paragraph("Nombre y apellidos"), Paragraph(usuario.nombre_completo)],
        [Paragraph("Rol"), Paragraph(usuario.rol.nombre)],
        [Paragraph("Dependencia"), Paragraph(usuario.dependencia.nombre)],
        [Paragraph("Correo Electrónico"), Paragraph(usuario.correo_electronico)],
        [Paragraph("4. DATOS DEL COOPERANTE Y PROGRAMA, PROYECTO O PLAN", styles['TableHeader'])],
        [Paragraph("NOMBRE DEL COOPERANTE"), Paragraph(cooperante.nombre_cooperante)],
        [Paragraph("IDENTIFICACIÓN:"), Paragraph( cooperante.identificacion)],
        [Paragraph("NOMBRE DEL IMPLEMENTADOR U OPERADOR: "), Paragraph(cooperante.nombre_implementador)],
        [Paragraph("LÍNEA DE ACCIÓN / COMPONENTE: "), Paragraph(cooperante.linea_accion)],
        [Paragraph("ROL DE QUIEN REPORTA: "), Paragraph(cooperante.rol_quien_reporta)],
        [Paragraph("5. RESULTADOS, LOGROS Y/O AVANCES Y ADJUNTOS", styles['TableHeader'])],
        [Paragraph("Resultados/Productos Esperados"), Paragraph("Logros y/o avances"), Paragraph("Adjunto")]
    ]
    
   

    for logro in logros_avances.logros.all():  # Usamos related_name 'logros'
        data.append([
            Paragraph(logro.resultado.nombre, styles['TableContent']), 
            Paragraph(logro.logros_avances_texto, styles['TableContent']), 
            Paragraph(logro.adjunto.url if logro.adjunto else "", styles['TableContent'])
        ])
    
        data.append([Paragraph("", styles['TableHeader'])])
        data.append([Paragraph("¿Algún aspecto a resaltar como un logro significativo en este período?"), Paragraph(logros_avances.logros_significativos)])
        data.append([Paragraph("Comente en caso haya habido inconvenientes o dificultades presentadas en relación a este proyecto:"), Paragraph(logros_avances.dificultades)])
        data.append([Paragraph("¿Se ha presentado alguna situación que ponga en riesgo el buen relacionamiento con el cooperante?"), Paragraph('SI' if logros_avances.detalle_riesgo else 'NO'), Paragraph("Explique detalladamente"), Paragraph(logros_avances.detalle_riesgo if logros_avances.detalle_riesgo else '')])
        data.append([Paragraph("Observaciones y comentarios generales: otros aspectos respecto al desarrollo de este proyecto (sugerencias, inquietudes, etc.)"), Paragraph(logros_avances.observaciones_generales)])
       
    
    

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
        Paragraph(usuario.rol.nombre, styles['LeftAligned']),
        Paragraph(usuario.dependencia.nombre, styles['LeftAligned'])]
    
    doc.build(elements)

    # Obtener el PDF
    pdf = buffer.getvalue()
    buffer.close()

    # Crear la respuesta HTTP con el PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="reporteDeAvances_{reporte.id}.pdf"'
    response.write(pdf)

    return response