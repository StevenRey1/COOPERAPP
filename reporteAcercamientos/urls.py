from django.urls import path
from .views import *

app_name = 'reporteAcercamientos'
urlpatterns = [
    path('crear-reporte/', ReporteAcercamientosCreateView.as_view(), name='crear_reporte_acercamiento'),
    path('crear-datos-quien-reporta/<int:reporte_id>/', DatosQuienReportaCreateView.as_view(), name='crear_datos_quien_reporta'),
    path('crear-acercamiento/<int:reporte_id>/', AcercamientoCreateView.as_view(), name='crear_acercamiento'),
    path('crear-necesidades/<int:reporte_id>/', NecesidadesCreateView.as_view(), name='crear_necesidades'),
    path('', ReporteAcercamientoListView.as_view(), name='index'),
    path('reporte_pdf/<int:reporte_id>/', generar_pdf_reporte, name='reporte_pdf'),
    path('saltar-acercamiento/<int:reporte_id>/', SaltarAcercamientoView.as_view(), name='saltar_acercamiento'),
]
