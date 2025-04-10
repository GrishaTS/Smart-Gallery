from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from dataset.src.models import Model

# Путь к базе данных SQLite
DATABASE_URL = "sqlite:///./dataset/clip.db"

engine = create_engine(DATABASE_URL, echo=False)
sqlite_client = sessionmaker(bind=engine)


def init_db() -> None:
    """
    Инициализирует базу данных, создавая таблицы, определённые в модели.
    """
    Model.metadata.create_all(bind=engine)


# Инициализация БД при запуске скрипта напрямую
# python -m dataset.src.database
if __name__ == "__main__":
    init_db()
