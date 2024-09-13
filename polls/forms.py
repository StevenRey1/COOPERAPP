from django.forms import ModelForm, BooleanField, CharField, TextInput, Textarea
from polls.models import ReporteAcercamiento, AcercamientoCooperacion, NecesidadesCooperacion, DatosQuienReporta
from django import forms
import datetime

class ReporteAcercamientoForm(forms.ModelForm):
    class Meta:
        model = ReporteAcercamiento
        fields = ['fecha_elaboracion', 'periodo', 'desde', 'hasta']
        widgets = {
            'fecha_elaboracion': forms.DateInput(attrs={'readonly': 'readonly'}),  # Solo lectura
            'desde': forms.DateInput(format='%d/%m/%Y', attrs={'readonly': 'readonly'}),
            'hasta': forms.DateInput(format='%d/%m/%Y', attrs={'readonly': 'readonly'}),
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

            if periodo == '1':
                cleaned_data['desde'] = datetime.date(ano, 1, 1)
                cleaned_data['hasta'] = datetime.date(ano, 4, 30)
            elif periodo == '2':
                cleaned_data['desde'] = datetime.date(ano, 5, 1)
                cleaned_data['hasta'] = datetime.date(ano, 8, 31)
            elif periodo == '3':
                cleaned_data['desde'] = datetime.date(ano, 9, 1)
                cleaned_data['hasta'] = datetime.date(ano, 12, 31)
            else:
                self.add_error('periodo', 'Opción de período inválida.')

        return cleaned_data

class DatosQuienReportaForm(forms.ModelForm):
    class Meta:
        model = DatosQuienReporta
        exclude = ['reporte']  # Excluimos 'reporte' porque lo asignamos manualmente


    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # Pre-llenar el correo electrónico del usuario
        if user:
            self.fields['correo_electronico'].initial = 'EXAMPLE@GMAIL.COM'

        

class AcercamientoForm(ModelForm):
    class Meta:
        model = AcercamientoCooperacion
        fields = [ 'entidad', 'temas_perspectivas']
        widgets = {
            'entidad': TextInput(attrs={'class': 'form-control', 'placeholder': 'Texto máximo 20 palabras'}),
            'temas_perspectivas': Textarea(attrs={'class': 'form-control', 'placeholder': 'Texto máximo 100 palabras'}),
        }


class NecesidadesForm(ModelForm):
    class Meta:
        model = NecesidadesCooperacion
        fields = ['necesidad_identificado', 'necesidades_identificadas', 'cooperante_identificado', 'cooperante']
        widgets = {
            'necesidades_identificadas': Textarea(attrs={'class': 'form-control', 'placeholder': 'Texto máximo 50 palabras'}),
            'cooperante': TextInput(attrs={'class': 'form-control', 'placeholder': 'Texto máximo 15 palabras'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Ajusta los campos según los valores del formulario inicial
        necesidad_identificado = self.initial.get('necesidad_identificado', False)
        cooperante_identificado = self.initial.get('cooperante_identificado', False)

        self.fields['necesidades_identificadas'].required = necesidad_identificado
        self.fields['cooperante'].required = cooperante_identificado
