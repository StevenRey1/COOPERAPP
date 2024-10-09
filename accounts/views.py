from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from reporteAcercamientos.models import Reporte
from django.contrib.auth.decorators import login_required
from .utils import authenticate_ldap


def login_view(request):
    
    if request.user.is_authenticated:
        return redirect('accounts:listar_reportes')  # Redirigir a la vista deseada
    
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username or not password:
            return render(request, 'accounts/login.html', {'error': 'Por favor, ingrese usuario y contraseña'})

        try:
            user = authenticate_ldap(username, password)
            # tomar el id del usuario autenticado
            session_id = user.id
            print(f'El id del usuario autenticado es: {session_id}')
            # guardar el id en la sesión
            request.session['user_id'] = session_id
            login(request, user)  # Asegúrate de usar el login de Django
            return redirect('accounts:listar_reportes')  # Redirige a una vista de tu elección
            
        except Exception as e:
            form = AuthenticationForm()
            print(f'Ocurrió un error durante la autenticación: {e}')
            return render(request, 'accounts/login.html', {'error': 'Ocurrió un error durante la autenticación' ,'form': form} )
    else:
        form = AuthenticationForm()
        return render(request, 'accounts/login.html', {'form': form})  # Asegúrate de pasar el formulario al render


@login_required
def listar_reportes(request):
    user_id = request.user.id
    reportes= Reporte.objects.filter(usuario=user_id).order_by('periodo')
    context = {     
        'reportes': reportes
    }
    return render(request, 'accounts/listar_reportes.html', context)
    

@login_required
def logout_view(request):
    logout(request)  # Cierra la sesión del usuario
    return redirect('accounts:login')  # Redirige a la página de inicio de sesión


