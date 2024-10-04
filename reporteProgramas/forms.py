
from typing import Any
from reporteProgramas.models import  LogrosAvances, Logro, DatosCooperante
from django import forms
from reporteAcercamientos.models import Reporte, DatosQuienReporta
import datetime
from django.forms import modelformset_factory, inlineformset_factory
from django.core.exceptions import ValidationError

def validar_max_palabras(value, max_palabras=5):
    if not value:
        return
    num_palabras = len(value.split())
    if num_palabras > max_palabras:
        raise ValidationError(f'El texto no puede exceder las {max_palabras} palabras. Actualmente tienes {num_palabras} palabras.')
    

class ReporteAvancesForm(forms.ModelForm):
    class Meta:
        model = Reporte
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

class LogrosAvancesForm(forms.ModelForm):
    class Meta:
        model = LogrosAvances
        exclude = ['reporte']
        widgets = {
            'logros_significativos': forms.Textarea(attrs={'class':'form-control','rows':1, 'placeholder': 'Máximo 50 palabras'}),
            'dificultades': forms.Textarea(attrs={'class':'form-control', 'rows':1, 'placeholder': 'Máximo 50 palabras'}),
            'detalle_riesgo': forms.Textarea(attrs={'class':'form-control','rows':1, 'placeholder': 'Máximo 50 palabras'}),
            'observaciones_generales': forms.Textarea(attrs={'class':'form-control','rows':1, 'placeholder': 'Máximo 50 palabras'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        logros_significativos = cleaned_data.get('logros_significativos')
        dificultades = cleaned_data.get('dificultades')
        observaciones_generales = cleaned_data.get('observaciones_generales')
        detalle_riesgo = cleaned_data.get('detalle_riesgo')
        validar_max_palabras(detalle_riesgo, max_palabras=50)
        validar_max_palabras(logros_significativos, max_palabras=50)
        validar_max_palabras(dificultades, max_palabras=50)
        validar_max_palabras(observaciones_generales, max_palabras=50)

        return cleaned_data

class LogroForm(forms.ModelForm):
    class Meta:
        model = Logro
        fields = [
            'resultado',
            'logros_avances_texto',
            'departamento',
            'municipio',
            'adjunto',
        ]
        widgets = {
            'resultado': forms.HiddenInput(),
            'municipio': forms.Select(attrs={'class':'form-control','disabled': 'disabled', 'required':'required'}),
            'logros_avances_texto': forms.Textarea(attrs={'required':'required','class':'form-control', 'placeholder': 'Máximo 50 palabras', 'rows': 1}),
            'departamento': forms.Select(attrs={'class':'form-control', 'required':'required'}),
            'adjunto': forms.FileInput(attrs={'class':'form-control', 'accept': 'application/pdf,image/*', 'required':'required'}),
        }
    def clean(self):
        cleaned_data = super().clean()
        logros_avances_texto = cleaned_data.get('logros_avances_texto')
        validar_max_palabras(logros_avances_texto, max_palabras=50)
        return cleaned_data


LogroFormSet = inlineformset_factory(LogrosAvances, Logro, form=LogroForm, extra=0)  

    
class  DatosCooperanteForm(forms.ModelForm):
    class Meta:
        model = DatosCooperante
        fields = ['cooperante', 'identificacion', 'operador', 'proyecto_plan', 'linea_accion']
        widgets = {
            'cooperante': forms.Select(attrs={'class':'form-control', 'required':'required'}),
            'identificacion': forms.Select(attrs={'class':'form-control', 'required':'required', 'disabled': 'disabled'}),
            'operador': forms.Select(attrs={'class':'form-control', 'required':'required', 'disabled': 'disabled'}),
            'proyecto_plan': forms.Select(attrs={'class':'form-control', 'required':'required', 'disabled': 'disabled'}),
            'linea_accion': forms.Select(attrs={'class':'form-control', 'required':'required', 'disabled': 'disabled'}),
        }
        
    
    

    