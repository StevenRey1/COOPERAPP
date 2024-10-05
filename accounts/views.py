from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from reporteAcercamientos.models import Reporte
from django.contrib.auth.decorators import login_required
from .utils import authenticate_ldap


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('accounts:listar_reportes')  # Redirige a una vista de tu elección
    else:
        form = UserCreationForm()

    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
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
            print(f'Ocurrió un error durante la autenticación: {e}')
            return render(request, 'accounts/login.html', {'error': 'Ocurrió un error durante la autenticación'})
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
    
    


def logout_view(request):
    from django.contrib.auth import logout
    logout(request)
    return redirect('login')  # Redirige a la vista de inicio de sesión