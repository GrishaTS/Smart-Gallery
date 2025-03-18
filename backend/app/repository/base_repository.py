from abc import ABC, abstractmethod
from typing import Any


class BaseRepository(ABC):
    """Абстрактный базовый класс для репозитория."""

    @staticmethod
    @abstractmethod
    async def add(*args: Any, **kwargs: Any) -> None:
        """Добавляет запись в репозиторий."""
        ...

    @staticmethod
    @abstractmethod
    async def get_by_id(*args: Any, **kwargs: Any) -> Any:
        """Получает запись по идентификатору."""
        ...

    @staticmethod
    @abstractmethod
    async def delete(*args: Any, **kwargs: Any) -> None:
        """Удаляет запись из репозитория."""
        ...

    @staticmethod
    @abstractmethod
    async def delete_all() -> None:
        """Удаляет все записи из репозитория."""
        ...

    @staticmethod
    async def get_all() -> Any:
        """Получает все записи из репозитория."""
        ...

    @staticmethod
    async def search(*args: Any, **kwargs: Any) -> Any:
        """Ищет записи в репозитории по заданным параметрам."""
        ...
