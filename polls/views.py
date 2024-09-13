from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from . models import *
from . forms import *
from django.shortcuts import render, get_object_or_404, redirect

class ReporteAcercamientoCreateView(CreateView):
    model = ReporteAcercamiento
    form_class = ReporteAcercamientoForm
    template_name = 'polls/crear_reporte_acercamiento.html'
    def form_valid(self, form):
        response = super().form_valid(form)
        return redirect('crear_datos_quien_reporta', reporte_id=self.object.id)
    def get_success_url(self):
        return reverse_lazy('crear_datos_quien_reporta', kwargs={'reporte_id': self.object.id})

class DatosQuienReportaCreateView(CreateView):
    model = DatosQuienReporta
    form_class = DatosQuienReportaForm
    template_name = 'polls/crear_datos_quien_reporta.html'

    def form_valid(self, form):
        form.instance.reporte = get_object_or_404(ReporteAcercamiento, id=self.kwargs['reporte_id'])
        response = super().form_valid(form)
        return redirect('crear_acercamiento', reporte_id=self.kwargs['reporte_id'])

    def get_success_url(self):
        return reverse_lazy('crear_acercamiento', kwargs={'reporte_id': self.kwargs['reporte_id']})

class AcercamientoCreateView(CreateView):
    model = AcercamientoCooperacion
    form_class = AcercamientoForm
    template_name = 'polls/crear_acercamiento.html'

    def form_valid(self, form):
        form.instance.reporte = get_object_or_404(ReporteAcercamiento, id=self.kwargs['reporte_id'])
        response = super().form_valid(form)
        return redirect('crear_necesidades', reporte_id=self.kwargs['reporte_id'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reporte'] = get_object_or_404(ReporteAcercamiento, id=self.kwargs['reporte_id'])
        return context

    def get_success_url(self):
        return reverse_lazy('crear_necesidades', kwargs={'reporte_id': self.kwargs['reporte_id']})


class NecesidadesCreateView(CreateView):
    model = NecesidadesCooperacion
    form_class = NecesidadesForm
    template_name = 'polls/crear_necesidades.html'

    def form_valid(self, form):
        form.instance.reporte = get_object_or_404(ReporteAcercamiento, id=self.kwargs['reporte_id'])
        response = super().form_valid(form)
        return redirect('listar_reportes_acercamiento')

    def get_success_url(self):
        return reverse_lazy('listar_reportes_acercamiento')


from django.views.generic.list import ListView

class ReporteAcercamientoListView(ListView):
    model = ReporteAcercamiento
    template_name = 'polls/listar_reportes_acercamiento.html'
    context_object_name = 'reportes'


from django.views.generic.detail import DetailView

class DatosQuienReportaDetailView(DetailView):
    model = DatosQuienReporta
    template_name = 'polls/ver_datos_quien_reporta.html'
    context_object_name = 'datos_quien_reporta'

    def get_object(self):
        # Aquí usamos `informe` en lugar de `reporte`
        reporte = get_object_or_404(ReporteAcercamiento, id=self.kwargs['reporte_id'])
        return get_object_or_404(DatosQuienReporta, reporte=reporte)


class AcercamientoDetailView(DetailView):
    model = AcercamientoCooperacion
    template_name = 'polls/ver_acercamiento.html'
    context_object_name = 'acercamientos'

    def get_object(self):
        # Aquí usamos `informe` en lugar de `reporte`
        reporte = get_object_or_404(ReporteAcercamiento, id=self.kwargs['reporte_id'])
        return get_object_or_404(AcercamientoCooperacion, reporte=reporte)


class NecesidadesDetailView(DetailView):
    model = NecesidadesCooperacion
    template_name = 'polls/ver_necesidades.html'
    context_object_name = 'necesidades'

    def get_object(self):
        # Aquí usamos `informe` en lugar de `reporte`
        reporte = get_object_or_404(ReporteAcercamiento, id=self.kwargs['reporte_id'])
        return get_object_or_404(NecesidadesCooperacion, reporte=reporte)
