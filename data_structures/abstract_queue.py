from abc import ABC, abstractmethod
from typing import TypeVar, Generic

T = TypeVar('T')


class Queue(ABC, Generic[T]):
    """ Queue ADT
    Defines a generic abstract queue with the usual methods.
    """

    @abstractmethod
    def append(self, item:T) -> None:
        """ Adds an element to the rear of the queue."""
        pass

    @abstractmethod
    def serve(self) -> T:
        """ Deletes and returns the element at the queue's front."""
        pass

    @abstractmethod
    def __len__(self) -> int:
        """ Returns the number of elements in the queue."""
        pass

    def is_empty(self) -> bool:
        """ True if the queue is empty. """
        return len(self) == 0

    @abstractmethod
    def is_full(self) -> bool:
        """ True if the stack is full and no element can be pushed. """
        pass

    @abstractmethod
    def clear(self):
        """ Clears all elements from the queue. """
        pass
