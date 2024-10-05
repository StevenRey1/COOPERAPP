from django.forms import ModelForm, BooleanField, CharField, TextInput, Textarea, modelformset_factory
from reporteAcercamientos.models import Reporte, AcercamientoCooperacion, NecesidadesCooperacion, DatosQuienReporta, Rol, Dependencia
from django import forms
from django.core.exceptions import ValidationError
import datetime

class ReporteForm(forms.ModelForm):
    class Meta:
        model = Reporte
        fields = ['fecha_elaboracion', 'periodo', 'desde', 'hasta']
        widgets = {
            'fecha_elaboracion': forms.DateInput(attrs={'class':'form-control', 'readonly': 'readonly'}),  # Solo lectura
            'periodo': forms.Select(attrs={'class':'form-control'}),
            'desde': forms.DateInput(format='%d/%m/%Y', attrs={'class':'form-control','readonly': 'readonly', }),  # Solo lectura y deshabilitado
            'hasta': forms.DateInput(format='%d/%m/%Y', attrs={'class':'form-control','readonly': 'readonly', }),  # Solo lectura y deshabilitado
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['fecha_elaboracion'].initial = datetime.date.today()  # Mostrar la fecha actual
        self.fields['periodo'].widget.attrs.update({'onchange': 'updateFechas()'})

    def clean(self):
        cleaned_data = super().clean()
        periodo = cleaned_data.get('periodo')

        if periodo:
            hoy = datetime.date.today()
            ano = hoy.year

            if periodo == 1:
                cleaned_data['desde'] = datetime.date(ano, 1, 1)
                cleaned_data['hasta'] = datetime.date(ano, 4, 30)
            elif periodo == 2:
                cleaned_data['desde'] = datetime.date(ano, 5, 1)
                cleaned_data['hasta'] = datetime.date(ano, 8, 31)
            elif periodo == 3:
                cleaned_data['desde'] = datetime.date(ano, 9, 1)
                cleaned_data['hasta'] = datetime.date(ano, 12, 31)
            else:
                self.add_error('periodo', 'Opción de período inválida.')

        return cleaned_data

class DatosQuienReportaForm(forms.ModelForm):
    class Meta:
        model = DatosQuienReporta
        exclude = ['reporte']  # Excluimos 'reporte' porque lo asignamos manualmente
        widgets = {
            'nombre_completo': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'correo_electronico_sesion': forms.EmailInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'dependencia': forms.Select(attrs={'class': 'form-control'}),
            'rol': forms.Select(attrs={'class': 'form-control'}),
            'correo_electronico_institucional': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'nombre.apellido@urt.gov.co'}),
        }
        
    def clean_correo_electronico_institucional(self):
        correo = self.cleaned_data.get('correo_electronico_institucional')
        if correo and not correo.endswith('@urt.gov.co'):
            raise ValidationError("El correo debe terminar en @urt.gov.co")
        return correo

class AcercamientoForm(forms.ModelForm):
    class Meta:
        model = AcercamientoCooperacion
        fields = ['entidad', 'temas_perspectivas']
        widgets = {
            'entidad': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Texto máximo 20 palabras' , 'required': 'required'}),
            'temas_perspectivas': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Texto máximo 100 palabras', 'rows':3, 'required': 'required'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Asegurando que los campos sean requeridos
        self.fields['entidad'].required = True
        self.fields['temas_perspectivas'].required = True
        
        
AcercamientoFormSet = modelformset_factory(
    AcercamientoCooperacion,
    form=AcercamientoForm,
    extra=1,
    can_delete=True
)

class NecesidadesForm(ModelForm):
    class Meta:
        model = NecesidadesCooperacion
        fields = ['necesidad_identificado', 'necesidades_identificadas', 'cooperante_identificado', 'cooperante']
        widgets = {
            'necesidades_identificadas': Textarea(attrs={'class': 'form-control', 'rows':3, 'placeholder': 'Texto máximo 50 palabras'}),
            'cooperante': TextInput(attrs={'class': 'form-control', 'placeholder': 'Texto máximo 15 palabras'}),
        }

    