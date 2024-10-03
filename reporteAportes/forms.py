
from typing import Any
from django import forms
from django.forms import inlineformset_factory, modelformset_factory
from django.core.exceptions import ValidationError
from .models import ApoyoEventos,ApoyoViajes,ObjetivoViaje, ApoyoTerritorios,ApoyoContratacion,ApoyoMaterial ,\
                    ApoyoHerramientas, ApoyoLitigio, ApoyoSeguridadAlimentaria, ApoyoOrdenesJudiciales, ApoyoArchivoHistorico, \
                    OtrosApoyos,EstimacionEconomica, ApoyoTerritorioUbicacion, ContratacionDetalle, ApoyoSeguridadDetalle, ApoyoLitigioDetalle,\
                    TipoCaso, TipoProyecto





def validar_max_palabras(value, max_palabras=5):
    if not value:
        return
    num_palabras = len(value.split())
    if num_palabras > max_palabras:
        raise ValidationError(f'El texto no puede exceder las {max_palabras} palabras. Actualmente tienes {num_palabras} palabras.')

class ApoyoEventosForm(forms.ModelForm):
    class Meta:
        model = ApoyoEventos
        exclude = ['reporte']
        widgets = {
            'cantidad_eventos': forms.NumberInput(attrs={'class': 'form-control w-25', 'min': 0, 'max': 999, 'placeholder': '999'}),
            'eventos': forms.CheckboxSelectMultiple(),  # Checkbox para "eventos"
            'publico_objetivo': forms.CheckboxSelectMultiple(),
            'otros_eventos': forms.CheckboxInput(attrs={'class': 'otros-eventos-checkbox'}),  # Checkbox para "otros eventos"
            'cuales_eventos': forms.TextInput(attrs={'class': 'form-control', 'disabled': True}),  # Campo que se habilita/deshabilita
            'otro_publico': forms.CheckboxInput(attrs={'class': 'otro-publico-checkbox'}),  # Checkbox para "otro público"
            'cual_publico': forms.TextInput(attrs={'class': 'form-control', 'disabled': True}),  # Campo que se habilita/deshabilita
            'cantidad_participantes': forms.NumberInput(attrs={'class': 'form-control w-25', 'min': 0, 'max': 9999, 'placeholder': '9999'}),
            'objetivo_principal': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 160, 'placeholder': 'Texto máximo de 120 palabras'}),
       }
    
    def clean(self) :
        cleaned_data = super().clean()
        eventos = cleaned_data.get('eventos')
        publico_objetivo = cleaned_data.get('publico_objetivo')

        if not eventos:
            raise ValidationError('Debe seleccionar al menos un evento.')
        if not publico_objetivo:
            raise ValidationError('Debe seleccionar al menos un publico objetivo.')

        objetivo_principal = cleaned_data.get('objetivo_principal')
        validar_max_palabras(objetivo_principal, max_palabras=120)
        return cleaned_data

class ApoyoViajesForm(forms.ModelForm):
    objetivo_viajes = forms.ModelMultipleChoiceField(
        queryset=ObjetivoViaje.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label="Objeto de los viajes",
        required=False
    )

    class Meta:
        model = ApoyoViajes
        exclude = ['reporte']
        widgets = {
            'cantidad_locales': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 999}),
            'cantidad_nacionales': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 999}),
            'cantidad_internacionales': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 999}),
            'cuales_otros': forms.TextInput(attrs={'class': 'form-control ', 'disabled': 'disabled', 'placeholder': 'Se activa cuando selecciona otros'}),
            'resaltado_apoyo' : forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 160, 'placeholder': 'Texto máximo de 100 palabras'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        objetivo_viajes = cleaned_data.get('objetivo_viajes')
        cuales_otros = cleaned_data.get('cuales_otros')
        resaltado_apoyo = cleaned_data.get('resaltado_apoyo')
        validar_max_palabras(resaltado_apoyo, max_palabras=100)

        if not objetivo_viajes:
            raise ValidationError('Debe seleccionar al menos un objetivo de los viajes.')

        # Validar que "cuales_otros" solo se rellene si se selecciona "otros"
        otros = ObjetivoViaje.objects.filter(nombre='Otros').first()
        if otros in objetivo_viajes and not cuales_otros:
            self.add_error('cuales_otros', 'Por favor, especifique los otros viajes.')
        return cleaned_data
    
class ApoyoTerritoriosForm(forms.ModelForm):
    class Meta:
        model = ApoyoTerritorios
        exclude = ['reporte','ubicaciones'] 
        widgets = {
            'apoyo_recibido': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Texto máximo 50 palabras'}),
            'tipo_visitas': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Texto máximo 100 palabras'}),
            'cantidad_visitas': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 999, 'required': 'required'}),
            'resaltar_apoyo': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Texto máximo 100 palabras'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        apoyo_recibido = cleaned_data.get('apoyo_recibido')
        tipo_visitas = cleaned_data.get('tipo_visitas')
        resaltar_apoyo = cleaned_data.get('resaltar_apoyo')
        validar_max_palabras(apoyo_recibido, max_palabras=50)
        validar_max_palabras(tipo_visitas, max_palabras=100)
        validar_max_palabras(resaltar_apoyo, max_palabras=100)

        return cleaned_data
       

class ApoyoTerritorioUbicacionForm(forms.ModelForm):
    class Meta:
        model = ApoyoTerritorioUbicacion
        fields = ['departamento', 'municipio', 'vereda']
        widgets = {
            'departamento': forms.Select(attrs={'class': 'form-select', 'required': 'required'}),
            'municipio': forms.Select(attrs={'class': 'form-select', 'disabled': 'disabled', 'required': 'required'}),
            'vereda': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Vereda / territorio / cabildo', 'required': 'required'}),
        }

ApoyoTerritorioUbicacionFormset = inlineformset_factory(
    ApoyoTerritorios, 
    ApoyoTerritorioUbicacion, 
    form=ApoyoTerritorioUbicacionForm, 
    extra=1,  # Número de formularios vacíos adicionales
)

    
class ApoyoContratacionForm(forms.ModelForm):
    class Meta:
        model = ApoyoContratacion
        exclude = ['reporte', 'tipo_personal', 'area_profesional']
        widgets = {
            'otro_tipo': forms.Textarea(attrs={'class': 'form-control', 'rows':1, 'placeholder': 'Texto máximo 5 palabras', 'disabled': 'disabled'}),
            'objetivo_principal': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Texto máximo 120 palabras', 'required': 'required'}),
            'resaltar_apoyo': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Texto máximo 100 palabras', 'required': 'required'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        objetivo_principal = cleaned_data.get('objetivo_principal')
        resaltar_apoyo = cleaned_data.get('resaltar_apoyo')
        otro_tipo = cleaned_data.get('otro_tipo')
        validar_max_palabras(objetivo_principal, max_palabras=120)
        validar_max_palabras(resaltar_apoyo, max_palabras=100)
        validar_max_palabras(otro_tipo, max_palabras=5)

        return cleaned_data


class ContratacionDetalleForm(forms.ModelForm):
    class Meta:
        model = ContratacionDetalle
        fields = ['tipo_personal','area_profesional', 'cantidad_personas', 'tiempo_servicio']
        widgets = {
            'tipo_personal': forms.HiddenInput(),
            'area_profesional': forms.Select(attrs={'class': 'form-select' }),
            'cantidad_personas': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 999, 'required': 'required'}),
            'tiempo_servicio': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 99, 'required': 'required'}),
        }



class ApoyoMaterialForm(forms.ModelForm):
    class Meta:
        model = ApoyoMaterial
        exclude = ['reporte']
        widgets = {
            'titulo_material': forms.TextInput(attrs={'class': 'form-control'}),
            'objetivo_principal': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'publico_destinatario': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo_material': forms.Select(attrs={'class': 'form-select'}),
            'cantidad_originales': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 999}),
            'cantidad_reproducciones': forms.NumberInput(attrs={'class': 'form-control', 'min':0, 'max':999}),
            'resaltar_apoyo': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Texto máximo 100 palabras'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        resaltar_apoyo = cleaned_data.get('resaltar_apoyo')
        validar_max_palabras(resaltar_apoyo, max_palabras=100)

        return cleaned_data
    

ApoyoMaterialFormSet = forms.formset_factory(ApoyoMaterialForm, extra=3)



class ApoyoHerramientasForm(forms.ModelForm):
    class Meta:
        model = ApoyoHerramientas
        exclude = ['reporte']
        widgets = {
            'tipo_herramienta': forms.HiddenInput(),
            'cantidad_recibida': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 999}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control','rows':1, 'placeholder': 'Texto máx. 20 palabras', 'required': 'required'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control','rows':1 ,'placeholder': 'Texto máx. 20 palabras', 'required': 'required'}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        descripcion = cleaned_data.get('descripcion')
        observaciones = cleaned_data.get('observaciones')
        validar_max_palabras(descripcion, max_palabras=20)
        validar_max_palabras(observaciones, max_palabras=20)

        return cleaned_data

ApoyoHerramientasFormSet = forms.formset_factory(ApoyoHerramientasForm, extra=0)




# Formulario para ApoyoLitigio
class ApoyoLitigioForm(forms.ModelForm):
    class Meta:
        model = ApoyoLitigio
        exclude = ['reporte']
        widgets = {
            'resaltar_apoyo': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Texto máximo 100 palabras', 'required': 'required'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        resaltar_apoyo = cleaned_data.get('resaltar_apoyo')
        validar_max_palabras(resaltar_apoyo, max_palabras=100)
        return cleaned_data

# Formulario para ApoyoLitigioDetalle
class ApoyoLitigioDetalleForm(forms.ModelForm):
    class Meta:
        model = ApoyoLitigioDetalle
        fields = ['tipo_caso', 'nombre_caso', 'cantidad_ids']
        widgets = {
            'tipo_caso': forms.HiddenInput(),
            'nombre_caso': forms.Textarea(attrs={'class': 'form-control', 'rows': 1, 'placeholder': 'Texto máximo 5 palabras', 'required': 'required'}),
            'cantidad_ids': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 999}),
        }

    def clean(self):
        cleaned_data = super().clean()
        nombre_caso = cleaned_data.get('nombre_caso')
        validar_max_palabras(nombre_caso, max_palabras=5)
        return cleaned_data

# Crear el Formset utilizando ApoyoLitigioDetalle
ApoyoLitigioFormset = forms.modelformset_factory(
    ApoyoLitigioDetalle,  # Cambia a ApoyoLitigioDetalle
    form=ApoyoLitigioDetalleForm,
    extra=TipoCaso.objects.all().count(),  # Ajusta según sea necesario
    can_delete=False
)


class ApoyoSeguridadAlimentariaForm(forms.ModelForm):
    class Meta:
        model = ApoyoSeguridadAlimentaria
        fields = ['tipo_apoyo', 'otro_apoyo', 'resaltar_apoyo']
        widgets = {
            'tipo_apoyo': forms.CheckboxSelectMultiple(),
            'otro_apoyo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Se activa cuando se selecciona la opción otros'}),
            'resaltar_apoyo': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Texto máximo 120 palabras'}),
        }
    def clean(self) :
        cleaned_data = super().clean()
        tipo_apoyo = cleaned_data.get('tipo_apoyo')
        resaltar_apoyo = cleaned_data.get('resaltar_apoyo')
        validar_max_palabras(resaltar_apoyo, max_palabras=120)
        if not tipo_apoyo:
            raise ValidationError('Debe seleccionar al menos un tipo de apoyo.')
        
        return cleaned_data

class ApoyoDetallesForm(forms.ModelForm):
    class Meta:
        model = ApoyoSeguridadDetalle
        fields = ['tipo_proyecto', 'cantidad_proyectos', 'cantidad_familias']
        widgets = {
            'tipo_proyecto': forms.HiddenInput(),
            'cantidad_proyectos': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'cantidad_familias': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
        }

ApoyoDetallesFormSet = forms.modelformset_factory(
    ApoyoSeguridadDetalle,
    form=ApoyoDetallesForm,
    extra=TipoProyecto.objects.all().count(),
    can_delete=False
)


class ApoyoOrdenesJudicialesForm(forms.ModelForm):
    class Meta:
        model = ApoyoOrdenesJudiciales
        exclude = ['reporte']
        widgets = {
            'cantidad_sentencias': forms.NumberInput(attrs={'min': 0, 'max': 999}),
            'cantidad_ordenes': forms.NumberInput(attrs={'min': 0, 'max': 999})
        }

    tipo_apoyo = forms.CharField(label="Tipo de apoyo", 
                                 validators=[lambda value: validar_max_palabras(value, max_palabras=120)],
                                 widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Texto máximo 120 palabras'}), 
                                 )
    tipo_ordenes = forms.CharField(label="Tipo de órdenes", 
                                   validators=[lambda value: validar_max_palabras(value, max_palabras=120)], 
                                   widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Texto máximo 120 palabras'}),
                                   )

class ApoyoArchivoHistoricoForm(forms.ModelForm):
    class Meta:
        model = ApoyoArchivoHistorico
        exclude = ['reporte']
        widgets = {
            'acciones': forms.CheckboxSelectMultiple(),
            'cuales_acciones': forms.TextInput(attrs={'class': 'form-control','disabled':'disabled', 'placeholder': 'Se activa cuando se selecciona la opción otros'}),
            'comentarios': forms.Textarea(attrs={'class': 'form-control', 'rows':3, 'placeholder': 'Texto máximo 100 palabras'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        acciones = cleaned_data.get('acciones')
        # Validación para asegurarse de que al menos una acción esté seleccionada
        if not acciones:
            raise ValidationError('Debe seleccionar al menos una acción.')
        comentarios = cleaned_data.get('comentarios')
        validar_max_palabras(comentarios, max_palabras=100)

        return cleaned_data

class OtrosApoyosForm(forms.ModelForm):
    class Meta:
        model = OtrosApoyos
        exclude = ['reporte']
        widgets = {
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Texto máximo 150 palabras'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        descripcion = cleaned_data.get('descripcion')
        validar_max_palabras(descripcion, max_palabras=150)

        return cleaned_data

class EstimacionEconomicaForm(forms.ModelForm):
    class Meta:
        model = EstimacionEconomica
        exclude = ['reporte']
        widgets = {
            'valor_economico': forms.TextInput(attrs={'class': 'form-control','rows':1,  'required': 'required', 'placeholder': '00.000.000.000.000 / 99.999.999.999.999'}),
            'moneda': forms.Select(attrs={'class': 'form-select'}),
            'obtencion_valor': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        obtencion_valor = cleaned_data.get('obtencion_valor')
        validar_max_palabras(obtencion_valor, max_palabras=100)

        return cleaned_data