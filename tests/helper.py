from __future__ import annotations

from data_structures.array_list import ArrayList
"""
Helper class to help extract data from your ADTS
for testing purposes.

You cannot use methods in this class or you will recieve
a 0 for approach and test case marks.

"""
from typing import TypeVar, Union

import ast

from data_structures.array_set import ArraySet
from data_structures.bit_vector_set import BitVectorSet
from data_structures.array_sorted_list import ArraySortedList
from data_structures.abstract_hash_table import HashTable
from data_structures.linked_list import LinkedList
from data_structures.linked_queue import LinkedQueue
from data_structures.circular_queue import CircularQueue
from data_structures.linked_stack import LinkedStack
from data_structures.referential_array import ArrayR

from data_structures.hash_table_linear_probing import LinearProbeTable
from data_structures.hash_table_separate_chaining import HashTableSeparateChaining

T = TypeVar('T')

POSSIBLE_ADT_TYPES = Union[
    ArrayR, ArrayList, ArraySet, BitVectorSet, CircularQueue,
    LinkedList, LinkedQueue, LinkedStack
]


class CollectionsFinder(ast.NodeVisitor):
    def __init__(self, filename, forbidden_types=None):
        self.filename = filename
        self.current_function = None
        self.failures = []
        self.forbidden_types = forbidden_types or {"list", "set", "dict"}
        
    def visit_FunctionDef(self, node):
        old_function = self.current_function
        self.current_function = node.name
        
        # Visit children
        self.generic_visit(node)
        
        self.current_function = old_function
        
    def visit_Assign(self, node):
        if self.current_function == "__str__":
            return
            
        if isinstance(node.value, (ast.List, ast.Set, ast.Dict)):
            self.failures.append(
                f"{self.filename} should not use built-in collections, but found usage at line {node.lineno}."
            )
        self.generic_visit(node)
        
    def visit_Call(self, node):
        if self.current_function == "__str__":
            return
            
        if isinstance(node.func, ast.Name) and node.func.id in self.forbidden_types:
            self.failures.append(
                f"{self.filename} should not use built-in collections, but found '{node.func.id}()' at line {node.lineno}."
            )
        self.generic_visit(node)


def take_out_from_adt(adt: POSSIBLE_ADT_TYPES) -> ArrayR[T] | None:
    """
    Take out n elements from the ADT
    """
    if len(adt) == 0:
        return None

    output: ArrayR[T] = ArrayR(len(adt))

    # Some of the below methods mutate the ADT so we will make a copy of the ADT
    adt_type = type(adt)
    if adt_type in [LinkedQueue, CircularQueue]:
        for index in range(len(adt)):
            output[index] = adt.serve()
            adt.append(output[index])

    elif adt_type == LinkedStack:
        temp_stack = LinkedStack()
        for index in range(len(adt)):
            output[index] = adt.pop()
            temp_stack.push(output[index])
        
        for index in range(len(temp_stack)):
            adt.push(temp_stack.pop())

    elif adt_type in [ArrayList, LinkedList, ArrayR]:
        for index in range(len(adt)):
            output[index] = adt[index]

    elif isinstance(adt, HashTable):
        values: list[T] = adt.values()
        for index in range(len(adt)):
            output[index] = values[index]

    elif adt_type == ArraySortedList:
        for index in range(len(adt)):
            output[index] = adt[index]

    elif adt_type == ArraySet:
        for index in range(len(adt)):
            output[index] = adt.__array[index]

    elif adt_type == BitVectorSet:
        i: int = 0
        for item in range(1, int.bit_length(adt.elems) + 1):
            if item in adt:
                output[i] = item
                i += 1

    else:
        raise ValueError("Invalid ADT type")

    return output


def test_queue() -> None:
    """
    Test the take_out_from_adt function with a queue
    """
    queue: LinkedQueue = LinkedQueue()
    for i in range(1, 11):
        queue.append(i)
    # print(take_out_n_from_adt(queue, 5))
    # Test the queue is not modified
    for i in range(1, 11):
        assert queue.serve() == i, "The queue has been modified"
    print("Queue test passed")

def test_stack() -> None:
    """
    Test the take_out_from_adt function with a stack
    """
    stack: LinkedStack = LinkedStack()
    for i in range(1, 11):
        stack.push(i)
    # print(take_out_n_from_adt(stack, 5))
    # Test the stack is not modified
    for i in range(1, 11):
        assert stack.pop() == 11 - i, "The stack has been modified"
    print("Stack test passed")

def test_linked_list() -> None:
    """
    Test the take_out_from_adt function with a linked list
    """
    linked_list: LinkedList = LinkedList()
    for i in range(1, 11):
        linked_list.append(i)
    # print(take_out_n_from_adt(linked_list, 5))
    # Test the linked list is not modified
    for i in range(0, 10):
        assert linked_list[i] == i + \
            1, f"The linked list has been modified. Expected {i-1}, got {linked_list[i]} at index {i}"
    print("Linked list test passed")

def test_hash_table(hash_table_class) -> None:
    """
    Test the take_out_from_adt function with a hash table
    """
    hash_table = hash_table_class()
    expected = []
    for i in range(1, 11):
        key = f"key{i}"
        value = f"value{i}"
        hash_table[key] = value
        # update the value
        value += "updated"
        hash_table[key] = value
        expected.append((key, value))
    # print(take_out_n_from_adt(hash_table, 5))
    # Test the hash table is not modified
    for key, value in expected:
        assert hash_table[key] == value, f"The hash table has been modified. "\
            f"Expected {value}, got {hash_table[key]} at key {key}"
    print(f"{hash_table_class.__name__} test passed")

def test_array_sorted_list() -> None:
    """
    Test the take_out_from_adt function with an ArraySortedList
    """
    sorted_list: ArraySortedList[T] = ArraySortedList(11)
    for i in range(1, 11):
        sorted_list.add(i)
    # print(take_out_n_from_adt(linked_list, 5))
    # Test the linked list is not modified
    for i in range(0, 10):
        assert sorted_list[i] == i + \
            1, f"The sorted list has been modified. Expected {i-1}, got {sorted_list[i]} at index {i}"
    print("Sorted list test passed")

def test_arrayR() -> None:
    """
    Test the take_out_from_adt function with an ArrayR
    """
    array: ArrayR[T] = ArrayR(10)
    for i in range(1, 11):
        array[i-1] = i
    # print(take_out_n_from_adt(array, 5))
    # Test the array is not modified
    for i in range(0, 10):
        assert array[i] == i+1, f"The array has been modified. Expected {i-1}, got {array[i]} at index {i}"
    print("ArrayR test passed")

def test_aset() -> None:
    """
    Test the take_out_from_adt function with an ASet
    """
    aset: ArraySet = ArraySet(10)
    for i in range(1, 11):
        aset.add(i)
        aset.add(i)  # Duplicates should not be added
    # print(take_out_from_adt(aset))
    # Test the aset is not modified
    for i in range(1, 11):
        assert i in aset, f"The aset has been modified. Expected {i} to be in the set"
    print("ASet test passed")

def test_bset() -> None:
    """
    Test the take_out_from_adt function with an ASet
    """
    bset: BitVectorSet = BitVectorSet(10)
    for i in range(1, 11):
        bset.add(i)
        bset.add(i)  # Duplicates should not be added
    # print(take_out_from_adt(aset))
    # Test the bset is not modified
    for i in range(1, 11):
        assert i in bset, f"The bset has been modified. Expected {i} to be in the set"
    print("BSet test passed")


if __name__ == "__main__":
    test_queue()
    test_stack()
    test_linked_list()
    test_hash_table(HashTableSeparateChaining)
    test_hash_table(LinearProbeTable)
    test_array_sorted_list()
    test_arrayR()
    test_aset()
    test_bset()
