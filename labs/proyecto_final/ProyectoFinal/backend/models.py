from pydantic import BaseModel, Field


class PredictionRequest(BaseModel):
    asunto_ticket: str = Field(..., description="Asunto del ticket de soporte")
    contenido_ticket: str = Field(..., description="Contenido/descripción del ticket de soporte")


class PredictionResponse(BaseModel):
    nivel_prioridad: str = Field(..., description="Prioridad predicha: Baja, Media, Alta o Critica")
