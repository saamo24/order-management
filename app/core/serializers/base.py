from abc import ABC, abstractmethod
from typing import Any, Dict, List, TypeVar, Generic

T = TypeVar('T')
S = TypeVar('S')


class BaseSerializer(ABC, Generic[T, S]):
    """Base serializer class."""
    
    @abstractmethod
    async def serialize(self, data: T) -> S:
        """Serialize data."""
        raise NotImplementedError
        
    async def serialize_list(self, data_list: List[T]) -> List[S]:
        """Serialize a list of data."""
        return [await self.serialize(item) for item in data_list]
    
