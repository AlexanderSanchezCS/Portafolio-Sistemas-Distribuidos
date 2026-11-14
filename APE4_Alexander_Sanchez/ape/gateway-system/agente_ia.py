import os
import requests
import json

# Configuración del servidor de IA (Open WebUI / Ollama de la carrera).
# Se leen de variables de entorno para no dejar credenciales en el código.
URL_COMPLETA = os.getenv("IA_URL", "")
API_KEY = os.getenv("IA_API_KEY", "")
MODELO = os.getenv("IA_MODELO", "qwen3-coder:30b")

def decidir_worker(pedido, estado_workers):
    prompt = f"""
    Eres un asignador inteligente de un sistema de delivery distribuido.
    Asigna el siguiente pedido al worker más adecuado (7001 o 7002):

    DATOS DEL PEDIDO:
    - ID: {pedido['id_pedido']}
    - Distancia del cliente: {pedido['distancia_km']} km
    - Prioridad: {pedido['prioridad']}

    ESTADO ACTUAL DE LOS WORKERS:
    - Worker 7001: Distancia = {estado_workers['7001']['distancia']} km, Carga actual = {estado_workers['7001']['carga']} pedidos
    - Worker 7002: Distancia = {estado_workers['7002']['distancia']} km, Carga actual = {estado_workers['7002']['carga']} pedidos

    Criterio: Balancear la carga sin descuidar pedidos de alta prioridad o distancias lejanas.
    Responde ÚNICAMENTE un JSON válido con esta estructura exacta:
    {{"worker_seleccionado": "7001" o "7002", "razon": "explicación breve"}}
    """

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODELO,
        "messages": [{"role": "user", "content": prompt}],
        "stream": False
    }

    try:
        if not URL_COMPLETA:
            raise RuntimeError("IA_URL no configurada")
        response = requests.post(URL_COMPLETA, headers=headers, json=payload, timeout=12)
        response.raise_for_status()
        
        resultado = response.json()
        texto_respuesta = resultado["choices"][0]["message"]["content"]
        
        return json.loads(texto_respuesta)

    except Exception as e:
        print(f"[Agente IA Error] {e}. Aplicando regla fija de respaldo.")
        if estado_workers['7001']['carga'] <= estado_workers['7002']['carga']:
            return {"worker_seleccionado": "7001", "razon": "Respaldo: Menor carga"}
        return {"worker_seleccionado": "7002", "razon": "Respaldo: Menor carga"}