from django.db import models
from reporteAcercamientos.models import Dependencia
from django.core.validators import RegexValidator

class RolUsuarioCooperacion(models.Model):
        
    nombre = models.CharField(max_length=50)
    
    def __str__(self):
        return f"{self.nombre}"
        
        

class UsuarioCooperacion(models.Model):
    
    telefono_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="El número de teléfono debe tener entre 9 y 15 dígitos. Puede incluir el signo '+' al principio."
    )
    
    nombre = models.CharField(max_length=50)
    email = models.EmailField()
    telefono = models.CharField(validators=[telefono_regex], max_length=16, blank=True)  # el máximo tamaño incluye el signo +
    rol = models.ForeignKey(RolUsuarioCooperacion, on_delete=models.SET_NULL, null=True)
    dependencia = models.ForeignKey(Dependencia, on_delete=models.SET_NULL, null=True)  
    
    def __str__(self):
        return f"{self.nombre}" 
