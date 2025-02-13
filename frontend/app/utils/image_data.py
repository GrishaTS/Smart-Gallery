from dataclasses import dataclass
from datetime import datetime

@dataclass
class ImageData:
    image_path: str
    preview_path: str
    embedding_path: str
    created_at: datetime
    size_bytes: int
    
    def __post_init__(self):
        self.uploaded_at = datetime.strptime(self.uploaded_at, "%Y-%m-%d %H:%M:%S")
