from __future__ import annotations
from data_structures.referential_array import ArrayR
from data_structures.array_list import ArrayList
from typing import TypeVar, Union

T = TypeVar("T")


def merge(list1: Union[ArrayList[T], ArrayR[T]], list2: Union[ArrayList[T], ArrayR[T]], key=lambda x: x) -> Union[ArrayList[T], ArrayR[T]]:
    """
    Merges two sorted lists into one larger sorted list,
    containing all elements from the smaller lists.

    The `key` kwarg allows you to define a custom sorting order.

    returns:
    The sorted list in the same type as the input lists.
    If both lists are of type ArrayR, the result will be an ArrayR.
    If both lists are of type ArrayList, the result will be an ArrayList.

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
    
    # Append any remaining elements from list1 or list2
    for i in range(cur_left, len(list1)):
        new_list.append(list1[i])
    for i in range(cur_right, len(list2)):
        new_list.append(list2[i])
    
    # Create the result list based on the type of the input lists
    # If it's an ArrayR, we can create it directly from the list
    # If it's an ArrayList, we need to append the elements
    if isinstance(list1, ArrayR):
        return ArrayR.from_list(new_list)
    elif isinstance(list1, ArrayList):
        result = ArrayList(len(new_list))
        for i in range(len(new_list)):
            result.append(new_list[i])
        return result
    else:
        raise TypeError("Unsupported type for list1 and list2. Must be ArrayR or ArrayList.")


def mergesort(my_list: Union[ArrayList[T], ArrayR], key=lambda x: x) -> Union[ArrayList[T], ArrayR]:
    """
    Sort a list using the mergesort operation.

    complexity:
    Best/Worst Case: O(NlogN * comp(T)) where N is the length of the list and comp is the cost of comparison for the
    object type T (the elements in the list).

    Return type is the same as the input type.
    If the input is an ArrayR, the output will be an ArrayR.
    If the input is an ArrayList, the output will be an ArrayList.
    """
    if len(my_list) <= 1:
        return my_list
    
    # Split the list into two halves
    break_index = (len(my_list)+1) // 2
    
    # Create two new lists to hold the two halves. Create them
    # with the same type as the original list
    if isinstance(my_list, ArrayR):
        left_half = ArrayR(break_index)
        right_half = ArrayR(len(my_list) - break_index)
    elif isinstance(my_list, ArrayList):
        left_half = ArrayList(break_index)
        right_half = ArrayList(len(my_list) - break_index)
    else:
        raise TypeError("Unsupported type for my_list. Must be ArrayR or ArrayList.")
    
    # Now fill the two halves with the elements from the original list
    # If it's an ArrayR, we can set the elements directly
    # If it's an ArrayList, we need to append the elements
    
    # Left half
    for i in range(break_index):
        if isinstance(left_half, ArrayR):
            left_half[i] = my_list[i]
        else:
            left_half.append(my_list[i])
    
    # Right half
    for i in range(break_index, len(my_list)):
        if isinstance(right_half, ArrayR):
            right_half[i - break_index] = my_list[i]
        else:
            right_half.append(my_list[i])
    
    # Recursively sort the two halves and merge them
    list1 = mergesort(left_half, key)
    list2 = mergesort(right_half, key)
    return merge(list1, list2, key)
