
from typing import TypeVar

from data_structures.node import Node
from data_structures.abstract_queue import Queue

T = TypeVar("T")


class LinkedQueue(Queue[T]):
    """ Linked Queue
    The Queue ADT implemented using a linked structure.
    """

    def __init__(self) -> None:
        Queue.__init__(self)
        self.__front = None
        self.__rear = None
        self.__length = 0

    def __len__(self) -> int:
        """ Returns the number of elements in the queue. """
        return self.__length
    
    def append(self, item: T) -> None:
        """ Adds an element to the rear of the queue.
        :raises Exception: if the queueu is full.
        """
        # Case 1: Empty queue
        if self.__front is None:
            self.__front = Node(item)
            self.__rear = self.__front
            self.__length += 1
            return

        # Case 2: Non Empty queue
        # Add to the rear
        new_node = Node(item)
        self.__rear.link = new_node
        self.__rear = new_node
        self.__length += 1

    def serve(self) -> T:
        """ Deletes and returns the element at the queue's front.
        :raises Exception: if the queue is empty
        """
        if self.is_empty():
            raise Exception("Queue is empty")

        # Case 1: Single element in the queue
        if self.__front == self.__rear:
            item = self.__front.item
            self.__front = None
            self.__rear = None
            self.__length -= 1
            return item

        # Case 2: Multiple elements in the queue
        item = self.__front.item
        self.__front = self.__front.link
        self.__length -= 1
        return item

    def peek(self) -> T:
        """ Returns the element at the queue's front without deleting it.
        :raises Exception: if the queue is empty
        """
        if self.is_empty():
            raise Exception("Queue is empty")
        return self.__front.item

    def peek_node(self) -> Node:
        """ Returns the node at the queue's front without deleting it.
        :pre: queue is not empty
        :raises Exception: if the queue is empty
        """
        if self.is_empty():
            raise Exception("Queue is empty")
        return self.__front

    def is_full(self) -> bool:
        """ Checks if the queue is full.
        Unlike an array-based queue, a linked queue cannot be full, unless
        the system runs out of memory which is a different issue.
        """
        return False

    def clear(self) -> None:
        """ Clears all elements from the queue. """
        Queue.__init__(self)
        self.__front = None
        self.__rear = None
        self.__length = 0

    def __str__(self) -> str:
        """ Returns a string representation of the queue."""
        i = self.__front
        result = ""
        count = 1  # 1-based counting
        while i is not None:
            result += f"p{count}: " + (str(i.item) if type(i.item) != str else "'{0}'".format(i.item))
            if i.link is not None:
                result += ", "
            i = i.link
            count += 1
        return result

    def __repr__(self) -> str:
        """Returns a string representation of the queue object.
        Useful for debugging or when the queue is held in another data structure."""
        return str(self)
