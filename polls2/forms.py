from django.forms import ModelForm, BooleanField, CharField, TextInput, Textarea
from polls2.models import ReporteAvances, DatosQuienReporta, DatosCooperante, LogrosAvances, ApoyoEventos
from django import forms
import datetime

class ReporteAvancesForm(forms.ModelForm):
    class Meta:
        model = ReporteAvances
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
        exclude = ['reporte']
        
        widgets = {
            'logros_avances_1': forms.TextInput(attrs={'placeholder': 'Logros y/o avances para Resultado 1'}),
            'departamento_1': forms.Select(choices=[
                ('departamento_1', 'Departamento 1'),
                ('departamento_2', 'Departamento 2'),
                ('departamento_3', 'Departamento 3')
            ]),
            'logros_avances_2': forms.TextInput(attrs={'placeholder': 'Logros y/o avances para Resultado 2'}),
            'departamento_2': forms.Select(choices=[
                ('departamento_1', 'Departamento 1'),
                ('departamento_2', 'Departamento 2'),
                ('departamento_3', 'Departamento 3')
            ]),
            'logros_avances_3': forms.TextInput(attrs={'placeholder': 'Logros y/o avances para Resultado 3'}),
            'departamento_3': forms.Select(choices=[
                ('departamento_1', 'Departamento 1'),
                ('departamento_2', 'Departamento 2'),
                ('departamento_3', 'Departamento 3')
            ]),
            'municipio_1': forms.Select(choices=[
                ('municipio_1', 'Municipio 1'),
                ('municipio_2', 'Municipio 2'),
                ('municipio_3', 'Municipio 3')
            ]),
            'municipio_2': forms.Select(choices=[
                ('municipio_1', 'Municipio 1'),
                ('municipio_2', 'Municipio 2'),
                ('municipio_3', 'Municipio 3')
            ]),
            'municipio_3': forms.Select(choices=[
               ('municipio_1', 'Municipio 1'),
                ('municipio_2', 'Municipio 2'),
                ('municipio_3', 'Municipio 3')
            ]),
            
            
            'logros_significativos': forms.Textarea(attrs={'rows': 3}),
            'dificultades': forms.Textarea(attrs={'rows': 3}),
            'detalle_riesgo': forms.TextInput(attrs={'placeholder': 'Detalle de la situación de riesgo'}),
            'observaciones_generales': forms.Textarea(attrs={'rows': 3}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        riesgo_relacionamiento = cleaned_data.get('riesgo_relacionamiento')
        detalle_riesgo = cleaned_data.get('detalle_riesgo')

        # Verificar que el campo "detalle_riesgo" sea obligatorio si "riesgo_relacionamiento" es True
        if riesgo_relacionamiento and not detalle_riesgo:
            self.add_error('detalle_riesgo', 'Este campo es obligatorio si hay una situación de riesgo.')
        
        return cleaned_data
    
OPCIONES_EVENTOS = [
    ('opcion_1', 'Jornadas de información / sensibilización'),
    ('opcion_2', 'Talleres de capacitación / formación'),
    ('opcion_3', 'Jornadas de atención y servicio'),
    ('opcion_4', 'Cursos de capacitación'),
    ('Otros', 'Otros'),

]
OPCIONES_PUBLICO = [
    ('opcion_1', 'Beneficiarios, solicitantes, comunidad en general'),
    ('opcion_2', 'Funcionarios y/o contratistas de la URT'),
    ('opcion_3', 'Funcionarios y/o contratistas de otras entidades'),
    ('Otros', 'Otros' ),
    
]
    
class ApoyoEventosForm(forms.ModelForm):
    opciones_eventos = forms.MultipleChoiceField(choices=OPCIONES_EVENTOS, widget=forms.CheckboxSelectMultiple)  # O puedes usar forms.SelectMultiple
    opciones_publico = forms.MultipleChoiceField(choices=OPCIONES_PUBLICO, widget=forms.CheckboxSelectMultiple)  # O puedes usar forms.SelectMultiple
    class Meta:
        model = ApoyoEventos
        fields = [ 'cantidad_eventos', 'opciones_eventos', 'otros_eventos', 'objetivo_principal', 'opciones_publico', 'otros_publicos', 'cantidad_participantes']
    def save(self, commit=True):
        ApoyoEventos = super().save(commit=False)
        ApoyoEventos.eventos_seleccionados = ','.join(self.cleaned_data['opciones_eventos'])  # Almacena como una cadena separada por comas
        ApoyoEventos.publico_seleccionados = ','.join(self.cleaned_data['opciones_publico'])  # Almacena como una cadena separada por comas
        if commit:
            ApoyoEventos.save()
        return ApoyoEventos

        
    

        
    
    

    