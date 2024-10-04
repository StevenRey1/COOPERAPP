from django.urls import path
from . import views    

app_name = 'reporteAportes'

urlpatterns = [
    path('crear-apoyo-eventos/<int:reporte_id>/',views.crear_apoyo_eventos, name='crear_apoyo_eventos'),
    path('editar-apoyo-eventos/<int:reporte_id>/', views.editar_apoyo_eventos, name='editar_apoyo_eventos'),
    path('crear-apoyo-viajes/<int:reporte_id>/', views.crear_apoyo_viajes, name='crear_apoyo_viajes'),
    path('editar-apoyo-viajes/<int:reporte_id>/', views.editar_apoyo_viajes, name='editar_apoyo_viajes'),
    path('crear-apoyo-territorios/<int:reporte_id>/', views.crear_apoyo_territorios, name='crear_apoyo_territorios'),
    path('editar-apoyo-territorios/<int:reporte_id>/', views.editar_apoyo_territorios, name='editar_apoyo_territorios'),
    path('crear-apoyo-contratacion/<int:reporte_id>/', views.crear_apoyo_contratacion, name='crear_apoyo_contratacion'),
    path('editar-apoyo-contratacion/<int:reporte_id>/', views.editar_apoyo_contratacion, name='editar_apoyo_contratacion'),
    path('crear-apoyo-material/<int:reporte_id>/', views.crear_apoyo_material, name='crear_apoyo_material'),
    path('editar-apoyo-material/<int:reporte_id>/', views.editar_apoyo_material, name='editar_apoyo_material'),
    path('crear-apoyo-herramientas/<int:reporte_id>/', views.crear_apoyo_herramientas, name='crear_apoyo_herramientas'),
    path('editar-apoyo-herramientas/<int:reporte_id>/', views.editar_apoyo_herramientas, name='editar_apoyo_herramientas'),
    path('crear-apoyo-litigio/<int:reporte_id>/', views.crear_apoyo_litigio, name='crear_apoyo_litigio'),
    path('editar-apoyo-litigio/<int:reporte_id>/', views.editar_apoyo_litigio, name='editar_apoyo_litigio'),
    path('crear-apoyo-seguridad-alimentaria/<int:reporte_id>/', views.crear_apoyo_seguridad_alimentaria, name='crear_apoyo_seguridad_alimentaria'),
    path('editar-apoyo-seguridad-alimentaria/<int:reporte_id>/', views.editar_apoyo_seguridad_alimentaria, name='editar_apoyo_seguridad_alimentaria'),
    path('crear-apoyo-ordenes-judiciales/<int:reporte_id>/', views.crear_apoyo_ordenes_judiciales, name='crear_apoyo_ordenes_judiciales'),
    path('editar-apoyo-ordenes-judiciales/<int:reporte_id>/', views.editar_apoyo_ordenes_judiciales, name='editar_apoyo_ordenes_judiciales'),
    path('crear-apoyo-archivo-historico/<int:reporte_id>/', views.crear_apoyo_archivo_historico, name='crear_apoyo_archivo_historico'),
    path('editar-apoyo-archivo-historico/<int:reporte_id>/', views.editar_apoyo_archivo_historico, name='editar_apoyo_archivo_historico'),
    path('crear-otros-apoyos/<int:reporte_id>/', views.crear_otros_apoyos, name='crear_otros_apoyos'),
    path('editar-otros-apoyos/<int:reporte_id>/', views.editar_otros_apoyos, name='editar_otros_apoyos'),
    path('crear-estimacion-economica/<int:reporte_id>/', views.crear_estimacion_economica, name='crear_estimacion_economica'),
    path('editar-estimacion-economica/<int:reporte_id>/', views.editar_estimacion_economica, name='editar_estimacion_economica'),
    path('reporte-pdf/<int:reporte_id>/', views.crear_reporte_pdf, name='reporte_pdf'),
    path('editar-reporte/<int:reporte_id>/', views.editar_reporte, name='editar_reporte'),

]