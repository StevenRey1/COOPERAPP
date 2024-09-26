
from django import forms
from django.core.exceptions import ValidationError
from .models import ApoyoEventos,ApoyoViajes,ObjetivoViaje, ApoyoTerritorios,ApoyoContratacion,ApoyoMaterial ,\
                    ApoyoHerramientas, ApoyoLitigio, ApoyoSeguridadAlimentaria, ApoyoOrdenesJudiciales, ApoyoArchivoHistorico, \
                    OtrosApoyos,EstimacionEconomica




# Validador personalizado para contar palabras
def validar_max_palabras(value, max_palabras=5):
    num_palabras = len(value.split())
    if num_palabras > max_palabras:
        raise ValidationError(f'El texto no puede exceder las {max_palabras} palabras. Actualmente tienes {num_palabras} palabras.')

class ApoyoEventosForm(forms.ModelForm):
    class Meta:
        model = ApoyoEventos
        exclude = ['reporte']
        widgets = {
            'cantidad_eventos': forms.NumberInput(attrs={'class': 'form-control w-25', 'min': 0, 'max': 999}),
            'eventos': forms.CheckboxSelectMultiple(),  # Checkbox para "eventos"
            'publico_objetivo': forms.CheckboxSelectMultiple(),
            'otros_eventos': forms.CheckboxInput(attrs={'class': 'otros-eventos-checkbox'}),  # Checkbox para "otros eventos"
            'cuales_eventos': forms.TextInput(attrs={'class': 'form-control', 'disabled': True}),  # Campo que se habilita/deshabilita
            'otro_publico': forms.CheckboxInput(attrs={'class': 'otro-publico-checkbox'}),  # Checkbox para "otro público"
            'cual_publico': forms.TextInput(attrs={'class': 'form-control', 'disabled': True}),  # Campo que se habilita/deshabilita
            'cantidad_participantes': forms.NumberInput(attrs={'class': 'form-control w-25', 'min': 0, 'max': 9999}),
        }
    
    objetivo_principal = forms.CharField(
        label="Objetivo principal",
        validators=[lambda value: validar_max_palabras(value, max_palabras=120)],  # Usar la función directamente
        required=True,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 160, 'placeholder': 'Texto máximo de 120 palabras'})
    )

class ApoyoViajesForm(forms.ModelForm):
    objetivo_viajes = forms.ModelMultipleChoiceField(
        queryset=ObjetivoViaje.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label="Objeto de los viajes",
        required=False
    )

    class Meta:
        model = ApoyoViajes
        fields = [
            'cantidad_locales', 
            'cantidad_nacionales', 
            'cantidad_internacionales', 
            'objetivo_viajes', 
            'cuales_otros',
            'resaltado_apoyo'
        ]
        widgets = {
            'cantidad_locales': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 999}),
            'cantidad_nacionales': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 999}),
            'cantidad_internacionales': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 999}),
            'cuales_otros': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Se activa cuando selecciona otros'}),
            'resaltado_apoyo': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Texto máximo 100 palabras', 'rows': 3}),
        }

    def clean(self):
        cleaned_data = super().clean()
        objetivo_viajes = cleaned_data.get('objetivo_viajes')
        cuales_otros = cleaned_data.get('cuales_otros')

        # Validar que "cuales_otros" solo se rellene si se selecciona "otros"
        otros = ObjetivoViaje.objects.filter(nombre='Otros').first()
        if otros in objetivo_viajes and not cuales_otros:
            self.add_error('cuales_otros', 'Por favor, especifique los otros viajes.')
        return cleaned_data
    


class ApoyoTerritoriosForm(forms.ModelForm):
    class Meta:
        model = ApoyoTerritorios
        fields = '__all__'
        widgets = {
            'departamento': forms.Select(attrs={'class': 'form-select', 'required': 'required'}),
            'municipio': forms.Select(attrs={'class': 'form-select', 'required': 'required', 'disabled': 'disabled'}),
            'vereda': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Texto máximo 20 palabras', 'required': 'required'}),
            'apoyo_recibido': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Texto máximo 50 palabras', 'required': 'required'}),
            'tipo_visitas': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Texto máximo 100 palabras', 'required': 'required'}),
            'cantidad_visitas': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 999, 'required': 'required'}),
            'resaltar_apoyo': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Texto máximo 100 palabras', 'required': 'required'}),
        }

    
class ApoyoContratacionForm(forms.ModelForm):
    class Meta:
        model = ApoyoContratacion
        fields = '__all__'
        widgets = {
            'tipo_personal': forms.HiddenInput(),
            'cantidad_personas': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 999}),
            'tiempo_servicio': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 99}),
            'area_profesional': forms.Select(attrs={'class': 'form-select'}),
            'otro_tipo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Texto máximo 5 palabras'}),
            'objetivo_contratos': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Texto máximo 120 palabras'}),
            'resaltar_apoyo': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Texto máximo 100 palabras'}),
        }

    def clean_otro_tipo(self):
        data = self.cleaned_data['otro_tipo']
        if len(data.split()) > 5:
            raise forms.ValidationError("El texto no puede exceder 5 palabras.")
        return data

    def clean_objetivo_contratos(self):
        data = self.cleaned_data['objetivo_contratos']
        if len(data.split()) > 120:
            raise forms.ValidationError("El texto no puede exceder 120 palabras.")
        return data

    def clean_resaltar_apoyo(self):
        data = self.cleaned_data['resaltar_apoyo']
        if len(data.split()) > 100:
            raise forms.ValidationError("El texto no puede exceder 100 palabras.")
        return data

ApoyoContratacionFormSet = forms.formset_factory(
    ApoyoContratacionForm, 
    extra=0  # No crear formularios extra 
)



class ApoyoMaterialForm(forms.ModelForm):
    class Meta:
        model = ApoyoMaterial
        fields = '__all__'
        widgets = {
            'titulo_material': forms.TextInput(attrs={'class': 'form-control'}),
            'objetivo_principal': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'publico_destinatario': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo_material': forms.Select(attrs={'class': 'form-select'}),
            'cantidad_originales': forms.NumberInput(attrs={'class': 'form-control'}),
            'cantidad_reproducciones': forms.NumberInput(attrs={'class': 'form-control'}),
            'resaltar_apoyo': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Texto máximo 100 palabras'}),
        }

ApoyoMaterialFormSet = forms.formset_factory(ApoyoMaterialForm, extra=3)



class ApoyoHerramientasForm(forms.ModelForm):
    class Meta:
        model = ApoyoHerramientas
        fields = '__all__'
        widgets = {
            'tipo_herramienta': forms.HiddenInput(),
            'cantidad_recibida': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 999}),
            'descripcion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Texto máx. 20 palabras'}),
            'observaciones': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Texto máx. 20 palabras'}),
        }

ApoyoHerramientasFormSet = forms.formset_factory(ApoyoHerramientasForm, extra=0)




class ApoyoLitigioForm(forms.ModelForm):
    class Meta:
        model = ApoyoLitigio
        fields = '__all__'
        widgets = {
            'tipo_caso': forms.HiddenInput(),
            'nombre_caso': forms.TextInput(attrs={'class': 'form-control'}),
            'cantidad_ids': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 999}),
            'otro_tipo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Texto máximo 5 palabras'}),
            'resaltar_apoyo': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Texto máximo 150 palabras'}),
        }

ApoyoLitigioFormSet = forms.formset_factory(ApoyoLitigioForm, extra=0)




class ApoyoSeguridadAlimentariaForm(forms.ModelForm):
    class Meta:
        model = ApoyoSeguridadAlimentaria
        fields = '__all__'
        widgets = {
            'tipo_proyecto': forms.HiddenInput(),
            'cantidad_proyectos': forms.NumberInput(attrs={'class': 'form-control'}),
            'cantidad_familias': forms.NumberInput(attrs={'class': 'form-control'}),
            'tipo_apoyo': forms.CheckboxSelectMultiple(),
            'otro_apoyo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Se activa cuando se selecciona la opción otros'}),
            'resaltar_apoyo': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Texto máximo 120 palabras'}),
        }

ApoyoSeguridadAlimentariaFormSet = forms.formset_factory(ApoyoSeguridadAlimentariaForm, extra=0)


class ApoyoOrdenesJudicialesForm(forms.ModelForm):
    class Meta:
        model = ApoyoOrdenesJudiciales
        fields = '__all__'
        widgets = {
            'tipo_apoyo': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Texto máximo 120 palabras'}),
            'tipo_ordenes': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Texto máximo 120 palabras'}),
            'cantidad_sentencias': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 999}),
            'cantidad_ordenes': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 999}),
        }

class ApoyoArchivoHistoricoForm(forms.ModelForm):
    class Meta:
        model = ApoyoArchivoHistorico
        fields = '__all__'
        widgets = {
            'acciones': forms.CheckboxSelectMultiple(),
            'cuales_acciones': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Se activa cuando se selecciona la opción otros'}),
            'comentarios': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Texto máximo 100 palabras'}),
        }

class OtrosApoyosForm(forms.ModelForm):
    class Meta:
        model = OtrosApoyos
        fields = ['descripcion']
        widgets = {
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Texto máximo 150 palabras'}),
        }

class EstimacionEconomicaForm(forms.ModelForm):
    class Meta:
        model = EstimacionEconomica
        fields = '__all__'
        widgets = {
            'valor_economico': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '00.000.000.000.000 / 99.999.999.999.999'}),
            'moneda': forms.Select(attrs={'class': 'form-select'}),
            'obtencion_valor': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }