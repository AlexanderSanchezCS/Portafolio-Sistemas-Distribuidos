import json
import time
from datetime import datetime, timezone

import paho.mqtt.client as mqtt

BROKER = "localhost"
PUERTO = 1883

cliente = mqtt.Client(
    callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
    client_id="prueba_controlada"
)

cliente.connect(BROKER, PUERTO, 60)
cliente.loop_start()

while not cliente.is_connected():
    time.sleep(0.1)

timestamp = datetime.now(timezone.utc).isoformat()

pruebas = [
    (
        "flota/VH-001/gps",
        {
            "vehicle_id": "VH-001",
            "timestamp": timestamp,
            "lat": -2.1709,
            "lng": -79.9224,
            "speed": 42
        }
    ),
    (
        "flota/VH-001/temperatura",
        {
            "vehicle_id": "VH-001",
            "timestamp": timestamp,
            "temperature": 7,
            "unit": "celsius"
        }
    ),
    (
        "flota/VH-001/combustible",
        {
            "vehicle_id": "VH-001",
            "timestamp": timestamp,
            "fuel_level": 15,
            "unit": "percent"
        }
    )
]

print("\nINICIANDO PRUEBAS CONTROLADAS\n")

for topic, datos in pruebas:
    resultado = cliente.publish(
        topic,
        json.dumps(datos),
        qos=1
    )

    resultado.wait_for_publish()

    print(f"PUBLICADO: {topic}")
    print(json.dumps(datos, indent=2))
    time.sleep(1)

print("\nPRUEBAS COMPLETADAS.")

cliente.disconnect()
cliente.loop_stop()
