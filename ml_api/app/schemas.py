from datetime import datetime
from pydantic import BaseModel, ConfigDict

class ImageRequest(BaseModel):
    image_url: str


class TextRequest(BaseModel):
    text: str
