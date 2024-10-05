from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractUser

class UserManager(BaseUserManager):
    def create_user(self, identificacion, password=None, **extra_fields):
        """Crea y devuelve un usuario con un identificador y contraseña."""
        if not identificacion:
            raise ValueError('El identificador debe ser establecido')
        
        user = self.model(identificacion=identificacion, **extra_fields)
        user.set_password(password)  # Asegúrate de encriptar la contraseña
        user.save(using=self._db)  # Guarda el usuario en la base de datos
        return user

    def create_superuser(self, identificacion, password=None, **extra_fields):
        """Crea y devuelve un superusuario con el identificador y contraseña dados."""
        extra_fields.setdefault('is_staff', True)  # El superusuario debe tener permisos de administrador
        extra_fields.setdefault('is_superuser', True)  # El superusuario debe ser un superusuario
        
        return self.create_user(identificacion, password, **extra_fields)
    
    
class User(AbstractUser):
    identificacion = models.CharField(max_length=20, unique=True)  # Asegúrate de que identificacion sea único

    objects = UserManager()  # Asigna el UserManager personalizado

    def __str__(self):
        return self.get_full_name()  # O cualquier otro campo que prefieras
    
    
