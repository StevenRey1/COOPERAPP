from django.urls import path
from reporteProgramas.views import *
from django.conf import settings
from django.conf.urls.static import static


app_name = 'reporteProgramas'
urlpatterns = [
    path('',ReporteProgramasListView.as_view(), name='index'),
    path('crear-reporte/', ReporteProgramaCreateView.as_view(), name='crear_reporte_avances'),
    path('crear-datos-quien-reporta/<int:reporte_id>/', DatosQuienReportaCreateView.as_view(), name='crear_datos_quien_reporta'),
    path('crear-logros-avances/<int:reporte_id>/', crear_reporte_logros, name='crear_logros_avances'),
    path('reporte-avances-pdf/<int:reporte_id>/', generar_pdf_reporte_avances, name='reporte_avances_pdf'),
    path('get_municipios/<int:departamento_id>/', get_municipios, name='get_municipios'),
]

# Añade esta línea para servir los archivos durante el desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)