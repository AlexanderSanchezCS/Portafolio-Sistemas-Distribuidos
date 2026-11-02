import json
import sqlite3
from datetime import datetime, timezone

import paho.mqtt.client as mqtt

BROKER = "localhost"
PUERTO = 1883
BASE_DATOS = "telemetria.db"


def inicializar_base_datos():
    conexion = sqlite3.connect(BASE_DATOS)
    cursor = conexion.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS gps_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            vehicle_id TEXT NOT NULL,
            lat REAL,
            lng REAL,
            speed REAL,
            timestamp TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS temp_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            vehicle_id TEXT NOT NULL,
            temperature REAL,
            unit TEXT,
            timestamp TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS fuel_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            vehicle_id TEXT NOT NULL,
            fuel_level REAL,
            unit TEXT,
            timestamp TEXT
        )
    """)

    conexion.commit()
    conexion.close()

    print("Base de datos inicializada correctamente.")


def guardar_datos(topic, datos):
    conexion = sqlite3.connect(BASE_DATOS)
    cursor = conexion.cursor()

    if topic.endswith("/gps"):
        cursor.execute("""
            INSERT INTO gps_data
            (vehicle_id, lat, lng, speed, timestamp)
            VALUES (?, ?, ?, ?, ?)
        """, (
            datos["vehicle_id"],
            datos["lat"],
            datos["lng"],
            datos["speed"],
            datos["timestamp"]
        ))

        print(
            f"[GPS] {datos['vehicle_id']} "
            f"Velocidad: {datos['speed']} km/h"
        )

    elif topic.endswith("/temperatura"):
        temperatura = datos["temperature"]

        cursor.execute("""
            INSERT INTO temp_data
            (vehicle_id, temperature, unit, timestamp)
            VALUES (?, ?, ?, ?)
        """, (
            datos["vehicle_id"],
            temperatura,
            datos["unit"],
            datos["timestamp"]
        ))

        if temperatura > 4:
            print(
                f"[ALERTA TEMPERATURA] {datos['vehicle_id']} "
                f"Temperatura alta: {temperatura} °C"
            )
        else:
            print(
                f"[TEMPERATURA NORMAL] {datos['vehicle_id']}: "
                f"{temperatura} °C"
            )

    elif topic.endswith("/combustible"):
        combustible = datos["fuel_level"]

        cursor.execute("""
            INSERT INTO fuel_data
            (vehicle_id, fuel_level, unit, timestamp)
            VALUES (?, ?, ?, ?)
        """, (
            datos["vehicle_id"],
            combustible,
            datos["unit"],
            datos["timestamp"]
        ))

        if combustible < 20:
            print(
                f"[ALERTA COMBUSTIBLE] {datos['vehicle_id']} "
                f"Nivel bajo: {combustible}%"
            )
        else:
            print(
                f"[COMBUSTIBLE NORMAL] {datos['vehicle_id']}: "
                f"{combustible}%"
            )

    conexion.commit()
    conexion.close()


def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        print("Suscriptor conectado a Mosquitto.")

        client.subscribe([
            ("flota/+/gps", 1),
            ("flota/+/temperatura", 1),
            ("flota/+/combustible", 1)
        ])

        print("Suscrito a los tres tipos de sensores.")

    else:
        print(f"Error de conexión: {reason_code}")


def on_message(client, userdata, mensaje):
    try:
        topic = mensaje.topic
        datos = json.loads(mensaje.payload.decode("utf-8"))

        guardar_datos(topic, datos)

    except (ValueError, KeyError, sqlite3.Error) as error:
        print(f"Error procesando mensaje: {error}")


def main():
    inicializar_base_datos()

    cliente = mqtt.Client(
        callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
        client_id="suscriptor_sqlite"
    )

    cliente.on_connect = on_connect
    cliente.on_message = on_message

    try:
        cliente.connect(BROKER, PUERTO, 60)
        print("Esperando mensajes MQTT...")
        cliente.loop_forever()

    except KeyboardInterrupt:
        print("\nSuscriptor detenido.")

    finally:
        cliente.disconnect()


if __name__ == "__main__":
    main()
