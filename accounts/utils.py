from ldap3 import Server, Connection, ALL, NTLM
from django.conf import settings
from .models import User

def authenticate_ldap(username, password):
    # Prefijo del nombre de usuario
    full_username = f"{settings.LDAP_USERNAME_PREFIX}{username}"
    
    # Conectar al servidor LDAP
    server = Server(settings.LDAP_SERVER, port=settings.LDAP_PORT, get_info=ALL)
    
    try:
        # Intenta establecer una conexión utilizando NTLM
        conn = Connection(server, user=full_username, password=password, authentication=NTLM)
        
        if conn.bind():
            # Buscar los datos del usuario
            conn.search(settings.LDAP_BASE_DN, f'(sAMAccountName={username})', 
                        attributes=['displayName', 'mail', 'urtTipoDocumento', 'urtIdentificacion', 'givenName', 'sn', 'sAMAccountName'])
            
            user_data = conn.entries[0] if conn.entries else None
            
            if user_data:
                # Actualiza o crea el usuario en la base de datos
                user, created = User.objects.update_or_create(
                    identificacion=user_data.urtIdentificacion.value,
                    defaults={
                        'first_name': user_data.givenName.value,
                        'last_name': user_data.sn.value,
                        'email': user_data.mail.value,
                        'username': user_data.sAMAccountName.value
                    }
                )
                
                return user  # Retorna el usuario autenticado
            
            return None  # No se encontró el usuario en LDAP
        
        return False  # Falló la autenticación
    except Exception as e:
        print(f"Error de autenticación LDAP: {e}")
        return None  # O manejar el error de otra manera