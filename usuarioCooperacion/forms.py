from .models import UsuarioCooperacion
from django import forms
from reporteAcercamientos.models import Dependencia



# Este formulario servirá para buscar al usuario
class BuscarUsuarioForm(forms.Form):
    email = forms.EmailField(label="Correo Electrónico", max_length=100)
    
    

#crear formulario para crear usuario
class CrearUsuarioCooperacionForm(forms.ModelForm):
    class Meta:
        model = UsuarioCooperacion
        fields = ['nombre', 'email', 'telefono', 'rol', 'dependencia']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'rol': forms.Select(attrs={'class': 'form-control'}),
            'dependencia': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'nombre': 'Nombre',
            'email': 'Correo electrónico',
            'telefono': 'Teléfono',
            'rol': 'Rol',
            'dependencia': 'Dependencia'
        }
        
    def clean_telefono(self):
        
        telefono = self.cleaned_data.get('telefono')
        return telefono




# Formulario para buscar por dependencia
# Formulario actualizado para buscar por dependencia usando un Select
class BuscarPorDependenciaForm(forms.Form):
    dependencia = forms.ModelChoiceField(
        queryset=Dependencia.objects.all(),
        label="Dependencia",
        empty_label="Seleccione una dependencia",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

