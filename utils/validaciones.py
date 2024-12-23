import re

# Validación para el teléfono (debe tener 9 dígitos)
def validar_telefono(telefono):
    return bool(re.match(r'^[0-9]{9}$', telefono))

# Validación para el DNI (8 dígitos seguidos de una letra)
def validar_dni(dni_cliente):
    return bool(re.match(r'^[0-9]{8}[A-Za-z]$', dni_cliente))

# Validación para el DNI (8 dígitos seguidos de una letra)
def validar_dni(dni_trabajador):
    return bool(re.match(r'^[0-9]{8}[A-Za-z]$', dni_trabajador))