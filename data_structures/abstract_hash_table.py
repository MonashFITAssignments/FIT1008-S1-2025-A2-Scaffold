from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TypeVar, Generic
from data_structures.referential_array import ArrayR

K = TypeVar('K')
V = TypeVar('V')


class HashTable(ABC, Generic[K, V]):
    """
    Hash Table (Map/Dictionary) ADT. 
    Defines a generic abstract list with the standard methods.
    """

    @abstractmethod
    def __len__(self) -> int:
        pass
    
    @abstractmethod
    def keys(self) -> ArrayR[K]:
        pass

    @abstractmethod
    def values(self) -> ArrayR[V]:
        pass

    @abstractmethod
    def __contains__(self, key: K) -> bool:
        pass

    @abstractmethod
    def __getitem__(self, key: K) -> V:
        pass

    @abstractmethod
    def __setitem__(self, key: K, data: V) -> None:
        pass

    @abstractmethod
    def __delitem__(self, key: K) -> None:
        pass

    @abstractmethod
    def is_empty(self) -> bool:
        return len(self) == 0

    @abstractmethod
    def __str__(self) -> str:
        pass
