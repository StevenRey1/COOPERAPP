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
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('accounts:listar_reportes')  # Redirige a una vista de tu elección
    else:
        form = AuthenticationForm()

    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    from django.contrib.auth import logout
    logout(request)
    return redirect('login')  # Redirige a la vista de inicio de sesión


""" def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            user_data = authenticate_ldap(username, password)
            request.session['user_data'] = user_data
            return redirect('accounts:listar_reportes')
        except Exception as e:
            print(e)
            return render(request, 'accounts/login.html', {'error': 'Usuario o contraseña incorrectos'}) """


@login_required
def listar_reportes(request):
    reportes= Reporte.objects.filter(usuario=request.user).order_by('periodo')
    context = {
        'reportes': reportes
    }
    return render(request, 'accounts/listar_reportes.html', context)
    