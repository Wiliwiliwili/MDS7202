import os

import requests

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")


def enviar_prediccion(asunto_ticket: str, contenido_ticket: str) -> str:
    """Llama al endpoint /predict del backend y retorna el Nivel_Prioridad predicho."""
    response = requests.post(
        f"{BACKEND_URL}/predict",
        json={"asunto_ticket": asunto_ticket, "contenido_ticket": contenido_ticket},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()["nivel_prioridad"]
