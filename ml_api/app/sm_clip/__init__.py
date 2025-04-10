from app.config import settings
from .base_clip import BaseClip
match settings.ML_API_MODEL:
    case 'ViT-B-32':
        from .clip_vit_b_32 import ClipVitB32
    case 'ruclip_clip993':
        from .ruclip_clip993 import RuClipFTClip933
model = BaseClip.get_model()