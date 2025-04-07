from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TypeVar, Generic
from data_structures.referential_array import ArrayR

T = TypeVar('T')


class Set(ABC, Generic[T]):
    """ Set ADT.
    Defines a generic abstract set with the usual methods.
    """

    @abstractmethod
    def __len__(self) -> int:
        """ Returns the number of elements in the set. """
        pass

    @abstractmethod
    def is_empty(self) -> bool:
        """ True if the set is empty. """
        pass

    @abstractmethod
    def clear(self) -> None:
        """ Clear the set. """
        pass

    @abstractmethod
    def __contains__(self, item: T) -> bool:
        """ True if the set contains the item. """
        pass

    @abstractmethod
    def add(self, item: T) -> None:
        """
        Adds an element to the set.
        Note that an element already present in the set should not be added.
        """
        pass

    @abstractmethod
    def remove(self, item: T) -> None:
        """
        Removes an element from the set.
        An exception should be raised if the element to remove is not present in the set.
        """
        pass

    @abstractmethod
    def values(self) -> ArrayR[T]:
        """
        Returns an array of all the items in the set in no particular order.
        """
        pass

    @abstractmethod
    def union(self, other: Set[T]) -> Set[T]:
        """ Makes a union of the set with another set. """
        pass

    @abstractmethod
    def intersection(self, other: Set[T]) -> Set[T]:
        """ Makes an intersection of the set with another set. """
        pass

    @abstractmethod
    def difference(self, other: Set[T]) -> Set[T]:
        """ Creates a difference of the set with another set. """
        pass

    def __and__(self, other: Set[T]) -> Set[T]:
        """ Magic method alias for intersection """
        return self.intersection(other)
    
    def __or__(self, other: Set[T]) -> Set[T]:
        """ Magic method alias for union """
        return self.union(other)
    
    def __sub__(self, other: Set[T]) -> Set[T]:
        """ Magic method alias for difference """
        return self.difference(other)
    