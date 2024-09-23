from django.forms import ModelForm, BooleanField, CharField, TextInput, Textarea
from reporteProgramas.models import  DatosCooperante, LogrosAvances, Logro, Departamento, Municipio,Resultado
from django import forms
from reporteAcercamientos.models import Reporte, DatosQuienReporta
import datetime
from django.forms import modelformset_factory

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
            

class DatosCooperanteForm(forms.ModelForm):
    class Meta:
        model = DatosCooperante
        exclude = ['reporte']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Campo "Nombre del Cooperante"
        self.fields['nombre_cooperante'].widget = forms.Select(choices=[
            # Aquí debes definir las opciones para el campo "nombre_cooperante"
            # Por ejemplo:
            ('opcion1', 'Opción 1'),
            ('opcion2', 'Opción 2'),
            ('otro', 'Otro'), 
        ])

        # Campo "Programa / Proyecto o plan"
        self.fields['programa_proyecto_plan'].widget = forms.Select(choices=[
              # Aquí debes definir las opciones para el campo "nombre_cooperante"
            # Por ejemplo:
            ('opcion1', 'Opción 1'),
            ('opcion2', 'Opción 2'),
            ('otro', 'Otro'), 
        ])

        # Campo "Línea de acción / componente"
        self.fields['linea_accion'].widget = forms.Select(choices=[
              # Aquí debes definir las opciones para el campo "nombre_cooperante"
            # Por ejemplo:
            ('opcion1', 'Opción 1'),
            ('opcion2', 'Opción 2'),
            ('otro', 'Otro'), 
        ])

        # Campo "Rol de quien reporta"
        self.fields['rol_quien_reporta'].widget = forms.Select(choices=[
              # Aquí debes definir las opciones para el campo "nombre_cooperante"
            # Por ejemplo:
            ('opcion1', 'Opción 1'),
            ('opcion2', 'Opción 2'),
            ('otro', 'Otro'), 
        ])

        # Campo "Nombre del implementador u operador" (readonly)
        self.fields['nombre_implementador'].widget.attrs.update({'readonly': 'readonly'})
        self.fields['nombre_implementador'].initial = 'Automático'
        


class LogrosAvancesForm(forms.ModelForm):
    class Meta:
        model = LogrosAvances
        fields = [
            'riesgo_relacionamiento',
            'logros_significativos',
            'dificultades',
            'detalle_riesgo',
            'observaciones_generales',
        ]
        
        widgets = {
            'logros_significativos': forms.Textarea(attrs={'rows': 4, 'cols': 180}),
            'dificultades': forms.Textarea(attrs={'rows': 4, 'cols': 180}),
            'detalle_riesgo': forms.Textarea(attrs={'rows': 4, 'cols': 180}),
            'observaciones_generales': forms.Textarea(attrs={'rows': 4, 'cols': 180}),
        }

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
            'municipio': forms.Select(attrs={'disabled': 'disabled'}),  # Desactiva inicialmente
            'resultado': forms.Select(attrs={'disabled': 'disabled'}),  # Desactiva inicialmente
        }
        


   


    

LogroFormSet = modelformset_factory(Logro, form=LogroForm, extra=1, can_delete=True)
    

    

        
    
    

    