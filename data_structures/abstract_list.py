from abc import ABC, abstractmethod
from typing import TypeVar, Generic

T = TypeVar('T')


class List(ABC, Generic[T]):
    """ List ADT. 
    Defines a generic abstract list with the standard methods.
    """

    @abstractmethod
    def __getitem__(self, index: int) -> T:
        """ Return the element at the given position. """
        pass

    @abstractmethod
    def __setitem__(self, index: int, item: T) -> None:
        """ Insert the item at the given position. """
        pass

    @abstractmethod
    def __len__(self) -> int:
        """ Return the size of the list. """
        pass

    def __str__(self) -> str:
        """ String representation of the list object. """
        result = '['
        for i in range(len(self)):
            if i > 0:
                result += ', '
            result += str(self[i]) if type(self[i]) != str else f"'{self[i]}'"
        result += ']'
        return result

    def append(self, item: T) -> None:
        """ Append a new item to the end of the list. """
        self.insert(len(self), item)

    @abstractmethod
    def insert(self, index: int, item: T) -> None:
        """ Insert an item at the given position. """
        pass

    def remove(self, item: T) -> None:
        """ Remove an item from the list. """
        index = self.index(item)
        self.delete_at_index(index)

    @abstractmethod
    def delete_at_index(self, index: int) -> T:
        """ Delete item at a given position. """
        pass

    @abstractmethod
    def index(self, item: T) -> int:
        """ Find the position of a given item in the list. """
        pass

    def is_empty(self) -> bool:
        """ Check if the list of empty. """
        return len(self) == 0

    @abstractmethod
    def clear(self) -> None:
        """ Clear the list. """
        pass
