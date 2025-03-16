from abc import ABC, abstractmethod

class BaseRepository(ABC):

    @staticmethod
    @abstractmethod
    async def add(*args, **kwargs):
        ...
    
    @staticmethod
    @abstractmethod
    async def get_by_id(*args, **kwargs):
        ...
    
    @staticmethod
    @abstractmethod
    async def delete(*args, **kwargs):
        ...
    
    @staticmethod
    @abstractmethod
    async def delete_all():
        ...

    @staticmethod
    async def get_all():
        ...
    
    @staticmethod
    async def search(*args, **kwargs):
        ...
