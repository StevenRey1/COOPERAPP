import json
from datetime import datetime, date
from decimal import Decimal
from django.db import models
from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver
from .models import AuditLog
from .middleware import thread_local  # Importar thread_local desde middleware.py

# Función para convertir valores no serializables a un formato JSON compatible
def convert_to_serializable(value):
    if isinstance(value, datetime):
        return value.strftime('%Y-%m-%d %H:%M:%S')
    elif isinstance(value, date):  # Manejar objetos de tipo date
        return value.strftime('%Y-%m-%d')  # Convertir a cadena de texto
    elif isinstance(value, Decimal):
        return float(value)
    elif isinstance(value, list):  # Si es una lista, recorre los elementos
        return [convert_to_serializable(item) for item in value]
    elif isinstance(value, dict):  # Si es un diccionario, recorre los elementos
        return {key: convert_to_serializable(val) for key, val in value.items()}
    elif hasattr(value, '__dict__'):  # Si es un objeto, convierte sus atributos
        return convert_object_to_serializable(value)
    # Agrega más tipos según sea necesario
    return value

# Función para convertir un objeto a un formato serializable
def convert_object_to_serializable(obj):
    serialized_data = {}
    for field in obj._meta.fields:
        field_name = field.name
        field_value = getattr(obj, field_name)
        serialized_data[field_name] = convert_to_serializable(field_value)
    return serialized_data

# Define thread_local at the beginning of the file

@receiver(pre_save)
def log_update(sender, instance, **kwargs):
    # Ignorar si el modelo es AuditLog
    if sender.__name__ == 'AuditLog':
        return
    
    model_name = sender.__name__
    object_id = str(instance.pk) if instance.pk else None

    # Solo registrar actualizaciones
    if instance.pk:  # Es una actualización
        action = 'U'
        # Registrar cambios (comparar con la instancia anterior)
        old_instance = sender.objects.filter(pk=instance.pk).first()
        changes = {}
        if old_instance:
            for field in instance._meta.fields:
                field_name = field.name
                old_value = getattr(old_instance, field_name)
                new_value = getattr(instance, field_name)
                
                # Omitir campos de archivo
                if isinstance(field, (models.FileField, models.ImageField)):
                    continue

                # Convertir los valores a serializables
                old_value = convert_to_serializable(old_value)
                new_value = convert_to_serializable(new_value)
                

                if old_value != new_value:
                    changes[field_name] = {'old': old_value, 'new': new_value}
                    
                

            # Solo registrar si hay cambios
            if changes:
                
                # Obtener la solicitud actual del thread local
                request = getattr(thread_local, 'request', None)  # Usar thread_local importado
                # Registrar en la tabla de auditoría
                AuditLog.objects.create(
                    user = request.user if request else None,  # Si tienes acceso al usuario
                    action=action,
                    model_name=model_name,
                    object_id=object_id,
                    changes=changes,
                )

@receiver(pre_delete)
def log_delete(sender, instance, **kwargs):
    # Ignorar si el modelo es AuditLog
    if sender.__name__ == 'AuditLog':
        return
    
    model_name = sender.__name__
    object_id = str(instance.pk)
    
    # Obtener la solicitud actual del thread local
    request = getattr(thread_local, 'request', None)  # Usar thread_local importado
    
    # Registrar la eliminación
    AuditLog.objects.create(
        user=request.user if request else None,  # Si tienes acceso al usuario
        action='D',
        model_name=model_name,
        object_id=object_id,
        changes='Eliminado',  # Puedes incluir más detalles si lo deseas
    )