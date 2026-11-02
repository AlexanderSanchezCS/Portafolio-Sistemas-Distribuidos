import json
import time
import random
import argparse
from datetime import datetime, timezone

import paho.mqtt.client as mqtt

BROKER = "localhost"
PUERTO = 1883

VEHICULOS = ["VH-001", "VH-002", "VH-003"]


def simular_gps():
    return {
        "lat": round(-2.1709 + random.uniform(-0.01, 0.01), 6),
        "lng": round(-79.9224 + random.uniform(-0.01, 0.01), 6),
        "speed": round(random.uniform(20, 80), 1)
    }


def simular_temperatura():
    return {
        "temperature": round(random.uniform(-5, 8), 1),
        "unit": "celsius"
    }


def simular_combustible():
    return {
        "fuel_level": round(random.uniform(10, 100), 1),
        "unit": "percent"
    }


def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        print("Conectado correctamente al broker MQTT.")
    else:
        print(f"Error de conexión: {reason_code}")


def publicar(cliente, vehiculo, sensor, datos):
    timestamp = datetime.now(timezone.utc).isoformat()

    payload = {
        "vehicle_id": vehiculo,
        "timestamp": timestamp,
        **datos
    }

    topic = f"flota/{vehiculo}/{sensor}"

    resultado = cliente.publish(
        topic,
        json.dumps(payload),
        qos=1
    )

    resultado.wait_for_publish()

    if resultado.rc == mqtt.MQTT_ERR_SUCCESS:
        print(f"[PUBLICADO] {topic}")
        print(json.dumps(payload, indent=2))
    else:
        print(f"Error al publicar: {topic}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--rondas",
        type=int,
        default=0,
        help="Número de rondas. 0 significa ejecución continua."
    )
    args = parser.parse_args()

    cliente = mqtt.Client(
        callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
        client_id="simulador_flota"
    )

    cliente.on_connect = on_connect

    try:
        cliente.connect(BROKER, PUERTO, 60)
        cliente.loop_start()

        while not cliente.is_connected():
            time.sleep(0.1)

        print("\nSIMULADOR DE SENSORES IOT INICIADO")
        print(f"Vehículos: {len(VEHICULOS)}")
        print("Sensores: GPS, temperatura y combustible")
        print("QoS: 1\n")

        ronda = 0

        while args.rondas == 0 or ronda < args.rondas:
            ronda += 1
            print(f"\n========== RONDA {ronda} ==========")

            for vehiculo in VEHICULOS:

                print(f"\nVehículo: {vehiculo}")

                publicar(cliente, vehiculo, "gps", simular_gps())

                publicar(
                    cliente,
                    vehiculo,
                    "temperatura",
                    simular_temperatura()
                )

                publicar(
                    cliente,
                    vehiculo,
                    "combustible",
                    simular_combustible()
                )

                print("Esperando 5 segundos...")
                time.sleep(5)

            print(f"\nRonda {ronda} completada: 9 mensajes.")

    except KeyboardInterrupt:
        print("\nSimulador detenido por el usuario.")

    except Exception as error:
        print(f"Error: {error}")

    finally:
        cliente.disconnect()
        cliente.loop_stop()


if __name__ == "__main__":
    main()
