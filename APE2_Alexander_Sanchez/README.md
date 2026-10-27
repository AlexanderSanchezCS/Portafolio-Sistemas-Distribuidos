# APE 2 – Cliente-servidor con archivos

Requisitos: Python 3 y Git. Se usan 3 terminales (en Windows: `python` y `type`).

```bash
# Descargar (una sola vez)
git clone https://github.com/AlexanderSanchezCS/Portafolio-Sistemas-Distribuidos.git
cd Portafolio-Sistemas-Distribuidos/APE2_Alexander_Sanchez
mkdir -p ../comunicacion

# Terminal 1: servidor (debe mostrar "Servidor activo..." y quedarse corriendo)
python3 servidor.py

# Terminal 2: cliente (misma carpeta). Escribe: hola, sistemas distribuidos, prueba 3, salir
python3 cliente.py

# Terminal 3: evidencia (misma carpeta)
cat ../comunicacion/entrada_servidor.txt
cat ../comunicacion/salida_servidor.txt
```

Para detener: `Ctrl + C` en la Terminal 1.
