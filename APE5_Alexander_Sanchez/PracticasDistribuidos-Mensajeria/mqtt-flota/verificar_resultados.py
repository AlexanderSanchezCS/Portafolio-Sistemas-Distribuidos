import sqlite3

BASE_DATOS = "telemetria.db"


def verificar():
    conexion = sqlite3.connect(BASE_DATOS)
    cursor = conexion.cursor()

    tablas = ["gps_data", "temp_data", "fuel_data"]

    print("\n========== VERIFICACIÓN SQLITE ==========")

    for tabla in tablas:
        cursor.execute(f"SELECT COUNT(*) FROM {tabla}")
        cantidad = cursor.fetchone()[0]

        print(f"{tabla}: {cantidad} registros")

    print("\n========== DATOS DE TEMPERATURA ==========")

    cursor.execute("""
        SELECT vehicle_id, temperature, timestamp
        FROM temp_data
        ORDER BY id DESC
        LIMIT 10
    """)

    for fila in cursor.fetchall():
        print(fila)

    print("\n========== DATOS DE COMBUSTIBLE ==========")

    cursor.execute("""
        SELECT vehicle_id, fuel_level, timestamp
        FROM fuel_data
        ORDER BY id DESC
        LIMIT 10
    """)

    for fila in cursor.fetchall():
        print(fila)

    conexion.close()


if __name__ == "__main__":
    verificar()
