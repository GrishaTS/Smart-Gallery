from datetime import datetime
from pydantic import BaseModel, ConfigDict

class SImageAdd(BaseModel):
    image_path: str
    preview_path: str
    embedding_path: str
    size: int
    uploaded_at: datetime | None = None

class SImage(SImageAdd):
    id: int

    model_config = ConfigDict(from_attributes=True)

class SImageId(BaseModel):
    id: int
