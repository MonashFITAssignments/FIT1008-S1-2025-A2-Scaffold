from data_structures.abstract_queue import Queue, T
from data_structures.referential_array import ArrayR


class CircularQueue(Queue[T]):
    """ Circular implementation of a queue with arrays.

    Attributes:
         length (int): number of elements in the stack (inherited)
         front (int): index of the element at the front of the queue
         rear (int): index of the first empty space at the back of the queue
         array (ArrayR[T]): array storing the elements of the queue
    """

    def __init__(self, max_capacity: int) -> None:
        if max_capacity <= 0:
            raise ValueError("Capacity should be larger than 0.")

        Queue.__init__(self)
        self.__front = 0
        self.__rear = 0
        self.__length = 0
        self.__array = ArrayR(max_capacity)

    def append(self, item: T) -> None:
        """ Adds an element to the rear of the queue.
        :raises Exception: if the queue is full
        """
        if self.is_full():
            raise Exception("Queue is full")

        self.__array[self.__rear] = item
        self.__length += 1
        self.__rear = (self.__rear + 1) % len(self.__array)

    def serve(self) -> T:
        """ Deletes and returns the element at the queue's front.
        :raises Exception: if the queue is empty
        """
        if self.is_empty():
            raise Exception("Queue is empty")

        self.__length -= 1
        item = self.__array[self.__front]
        self.__front = (self.__front+1) % len(self.__array)
        return item

    def peek(self) -> T:
        """ Returns the element at the queue's front.
        :raises Exception: if the queue is empty
        """
        if self.is_empty():
            raise Exception("Queue is empty")

        return self.__array[self.__front]

    def is_full(self) -> bool:
        """ True if the queue is full and no element can be appended. """
        return len(self) == len(self.__array)

    def clear(self) -> None:
        """ Clears all elements from the queue. """
        Queue.__init__(self)
        self.__front = 0
        self.__rear = 0
        self.__length = 0

    def __len__(self) -> int:
        """ Returns the number of elements in the queue. """
        return self.__length