from data_structures.node import Node
from data_structures.abstract_stack import Stack, T


class LinkedStack(Stack[T]):
    """ Implementation of a stack with linked nodes. """

    def __init__(self, _=None) -> None:
        Stack.__init__(self)
        self.__top = None
        self.__length = 0

    def clear(self) -> None:
        """" Resets the stack to an empty state. """
        Stack.clear(self)
        self.__top = None
        self.__length = 0

    def __len__(self) -> int:
        """ Returns the number of elements in the stack.
        :complexity: O(1)
        """
        return self.__length

    def is_full(self) -> bool:
        """ Returns whether the stack is full
        The linked implementation is never full.
        """
        return False

    def push(self, item: T) -> None:
        """ Pushes an element to the top of the stack.
        :complexity: O(1)
        """
        new_node = Node(item)
        new_node.link = self.__top
        self.__top = new_node
        self.__length += 1

    def pop(self) -> T:
        """ Pops the element at the top of the stack.
        :complexity: O(1)
        :raises Exception: if the stack is empty
        """
        if self.is_empty():
            raise Exception('Stack is empty')

        item = self.__top.item
        self.__top = self.__top.link
        self.__length -= 1
        return item

    def peek(self) -> T:
        """ Returns the element at the top, without popping it from stack.
        :complexity: O(1)
        :raises Exception: if the stack is empty
        """
        if self.is_empty():
            raise Exception('Stack is empty')
        return self.__top.item
