from decimal import Decimal

# Códigos de Provincia (ISO 3166-2:AR sin el prefijo 'AR-' para simplicidad interna o validación)
PROVINCES = [
    ('B', 'Buenos Aires'),
    ('C', 'Ciudad Autónoma de Buenos Aires'),
    ('K', 'Catamarca'),
    ('H', 'Chaco'),
    ('U', 'Chubut'),
    ('X', 'Córdoba'),
    ('W', 'Corrientes'),
    ('E', 'Entre Ríos'),
    ('P', 'Formosa'),
    ('Y', 'Jujuy'),
    ('L', 'La Pampa'),
    ('F', 'La Rioja'),
    ('M', 'Mendoza'),
    ('N', 'Misiones'),
    ('Q', 'Neuquén'),
    ('R', 'Río Negro'),
    ('A', 'Salta'),
    ('J', 'San Juan'),
    ('D', 'San Luis'),
    ('Z', 'Santa Cruz'),
    ('S', 'Santa Fe'),
    ('G', 'Santiago del Estero'),
    ('V', 'Tierra del Fuego'),
    ('T', 'Tucumán'),
]

# Zonas definidas por el usuario
ZONE_LOCAL = ['L'] # La Pampa
ZONE_NEAR = ['B', 'C', 'X', 'D', 'R', 'Q'] # BsAs, CABA, Cordoba, San Luis, Rio Negro, Neuquen
ZONE_TDF = ['V'] # Tierra del Fuego
# El resto cae en "Resto del País"

def get_shipping_cost(province_code, subtotal):
    """
    Calcula el costo de envío basado en la provincia y el subtotal de la compra.
    """
    subtotal = Decimal(subtotal)
    
    # Envío gratis para compras mayores a $100,000
    if subtotal > 100000:
        return Decimal(0)

    if province_code in ZONE_LOCAL:
        return Decimal(5000)
    elif province_code in ZONE_NEAR:
        return Decimal(15500)
    elif province_code in ZONE_TDF:
        return Decimal(25000)
    else:
        # Resto del País
        return Decimal(20000)
