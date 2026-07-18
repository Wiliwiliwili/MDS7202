from fastapi import FastAPI, HTTPException
from generate_prediction import generate_prediction
from models import PredictionRequest, PredictionResponse

app = FastAPI(title="ChaucherApp - Priorizacion de Tickets")


@app.post("/predict", response_model=PredictionResponse)
def predict(request: PredictionRequest) -> PredictionResponse:
    try:
        nivel_prioridad = generate_prediction(
            asunto_ticket=request.asunto_ticket,
            contenido_ticket=request.contenido_ticket,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e

    return PredictionResponse(nivel_prioridad=nivel_prioridad)
