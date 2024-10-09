from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .forms import CrearUsuarioCooperacionForm, BuscarUsuarioForm, BuscarPorDependenciaForm
from .models import UsuarioCooperacion
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from reporteAcercamientos.models import Dependencia
from django.contrib.auth.decorators import login_required
# Create your views here.
#Vista para crear usuario 
@login_required
def crear_usuario_cooperacion(request):
    if request.method == 'POST':
        form = CrearUsuarioCooperacionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('accounts:listar_reportes')  # Redirigir después de guardar
    else:
        form = CrearUsuarioCooperacionForm()  # Manejar GET para mostrar el formulario

    # Asegúrate de que siempre se devuelva una respuesta
    return render(request, 'usuarioCooperacion/crear_usuario_cooperacion.html', {'form': form})
@login_required
def buscar_usuario_cooperacion(request):
    usuario = None
    if request.method == 'POST':
        buscar_form = BuscarUsuarioForm(request.POST)

        # Si el formulario de búsqueda es válido
        if buscar_form.is_valid():
            email = buscar_form.cleaned_data['email']
            try:
                usuario = UsuarioCooperacion.objects.get(email=email)  # Buscar usuario por correo
            except UsuarioCooperacion.DoesNotExist:
                usuario = None

    else:
        buscar_form = BuscarUsuarioForm()  # Mostrar el formulario vacío

    # Si se encontró el usuario, mostrar el formulario prellenado con los datos
    if usuario:
        form = CrearUsuarioCooperacionForm(instance=usuario)
    else:
        form = None  # No mostrar el formulario si no se encontró el usuario

    return render(request, 'usuarioCooperacion/buscar_usuario_cooperacion.html', {
        'buscar_form': buscar_form,
        'form': form,
        'usuario': usuario
    })
@login_required
def editar_usuario_cooperacion(request, usuario_id):
    usuario = get_object_or_404(UsuarioCooperacion, id=usuario_id)

    if request.method == 'POST':
        form = CrearUsuarioCooperacionForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            return redirect('accounts:listar_reportes')  # Redirigir después de guardar
    else:
        form = CrearUsuarioCooperacionForm(instance=usuario)  # Mostrar el formulario prellenado

    return render(request, 'usuarioCooperacion/editar_usuario_cooperacion.html', {
        'form': form,
        'usuario': usuario
    })

# Vista para buscar usuarios por dependencia
@login_required
def buscar_por_dependencia(request):
    usuarios = None

    if request.method == 'POST':
        buscar_form = BuscarPorDependenciaForm(request.POST)
        if buscar_form.is_valid():
            dependencia = buscar_form.cleaned_data['dependencia']
            # Buscar usuarios por dependencia
            usuarios = UsuarioCooperacion.objects.filter(dependencia=dependencia)
    else:
        buscar_form = BuscarPorDependenciaForm()

    return render(request, 'usuarioCooperacion/buscar_por_dependencia.html', {
        'buscar_form': buscar_form,
        'usuarios': usuarios,
    })

# Vista para generar PDF con los usuarios
@login_required
def generar_pdf_usuarios(request, dependencia):
    # Buscar usuarios por dependencia
    usuarios = UsuarioCooperacion.objects.filter(dependencia=dependencia)
    nombre_dependencia = Dependencia.objects.get(id=dependencia).nombre
    
    # Crear response que será un PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{nombre_dependencia}.pdf"'
    
    # Crear el documento PDF
    doc = SimpleDocTemplate(response, pagesize=letter)
    
    # Datos para la tabla (encabezado y cuerpo)
    data_header = [
        ['Nombre dependencia', nombre_dependencia],
        ['Nombre del usuario', 'Rol de usuario' , 'Correo Electrónico', 'Número de teléfono']
    ]
    
    # Agregar los datos de los usuarios
    data = [
        [usuario.nombre, usuario.rol.nombre, usuario.email, usuario.telefono]
        for usuario in usuarios
    ]
    
    # Unir encabezado con datos
    elements = data_header + data
    
    # Crear la tabla
    table = Table(elements)
    
    # Aplicar estilos a la tabla
    table.setStyle(TableStyle([
        ('SPAN', (1, 0), (-1, 0)),  # Unir celdas para el nombre de la dependencia
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Alinear todo el contenido al centro
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Negrita para la fila de dependencia
        ('FONTNAME', (0, 1), (-1, 1), 'Helvetica-Bold'),  # Negrita para encabezado
        ('GRID', (0, 0), (-1, -1), 1, colors.black),  # Bordes negros en la tabla
    ]))
    
    # Crear el flujo del documento
    elements = [table]
    
    # Construir el PDF
    doc.build(elements)
    
    return response
    

    
    

   