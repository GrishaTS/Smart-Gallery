import re
import base64
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

@dataclass
class ImageData:
    id: int = None
    image_path: str = None
    preview_path: str = None
    embedding_path: str = None
    uploaded_at: datetime = None
    size: int = None

    def __post_init__(self):
        if isinstance(self.uploaded_at, str) and re.fullmatch(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}', self.uploaded_at):
            self.uploaded_at = datetime.strptime(self.uploaded_at, '%Y-%m-%dT%H:%M:%S')
        else:
            self.uploaded_at = None

    def __eq__(self, other):
        return isinstance(other, ImageData) and self.id is not None and self.id == other.id

    @staticmethod
    def img_to_base64(path: str) -> str:
        img_path = Path(path)
        if img_path.exists():
            ext = img_path.suffix[1:]
            with img_path.open('rb') as img_file:
                base64_str = base64.b64encode(img_file.read()).decode('utf-8')
            return f'data:image/{ext};base64,{base64_str}'
        return None
