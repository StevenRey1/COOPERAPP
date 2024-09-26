from django.shortcuts import render, redirect
from . forms import ApoyoEventosForm, ApoyoViajesForm, ApoyoTerritoriosForm, ApoyoContratacionFormSet, ApoyoMaterialFormSet, ApoyoHerramientasFormSet, \
                    ApoyoLitigioFormSet, ApoyoSeguridadAlimentariaFormSet, ApoyoOrdenesJudicialesForm, ApoyoArchivoHistoricoForm, OtrosApoyosForm, \
                    EstimacionEconomicaForm
from .models import TipoPersonal, AreaProfesional, TipoMaterial, TipoHerramienta, TipoCaso, TipoProyecto , TipoApoyo

def crear_apoyo_eventos(request):
    if request.method == 'POST':
        form = ApoyoEventosForm(request.POST)
        if form.is_valid():
            form.save()  # Guarda el informe con los eventos seleccionados
            return redirect('accounts:listar_reportes')  # Redirige a otra vista después de guardar
    else:
        form = ApoyoEventosForm()

    return render(request, 'reporteAportes/crear_apoyo_eventos.html', {'form': form})


def crear_apoyo_viajes(request):
    if request.method == 'POST':
        form = ApoyoViajesForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('viajes_success')  # Redirige a una página de éxito
    else:
        form = ApoyoViajesForm()

    return render(request, 'reporteAportes/crear_apoyo_viajes.html', {'form': form})



def crear_apoyo_territorios(request):
    if request.method == 'POST':
        form = ApoyoTerritoriosForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('accounts:listar_reportes')  # Reemplaza con la URL adecuada
        else:
            print(form.errors)  # Consider using logging instead of print for production

    else:
        form = ApoyoTerritoriosForm()

    return render(request, 'reporteAportes/crear_apoyo_territorios.html', {'form': form})


def crear_apoyo_contratacion(request):
    tipos_personal = TipoPersonal.objects.all()
    area_profesional = AreaProfesional.objects.all()

    if request.method == 'POST':
        formset = ApoyoContratacionFormSet(request.POST)
        # ... (guardar datos si el formset es válido)

    else:
        initial_data = [{'tipo_personal': tipo.id} for tipo in tipos_personal]  # ID en los datos iniciales
        formset = ApoyoContratacionFormSet(initial=initial_data)

    context = {
        'formset': formset,
        'tipos_personal': tipos_personal,  # Pass the entire queryset
        'area_profesional': area_profesional,
    }
    return render(request, 'reporteAportes/crear_apoyo_contratacion.html', context)


def crear_apoyo_material(request):
    
    tipo_material = TipoMaterial.objects.all()

    if request.method == 'POST':
        formset = ApoyoMaterialFormSet(request.POST)
        if formset.is_valid():
            formset.save()  # Guarda los datos del formset
                    
            return redirect('accounts:listar_reportes')  # Reemplaza con la URL correcta
    else:
        formset = ApoyoMaterialFormSet()

    context = {
        'formset': formset,
        'tipo_material': tipo_material,
    }
    return render(request, 'reporteAportes/crear_apoyo_material.html', context)


def crear_apoyo_herramientas(request):
    
    tipos_herramienta = TipoHerramienta.objects.all()

    if request.method == 'POST':
        formset = ApoyoHerramientasFormSet(request.POST)
        if formset.is_valid():
            formset.save()
                    
            return redirect('accounts:listar_reportes')  # Reemplaza con la URL adecuada
    else:
        initial_data = [{'tipo_herramienta': tipo.id} for tipo in tipos_herramienta]
        formset = ApoyoHerramientasFormSet(initial=initial_data)

    context = {
        'formset': formset,
        'tipos_herramienta': tipos_herramienta,
    }
    return render(request, 'reporteAportes/crear_apoyo_herramientas.html', context)


def crear_apoyo_litigio(request):
    tipos_caso = TipoCaso.objects.all()

    if request.method == 'POST':
        formset = ApoyoLitigioFormSet(request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('accounts:listar_reportes')  # Reemplaza con la URL correcta
    else:
        initial_data = [{'tipo_caso': tipo.id} for tipo in tipos_caso]
        formset = ApoyoLitigioFormSet(initial=initial_data)
        print(initial_data)
    context = {
        'formset': formset,
        'tipos_caso': tipos_caso,
    }
    return render(request, 'reporteAportes/crear_apoyo_litigio.html', context)


def crear_apoyo_seguridad_alimentaria(request):
    
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

def crear_apoyo_ordenes_judiciales(request):
    
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

def crear_apoyo_archivo_historico(request):
    
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

def crear_otros_apoyos(request):
    
    
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

def crear_estimacion_economica(request):
    
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