import json
import pika
import paho.mqtt.client as mqtt

MQTT_BROKER = "localhost"
MQTT_PORT = 1883

RABBITMQ_HOST = "localhost"
RABBITMQ_USER = "guest"
RABBITMQ_PASS = "guest"

COLA_GPS = "cola.gps.telemetria"
COLA_TEMP = "cola.alertas.temperatura"
COLA_FUEL = "cola.combustible.nivel"


def configurar_rabbitmq():
    credenciales = pika.PlainCredentials(
        RABBITMQ_USER,
        RABBITMQ_PASS
    )

    parametros = pika.ConnectionParameters(
        host=RABBITMQ_HOST,
        port=5672,
        credentials=credenciales,
        heartbeat=60
    )

    conexion = pika.BlockingConnection(parametros)
    canal = conexion.channel()

    canal.queue_declare(queue=COLA_GPS, durable=True)
    canal.queue_declare(queue=COLA_TEMP, durable=True)
    canal.queue_declare(queue=COLA_FUEL, durable=True)

    print("Tres colas RabbitMQ declaradas correctamente.")

    return conexion, canal


def publicar_en_cola(canal, cola, datos):
    mensaje = json.dumps(datos)

    canal.basic_publish(
        exchange="",
        routing_key=cola,
        body=mensaje,
        properties=pika.BasicProperties(
            delivery_mode=2,
            content_type="application/json"
        )
    )

    print(f"[RABBITMQ] Mensaje enviado a: {cola}")


def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        print("Puente conectado a Mosquitto.")
        client.subscribe("flota/#", qos=1)
        print("Escuchando todos los topics de flota/#")
    else:
        print(f"Error MQTT: {reason_code}")


def on_message(client, userdata, mensaje):
    canal = userdata["canal"]

    try:
        topic = mensaje.topic
        datos = json.loads(mensaje.payload.decode("utf-8"))

        if topic.endswith("/gps"):
            publicar_en_cola(canal, COLA_GPS, datos)

        elif topic.endswith("/temperatura"):
            temperatura = datos["temperature"]

            if temperatura > 4:
                alerta = {
                    "type": "TEMP_ALERT",
                    "message": "Temperatura excedida",
                    **datos
                }

                publicar_en_cola(canal, COLA_TEMP, alerta)

        elif topic.endswith("/combustible"):
            combustible = datos["fuel_level"]

            if combustible < 20:
                alerta = {
                    "type": "FUEL_LOW",
                    "message": "Combustible bajo",
                    **datos
                }

                publicar_en_cola(canal, COLA_FUEL, alerta)

    except Exception as error:
        print(f"Error procesando mensaje: {error}")


def main():
    conexion, canal = configurar_rabbitmq()

    cliente = mqtt.Client(
        callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
        client_id="puente_mqtt_rabbitmq",
        userdata={"canal": canal}
    )

    cliente.on_connect = on_connect
    cliente.on_message = on_message

    try:
        cliente.connect(MQTT_BROKER, MQTT_PORT, 60)

        print("Puente MQTT-RabbitMQ iniciado.")

        # Atiende MQTT y los heartbeats de RabbitMQ en el mismo hilo.
        while True:
            cliente.loop(timeout=1.0)
            conexion.process_data_events(time_limit=0)

    except KeyboardInterrupt:
        print("\nDeteniendo puente...")

    finally:
        cliente.disconnect()

        if conexion.is_open:
            conexion.close()

        print("Conexiones cerradas.")


if __name__ == "__main__":
    main()
