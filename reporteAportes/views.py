from django.shortcuts import render

""" class ApoyoEventosCreateView(LoginRequiredMixin,CreateView):
    model = ApoyoEventos
    form_class = ApoyoEventosForm
    template_name = 'reporteProgramas/crear_apoyo_eventos.html'
    
    def form_valid(self, form):
        form.instance.reporte = get_object_or_404(ReporteAvances, id=self.kwargs['reporte_id'])
        response = super().form_valid(form)
        reporte = form.instance.reporte
        reporte.save()
        
        return redirect('reporteProgramas:crear_datos_quien_reporta', reporte_id=self.kwargs['reporte_id'])
    
    def get_success_url(self):
        return reverse_lazy('reporteProgramas:crear_datos_quien_reporta', kwargs={'reporte_id': self.kwargs['reporte_id']}) """
