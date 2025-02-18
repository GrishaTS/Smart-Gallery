from dataclasses import dataclass
from datetime import datetime

@dataclass
class ImageData:
    id: int
    image_path: str
    preview_path: str
    embedding_path: str
    uploaded_at: datetime
    size: int
    
    def __post_init__(self):
        self.uploaded_at = datetime.strptime(self.uploaded_at, "%Y-%m-%dT%H:%M:%S")
