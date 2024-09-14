from django.urls import path
from .views import *


urlpatterns = [
    path('crear-reporte/', ReporteAcercamientoCreateView.as_view(), name='crear_reporte_acercamiento'),
    path('crear-datos-quien-reporta/<int:reporte_id>/', DatosQuienReportaCreateView.as_view(), name='crear_datos_quien_reporta'),
    path('crear-acercamiento/<int:reporte_id>/', AcercamientoCreateView.as_view(), name='crear_acercamiento'),
    path('crear-necesidades/<int:reporte_id>/', NecesidadesCreateView.as_view(), name='crear_necesidades'),
    path('reportes/', ReporteAcercamientoListView.as_view(), name='listar_reportes_acercamiento'),
    path('datos-quien-reporta/<int:reporte_id>/', DatosQuienReportaDetailView.as_view(), name='ver_datos_quien_reporta'),
    path('acercamientos/<int:reporte_id>/', AcercamientoDetailView.as_view(), name='ver_acercamiento'),
    path('necesidades/<int:reporte_id>/', NecesidadesDetailView.as_view(), name='ver_necesidades'),
    path('editar_datos_quien_reporta/<int:reporte_id>/', DatosQuienReportaUpdateView.as_view(), name='editar_datos_quien_reporta'),
    path('editar_acercamiento/<int:reporte_id>/<int:pk>/', AcercamientoUpdateView.as_view(), name='editar_acercamiento'),
    path('editar_necesidades/<int:reporte_id>/', NecesidadesCooperacionUpdateView.as_view(), name='editar_necesidades'),
    path('reporte_pdf/<int:reporte_id>/', generar_pdf_reporte, name='reporte_pdf'),
]
