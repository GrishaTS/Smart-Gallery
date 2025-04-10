from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import DeclarativeBase


class Model(DeclarativeBase):
    """
    Базовый класс для декларативного объявления моделей SQLAlchemy.
    Используется как родительский для всех ORM-классов.
    """
    pass


class Clip993Orm(Model):
    """
    ORM-модель для таблицы clip993. Хранит ссылку на изображение и 10 текстовых описаний.

    Атрибуты:
        id (int): Уникальный идентификатор.
        image_url (str): URL изображения (уникальный).
        description1..10 (str): Текстовые описания, связанные с изображением.
    """
    __tablename__ = 'clip993'

    id = Column(Integer, primary_key=True)
    image_url = Column(String, nullable=False, unique=True)
    description1 = Column(String, nullable=False)
    description2 = Column(String, nullable=False)
    description3 = Column(String, nullable=False)
    description4 = Column(String, nullable=False)
    description5 = Column(String, nullable=False)
    description6 = Column(String, nullable=False)
    description7 = Column(String, nullable=False)
    description8 = Column(String, nullable=False)
    description9 = Column(String, nullable=False)
    description10 = Column(String, nullable=False)
