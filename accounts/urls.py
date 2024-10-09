from django.urls import path
from . import views
app_name = 'accounts'
urlpatterns = [
    
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('listar-reportes/', views.listar_reportes, name='listar_reportes')
]