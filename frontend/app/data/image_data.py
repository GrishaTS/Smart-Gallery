import re
import base64
from dataclasses import dataclass
from datetime import datetime
from config import settings

@dataclass
class ImageData:
    id: int = None
    image_object_name: str = None
    thumbnail_object_name: str = None
    embedding_vector_id: str = None
    uploaded_at: datetime = None
    size: int = None

    def __post_init__(self):
        if isinstance(self.uploaded_at, str) and re.fullmatch(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.\d{6}', self.uploaded_at):
            self.uploaded_at = datetime.strptime(self.uploaded_at, '%Y-%m-%dT%H:%M:%S.%f')
        else:
            self.uploaded_at = None

    def __eq__(self, other):
        return isinstance(other, ImageData) and self.id is not None and self.id == other.id
    
    @staticmethod
    def minio_link(object_name: str):
        return f'{settings.MINIO_BUCKET_URL}/{object_name}'
