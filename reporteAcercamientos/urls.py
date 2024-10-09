from django.urls import path
from .views import *

app_name = 'reporteAcercamientos'
urlpatterns = [
    path('crear-reporte/', ReporteAcercamientosCreateView.as_view(), name='crear_reporte_acercamiento'),
    path('crear-datos-quien-reporta/<int:reporte_id>/', DatosQuienReportaCreateView.as_view(), name='crear_datos_quien_reporta'),
    path('crear-acercamiento/<int:reporte_id>/', crear_acercamiento, name='crear_acercamiento'),
    path('crear-necesidades/<int:reporte_id>/', NecesidadesCreateView.as_view(), name='crear_necesidades'),
    path('reporte_pdf/<int:reporte_id>/', generar_pdf_reporte, name='reporte_pdf'),
    path('saltar-acercamiento/<int:reporte_id>/', SaltarAcercamientoView.as_view(), name='saltar_acercamiento'),
    path('editar-reporte/<int:reporte_id>/', editar_reporte, name='editar_reporte'),
    path('editar-datos-quien-reporta/<int:reporte_id>/', DatosQuienReportaUpdateView.as_view(), name='editar_datos_quien_reporta'),
    path('editar-datos-acercamiento/<int:reporte_id>/', editar_acercamiento, name='editar_datos_acercamiento'),
    path('editar-necesidades/<int:reporte_id>/', NecesidadesUpdateView.as_view(), name='editar_necesidades'),
]
