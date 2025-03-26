from data_structures.abstract_hash_table import HashTable
from data_structures.referential_array import ArrayR
from data_structures.linked_list import LinkedList
from typing import TypeVar

V = TypeVar('V')

class HashTableSeparateChaining(HashTable[str, V]):
    """
    Separate Chaining Hash Table Implementation using a Linked List.
    It currently rehashes the primary cluster to handle deletion.

    constants:
        DEFAULT_TABLE_SIZE: default table size used in the __init__
        DEFAULT_HASH_TABLE: default hash base used for the hash function

    attributes:
        length: number of elements in the hash table
        array: used to represent our internal array
    """

    DEFAULT_TABLE_SIZE = 17
    DEFAULT_HASH_BASE = 31

    def __init__(self, table_size: int = DEFAULT_TABLE_SIZE) -> None:
        """
        :complexity: O(N) where N is the table size.
        """
        if table_size <= 0:
            raise ValueError("Table size should be larger than 0.")
        
        self.__length = 0
        self.__table = ArrayR(table_size)

    def __len__(self) -> int:
        """
        Returns number of elements in the hash table
        """
        return self.__length

    def __delitem__(self, key: str) -> None:
        """
        Deletes an item from our hash table
        :raises KeyError: when the key doesn't exist
        """
        position = self.hash(key)
        if self.__table[position] is None:
            raise KeyError(key)

        for index, item in enumerate(self.__table[position]):
            if item[0] == key:
                if len(self.__table[position]) <= 1:
                    self.__table[position] = None
                else:
                    self.__table[position].delete_at_index(index)

                self.__length -= 1
                return

        raise KeyError(key)

    def __setitem__(self, key: str, data: V) -> None:
        """
        Set a (key, data) pair in our hash table
        """
        position = self.hash(key)
        if self.__table[position] is None:
            self.__table[position] = LinkedList()

        # Attempt to find the key in our linked list
        if len(self.__table[position]) > 0:
            for index, item in enumerate(self.__table[position]):
                if item[0] == key:
                    # If found update the data
                    self.__table[position][index] = (key, data)
                    return
                
        # Insert at the beginning for better time complexity
        self.__table[position].insert(0, (key, data))
        self.__length += 1

    def __contains__(self, key: str) -> bool:
        """
        Checks to see if the given key is in the Hash Table
        """
        try:
            _ = self[key]
        except KeyError:
            return False
        else:
            return True

    def __getitem__(self, key: str) -> V:
        """
        Get the data associated with a key
        :raises KeyError: when the key doesn't exist
        """
        position = self.hash(key)
        if self.__table[position] is None:
            raise KeyError(key)
        for item in self.__table[position]:
            if item[0] == key:
                return item[1]

        raise KeyError(key)

    def is_empty(self):
        """
        Returns whether the hash table is empty
        :complexity: O(1)
        """
        return self.__length == 0

    def hash(self, key: str) -> int:
        """
        Universal Hash function
        :returns: a valid position (0 <= value < table_size) in the hash table
        :complexity: O(K) where K is the size of the key
        """
        value = 0
        a = 31415
        for char in key:
            value = (ord(char) + a * value) % len(self.__table)
            a = a * HashTableSeparateChaining.DEFAULT_HASH_BASE % (len(self.__table) - 1)
        return value

    def insert(self, key: str, data: V) -> None:
        """
        Utility method to call our setitem method
        """
        self[key] = data

    def __iter__(self):
        """
        Returns an iterator for the hash table
        :complexity: O(N) where N n is the number of items in our hash table
        """
        for list in self.__table:
            if list is not None:
                for item in list:
                    yield item[1]

    def keys(self) -> ArrayR[str]:
        """
        Returns all keys in the hash table
        :complexity: O(N) where N is the number of items in our hash table
        """
        res = ArrayR(self.__length)
        i = 0
        for list in self.__table:
            if list is not None:
                for item in list:
                    res[i] = item[0]
                    i += 1
        return res

    def values(self) -> ArrayR[V]:
        """
        Returns all values in the hash table
        :complexity: O(N) where N is the number of items in our hash table
        """
        res = ArrayR(self.__length)
        i = 0
        for list in self.__table:
            if list is not None:
                for item in list:
                    res[i] = item[1]
                    i += 1
        return res

    def __str__(self) -> str:
        """
        Returns all they key/value pairs in our hash table (no particular order)
        :complexity: O(N) where N is the number of items in our hash table
        """
        result = ""
        for list in self.__table:
            if list is not None:
                first = True
                for item in list:
                    if not first:
                        result += ' -> '
                    (key, value) = item
                    result += "(" + str(key) + "," + str(value) + ")"
                    first = False
                result += '\n'
        return result
    
    def __repr__(self) -> str:
        return str(self)
