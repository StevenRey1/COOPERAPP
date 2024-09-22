from django.urls import path
from reporteProgramas.views import *
from django.conf import settings
from django.conf.urls.static import static


app_name = 'reporteProgramas'
urlpatterns = [
    path('',ListarReportesView.as_view(), name='index'),
    path('crear-reporte/', ReporteAvancesCreateView.as_view(), name='crear_reporte_avances'),
    path('crear-datos-quien-reporta/<int:reporte_id>/', DatosQuienReportaCreateView.as_view(), name='crear_datos_quien_reporta'),
    path('crear-datos-cooperante/<int:reporte_id>/', DatosCooperanteCreateView.as_view(), name='crear_datos_cooperante'),
    path('crear-logros-avances/<int:reporte_id>/', LogrosAvancesCreateView.as_view(), name='crear_logros_avances'),
    path('crear-apoyo-actividades/<int:reporte_id>/', ApoyoEventosCreateView.as_view(), name='crear_apoyo_actividades'),
    path('ver-datos-quien-reporta/<int:reporte_id>/', DatosQuienReportaDetailView.as_view(), name='ver_datos_quien_reporta'),
    path('ver-datos-cooperante/<int:reporte_id>/', DatosCooperanteDetailView.as_view(), name='ver_datos_cooperante'),
    path('ver-logros-avances/<int:reporte_id>/', LogrosAvancesDetailView.as_view(), name='ver_logros_avances'),
    path('reporte-avances-pdf/<int:reporte_id>/', generar_pdf_reporte_avances, name='reporte_avances_pdf'),
    
]

# Añade esta línea para servir los archivos durante el desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)