from abc import ABC, abstractmethod
from typing import TypeVar, Generic

T = TypeVar('T')


class Stack(ABC, Generic[T]):
    """ Stack ADT. 
    Defines a generic abstract stack with the usual methods.
    """

    @abstractmethod
    def push(self, item: T) -> None:
        """ Pushes an element to the top of the stack."""
        pass

    @abstractmethod
    def pop(self) -> T:
        """ Pops an element from the top of the stack."""
        pass

    @abstractmethod
    def peek(self) -> T:
        """ Pops the element at the top of the stack."""
        pass

    @abstractmethod
    def __len__(self) -> int:
        """ Returns the number of elements in the stack."""
        pass

    def is_empty(self) -> bool:
        """ Returns True iff the stack is empty. """
        return len(self) == 0

    @abstractmethod
    def is_full(self) -> bool:
        """ Returns True iff the stack is full and no element can be pushed. """
        pass

    @abstractmethod
    def clear(self):
        """ Clears all elements from the stack. """
        pass
