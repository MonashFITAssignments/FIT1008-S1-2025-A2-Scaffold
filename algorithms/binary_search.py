from __future__ import annotations
from data_structures.referential_array import ArrayR
from typing import TypeVar, Union

T = TypeVar("T")


def binary_search(my_list: Union[list[T], ArrayR], target_item: T) -> int:
    """
    Utilise the binary search algorithm to find the index where a particular element would be stored.
    This implementation assumes the item is in the list and the list is sorted.

    Args:
        my_list (Union[list[T], ArrayR]): the list to be searched.
        target_item (T): the target element to be found.

    Returns:
        The index at which either:
            * This item is located, or
            * ValueError if the item cannot be found.

    Complexity:
        Best Case Complexity: O(comp(T)), when middle index contains item. Comp is the cost of comparison.
        Worst Case Complexity: O(log(N) * comp(T)), where N is the length of my_list.
    """
    def _binary_search_aux(my_list: Union[list[T], ArrayR[T]], target_item: T, lo: int, hi: int) -> int:
        """
        Auxiliary method used by binary search.

        Args:
            my_list (Union[list[T], ArrayR[T]]): The list we wish to search.
            target_item (T): the target element to be found.
            lo (int): smallest index where the return value could be.
            hi (int): largest index where the return value could be.
        """
        if lo == hi:
            return lo
        mid = (hi + lo) // 2
        if my_list[mid] > target_item:
            # Item would be before mid
            return _binary_search_aux(my_list, target_item, lo, mid)
        elif my_list[mid] < target_item:
            # Item would be after mid
            return _binary_search_aux(my_list, target_item, mid + 1, hi)
        elif my_list[mid] == target_item:
            return mid
        raise ValueError(f"Comparison operator poorly implemented {target_item} and {my_list[mid]} cannot be compared.")

    return _binary_search_aux(my_list, target_item, 0, len(my_list))
