from django.urls import path
from polls2.views import *

app_name = 'polls2'
urlpatterns = [
    path('crear-reporte/', ReporteAvancesCreateView.as_view(), name='crear_reporte_acercamiento'),
    path('crear-datos-quien-reporta/<int:reporte_id>/', DatosQuienReportaCreateView.as_view(), name='crear_datos_quien_reporta'),
    path('crear-datos-cooperante/<int:reporte_id>/', DatosCooperanteCreateView.as_view(), name='crear_datos_cooperante'),
    path('crear-logros-avances/<int:reporte_id>/', LogrosAvancesCreateView.as_view(), name='crear_logros_avances'),
    path('crear-apoyo-actividades/<int:reporte_id>/', ApoyoEventosCreateView.as_view(), name='crear_apoyo_actividades')
]
