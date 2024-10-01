from django.shortcuts import render, redirect, get_object_or_404
from . forms import ApoyoEventosForm, ApoyoViajesForm, ApoyoMaterialFormSet, ApoyoHerramientasFormSet, \
                    ApoyoLitigioFormSet, ApoyoSeguridadAlimentariaFormSet, ApoyoOrdenesJudicialesForm, ApoyoArchivoHistoricoForm, OtrosApoyosForm, \
                    EstimacionEconomicaForm, ApoyoTerritorioUbicacionFormset, ApoyoTerritoriosForm, ApoyoContratacionForm, ContratacionDetalle,  ContratacionDetalleForm
from django.forms.models import inlineformset_factory
from .models import TipoPersonal, AreaProfesional, TipoMaterial, TipoHerramienta, TipoCaso, TipoProyecto , TipoApoyo, \
                    ApoyoTerritorios, ApoyoContratacion


from reporteAcercamientos.models import Reporte

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

            return redirect('reporteAportes:crear_apoyo_material')  # Redirige a una página de éxito
        else:
            print("Form errors:", form.errors)
            print("Formset errors:", formset.errors)
            context = {
                'form': form,
                'formset': formset,
                'tipos_personal': tipos_personal,
                'area_profesional': area_profesional,
            }
            return render(request, 'reporteAportes/crear_apoyo_contratacion.html', context)  # Renderiza la plantilla con errores

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

def crear_apoyo_material(request,reporte_id):
    
    tipo_material = TipoMaterial.objects.all()

    if request.method == 'POST':
        formset = ApoyoMaterialFormSet(request.POST)
        if formset.is_valid():
            formset.save()  # Guarda los datos del formset
                    
            return redirect('reporteAportes:crear_apoyo_herramientas')  # Reemplaza con la URL correcta
    else:
        formset = ApoyoMaterialFormSet()

    context = {
        'formset': formset,
        'tipo_material': tipo_material,
    }
    return render(request, 'reporteAportes/crear_apoyo_material.html', context)


def crear_apoyo_herramientas(request, reporte_id):
    reporte = Reporte.objects.get(id=reporte_id)
    tipos_herramienta = TipoHerramienta.objects.all()

    if request.method == 'POST':
        formset = ApoyoHerramientasFormSet(request.POST)
        if formset.is_valid():
            for form in formset:
                apoyo = form.save(commit=False)
                apoyo.reporte = reporte  # Ensure you are setting the report here
                apoyo.save()
            reporte.avance = 9
            reporte.save()   
            return redirect('reporteAportes:crear_apoyo_litigio')  # Update with the correct URL
        else:
            print(formset.errors)
    else:
        initial_data = [{'tipo_herramienta': tipo.id} for tipo in tipos_herramienta]
        formset = ApoyoHerramientasFormSet(initial=initial_data)

    context = {
        'formset': formset,
        'tipos_herramienta': tipos_herramienta,
    }
    return render(request, 'reporteAportes/crear_apoyo_herramientas.html', context)

def crear_apoyo_litigio(request, reporte_id):
    reporte = Reporte.objects.get(id=reporte_id)
    tipos_caso = TipoCaso.objects.all()

    if request.method == 'POST':
        formset = ApoyoLitigioFormSet(request.POST)
        if formset.is_valid():
            for form in formset:
                apoyo = form.save(commit=False)
                apoyo.reporte = reporte
                apoyo.save()
            reporte.avance = 10
            reporte.save()
            return redirect('reporteAportes:crear_apoyo_seguridad_alimentaria')
        else:
            print(formset.errors)
    else:
        initial_data = [{'tipo_caso': tipo.id} for tipo in tipos_caso]
        formset = ApoyoLitigioFormSet(initial=initial_data)
    context = {
        'formset': formset,
        'tipos_caso': tipos_caso,
    }
    return render(request, 'reporteAportes/crear_apoyo_litigio.html', context)



def crear_apoyo_seguridad_alimentaria(request,reporte_id):
    
    tipos_proyecto = TipoProyecto.objects.all()
    tipos_apoyo = TipoApoyo.objects.all()

    if request.method == 'POST':
        formset = ApoyoSeguridadAlimentariaFormSet(request.POST)
        if formset.is_valid():
            for form in formset:
                form.save()
            return redirect('accounts:listar_reportes')  # Reemplaza con la URL adecuada
    else:
        initial_data = [{'tipo_proyecto': tipo.id} for tipo in tipos_proyecto]
        formset = ApoyoSeguridadAlimentariaFormSet(initial=initial_data)

    context = {
        'formset': formset,
        'tipos_proyecto': tipos_proyecto,
        'tipos_apoyo': tipos_apoyo,
    }
    return render(request, 'reporteAportes/crear_apoyo_seguridad_alimentaria.html', context)

def crear_apoyo_ordenes_judiciales(request,reporte_id):
    
    if request.method == 'POST':
        form = ApoyoOrdenesJudicialesForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('accounts:listar_reportes')  # Reemplaza con la URL correcta
    else:
        form = ApoyoOrdenesJudicialesForm()

    context = {
        'form': form,
        
    }
    return render(request, 'reporteAportes/crear_apoyo_ordenes_judiciales.html', context)

def crear_apoyo_archivo_historico(request,reporte_id):
    
    if request.method == 'POST':
        form = ApoyoArchivoHistoricoForm(request.POST)
        if form.is_valid():
            form.save_m2m()  # Guarda las relaciones ManyToMany
            return redirect('accounts:listar_reportes')  # Reemplaza con la URL correcta
    else:
        form = ApoyoArchivoHistoricoForm()

    context = {
        'form': form,
    }
    return render(request, 'reporteAportes/crear_apoyo_archivo_historico.html', context)

def crear_otros_apoyos(request,reporte_id):
    
    
    if request.method == 'POST':
        form = OtrosApoyosForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('accounts:listar_reportes') # Reemplaza con la URL adecuada
    else:
        form = OtrosApoyosForm()
        
    context = {
        'form': form,

    }
    return render(request, 'reporteAportes/crear_otros_apoyos.html', context)

def crear_estimacion_economica(request,reporte_id):
    
    if request.method == 'POST':
        form = EstimacionEconomicaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('accounts:listar_reportes')  # Reemplaza con la URL correcta
    else:
        form = EstimacionEconomicaForm()

    context = {
        'form': form,
        
    }
    return render(request, 'reporteAportes/crear_estimacion_economica.html', context)