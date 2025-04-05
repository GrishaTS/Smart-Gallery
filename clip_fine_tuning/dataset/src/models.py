from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import DeclarativeBase

class Model(DeclarativeBase):
    """Базовая модель для декларативного объявления ORM."""
    pass


class Clip100Orm(Model):
    __tablename__ = 'clip100'

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
