# APE 3 – Ejercicio 3: Productor-Consumidor

Tres microservicios Spring Boot (almacén 8080, productor 8081, consumidor 8082) y un panel web (5500).

Requisitos: Git y Docker con Compose v2. Puertos libres: 5500, 8080, 8081 y 8082.

```bash
git clone https://github.com/AlexanderSanchezCS/Portafolio-Sistemas-Distribuidos.git
cd Portafolio-Sistemas-Distribuidos/APE3_Alexander_Sanchez/EJERCICIO3
docker compose up -d --build   # la primera vez tarda unos minutos
docker compose ps              # los 4 contenedores deben estar Up
```

Abrir **http://localhost:5500** (arriba, los 3 servicios deben salir en `UP`).

**Probar:**
1. Productores (2 hilos, 5 piezas) → **Ejecutar**: el almacén llega a 5/5 y 2 productores quedan bloqueados.
2. Consumidores (2 hilos, 5 piezas) → **Ejecutar**: Producidas 10 = Consumidas 10, ocupación 0/5, máx. ocupación 5.

```bash
docker compose restart almacen productor consumidor   # reinicia los contadores
docker compose down                                   # apagar todo
```

Si un puerto está ocupado, ejecuta `docker compose down` o cierra el programa que lo usa.
En Linux, si da `permission denied`: `sudo usermod -aG docker $USER` y reinicia la sesión.
