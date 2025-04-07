from __future__ import annotations
from data_structures.referential_array import ArrayR
from typing import List, TypeVar, Union

T = TypeVar("T")


def merge(list1: Union[List[T], ArrayR[T]], list2: Union[List[T], ArrayR[T]], key=lambda x: x) -> List[T]:
    """
    Merges two sorted lists into one larger sorted list,
    containing all elements from the smaller lists.

    The `key` kwarg allows you to define a custom sorting order.

    returns:
    The sorted list.

    pre:
    Both l1 and l2 are sorted, and contain comparable elements.

    complexity:
    Best/Worst Case: O(n * comp(T)), n = len(l1)+len(l2) and comp is the cost of comparison.
    """
    new_list = []
    cur_left = 0
    cur_right = 0
    while cur_left < len(list1) and cur_right < len(list2):
        if key(list1[cur_left]) <= key(list2[cur_right]):
            new_list.append(list1[cur_left])
            cur_left += 1
        else:
            new_list.append(list2[cur_right])
            cur_right += 1
    new_list += list1[cur_left:]
    new_list += list2[cur_right:]
    return new_list


def mergesort(my_list: Union[List[T], ArrayR], key=lambda x: x) -> List[T]:
    """
    Sort a list using the mergesort operation.

    complexity:
    Best/Worst Case: O(NlogN * comp(T)) where N is the length of the list and comp is the cost of comparison.
    """
    if len(my_list) <= 1:
        return my_list
    break_index = (len(my_list)+1) // 2
    list1 = mergesort(my_list[:break_index], key)
    list2 = mergesort(my_list[break_index:], key)
    return merge(list1, list2, key)
