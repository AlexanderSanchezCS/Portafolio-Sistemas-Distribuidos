# De los sensores a las colas: MQTT + SQLite + RabbitMQ

## Descripción
Proyecto de integración de sensores de telemetría vehicular mediante el protocolo MQTT, almacenamiento de información en SQLite y distribución de mensajes mediante RabbitMQ.

El sistema simula información de vehículos, recibe los datos mediante Mosquitto, identifica condiciones de alerta y almacena los registros para su posterior verificación.

## Contenido de esta carpeta
- [Informe del APE 5 (PDF)](APE5_Alexander_S%C3%A1nchez.pdf)
- `PracticasDistribuidos-Mensajeria/`: código fuente y configuración de la práctica

## Tecnologías utilizadas
- Python
- MQTT (Mosquitto)
- SQLite
- RabbitMQ
- Docker y Docker Compose
- Paho MQTT
- Pika

## Estructura del proyecto
```
mqtt-flota/
├── docker-compose.yml
├── mosquitto/
│   ├── config/
│   │   └── mosquitto.conf
│   ├── data/
│   └── log/
├── simulador_sensores.py
├── suscriptor_sqlite.py
├── mqtt_rabbitmq_bridge.py
├── prueba_alertas.py
├── verificar_resultados.py
├── requirements.txt
└── telemetria.db
```

## Instalación
Entrar a la carpeta del proyecto:
```
cd PracticasDistribuidos-Mensajeria/mqtt-flota
```

Crear y activar el entorno virtual:
```
python -m venv .venv
source .venv/bin/activate
```

Instalar dependencias:
```
pip install -r requirements.txt
```

Iniciar los servicios:
```
docker compose up -d
```

## Ejecución
Ejecutar cada componente en una terminal independiente (dentro de `PracticasDistribuidos-Mensajeria/mqtt-flota` y con el entorno virtual activado):

1. Suscriptor MQTT y SQLite
```
python -u suscriptor_sqlite.py
```

2. Puente MQTT-RabbitMQ
```
python -u mqtt_rabbitmq_bridge.py
```

3. Simulación de sensores
```
python -u simulador_sensores.py
```

4. Pruebas controladas
```
python -u prueba_alertas.py
```

5. Verificación de resultados
```
python -u verificar_resultados.py
```

## Condiciones de alerta
- Temperatura superior a 4 °C: genera una alerta de temperatura.
- Nivel de combustible inferior al 20 %: genera una alerta de combustible bajo.

## Colas de RabbitMQ
- `cola.gps.telemetria`
- `cola.alertas.temperatura`
- `cola.combustible.nivel`

## Resultados
La información recibida se almacena en SQLite y los mensajes correspondientes se distribuyen en las colas de RabbitMQ para su procesamiento.

## Detener los servicios
```
docker compose down
```
