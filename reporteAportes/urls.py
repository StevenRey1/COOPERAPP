from django.urls import path
from django.conf.urls.static import static
from . import views    

app_name = 'reporteAportes'

urlpatterns = [
    path('crear-apoyo-eventos/<int:reporte_id>/',views.crear_apoyo_eventos, name='crear_apoyo_eventos'),
    path('crear-apoyo-viajes/<int:reporte_id>/', views.crear_apoyo_viajes, name='crear_apoyo_viajes'),
    path('crear-apoyo-territorios/<int:reporte_id>/', views.crear_apoyo_territorios, name='crear_apoyo_territorios'),
    path('crear-apoyo-contratacion/<int:reporte_id>/', views.crear_apoyo_contratacion, name='crear_apoyo_contratacion'),
    path('crear-apoyo-material/<int:reporte_id>/', views.crear_apoyo_material, name='crear_apoyo_material'),
    path('crear-apoyo-herramientas/<int:reporte_id>/', views.crear_apoyo_herramientas, name='crear_apoyo_herramientas'),
    path('crear-apoyo-litigio/<int:reporte_id>/', views.crear_apoyo_litigio, name='crear_apoyo_litigio'),
    path('crear-apoyo-seguridad-alimentaria/<int:reporte_id>/', views.crear_apoyo_seguridad_alimentaria, name='crear_apoyo_seguridad_alimentaria'),
    path('crear-apoyo-ordenes-judiciales/<int:reporte_id>/', views.crear_apoyo_ordenes_judiciales, name='crear_apoyo_ordenes_judiciales'),
    path('crear-apoyo-archivo-historico/<int:reporte_id>/', views.crear_apoyo_archivo_historico, name='crear_apoyo_archivo_historico'),
    path('crear-otros-apoyos/<int:reporte_id>/', views.crear_otros_apoyos, name='crear_otros_apoyos'),
    path('crear-estimacion-economica/<int:reporte_id>/', views.crear_estimacion_economica, name='crear_estimacion_economica'),

]