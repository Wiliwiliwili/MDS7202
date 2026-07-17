from pathlib import Path

import cloudpickle
import pandas as pd
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

MODEL_PATH = Path(__file__).resolve().parent / "modelo_final.pkl"
EMBEDDING_MODEL = "gemini-embedding-001"
EMBEDDING_DIMENSIONS = 1024
EMBEDDING_COLUMNS = [f"embedding_dim_{i}" for i in range(1, EMBEDDING_DIMENSIONS + 1)]

with open(MODEL_PATH, "rb") as f:
    _pipeline = cloudpickle.load(f)

_embeddings_client = GoogleGenerativeAIEmbeddings(
    model=EMBEDDING_MODEL,
    output_dimensionality=EMBEDDING_DIMENSIONS,
)


def generate_prediction(asunto_ticket: str, contenido_ticket: str) -> str:
    """Predice el Nivel_Prioridad (Baja/Media/Alta/Critica) de un ticket de soporte.

    Vectoriza el asunto y contenido del ticket de forma idéntica a como se
    construyeron los embeddings usados para entrenar el modelo, y usa el
    pipeline entrenado (modelo_final.pkl) para generar la predicción.
    """
    texto = f"Asunto_Ticket: {asunto_ticket}\nContenido_Ticket: {contenido_ticket}\n"
    vector = _embeddings_client.embed_query(texto)

    X = pd.DataFrame([vector], columns=EMBEDDING_COLUMNS)
    prediction = _pipeline.predict(X)[0]
    return prediction


if __name__ == "__main__":
    ejemplo_asunto = "No puedo acceder a mi cuenta y tengo una transferencia urgente pendiente"
    ejemplo_contenido = (
        "Hola, buenas tardes. Intente ingresar a mi cuenta y me sale un error de "
        "autenticacion. Tengo una transferencia urgente que debo hacer hoy y no puedo "
        "acceder a mis fondos. Por favor ayudenme lo antes posible, es urgente."
    )
    resultado = generate_prediction(ejemplo_asunto, ejemplo_contenido)
    print(f"Asunto: {ejemplo_asunto}")
    print(f"Prediccion de Nivel_Prioridad: {resultado}")
