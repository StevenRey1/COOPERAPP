from django.urls import path
from . import views


app_name = 'usuarioCooperacion'
urlpatterns = [
    path('crear-usuario-cooperacion/', views.crear_usuario_cooperacion, name='crear_usuario_cooperacion'),
    path('buscar-usuario-cooperacion/', views.buscar_usuario_cooperacion, name='buscar_usuario_cooperacion'),
    path('editar-usuario-cooperacion/<int:usuario_id>', views.editar_usuario_cooperacion, name='editar_usuario_cooperacion'),
     path('buscar-por-dependencia/', views.buscar_por_dependencia, name='buscar_por_dependencia'),
    path('generar-pdf/<str:dependencia>/', views.generar_pdf_usuarios, name='generar_pdf_usuarios'),
   
]

