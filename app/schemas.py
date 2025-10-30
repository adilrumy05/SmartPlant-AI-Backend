from pydantic import BaseModel
from datetime import datetime

class PredictionOut(BaseModel):
    id: int
    species_name: str
    confidence_score: float
    image_path: str
    timestamp: datetime
    flagged_unsure: bool

    class Config:
        orm_mode = True
