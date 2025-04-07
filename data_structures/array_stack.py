from data_structures.abstract_stack import Stack
from data_structures.referential_array import ArrayR, T

class ArrayStack(Stack[T]):
    """ Implementation of a stack with arrays.

    Attributes:
         length (int): number of elements in the stack (inherited)
         array (ArrayR[T]): array storing the elements of the queue
    """

    def __init__(self, max_capacity: int) -> None:
        if max_capacity <= 0:
            raise ValueError("Capacity should be larger than 0.")
        Stack.__init__(self)
        self.__array = ArrayR(max_capacity)
        self.__length = 0

    def is_full(self) -> bool:
        """ True if the stack is full and no element can be pushed. """
        return len(self) == len(self.__array)

    def push(self, item: T) -> None:
        """ Pushes an element to the top of the stack.
        :raises Exception: if the stack is full
        """
        if self.is_full():
            raise Exception("Stack is full")
        self.__array[len(self)] = item
        self.__length += 1

    def pop(self) -> T:
        """ Pops the element at the top of the stack.
        :raises Exception: if the stack is empty
        """
        if self.is_empty():
            raise Exception("Stack is empty")
        self.__length -= 1
        return self.__array[self.__length]

    def peek(self) -> T:
        """ Returns the element at the top, without popping it from stack.
        :raises Exception: if the stack is empty
        """
        if self.is_empty():
            raise Exception("Stack is empty")
        return self.__array[self.__length-1]
    
    def clear(self):
        self.__length = 0
    
    def __len__(self) -> int:
        """ Returns the number of items in the stack"""
        return self.__length
