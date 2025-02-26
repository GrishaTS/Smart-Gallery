import base64
from dataclasses import dataclass
from datetime import datetime

@dataclass
class ImageData:
    id: int = None
    image_path: str = None
    preview_path: str = None
    embedding_path: str = None
    uploaded_at: datetime = None
    size: int = None
    
    def __post_init__(self):
        if self.uploaded_at:
            self.uploaded_at = datetime.strptime(self.uploaded_at, "%Y-%m-%dT%H:%M:%S")
    
    def __eq__(self, other):
        return self.id == other.id
    
    @staticmethod
    def img_to_base64(path):
        data_url = None
        with open(path, "rb") as img_file:
            img_bytes = img_file.read()
            base64_str = base64.b64encode(img_bytes).decode('utf-8')
            data_url = f'data:image/png;base64,{base64_str}'
        return data_url
