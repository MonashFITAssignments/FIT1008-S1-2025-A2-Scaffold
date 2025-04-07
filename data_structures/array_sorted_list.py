from data_structures.referential_array import ArrayR
from data_structures.abstract_sorted_list import SortedList, T

__author__ = 'Maria Garcia de la Banda and Brendon Taylor. Modified by Alexey Ignatiev'
__docformat__ = 'reStructuredText'


class ArraySortedList(SortedList[T]):
    """ Array-based implementation of the Abstract Sorted List. """

    def __init__(self, initial_capacity: int = 1) -> None:
        if initial_capacity < 0:
            raise ValueError("Capacity cannot be negative.")

        # Call the base class constructor
        SortedList.__init__(self)

        # Initialize the length of the list
        self.__length = 0

        # Create the internal array where the items will be stored
        self.__array = ArrayR(initial_capacity)

    def clear(self):
        """ Clear the list.
        All we need to do is reset the length of the list to 0.
        This will start writing elements from the beginning of the array.
        """
        self.__length = 0

    def __len__(self):
        return self.__length

    def __getitem__(self, index: int) -> T:
        """ Return the element at the given position.
        :raises IndexError: if the index is out of bounds.
        """
        if index < -1 * len(self) or len(self) <= index:
            raise IndexError('Out of bounds access in list.')
        if index < 0:
            index = len(self) + index
        return self.__array[index]

    def __contains__(self, item):
        """ Checks if the item is in the list.
        :returns: True if the item is in the list, False otherwise.
        """
        try:
            _ = self.index(item)
            return True
        except ValueError:
            return False

    def __shuffle_right(self, index: int) -> None:
        """
        Shuffle items to the right up to a given position.
        """
        for i in range(len(self), index, -1):
            self.__array[i] = self.__array[i - 1]

    def __shuffle_left(self, index: int) -> None:
        """
        Shuffle items starting at the given position to the left.
        """
        for i in range(index, len(self)):
            self.__array[i] = self.__array[i + 1]

    def __resize(self) -> None:
        """ Resize the list.
        It only sizes up, so should only be called when adding new items.
        """
        # Double the size of the array
        new_array = ArrayR(2 * len(self.__array) + 1)

        # copying the contents
        for i in range(self.__length):
            new_array[i] = self.__array[i]

        # referring to the new array
        self.__array = new_array

    def delete_at_index(self, index: int) -> T:
        """ Delete item at the given position. """
        item = self[index]
        self.__length -= 1
        self.__shuffle_left(index)
        return item

    def index(self, item: T) -> int:
        """
        Find the position of a given item in the list,
        by means of calling the __index_to_add() method.
        :raises ValueError: if the item is not found.
        """
        # Try finding the index
        index = self.__index_to_add(item)

        if index < len(self) and self.__array[index] == item:
            return index

        raise ValueError(f"{item} not found")

    def add(self, item: T) -> None:
        """ Add new element to the list. """
        if len(self) == len(self.__array):
            self.__resize()
        index = self.__index_to_add(item)
        self.__shuffle_right(index)
        self.__array[index] = item
        self.__length += 1

    def __index_to_add(self, item: T) -> int:
        """
        Find the position where the new item should be placed.
        :complexity best: O(comp)   item is the middle element
        :complexity worst: O(logn * comp)  first or last element
            comp - cost of comparision
            n - length of the list
        """

        low = 0
        high = len(self) - 1

        # until we have checked all elements in the search space
        while low <= high:
            mid = (low + high) // 2
            # Found the item
            if self[mid] == item:
                return mid
            # check right of the remaining list
            elif self[mid] < item:
                low = mid + 1
            # check left of the remaining list
            else:
                high = mid - 1

        return low
