from data_structures.abstract_list import List, T
from data_structures.node import Node


class LinkedListIterator:
    """ Iterator for LinkedList. """
    def __init__(self, head_node: Node):
        self.__current = head_node

    def __iter__(self):
        return self

    def __next__(self):
        if self.__current is None:
            raise StopIteration
        else:
            item = self.__current.item
            self.__current = self.__current.link
            return item


class LinkedList(List[T]):
    """ Linked-node based implementation of List ADT. """

    def __init__(self):
        List.__init__(self)
        self.__head = None
        self.__rear = None
        self.__length = 0

    def clear(self):
        """ Clear the list. """
        List.clear(self)
        self.__head = None
        self.__rear = None
        self.__length = 0

    def __setitem__(self, index: int, item: T) -> None:
        """ Insert the item at a given position. """
        node_at_index = self.__get_node_at_index(index)
        node_at_index.item = item

    def __getitem__(self, index: int) -> T:
        """ Return the element at a given position. """
        node_at_index = self.__get_node_at_index(index)
        return node_at_index.item

    def __len__(self) -> int:
        """ Return the number of elements in the list. """
        return self.__length

    def __iter__(self):
        """ Iterate through the list. """
        return LinkedListIterator(self.__head)

    def __contains__(self, item: T) -> bool:
        """ Check if the item is in the list. """
        current = self.__head
        while current is not None and current.item != item:
            current = current.link
        return current is not None

    def append(self, item: T) -> None:
        """ Append the item to the end of the list. 
        Given we have a reference to the rear of the list, this is O(1).
        """
        new_node = Node(item)
        if self.__head is None:
            self.__head = new_node
        else:
            self.__rear.link = new_node
        self.__rear = new_node
        self.__length += 1

    def __get_node_at_index(self, index: int) -> Node[T]:
        if -1 * len(self) <= index and index < len(self):
            if index < 0:
                index = len(self) + index
            current = self.__head
            for i in range(index):
                current = current.link
            return current
        else:
            raise IndexError('Out of bounds access in list.')

    def index(self, item: T) -> int:
        """ Find the position of a given item in the list. """
        current = self.__head
        index = 0
        while current is not None and current.item != item:
            current = current.link
            index += 1
        if current is None:
            raise ValueError('Item is not in list')
        else:
            return index

    def delete_at_index(self, index: int) -> T:
        if not self.is_empty():
            if index > 0:
                previous_node = self.__get_node_at_index(index-1)
                item = previous_node.link.item
                previous_node.link = previous_node.link.link
            elif index == 0:
                item = self.__head.item
                self.__head = self.__head.link
                previous_node = self.__head
            else:
                raise ValueError("Index out of bounds")

            if index == len(self) - 1:
                self.__rear = previous_node

            self.__length -= 1
            return item
        else:
            raise ValueError("Index out of bounds: list is empty")

    def insert(self, index: int, item: T) -> None:
        new_node = Node(item)
        if index == 0:
            new_node.link = self.__head
            self.__head = new_node
        else:
            previous_node = self.__get_node_at_index(index-1)
            new_node.link = previous_node.link
            previous_node.link = new_node

        if index == len(self):
            if len(self) > 0:
                self.__rear.link = new_node
            self.__rear = new_node

        self.__length += 1

    def is_empty(self) -> bool:
        """ Check if the list is empty. """
        return len(self) == 0

    def __str__(self) -> str:
        if not len(self):
            return "Linked List []"

        return "Linked List [" + ", ".join(str(item) for item in self) + "]"

    def __repr__(self) -> str:
        return str(self)
