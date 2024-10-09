from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden, HttpResponse
from . forms import ApoyoEventosForm, ApoyoViajesForm, ApoyoMaterialDetalleFormSet, ApoyoHerramientasFormSet, \
                    ApoyoLitigioForm, ApoyoOrdenesJudicialesForm, ApoyoArchivoHistoricoForm, OtrosApoyosForm, \
                    EstimacionEconomicaForm, ApoyoTerritorioUbicacionFormset, ApoyoTerritoriosForm, ApoyoContratacionForm, ContratacionDetalle,  ContratacionDetalleForm, \
                    ApoyoSeguridadAlimentariaForm, ApoyoDetallesFormSet,ApoyoLitigioFormset, ApoyoMaterialForm, ApoyoMaterialDetalleFormSet

from django.forms.models import inlineformset_factory
from .models import TipoPersonal, AreaProfesional, TipoMaterial, TipoHerramienta, TipoCaso, TipoProyecto ,ApoyoHerramientas, \
                    ApoyoTerritorios, ApoyoContratacion, ApoyoSeguridadAlimentaria, ApoyoSeguridadDetalle, ApoyoLitigio, ApoyoLitigioDetalle, \
                    ApoyoEventos, ApoyoViajes, ApoyoMaterial, ApoyoMaterialDetalle, ApoyoOrdenesJudiciales, ApoyoArchivoHistorico, OtrosApoyos, \
                    EstimacionEconomica

from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib import colors, fonts
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib.units import inch
from django.contrib.auth.decorators import login_required
from reporteAcercamientos.models import Reporte

# APOYO EVENTOS
@login_required
def crear_apoyo_eventos(request, reporte_id):
    reporte = Reporte.objects.get(id=reporte_id)


    if request.method == 'POST':
        form = ApoyoEventosForm(request.POST)
        if form.is_valid():
            form.instance.reporte = reporte  # Asigna el reporte al informe
            reporte.avance = 4
            reporte.save()
            form.save()  # Guarda el informe con los eventos seleccionados
            return redirect('reporteAportes:crear_apoyo_viajes', reporte_id = reporte_id)  # Redirige a otra vista después de guardar
    else:
        form = ApoyoEventosForm()

    return render(request, 'reporteAportes/crear_apoyo_eventos.html', {'form': form})
@login_required
def editar_apoyo_eventos(request, reporte_id):
    reporte = Reporte.objects.get(id=reporte_id)
    apoyo_eventos = get_object_or_404(ApoyoEventos, reporte=reporte)
    

    if request.method == 'POST':
        form = ApoyoEventosForm(request.POST, instance=apoyo_eventos)
        if form.is_valid():
            form.save()
            return redirect('accounts:listar_reportes')  # Redirige a otra vista después de guardar
    else:
        form = ApoyoEventosForm(instance=apoyo_eventos)

    return render(request, 'reporteAportes/editar_apoyo_eventos.html', {'form': form})

# APOYO VIAJES
@login_required
def crear_apoyo_viajes(request,reporte_id):
    reporte = Reporte.objects.get(id=reporte_id)
    if request.method == 'POST':
        form = ApoyoViajesForm(request.POST)
        if form.is_valid():
            form.instance.reporte = reporte  # Asigna el reporte al informe
            reporte.avance = 5
            reporte.save()
            form.save()
            return redirect('reporteAportes:crear_apoyo_territorios', reporte_id = reporte_id)  # Redirige a una página de éxito
    else:
        form = ApoyoViajesForm()

    return render(request, 'reporteAportes/crear_apoyo_viajes.html', {'form': form})
@login_required
def editar_apoyo_viajes(request, reporte_id):
    reporte = Reporte.objects.get(id=reporte_id)
    apoyo_viajes = get_object_or_404(ApoyoViajes, reporte=reporte)

    if request.method == 'POST':
        form = ApoyoViajesForm(request.POST, instance=apoyo_viajes)
        if form.is_valid():
            form.save()
            return redirect('accounts:listar_reportes')  # Redirige a otra vista después de guardar
    else:
        form = ApoyoViajesForm(instance=apoyo_viajes)

    return render(request, 'reporteAportes/editar_apoyo_viajes.html', {'form': form})

# APOYO TERRITORIOS
@login_required
def crear_apoyo_territorios(request, reporte_id):
    reporte = get_object_or_404(Reporte, pk=reporte_id)

    if request.method == 'POST':
        
        form = ApoyoTerritoriosForm(request.POST)
        apoyo_territorios = ApoyoTerritorios(reporte=reporte)  # Crea la instancia aquí
        formset_ubicaciones = ApoyoTerritorioUbicacionFormset(request.POST, instance=apoyo_territorios)
        
        if form.is_valid() and formset_ubicaciones.is_valid():
            apoyo_territorios = form.save(commit=False)
            apoyo_territorios.reporte = reporte
            reporte.avance = 6
            reporte.save()
            apoyo_territorios.save()  # Guarda la instancia de ApoyoTerritorios primero

            # Asocia la instancia al formset y guarda
            formset_ubicaciones.instance = apoyo_territorios  
            formset_ubicaciones.save()

            return redirect('reporteAportes:crear_apoyo_contratacion', reporte_id = reporte_id)  # Redirige a una página de éxito
        else:
            print(form.errors, formset_ubicaciones.errors)
    else:
        form = ApoyoTerritoriosForm()
        formset_ubicaciones = ApoyoTerritorioUbicacionFormset(instance=ApoyoTerritorios())  # Crea una instancia vacía

    context = {
        'form': form,
        'formset_ubicaciones': formset_ubicaciones,
        'reporte': reporte,
    }
    return render(request, 'reporteAportes/crear_apoyo_territorios.html', context)
@login_required
def editar_apoyo_territorios(request, reporte_id):
    reporte = get_object_or_404(Reporte, id=reporte_id)
    apoyo_territorios = get_object_or_404(ApoyoTerritorios, reporte=reporte)
  

    if request.method == 'POST':
        form = ApoyoTerritoriosForm(request.POST, instance=apoyo_territorios)
        formset_ubicaciones = ApoyoTerritorioUbicacionFormset(request.POST, instance=apoyo_territorios)

        if form.is_valid() and formset_ubicaciones.is_valid():
            form.save()
            formset_ubicaciones.save()
            return redirect('accounts:listar_reportes')
        else:
            # Render errors in template instead of console
            print('error form:', form.errors)
            print('error form_set:',formset_ubicaciones.errors)
            print(form.non_field_errors())
    else:
        form = ApoyoTerritoriosForm(instance=apoyo_territorios)
        formset_ubicaciones = ApoyoTerritorioUbicacionFormset(instance=apoyo_territorios)
        formset_ubicaciones.extra = 0
        formset_ubicaciones.can_delete = True

    return render(request, 'reporteAportes/editar_apoyo_territorios.html', {
        'form': form,
        'formset_ubicaciones': formset_ubicaciones,
    })

# APOYO CONTRATACIÓN
@login_required
def crear_apoyo_contratacion(request, reporte_id):
    reporte = get_object_or_404(Reporte, pk=reporte_id)
    tipos_personal = TipoPersonal.objects.all()
    area_profesional = AreaProfesional.objects.all()

    ContratacionDetalleFormSet = inlineformset_factory(
        ApoyoContratacion,
        ContratacionDetalle,
        form=ContratacionDetalleForm,
        extra=len(tipos_personal),
        can_delete=False
    )

    if request.method == 'POST':
        form = ApoyoContratacionForm(request.POST)
        formset = ContratacionDetalleFormSet(request.POST, instance=ApoyoContratacion())

        if form.is_valid() and formset.is_valid():
            # Guarda ApoyoContratacion primero
            apoyo_contratacion = form.save(commit=False)
            apoyo_contratacion.reporte = reporte
            reporte.avance = 7
            reporte.save()
            apoyo_contratacion.save()

            # Asocia la instancia de ApoyoContratacion al formset
            formset.instance = apoyo_contratacion
            formset.save()

            return redirect('reporteAportes:crear_apoyo_material', reporte_id=reporte_id)  # Redirige a una página de éxito
        else: 
            print(form.errors, formset.errors)
            print(form.non_field_errors())
    else:
        form = ApoyoContratacionForm()
        formset = ContratacionDetalleFormSet(
            instance=ApoyoContratacion(),
            initial=[{'tipo_personal': tipo.id} for tipo in tipos_personal]
        )

    context = {
        'form': form,
        'formset': formset,
        'tipos_personal': tipos_personal,
        'area_profesional': area_profesional,
    }
    return render(request, 'reporteAportes/crear_apoyo_contratacion.html', context)
@login_required
def editar_apoyo_contratacion(request, reporte_id):
    reporte = get_object_or_404(Reporte, id=reporte_id)
    apoyo_contratacion = get_object_or_404(ApoyoContratacion, reporte=reporte)
    tipos_personal = TipoPersonal.objects.all()
    area_profesional = AreaProfesional.objects.all()

    ContratacionDetalleFormSet = inlineformset_factory(
        ApoyoContratacion,
        ContratacionDetalle,
        form=ContratacionDetalleForm,
        extra=0,
        can_delete=True
    )

    if request.method == 'POST':
        form = ApoyoContratacionForm(request.POST, instance=apoyo_contratacion)
        formset = ContratacionDetalleFormSet(request.POST, instance=apoyo_contratacion)

        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect('accounts:listar_reportes')
        else:
            # Render errors in template instead of console
            print('error form:', form.errors)
            print('error form_set:',formset.errors)
            print(form.non_field_errors())
    else:
        form = ApoyoContratacionForm(instance=apoyo_contratacion)
        formset = ContratacionDetalleFormSet(instance=apoyo_contratacion)

    return render(request, 'reporteAportes/editar_apoyo_contratacion.html', {
        'form': form,
        'formset': formset,
        'tipos_personal': tipos_personal,
        'area_profesional': area_profesional,
    })

# APOYO MATERIAL
@login_required
def crear_apoyo_material(request,reporte_id):
    reporte = Reporte.objects.get(id=reporte_id)
    tipo_material = TipoMaterial.objects.all()

    try:
        apoyo = ApoyoMaterial.objects.get(reporte=reporte)
    except ApoyoMaterial.DoesNotExist:
        apoyo = None

    if request.method == 'POST':
        form = ApoyoMaterialForm(request.POST, instance=apoyo)
        formset = ApoyoMaterialDetalleFormSet(request.POST, queryset=ApoyoMaterialDetalle.objects.filter(apoyo_material=apoyo))
        if form.is_valid() and formset.is_valid():
            apoyo = form.save(commit=False)
            apoyo.reporte = reporte
            apoyo.save()

            detalles = formset.save(commit=False)
            for detalle in detalles:
                detalle.apoyo_material = apoyo
                detalle.save()

            reporte.avance = 8
            reporte.save()
            return redirect('reporteAportes:crear_apoyo_herramientas', reporte_id=reporte_id)
        else:
            print(form.errors, formset.errors)
    else:
        form = ApoyoMaterialForm(instance=apoyo)
        formset = ApoyoMaterialDetalleFormSet(queryset=ApoyoMaterialDetalle.objects.filter(apoyo_material=apoyo))

    context = {
        'form': form,
        'formset': formset,
        'tipo_material': tipo_material,
    }
    return render(request, 'reporteAportes/crear_apoyo_material.html', context)
@login_required
def editar_apoyo_material(request, reporte_id):
    reporte = Reporte.objects.get(id=reporte_id)
    apoyo_material = get_object_or_404(ApoyoMaterial, reporte=reporte)
    tipo_material = TipoMaterial.objects.all()

    if request.method == 'POST':
        form = ApoyoMaterialForm(request.POST, instance=apoyo_material)
        formset = ApoyoMaterialDetalleFormSet(request.POST, instance=apoyo_material)

        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect('accounts:listar_reportes')
        else:
            # Render errors in template instead of console
            print('error form:', form.errors)
            print('error form_set:',formset.errors)
            print(form.non_field_errors())
    else:
        form = ApoyoMaterialForm(instance=apoyo_material)
        formset = ApoyoMaterialDetalleFormSet(instance=apoyo_material)
        formset.extra = 0

    return render(request, 'reporteAportes/editar_apoyo_material.html', {
        'form': form,
        'formset': formset,
        'tipo_material': tipo_material,
    })

# APOYO HERRAMIENTAS
@login_required
def crear_apoyo_herramientas(request, reporte_id):
    reporte = get_object_or_404(Reporte, pk=reporte_id)
    tipos_herramienta = TipoHerramienta.objects.all()

    if request.method == 'POST':
        formset = ApoyoHerramientasFormSet(request.POST)
        if formset.is_valid():
            # Iterar sobre cada formulario en el formset
            for form in formset:
                apoyo = form.save(commit=False)  # Crear la instancia sin guardar
                apoyo.reporte = reporte  # Asignar el reporte a cada instancia
                apoyo.save()  # Guardar la instancia
            reporte.avance = 9
            reporte.save()

            return redirect('reporteAportes:crear_apoyo_litigio', reporte_id=reporte_id)
        else:
            print(formset.errors)
    else:
        # Siempre inicializar los formularios para cada tipo de herramienta
        initial_data = [{'tipo_herramienta': tipo.id} for tipo in tipos_herramienta]
        formset = ApoyoHerramientasFormSet(initial=initial_data)
        formset.extra = TipoHerramienta.objects.all().count()

    context = {
        'formset': formset,
        'tipos_herramienta': tipos_herramienta,
    }
    return render(request, 'reporteAportes/crear_apoyo_herramientas.html', context)
@login_required
def editar_apoyo_herramientas(request, reporte_id):
    reporte = Reporte.objects.get(id=reporte_id)
    apoyos_herramientas = ApoyoHerramientas.objects.filter(reporte=reporte)
    tipos_herramienta = TipoHerramienta.objects.all()

    if request.method == 'POST':
        formset = ApoyoHerramientasFormSet(request.POST)
        if formset.is_valid():
            for form in formset:
                apoyo = form.save(commit=False)
                apoyo.reporte = reporte  # Ensure you are setting the report here
                apoyo.save()
            return redirect('accounts:listar_reportes')
        else:
            print(formset.errors)
    else:
        formset = ApoyoHerramientasFormSet(queryset=apoyos_herramientas)
        formset.extra = 0

    context = {
        'formset': formset,
        'tipos_herramienta': tipos_herramienta,
    }
    return render(request, 'reporteAportes/editar_apoyo_herramientas.html', context)
# APOYO LITIGIO
@login_required
def crear_apoyo_litigio(request, reporte_id):
    reporte = Reporte.objects.get(id=reporte_id)
    tipos_caso = TipoCaso.objects.all()

    try:
        apoyo = ApoyoLitigio.objects.get(reporte=reporte)
    except ApoyoLitigio.DoesNotExist:
        apoyo = None

    if request.method == 'POST':
        form = ApoyoLitigioForm(request.POST, instance=apoyo)
        formset = ApoyoLitigioFormset(request.POST, queryset=ApoyoLitigioDetalle.objects.filter(apoyo_litigio=apoyo))

        if form.is_valid() and formset.is_valid():
            # Guarda el ApoyoLitigio
            apoyo = form.save(commit=False)
            apoyo.reporte = reporte
            apoyo.save()

            # Guarda los detalles del formset
            detalles = formset.save(commit=False)
            for detalle in detalles:
                detalle.apoyo_litigio = apoyo  # Asocia el detalle con el apoyo
                detalle.save()  # Guarda el detalle

            # Actualiza el avance del reporte
            reporte.avance = 10
            reporte.save()

            return redirect('reporteAportes:crear_apoyo_seguridad_alimentaria', reporte_id=reporte_id)
        else:
            print("Errores en el formulario:", form.errors)
            print("Errores en el formset:", formset.errors)
    else:
        form = ApoyoLitigioForm(instance=apoyo)
        formset = ApoyoLitigioFormset(
            queryset=ApoyoLitigioDetalle.objects.filter(apoyo_litigio=apoyo),
            initial=[{'tipo_caso': tipo.id} for tipo in tipos_caso]
        )
        formset.extra = TipoCaso.objects.all().count()

    context = {
        'form': form,
        'formset': formset,
        'tipos_caso': tipos_caso,
    }
    return render(request, 'reporteAportes/crear_apoyo_litigio.html', context)
@login_required
def editar_apoyo_litigio(request, reporte_id):
    reporte = get_object_or_404(Reporte, id=reporte_id)
    apoyo_litigio = get_object_or_404(ApoyoLitigio, reporte=reporte)
    tipos_caso = TipoCaso.objects.all()

    if request.method == 'POST':
        form = ApoyoLitigioForm(request.POST, instance=apoyo_litigio)
        formset = ApoyoLitigioFormset(request.POST, queryset=ApoyoLitigioDetalle.objects.filter(apoyo_litigio=apoyo_litigio))

        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect('accounts:listar_reportes')
        else:
            print(form.errors)
            print(formset.errors)
    else:
        form = ApoyoLitigioForm(instance=apoyo_litigio)
        formset = ApoyoLitigioFormset(queryset=ApoyoLitigioDetalle.objects.filter(apoyo_litigio=apoyo_litigio))
        formset.extra=0
    return render(request, 'reporteAportes/editar_apoyo_litigio.html', {
        'form': form,
        'formset': formset,
        'tipos_caso': tipos_caso,
    })
# APOYO SEGURIDAD ALIMENTARIA

@login_required
def crear_apoyo_seguridad_alimentaria(request, reporte_id):
    reporte = get_object_or_404(Reporte, id=reporte_id)
    tipos_proyecto = TipoProyecto.objects.all()
    
    try:
        apoyo = ApoyoSeguridadAlimentaria.objects.get(reporte=reporte)
    except ApoyoSeguridadAlimentaria.DoesNotExist:
        apoyo = None

    if request.method == 'POST':
        form = ApoyoSeguridadAlimentariaForm(request.POST, instance=apoyo)
        formset = ApoyoDetallesFormSet(request.POST, queryset=ApoyoSeguridadDetalle.objects.filter(apoyoSeguridadAlimentaria=apoyo))

        if form.is_valid() and formset.is_valid():
            apoyo = form.save(commit=False)
            apoyo.reporte = reporte
            apoyo.save()
            form.save_m2m()

            instances = formset.save(commit=False)
            for instance in instances:
                instance.apoyoSeguridadAlimentaria = apoyo
                instance.save()

            reporte.avance = 11  # Asumiendo que este es el paso correcto
            reporte.save()
            return redirect('reporteAportes:crear_apoyo_ordenes_judiciales', reporte_id=reporte_id)
        else:
            print(form.errors)
            print(formset.errors)
    else:
        form = ApoyoSeguridadAlimentariaForm(instance=apoyo)

    # El formset se inicializa aquí sin importar si hay errores en el formulario o no.
    formset = ApoyoDetallesFormSet(
        queryset=ApoyoSeguridadDetalle.objects.filter(apoyoSeguridadAlimentaria=apoyo),
        initial=[{'tipo_proyecto': tipo.id} for tipo in tipos_proyecto]
    )
    formset.extra = TipoProyecto.objects.all().count()  # Asegúrate de que sea un entero

    context = {
        'form': form,
        'formset': formset,
        'tipos_proyecto': tipos_proyecto,
    }

    return render(request, 'reporteAportes/crear_apoyo_seguridad_alimentaria.html', context)
@login_required
def editar_apoyo_seguridad_alimentaria(request, reporte_id):
    reporte = get_object_or_404(Reporte, id=reporte_id)
    apoyo_seguridad = get_object_or_404(ApoyoSeguridadAlimentaria, reporte=reporte)
    tipos_proyecto = TipoProyecto.objects.all()

    if request.method == 'POST':
        form = ApoyoSeguridadAlimentariaForm(request.POST, instance=apoyo_seguridad)
        formset = ApoyoDetallesFormSet(request.POST, queryset=ApoyoSeguridadDetalle.objects.filter(apoyoSeguridadAlimentaria=apoyo_seguridad))

        if form.is_valid() and formset.is_valid():
            apoyo = form.save(commit=False)
            apoyo.reporte = reporte
            apoyo.save()
            form.save_m2m()
            instances = formset.save(commit=False)
            for instance in instances:
                instance.apoyoSeguridadAlimentaria = apoyo
                instance.save()
            return redirect('accounts:listar_reportes')
        else:
            print(form.errors)
            print(formset.errors)
    else:
        form = ApoyoSeguridadAlimentariaForm(instance=apoyo_seguridad)
        formset = ApoyoDetallesFormSet(queryset=ApoyoSeguridadDetalle.objects.filter(apoyoSeguridadAlimentaria=apoyo_seguridad))
        formset.extra = 0

    return render(request, 'reporteAportes/editar_apoyo_seguridad_alimentaria.html', {
        'form': form,
        'formset': formset,
        'tipos_proyecto': tipos_proyecto,
    })
# APOYO ORDENES JUDICIALES
@login_required
def crear_apoyo_ordenes_judiciales(request,reporte_id):
    reporte = Reporte.objects.get(id=reporte_id)
    
    if request.method == 'POST':
        form = ApoyoOrdenesJudicialesForm(request.POST)
        if form.is_valid():
            apoyo = form.save(commit=False)
            apoyo.reporte = reporte
            apoyo.save()
            reporte.avance = 12
            reporte.save()
            return redirect('reporteAportes:crear_apoyo_archivo_historico', reporte_id = reporte_id)  # Reemplaza con la URL correcta
    else:
        form = ApoyoOrdenesJudicialesForm()

    context = {
        'form': form,
        
    }
    return render(request, 'reporteAportes/crear_apoyo_ordenes_judiciales.html', context)
@login_required
def editar_apoyo_ordenes_judiciales(request, reporte_id):
    reporte = Reporte.objects.get(id=reporte_id)
    apoyo_ordenes = get_object_or_404(ApoyoOrdenesJudiciales, reporte=reporte)

    if request.method == 'POST':
        form = ApoyoOrdenesJudicialesForm(request.POST, instance=apoyo_ordenes)
        if form.is_valid():
            form.save()
            return redirect('accounts:listar_reportes')
    else:
        form = ApoyoOrdenesJudicialesForm(instance=apoyo_ordenes)

    return render(request, 'reporteAportes/editar_apoyo_ordenes_judiciales.html', {'form': form})
# APOYO ARCHIVO HISTORICO
@login_required
def crear_apoyo_archivo_historico(request, reporte_id):
    reporte = Reporte.objects.get(id=reporte_id)

    if request.method == 'POST':
        form = ApoyoArchivoHistoricoForm(request.POST)
        if form.is_valid():
            apoyo = form.save(commit=False)
            apoyo.reporte = reporte
            apoyo.save()  # Save the instance first to create the database record
            
            # Save the many-to-many relationships
            form.save_m2m()  # This will save the 'acciones' field
            
            reporte.avance = 13
            reporte.save()
            return redirect('reporteAportes:crear_otros_apoyos', reporte_id=reporte_id)
        else:
            print(form.errors)
    else:
        form = ApoyoArchivoHistoricoForm()

    context = {
        'form': form,
    }
    return render(request, 'reporteAportes/crear_apoyo_archivo_historico.html', context)
@login_required
def editar_apoyo_archivo_historico(request, reporte_id):
    reporte = Reporte.objects.get(id=reporte_id)
    apoyo_archivo = get_object_or_404(ApoyoArchivoHistorico, reporte=reporte)

    if request.method == 'POST':
        form = ApoyoArchivoHistoricoForm(request.POST, instance=apoyo_archivo)
        if form.is_valid():
            form.save()
            return redirect('accounts:listar_reportes')
    else:
        form = ApoyoArchivoHistoricoForm(instance=apoyo_archivo)

    return render(request, 'reporteAportes/editar_apoyo_archivo_historico.html', {'form': form})
# OTROS APOYOS
@login_required
def crear_otros_apoyos(request,reporte_id):
    
    reporte = Reporte.objects.get(id=reporte_id)

    if request.method == 'POST':
        form = OtrosApoyosForm(request.POST)
        if form.is_valid():
            apoyo = form.save(commit=False)
            apoyo.reporte = reporte
            apoyo.save()
            reporte.avance = 14
            reporte.save()
            return redirect('reporteAportes:crear_estimacion_economica', reporte_id=reporte_id) # Reemplaza con la URL adecuada
    else:
        form = OtrosApoyosForm()
        
    context = {
        'form': form,

    }
    return render(request, 'reporteAportes/crear_otros_apoyos.html', context)
@login_required
def editar_otros_apoyos(request, reporte_id):
    reporte = Reporte.objects.get(id=reporte_id)
    apoyo_otros = get_object_or_404(OtrosApoyos, reporte=reporte)

    if request.method == 'POST':
        form = OtrosApoyosForm(request.POST, instance=apoyo_otros)
        if form.is_valid():
            form.save()
            return redirect('accounts:listar_reportes')
    else:
        form = OtrosApoyosForm(instance=apoyo_otros)

    return render(request, 'reporteAportes/editar_otros_apoyos.html', {'form': form})
# ESTIMACIÓN ECONÓMICA
@login_required
def crear_estimacion_economica(request,reporte_id):

    reporte = Reporte.objects.get(id=reporte_id)

    if request.method == 'POST':
        form = EstimacionEconomicaForm(request.POST)
        if form.is_valid():
            apoyo = form.save(commit=False)
            apoyo.reporte = reporte
            apoyo.save()
            reporte.avance = 15
            reporte.save()

            return redirect('accounts:listar_reportes')  # Reemplaza con la URL correcta
        else:
            print(form.errors)
            print(form.non_field_errors())
    else:
        form = EstimacionEconomicaForm()

    context = {
        'form': form,
        
    }
    return render(request, 'reporteAportes/crear_estimacion_economica.html', context)
@login_required
def editar_estimacion_economica(request, reporte_id):
    reporte = Reporte.objects.get(id=reporte_id)
    apoyo_economico = get_object_or_404(EstimacionEconomica, reporte=reporte)

    if request.method == 'POST':
        form = EstimacionEconomicaForm(request.POST, instance=apoyo_economico)
        if form.is_valid():
            form.save()
            return redirect('accounts:listar_reportes')
        else:
            print(form.errors)
            print(form.non_field_errors())
    else:
        form = EstimacionEconomicaForm(instance=apoyo_economico)

    return render(request, 'reporteAportes/editar_estimacion_economica.html', {'form': form})
# GENERAR REPORTE PDF
@login_required
def crear_reporte_pdf(request, reporte_id):
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
    if reporte.avance != 15:
        # Devolver un mensaje de error o redirigir al usuario
        return HttpResponseForbidden("No se puede generar el PDF hasta que el reporte esté finalizado.") 
    
    usuario = reporte.datosquienreporta
    reporte_fecha = reporte.fecha_elaboracion.strftime('%Y-%m-%d')
    reporte_hasta = reporte.hasta.strftime('%Y-%m-%d')
    reporte_desde = reporte.desde.strftime('%Y-%m-%d')

    # Extraer las ubicaciones del reporte
    ubicaciones = reporte.apoyoterritorios.ubicaciones.through.objects.filter(apoyo_territorio=reporte.apoyoterritorios)
    
    # Crear la estructura de la tabla
    tabla_dato_ubicaciones = [['Departamento', 'Municipio', 'Vereda/Territorio/Cabildo']]
    
    # Iterar sobre las ubicaciones y agregarlas a la lista de filas
    for ubicacion in ubicaciones:
        departamento = ubicacion.departamento.nombre
        municipio = ubicacion.municipio.nombre
        vereda = ubicacion.vereda or ''  # Si no hay vereda, mostrar una cadena vacía
        tabla_dato_ubicaciones.append([departamento, municipio, vereda])
    
    # Crear la tabla usando la clase Table de ReportLab
    tabla_ubicaciones = Table(tabla_dato_ubicaciones)

    # Aplicar estilo a la tabla
    tabla_ubicaciones.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),  # Encabezado en gris
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),  # Texto del encabezado en blanco
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Alinear el texto al centro
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Fuente del encabezado en negrita
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  # Espaciado del encabezado
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),  # Fondo de las filas
        ('GRID', (0, 0), (-1, -1), 1, colors.black)  # Bordes de la tabla
    ]))


    # Obtener detalles de contratación relacionados con el reporte
    contratacion = reporte.apoyocontratacion
    detalles = ContratacionDetalle.objects.filter(apoyo_contratacion=contratacion)

    tabla_datos_contratacion = [['Tipo de Personal', 'Cantidad', 'Tiempo de Servicio', 'Area Profesional']]
    for detalle in detalles:
        tipo_personal = detalle.tipo_personal.nombre
        cantidad = detalle.cantidad_personas
        tiempo_servicio = detalle.tiempo_servicio
        area_profesional = detalle.area_profesional
        tabla_datos_contratacion.append([tipo_personal, cantidad, tiempo_servicio, area_profesional])
    
    tabla_contratacion = Table(tabla_datos_contratacion)
      # Aplicar estilo a la tabla
    tabla_contratacion.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),  # Encabezado en gris
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),  # Texto del encabezado en blanco
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Alinear el texto al centro
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Fuente del encabezado en negrita
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  # Espaciado del encabezado
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),  # Fondo de las filas
        ('GRID', (0, 0), (-1, -1), 1, colors.black)  # Bordes de la tabla
    ]))


       # Obtener los apoyos de herramientas relacionados con el reporte
    apoyos_herramientas = ApoyoHerramientas.objects.filter(reporte=reporte)
    
    # Datos de la tabla
    tabla_datos_herramientas = [
        ['Tipo de herramienta / equipo', 'Cantidad recibida', 'Descripción', 'Observaciones / detalle']
    ]
    
    # Definir estilos de párrafo para el ajuste de texto
    styles = getSampleStyleSheet()
    adjusted_style = ParagraphStyle(
        name='AdjustedStyle',
        parent=styles['Normal'],
        fontSize=8,
        leading=10,
        spaceAfter=4
    )
    
    # Añadir filas con datos, ajustando el texto en celdas
    for apoyo in apoyos_herramientas:
        tipo_herramienta = Paragraph(apoyo.tipo_herramienta.nombre, adjusted_style)
        cantidad = Paragraph(str(apoyo.cantidad_recibida), adjusted_style)
        descripcion = Paragraph(apoyo.descripcion if apoyo.descripcion else 'N/A', adjusted_style)
        observaciones = Paragraph(apoyo.observaciones if apoyo.observaciones else 'N/A', adjusted_style)
        tabla_datos_herramientas.append([tipo_herramienta, cantidad, descripcion, observaciones])
    
    # Crear la tabla con tamaños de columna reducidos
    colWidths = [1.6 * inch, 1 * inch, 1.3* inch, 1.3 * inch]  # Ajustar anchos de columna
    
    # Crear la tabla
    tabla_herramientas = Table(tabla_datos_herramientas, colWidths=colWidths)
    
    # Aplicar estilo a la tabla
    tabla_herramientas.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),  # Encabezado en gris
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),  # Texto del encabezado en blanco
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Alinear el texto al centro
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Fuente del encabezado en negrita
        ('FONTSIZE', (0, 0), (-1, -1), 8),  # Reducir el tamaño de la fuente
        ('BOTTOMPADDING', (0, 0), (-1, 0), 6),  # Reducir espaciado del encabezado
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),  # Fondo de las filas
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),  # Bordes de la tabla, más finos
        ('LEFTPADDING', (0, 0), (-1, -1), 2),  # Reducir el padding izquierdo
        ('RIGHTPADDING', (0, 0), (-1, -1), 2),  # Reducir el padding derecho
    ]))



    # Obtener el apoyo relacionado con el reporte
    apoyo_litigio = ApoyoLitigio.objects.get(reporte=reporte)  # Asegúrate de que 'reporte' es la instancia correcta
    apoyos_litigio_detalle = ApoyoLitigioDetalle.objects.filter(apoyo_litigio=apoyo_litigio)

    # Datos de la tabla
    tabla_datos_detalle = [
        ['Tipo de Caso', 'Nombre de los Casos', 'Cantidad de IDs']  # Encabezado de la tabla
    ]
    
    # Definir estilos de párrafo para el ajuste de texto
    styles = getSampleStyleSheet()
    adjusted_style = ParagraphStyle(
        name='AdjustedStyle',
        parent=styles['Normal'],
        fontSize=8,
        leading=10,
        spaceAfter=4
    )
    
    # Añadir filas con datos, ajustando el texto en celdas
    for detalle in apoyos_litigio_detalle:
        tipo_caso = Paragraph(detalle.tipo_caso.nombre, adjusted_style)
        nombre_caso = Paragraph(detalle.nombre_caso, adjusted_style)
        cantidad_ids = Paragraph(str(detalle.cantidad_ids), adjusted_style)
        
        tabla_datos_detalle.append([tipo_caso, nombre_caso, cantidad_ids])

    # Crear la tabla con tamaños de columna reducidos
    colWidths = [2 * inch, 2 * inch, 1 * inch]  # Ajustar anchos de columna
    
    # Crear la tabla
    tabla_detalle_litigio = Table(tabla_datos_detalle, colWidths=colWidths)
    
    # Aplicar estilo a la tabla
    tabla_detalle_litigio.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),  # Encabezado en gris
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),  # Texto del encabezado en blanco
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Alinear el texto al centro
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Fuente del encabezado en negrita
        ('FONTSIZE', (0, 0), (-1, -1), 8),  # Reducir el tamaño de la fuente
        ('BOTTOMPADDING', (0, 0), (-1, 0), 6),  # Reducir espaciado del encabezado
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),  # Fondo de las filas
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),  # Bordes de la tabla, más finos
        ('LEFTPADDING', (0, 0), (-1, -1), 2),  # Reducir el padding izquierdo
        ('RIGHTPADDING', (0, 0), (-1, -1), 2),  # Reducir el padding derecho
    ]))


    # Obtener el apoyo de seguridad alimentaria relacionado con el reporte
    apoyo_seguridad = ApoyoSeguridadAlimentaria.objects.get(reporte=reporte)  # Asegúrate de que 'reporte' es la instancia correcta
    detalles_apoyo = ApoyoSeguridadDetalle.objects.filter(apoyoSeguridadAlimentaria=apoyo_seguridad)

    # Datos de la tabla
    tabla_datos_detalle = [
        ['Tipo de Proyecto', 'Cantidad Proyectos', 'Cantidad Familias Beneficiarias']  # Encabezado de la tabla
    ]
    

    
    # Añadir filas con datos, ajustando el texto en celdas
    for detalle in detalles_apoyo:
        tipo_proyecto = Paragraph(detalle.tipo_proyecto.nombre, adjusted_style)  # Asegúrate de que 'nombre' sea el campo correcto
        cantidad_proyectos = Paragraph(str(detalle.cantidad_proyectos), adjusted_style)
        cantidad_familias = Paragraph(str(detalle.cantidad_familias), adjusted_style)
        
        tabla_datos_detalle.append([tipo_proyecto, cantidad_proyectos, cantidad_familias])

    # Crear la tabla con tamaños de columna reducidos
    colWidths = [2 * inch, 1.2 * inch, 1.8 * inch]  # Ajustar anchos de columna
    
    # Crear la tabla
    tabla_detalle_seguridad = Table(tabla_datos_detalle, colWidths=colWidths)
    
    # Aplicar estilo a la tabla
    tabla_detalle_seguridad.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),  # Encabezado en gris
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),  # Texto del encabezado en blanco
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Alinear el texto al centro
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Fuente del encabezado en negrita
        ('FONTSIZE', (0, 0), (-1, -1), 8),  # Reducir el tamaño de la fuente
        ('BOTTOMPADDING', (0, 0), (-1, 0), 6),  # Reducir espaciado del encabezado
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),  # Fondo de las filas
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),  # Bordes de la tabla, más finos
        ('LEFTPADDING', (0, 0), (-1, -1), 2),  # Reducir el padding izquierdo
        ('RIGHTPADDING', (0, 0), (-1, -1), 2),  # Reducir el padding derecho
    ]))
    
    # Crear un estilo de párrafo para los títulos
    styles = getSampleStyleSheet()
    header_style = styles['Heading4']  # Estilo para los encabezados
    header_style.fontSize = 10  # Ajustar tamaño de fuente para los títulos
    header_style.alignment = 1  # Centrar el texto
    header_style.textColor = colors.whitesmoke  # Cambiar el color del texto a blanco
    
    # Obtener el apoyo de material relacionado al reporte
    apoyo_material = ApoyoMaterial.objects.get(reporte=reporte)
    detalles_material = ApoyoMaterialDetalle.objects.filter(apoyo_material=apoyo_material)
    
    # Crear la tabla de datos con los títulos incluidos
    tabla_datos_detalle = [
        [
            Paragraph('Título material', header_style),
            Paragraph('Objetivo principal', header_style),
            Paragraph('Público destinatario', header_style),
            Paragraph('Tipo de material', header_style),
            Paragraph('Cantidad originales', header_style),
            Paragraph('Cantidad reproducciones', header_style)
        ]
    ]
    
    # Agregar el contenido de los detalles
    for detalle in detalles_material:
        titulo_material = Paragraph(detalle.titulo_material, adjusted_style)
        objetivo_principal = Paragraph(detalle.objetivo_principal, adjusted_style)
        publico_destinatario = Paragraph(detalle.publico_destinatario.nombre, adjusted_style)
        tipo_material = Paragraph(detalle.tipo_material.nombre, adjusted_style)
        cantidad_material = Paragraph(str(detalle.cantidad_originales), adjusted_style)
        cantidad_reproducciones = Paragraph(str(detalle.cantidad_reproducciones), adjusted_style)
    
        tabla_datos_detalle.append([titulo_material, objetivo_principal, publico_destinatario, tipo_material, cantidad_material, cantidad_reproducciones])
    
    # Crear tabla con tamaños reducidos de columna
    colWidths = [
        0.8 * inch,  # Título material
        0.8 * inch,  # Objetivo principal
        0.8 * inch,  # Público destinatario
        0.8 * inch,  # Tipo de material
        0.8 * inch,  # Cantidad de material
        0.9 * inch,  # Cantidad de reproducciones
    ]
    
    # Crear la tabla
    tabla_material = Table(tabla_datos_detalle, colWidths=colWidths)
    
    # Aplicar estilo a la tabla
    tabla_material.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),  # Fondo gris para encabezados
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),  # Texto de encabezados en blanco
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Alinear el texto al centro
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Fuente del encabezado en negrita
        ('FONTSIZE', (0, 0), (-1, 0), 10),  # Tamaño de la fuente para los títulos
        ('FONTSIZE', (0, 1), (-1, -1), 8),  # Tamaño de la fuente para el contenido
        ('BOTTOMPADDING', (0, 0), (-1, 0), 6),  # Espaciado inferior para encabezados
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),  # Fondo beige para las filas
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),  # Bordes de la tabla
        ('LEFTPADDING', (0, 0), (-1, -1), 2),  # Padding izquierdo reducido
        ('RIGHTPADDING', (0, 0), (-1, -1), 2),  # Padding derecho reducido
    ]))




    
    


    # Definir estilos
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='CenteredHeading', parent=styles['Heading3'], alignment=TA_CENTER, fontSize=10))
    styles.add(ParagraphStyle(name='LeftAligned', parent=styles['Normal'], alignment=TA_LEFT, fontSize=10))
    styles.add(ParagraphStyle(name='TableHeader', fontSize=10, alignment=TA_CENTER, fontName='Helvetica-Bold'))
    styles.add(ParagraphStyle(name='TableContent', fontSize=9, alignment=TA_CENTER, fontName='Helvetica'))
    styles.add(ParagraphStyle(name='ObjectiveContent', alignment=TA_LEFT, fontSize=9))  # Estilo para el objetivo
    styles.add(ParagraphStyle(name='RightAligned', parent=styles['Normal'], alignment=TA_RIGHT, fontSize=9))  # Estilo alineado a la derecha
    styles.add(ParagraphStyle(name='Bold', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=11))  # Estilo para texto en negrita
    styles.add(ParagraphStyle(name='Normal-gray', parent=styles['Normal'], textColor=colors.gray, fontSize=9))


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
        [Paragraph("4. DATOS DEL COOPERANTE / PROGRAMA, PROYECTO O PLAN ", styles['TableHeader'])],
        [Paragraph("Nombre del Cooperante:"), Paragraph(reporte.datoscooperante.cooperante.nombre)],
        [Paragraph("Identificación:"), Paragraph(reporte.datoscooperante.identificacion.identificacion)],
        [Paragraph("Nombre del Implementador u Operador:"), Paragraph(reporte.datoscooperante.operador.nombre)],
        [Paragraph("Programa, Proyecto o Plan:"), Paragraph(reporte.datoscooperante.proyecto_plan.nombre)],
        [Paragraph("Línea de Acción o Componente:"), Paragraph(reporte.datoscooperante.linea_accion.nombre)],
        [Paragraph("Rol de Quien Reporta:"), Paragraph(reporte.datosquienreporta.rol.nombre)],
        [Paragraph("Apoyo de este proyecto / cooperante para asistir o realizar eventos, jornadas y otros espacios de información, sensibilización y/o capacitación ", styles['TableHeader'])],
        [Paragraph("Cantidad de eventos apoyados por este proyecto / cooperante en el periodo reportado:"), Paragraph(str(reporte.apoyoeventos.cantidad_eventos))],
        [Paragraph("Tipo de eventos apoyados:"), Paragraph(', '.join([str(evento) for evento in reporte.apoyoeventos.eventos.all()]))],
        [Paragraph("Objetivo principal de los eventos apoyados: "), Paragraph(reporte.apoyoeventos.objetivo_principal)],
        [Paragraph("Principal público objetivo de los eventos:"), Paragraph(', '.join([str(evento) for evento in reporte.apoyoeventos.publico_objetivo.all()]))],
        [Paragraph("Cantidad total de participantes en los eventos en este periodo: "), Paragraph(str(reporte.apoyoeventos.cantidad_participantes))], 
        [Paragraph("Apoyo de este proyecto / cooperante para la realización de viajes", styles['TableHeader'])],
        [Paragraph("Cantidad de viajes locales / regionales:"), Paragraph(str(reporte.apoyoviajes.cantidad_locales))],
        [Paragraph("Cantidad de viajes nacionales:"), Paragraph(str(reporte.apoyoviajes.cantidad_nacionales))],
        [Paragraph("Cantidad de viajes internacionales: "), Paragraph(str(reporte.apoyoviajes.cantidad_internacionales))],
        [Paragraph("Cantidad total de viajes apoyados por este proyecto /cooperante en el periodo:  "), Paragraph(str(reporte.apoyoviajes.suma_viajes))],
        [Paragraph("Objeto de los viajes:"), Paragraph(', '.join([str(evento) for evento in reporte.apoyoviajes.objetivo_viajes.all()]))],
        [Paragraph("¿Qué resaltaría de este apoyo relacionado con viajes por parte de este proyecto / cooperante? :"), Paragraph(reporte.apoyoviajes.resaltado_apoyo)],
        [Paragraph("Apoyo de este proyecto / cooperante para acceder a territorios o comunidades en este periodo", styles['TableHeader'])],
        [Paragraph("Indique para qué territorios (municipios, veredas, resguardos, etc.) tuvo acompañamiento o apoyo de este cooperante para el acceso durante este periodo:"), tabla_ubicaciones],
        [Paragraph("En qué consistió el apoyo recibido: "), Paragraph(reporte.apoyoterritorios.apoyo_recibido)],
        [Paragraph("Indique para qué tipo de visitas / actividades tuvo el acompañamiento o apoyo en cuanto al acceso:"), Paragraph(reporte.apoyoterritorios.tipo_visitas)],
        [Paragraph("¿Para cuántas visitas obtuvo apoyo de este cooperante para el acceso a territorios en este periodo? "), Paragraph(str(reporte.apoyoterritorios.cantidad_visitas))],
        [Paragraph("¿Qué resaltaría de este apoyo relacionado con acceso a los territorios por parte de este cooperante? "), Paragraph(reporte.apoyoterritorios.resaltar_apoyo)],
        [Paragraph("Apoyo de este proyecto / cooperante a través de contratación de personal ", styles['TableHeader'])],
        [Paragraph("Indique la cantidad de personas y el tiempo de servicio, para las cuales obtuvo apoyo de este proyecto / cooperante:"), tabla_contratacion],
        [Paragraph("¿Cuál es el objetivo principal de los contratos del personal con el cual apoya este proyecto / cooperante? "), Paragraph(reporte.apoyocontratacion.objetivo_principal)],
        [Paragraph("¿Qué resaltaría de este apoyo relacionado con la contratación de personal por parte de este cooperante?"), Paragraph(reporte.apoyocontratacion.resaltar_apoyo)],
        [Paragraph("Apoyo de este proyecto / cooperante para la producción de materiales en este periodo", styles['TableHeader'])],
        [Paragraph("Por cada tipo de material, indique la cantidad de materiales y reproducciones que haya sido apoyado por el proyecto / cooperante en este periodo: "),tabla_material],
        [Paragraph("¿Qué resaltaría de este apoyo a través de la producción de materiales?  "), Paragraph(reporte.apoyomaterial.resaltar_apoyo)],
        [Paragraph("Apoyo recibido de este proyecto / cooperante a través de herramientas y/o equipos tecnológicos en este periodo  ", styles['TableHeader'])],
        [Paragraph("Indique qué herramienta y/o equipo tecnológico recibió su dependencia de parte de este proyecto / cooperante en este periodo: "), tabla_herramientas],
        [Paragraph("Apoyo de este proyecto / cooperante para el litigio de casos ", styles['TableHeader'])],
        [Paragraph("Indique la información sobre el tipo, nombre de casos y cantidad de IDs, del apoyo que haya recibido para el litigio de casos en el periodo: "), tabla_detalle_litigio],
        [Paragraph("¿Qué resaltaría de este apoyo relacionado con el litigio de casos por parte de este cooperante o, alguna observación al respecto de este tipo de apoyo recibido? "), Paragraph(apoyo_litigio.resaltar_apoyo)],
        [Paragraph("Apoyo de este proyecto / cooperante para proyectos de seguridad alimentaria y proyectos productivos ", styles['TableHeader'])],
        [Paragraph("Indique en este periodo, para cuántos proyectos ha recibido apoyo por parte de este proyecto / cooperante:  "), tabla_detalle_seguridad],
        [Paragraph("Indique el tipo de apoyo recibido para los proyectos de seguridad alimentaria o productivos en este periodo:"), Paragraph(', '.join([str(evento) for evento in reporte.apoyoseguridadalimentaria.tipo_apoyo.all()]))],
        [Paragraph("¿Qué resaltaría de este apoyo relacionado con seguridad alimentaria o proyectos productivos por parte de este proyecto / cooperante? "), Paragraph(reporte.apoyoseguridadalimentaria.resaltar_apoyo)],
        [Paragraph("Apoyo de este proyecto / cooperante para el cumplimiento de órdenes judiciales  (diferente a seguridad alimentaria y proyectos productivos) ", styles['TableHeader'])],
        [Paragraph("Indique el tipo de apoyo que ha recibido de este proyecto / cooperante para el cumplimiento de órdenes judiciales  "), Paragraph(reporte.apoyoordenesjudiciales.tipo_apoyo)],
        [Paragraph("¿Para qué tipo de órdenes judiciales recibió el apoyo? "), Paragraph(reporte.apoyoordenesjudiciales.tipo_ordenes)],
        [Paragraph("Indique, si es posible, para cuántas sentencias ha contribuido el apoyo recibido de este proyecto / cooperante: "), Paragraph(str(reporte.apoyoordenesjudiciales.cantidad_sentencias))],
        [Paragraph("Indique, si es posible, para cuántas órdenes ha contribuido el apoyo recibido de este proyecto / cooperante: "), Paragraph(str(reporte.apoyoordenesjudiciales.cantidad_ordenes))],
        [Paragraph("Apoyo de este proyecto / cooperante para la gestión del archivo histórico de restitución de tierras", styles['TableHeader'])],
        [Paragraph("Indique el tipo de acciones para las cuales ha recibido apoyo de este proyecto / cooperante en función del fortalecimiento del sistema documental: "), Paragraph(', '.join([str(evento) for evento in reporte.apoyoarchivohistorico.acciones.all()]))],
        [Paragraph("¿Qué resaltaría o qué comentarios tiene sobre el apoyo recibido para la gestión documental?  "), Paragraph(reporte.apoyoarchivohistorico.comentarios)],
        [Paragraph("Otro tipo de apoyos de este proyecto / cooperante en el período ", styles['TableHeader'])],
        [Paragraph("Realice una breve descripción de algún otro tipo de apoyo recibido por este proyecto / cooperante, si no pudo registrarlo en las anteriores preguntas: "), Paragraph(reporte.otrosapoyos.descripcion)],
        [Paragraph("Estimación económica del aporte de este proyecto / cooperante durante el período", styles['TableHeader'])],
        [Paragraph("Si tiene un valor económico del presupuesto destinado desde el proyecto / cooperante para el aporte a su dependencia durante este período, por favor indíquela:  "), Paragraph('Valor económico:'+str(reporte.estimacioneconomica.valor_economico)+'\n'+'Moneda:'+reporte.estimacioneconomica.moneda.nombre)],
        [Paragraph("Indique por favor cómo obtuvo este valor reportado: (Ej: presupuesto aprobado por cooperante, presupuesto ejecutado, costo de personal o materiales, estimativo según costos de lo entregado, cotizaciones, etc.) "), Paragraph(reporte.estimacioneconomica.obtencion_valor)],
        [Paragraph("")]  
        ]




    
     # Crear buffer
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=30, bottomMargin=30, leftMargin=40, rightMargin=40)
    
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
        ('SPAN', (1, 17), (-1, 17)),
        ('SPAN', (0, 18), (-1, 18)),
        ('SPAN', (1, 19), (-1, 19)),
        ('SPAN', (1, 20), (-1, 20)),
        ('SPAN', (1, 21), (-1, 21)),
        ('SPAN', (1, 22), (-1, 22)),
        ('SPAN', (1, 23), (-1, 23)),
        ('SPAN', (0, 24), (-1, 24)),
        ('SPAN', (1, 25), (-1, 25)),
        ('SPAN', (1, 26), (-1, 26)),
        ('SPAN', (1, 27), (-1, 27)),
        ('SPAN', (1, 28), (-1, 28)),
        ('SPAN', (1, 29), (-1, 29)),
        ('SPAN', (1, 30), (-1, 30)),
        ('SPAN', (0, 31), (-1, 31)),
        ('SPAN', (1, 32), (-1, 32)),
        ('SPAN', (1, 33), (-1, 33)),
        ('SPAN', (1, 34), (-1, 34)),
        ('SPAN', (1, 35), (-1, 35)),
        ('SPAN', (1, 36), (-1, 36)),
        ('SPAN', (0, 37), (-1, 37)),
        ('SPAN', (1, 38), (-1, 38)),
        ('SPAN', (1, 39), (-1, 39)),
        ('SPAN', (1, 40), (-1, 40)),
        ('SPAN', (0, 41), (-1, 41)),
        ('SPAN', (1, 42), (-1, 42)),
        ('SPAN', (1, 43), (-1, 43)),
        ('SPAN', (0, 44), (-1, 44)),
        ('SPAN', (1, 45), (-1, 45)),
        ('SPAN', (0, 46), (-1, 46)),
        ('SPAN', (1, 47), (-1, 47)),
        ('SPAN', (1, 48), (-1, 48)),
        ('SPAN', (0, 49), (-1, 49)),
        ('SPAN', (1, 50), (-1, 50)),
        ('SPAN', (1, 51), (-1, 51)),
        ('SPAN', (1, 52), (-1, 52)),
        ('SPAN', (0, 53), (-1, 53)),
        ('SPAN', (1, 54), (-1, 54)),
        ('SPAN', (1, 55), (-1, 55)),
        ('SPAN', (1, 56), (-1, 56)),
        ('SPAN', (1, 57), (-1, 57)),
        ('SPAN', (0, 58), (-1, 58)),
        ('SPAN', (1, 59), (-1, 59)),
        ('SPAN', (1, 60), (-1, 60)),
        ('SPAN', (0, 61), (-1, 61)),
        ('SPAN', (1, 62), (-1, 62)),
        ('SPAN', (0, 63), (-1, 63)),
        ('SPAN', (1, 64), (-1, 64)),
        ('SPAN', (1, 65), (-1, 65)),
        ('SPAN', (0, 66), (-1, 66)),
  

        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey), 
        ('BACKGROUND', (0, 2), (-1, 2), colors.lightgrey),
        ('BACKGROUND', (0, 6), (-1, 6), colors.lightgrey),
        ('BACKGROUND', (0, 11), (-1, 11), colors.lightgrey),
        ('BACKGROUND', (0, 18), (-1, 18), colors.lightgrey),
        ('BACKGROUND', (0, 24), (-1, 24), colors.lightgrey),
        ('BACKGROUND', (0, 31), (-1, 31), colors.lightgrey),
        ('BACKGROUND', (0, 37), (-1, 37), colors.lightgrey),
        ('BACKGROUND', (0, 41), (-1, 41), colors.lightgrey),
        ('BACKGROUND', (0, 44), (-1, 44), colors.lightgrey),
        ('BACKGROUND', (0, 46), (-1, 46), colors.lightgrey),
        ('BACKGROUND', (0, 49), (-1, 49), colors.lightgrey),
        ('BACKGROUND', (0, 53), (-1, 53), colors.lightgrey),
        ('BACKGROUND', (0, 58), (-1, 58), colors.lightgrey),
        ('BACKGROUND', (0, 61), (-1, 61), colors.lightgrey),
        ('BACKGROUND', (0, 63), (-1, 63), colors.lightgrey),
        ('BACKGROUND', (0, 66), (-1, 66), colors.lightgrey),
  
   
        

        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),  
        ('ALIGN', (0, 2), (-1, 2), 'CENTER'),  
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),  
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  
        ('FONTNAME', (0, 2), (-1, 2), 'Helvetica-Bold'),  
        ('FONTNAME', (0, 3), (-1, -1), 'Helvetica'), 
        ('FONTSIZE', (0, 0), (-1, -1), 9),  
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')])

    table = Table(data, colWidths=[doc.width * 0.25, doc.width * 0.25, doc.width * 0.25, doc.width * 0.25])
    table.setStyle(table_style)
    
     # Crear una tabla con dos celdas: una para el texto de clasificación y otra para la fecha
    data_foot_header = [
        [Paragraph("Clasificación de la Información: Pública <b>■</b> Reservada  Clasificada  ", styles['Normal-gray']),
         Paragraph("Fecha de aprobación: 12/03/2024", styles['Normal-gray'])]
    ]
    
    # Agregar la tabla a 'elements'
    table_foot_header = Table(data_foot_header, colWidths=[300, 200])  # Puedes ajustar los anchos de columna según sea necesario


    elements = [header_table,	
                table_foot_header,
                Spacer(1, 12),  # Espacio después del encabezado 
                table,
                Spacer(1, 25),  # Espacio después de la tabla
                Paragraph("______________________________", styles['LeftAligned']),
                Paragraph("Firma", styles['LeftAligned']),
                Spacer(1, 12),
                Paragraph(reporte.usuario.first_name +' '+ reporte.usuario.last_name , styles['Bold']),
                Paragraph(reporte.datosquienreporta.rol.nombre, styles['LeftAligned']),
                Paragraph(reporte.datosquienreporta.dependencia.nombre, styles['LeftAligned'])
                ]
                
    
    doc.build(elements)

    # Obtener el PDF
    pdf = buffer.getvalue()
    buffer.close()
    
    #Guardar el pdf si no exite en media o reemplazarlo aún asi este creado
    with open(f'media/reportes3/reporte3_{reporte.usuario.identificacion}_periodo{reporte.periodo}.pdf', 'wb') as f:
        f.write(pdf)

    # Crear la respuesta HTTP con el PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="reporte_{reporte.id}.pdf"'
    response.write(pdf)

    return response




# Editar reporte
@login_required
def editar_reporte(request, reporte_id):
    reporte = get_object_or_404(Reporte, id=reporte_id)

    return render(request, 'reporteAportes/editar_reporte.html', {'reporte_id': reporte_id, 'reporte': reporte})        