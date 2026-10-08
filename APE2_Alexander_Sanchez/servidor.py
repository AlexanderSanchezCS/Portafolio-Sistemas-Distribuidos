import time
from pathlib import Path

COM = Path(__file__).resolve().parent.parent / "comunicacion"
ENTRADA = COM / "entrada_servidor.txt"
SALIDA = COM / "salida_servidor.txt"
INTERVALO = 1  # segundos entre revisiones


def leer_lineas(ruta):
    if not ruta.exists():
        return []
    return ruta.read_text(encoding="utf-8").splitlines()


def procesar(mensaje):
    if not mensaje.strip():
        return "(mensaje vacío)"
    return mensaje.upper()  # también puedes usar mensaje[::-1]


def main():
    # Una línea de salida por cada línea de entrada ya procesada.
    # Así, si reinicias el servidor, no reprocesa mensajes viejos.
    procesados = len(leer_lineas(SALIDA))
    print("Servidor activo. Esperando mensajes... (Ctrl+C para salir)")

    while True:
        lineas = leer_lineas(ENTRADA)
        for linea in lineas[procesados:]:
            resultado = procesar(linea)
            with open(SALIDA, "a", encoding="utf-8") as f:
                f.write(resultado + "\n")
            procesados += 1
            print(f"Procesado: {linea!r} -> {resultado!r}")
        time.sleep(INTERVALO)


if __name__ == "__main__":
    main()