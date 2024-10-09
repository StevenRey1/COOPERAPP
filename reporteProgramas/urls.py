from django.urls import path
from reporteProgramas.views import *
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'reporteProgramas'
urlpatterns = [
    path('crear-reporte/', ReporteProgramaCreateView.as_view(), name='crear_reporte_avances'),
    path('crear-datos-quien-reporta/<int:reporte_id>/', DatosQuienReportaCreateView.as_view(), name='crear_datos_quien_reporta'),
    path('editar-datos-quien-reporta/<int:reporte_id>/', DatosQuienReportaUpdateView.as_view(), name='editar_datos_quien_reporta'),
    path('crear-logros-avances/<int:reporte_id>/<int:linea_accion_id>', crear_reporte_logros, name='crear_logros_avances'),
    path('editar-logros-avances/<int:reporte_id>/', editar_reporte_logros, name='editar_logros_avances'),
    path('reporte-avances-pdf/<int:reporte_id>/', generar_pdf_reporte_avances, name='reporte_avances_pdf'),
    path('get_municipios/<int:departamento_id>/', get_municipios, name='get_municipios'),
    path('api/cooperantes/', views.obtener_cooperantes, name='obtener_cooperantes'),
    path('obtener-identificaciones/<int:cooperante_id>/', views.obtener_identificaciones_por_cooperante, name='obtener_identificaciones'),
    path('obtener-operadores/<int:identificacion_id>/', views.obtener_operadores_por_identificacion, name='obtener_operadores'),
    path('obtener_proyectos_plan/<int:cooperante_id>/<int:identificacion_id>/<int:operador_id>/', obtener_proyectos_plan, name='obtener_proyectos_plan'),
    path('obtener_lineas_accion/<int:cooperante_id>/<int:identificacion_id>/<int:operador_id>/<int:proyecto_plan_id>/', obtener_lineas_accion, name='obtener_lineas_accion'),
    path('crear-datos-cooperante/<int:reporte_id>/', views.crear_datos_cooperante, name='crear_datos_cooperante'),
    path('editar-datos-cooperante/<int:reporte_id>/', views.editar_datos_cooperante, name='editar_datos_cooperante'),

]

# Añade esta línea para servir los archivos durante el desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)