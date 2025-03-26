from data_structures.abstract_list import *
from data_structures.referential_array import ArrayR


class ArrayList(List[T]):
    """ Implementation of a generic list with arrays. """

    def __init__(self, initial_capacity: int = 1) -> None:
        if initial_capacity < 0:
            raise ValueError("Capacity cannot be negative.")
        
        List.__init__(self)
        self.__array = ArrayR(initial_capacity)
        self.__length = 0

    def __len__(self) -> int:
        """ Returns the number of elements in the list. """
        return self.__length
    
    def clear(self):
        """ Clear the list.
        It does so by setting the length to 0, which means the next items will
        write over the existing array.
        """
        List.clear(self)
        self.__length = 0

    def __getitem__(self, index: int) -> T:
        """ Get the item at index
        :raises IndexError: if index is out of bounds
        :complexity: O(1)
        """
        if index < -1 * len(self) or len(self) <= index:
            raise IndexError("Out of bounds access in list.")
        if index < 0:
            index = len(self) + index
        return self.__array[index]

    def __setitem__(self, index: int, value: T) -> None:
        """ Set the item at index to value
        :raises IndexError: if index is out of bounds
        :complexity: O(1)
        """
        if index < -1 * len(self) or len(self) <= index:
            raise IndexError("Out of bounds access in list.")
        if index < 0:
            index = len(self) + index
        self.__array[index] = value

    def __shuffle_right(self, index: int) -> None:
        """ Shuffles all the items to the right from index
        :complexity best: O(1) shuffle from the end of the list
        :complexity worst: O(N) shuffle from the start of the list
        where N is the number of items in the list
        """
        for i in range(len(self), index, -1):
            self.__array[i] = self.__array[i - 1]

    def __shuffle_left(self, index: int) -> None:
        """ Shuffles all the items to the left from index
        :complexity best: O(1) shuffle from the end of the list
        :complexity worst: O(N) shuffle from the start of the list
        where N is the number of items in the list
        """
        for i in range(index, len(self)):
            self.__array[i] = self.__array[i + 1]

    def __resize(self) -> None:
        """
        If the list is full, doubles the internal capacity of the list,
        copying all existing elements. Does nothing if the list is not full.

        :post:       Capacity is strictly greater than the list length.
        :complexity: Worst case O(N), for list of length N.
        """
        if len(self) == len(self.__array):
            new_cap = int(2 * len(self.__array)) + 1
            new_array = ArrayR(new_cap)
            for i in range(len(self)):
                new_array[i] = self.__array[i]
            self.__array = new_array
        assert len(self) < len(
            self.__array
        ), "Capacity not greater than length after __resize."

    def is_full(self):
        """ Returns true if the list is full
        :complexity: O(1)
        """
        return len(self) == len(self.__array)

    def index(self, item: T) -> int:
        """ Returns the position of the first occurrence of item
        :raises ValueError: if item not in the list
        :complexity: O(Comp==) if item is first; Comp== is the BigO of ==
                     O(len(self)*Comp==) if item is last
        """
        for i in range(len(self)):
            if item == self[i]:
                return i

        raise ValueError(f"{item} not in the list")

    def delete_at_index(self, index: int) -> T:
        """ Delete item at the given index.
        It will shuffle all the items to the left from index to fill the empty spot.
        :pre: index is 0 <= index < len(self) - this is checked by __getitem__() !
        :complexity: O(len(self) - index)
        """
        item = self[index]
        self.__length -= 1
        self.__shuffle_left(index)
        return item

    def insert(self, index: int, item: T) -> None:
        """ Insert item at the given index.
        It will shuffle all the items to the right from index to make space for the new item.
        If the list is full, it should be extended with the use of self.__resize().
        :complexity: O(len(self)-index) if no resizing needed, O(len(self)) otherwise
        """
        # Ensure index is valid
        if index < 0 or index > len(self):
            raise IndexError("Index out of bounds")

        # Resizes array if it's full
        if self.is_full():
            self.__resize()

        self.__shuffle_right(index)
        self.__length += 1
        self[index] = item
