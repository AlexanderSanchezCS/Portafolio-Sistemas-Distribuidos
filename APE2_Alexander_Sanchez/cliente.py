import time
from pathlib import Path

COM = Path(__file__).resolve().parent.parent / "comunicacion"
ENTRADA = COM / "entrada_servidor.txt"
SALIDA = COM / "salida_servidor.txt"
LATENCIA = 2   # espera inicial simulada
TIMEOUT = 10   # máximo de espera por respuesta


def leer_lineas(ruta):
    if not ruta.exists():
        return []
    return ruta.read_text(encoding="utf-8").splitlines()


def main():
    while True:
        mensaje = input("Mensaje (o 'salir'): ").strip()
        if mensaje.lower() == "salida" or mensaje.lower() == "salir":
            break
        if not mensaje:
            continue

        previas = len(leer_lineas(SALIDA))

        with open(ENTRADA, "a", encoding="utf-8") as f:
            f.write(mensaje + "\n")
        print("Mensaje enviado, esperando respuesta...")

        time.sleep(LATENCIA)
        inicio = time.time()
        while time.time() - inicio < TIMEOUT:
            lineas = leer_lineas(SALIDA)
            if len(lineas) > previas:
                print("Respuesta:", lineas[-1])
                break
            time.sleep(0.5)
        else:
            print("Sin respuesta: ¿el servidor está ejecutándose?")


if __name__ == "__main__":
    main()