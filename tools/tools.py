from datetime import datetime
import secrets
import string

def generar_codigo():
    longitud_codigo = 6
    caracteres = string.ascii_lowercase + string.digits
    codigo = ''.join(secrets.choice(caracteres) for _ in range(longitud_codigo))
    return codigo

def get_fecha():
    fecha_hora_actual = datetime.now()
    fecha_actual = fecha_hora_actual.strftime("%Y-%m-%d %H:%M:%S")
    return fecha_actual
