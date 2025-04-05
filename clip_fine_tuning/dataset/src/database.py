from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from dataset.src.models import Model

DATABASE_URL = "sqlite:///./dataset/clip.db"

engine = create_engine(DATABASE_URL, echo=False)
sqlite_client = sessionmaker(bind=engine)

def init_db():
    Model.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()
