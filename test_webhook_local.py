import requests
import json

# URL del webhook local
url = "http://127.0.0.1:8000/orders/webhook/"

# ID de un pago REAL que hayas hecho en Sandbox (puedes sacarlo de los logs del servidor o de tu cuenta MP)
# O usa un ID ficticio para ver si al menos llega la petición (aunque dará error al consultar a MP)
payment_id = "123456789" # CAMBIA ESTO POR UN ID REAL SI QUIERES QUE SE ACTUALICE LA DB

payload = {
    "action": "payment.created",
    "api_version": "v1",
    "data": {
        "id": payment_id
    },
    "date_created": "2021-11-01T02:02:02Z",
    "id": 123456,
    "live_mode": False,
    "type": "payment",
    "user_id": 123456789
}

print(f"Enviando webhook simulado a {url}...")
try:
    response = requests.post(url, json=payload)
    print(f"Respuesta del servidor: {response.status_code}")
    if response.status_code == 200:
        print("Webhook recibido correctamente (revisa la consola de Django para ver los logs).")
    else:
        print("Error en el servidor.")
except Exception as e:
    print(f"Error al conectar: {e}")
