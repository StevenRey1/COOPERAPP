from polls2.models import ReporteAvances, DatosQuienReporta, DatosCooperante, LogrosAvances, ApoyoEventos
from  polls2.forms import ReporteAvancesForm, DatosQuienReportaForm, DatosCooperanteForm, LogrosAvancesForm, ApoyoEventosForm
from django.views.generic.edit import CreateView
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.db.utils import IntegrityError

class ReporteAvancesCreateView(CreateView):
    model = ReporteAvances
    form_class = ReporteAvancesForm
    template_name = 'polls2/crear_reporte_avances.html'
    def form_valid(self, form):
        response = super().form_valid(form)
        return redirect('polls2:crear_datos_quien_reporta', reporte_id=self.object.id)
    def get_success_url(self):
        return reverse_lazy('polls2:crear_datos_quien_reporta', kwargs={'reporte_id': self.object.id})

class DatosQuienReportaCreateView(CreateView):
    model = DatosQuienReporta
    form_class = DatosQuienReportaForm
    template_name = 'polls2/crear_datos_quien_reporta.html'
    
    def form_valid(self, form):
        form.instance.reporte = get_object_or_404(ReporteAvances, id=self.kwargs['reporte_id'])
        
        try:
            response = super().form_valid(form)
        except IntegrityError:
            form.add_error(None, "Error: El ID ya está en uso.")
            return self.form_invalid(form)
        
        reporte = form.instance.reporte
        reporte.save()
        
        return redirect('polls2:crear_datos_cooperante', reporte_id=self.kwargs['reporte_id'])

    def get_success_url(self):
        return reverse_lazy('polls2:crear_datos_cooperante', kwargs={'reporte_id': self.kwargs['reporte_id']})
    
class DatosCooperanteCreateView(CreateView):
    model = DatosCooperante
    form_class = DatosCooperanteForm
    template_name = 'polls2/crear_datos_cooperante.html'
    
    def form_valid(self, form):
        form.instance.reporte = get_object_or_404(ReporteAvances, id=self.kwargs['reporte_id'])
        response = super().form_valid(form)
        reporte = form.instance.reporte
        reporte.save()
        
        return redirect('polls2:crear_datos_quien_reporta', reporte_id=self.kwargs['reporte_id'])
    
    def get_success_url(self):
        return reverse_lazy('polls2:crear_datos_quien_reporta', kwargs={'reporte_id': self.kwargs['reporte_id']})
    

class LogrosAvancesCreateView(CreateView):
    model = LogrosAvances
    form_class = LogrosAvancesForm  # Usa form_class en lugar de fields
    template_name = 'polls2/crear_logros_avances.html'
    
    def form_valid(self, form):
        form.instance.reporte = get_object_or_404(ReporteAvances, id=self.kwargs['reporte_id'])
        response = super().form_valid(form)
        reporte = form.instance.reporte
        reporte.save()
        
        return redirect('polls2:crear_datos_quien_reporta', reporte_id=self.kwargs['reporte_id'])
    
    def get_success_url(self):
        return reverse_lazy('polls2:crear_datos_quien_reporta', kwargs={'reporte_id': self.kwargs['reporte_id']})
    

class ApoyoEventosCreateView(CreateView):
    model = ApoyoEventos
    form_class = ApoyoEventosForm
    template_name = 'polls2/crear_apoyo_eventos.html'
    
    def form_valid(self, form):
        form.instance.reporte = get_object_or_404(ReporteAvances, id=self.kwargs['reporte_id'])
        response = super().form_valid(form)
        reporte = form.instance.reporte
        reporte.save()
        
        return redirect('polls2:crear_datos_quien_reporta', reporte_id=self.kwargs['reporte_id'])
    
    def get_success_url(self):
        return reverse_lazy('polls2:crear_datos_quien_reporta', kwargs={'reporte_id': self.kwargs['reporte_id']})
