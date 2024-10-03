from ldap3 import Server, Connection, ALL, NTLM
from django.conf import settings

def authenticate_ldap(username, password):
    full_username = f'{settings.LDAP_USERNAME_PREFIX}{username}'

    server = Server(settings.LDAP_SERVER, port=settings.LDAP_PORT, get_info=ALL)

    try:
        conn = Connection(server, user=full_username, password=password, authentication=NTLM)
        if conn.bind():
            conn.search(settings.LDAP_BASE_DN, f'(sAMAccountName={username}))', attributes=['displayName', 'mail'
                        'urtTipoDocumento','urtIdentificacion','givenName','sn','sAMAccountName'])
            user_data = conn.entries[0] if conn.entries else None
            return user_data
        else:
            return None
    except Exception as e:
        print(e)
