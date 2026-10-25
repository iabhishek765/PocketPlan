"""
sorting.py
----------
Merge Sort (Divide and Conquer).   Time: O(n log n)   Extra space: O(n)

Steps:
    1. DIVIDE   - split the list into two halves.
    2. CONQUER  - sort each half (by calling merge_sort again = recursion).
    3. COMBINE  - merge the two sorted halves into one sorted list.
"""


def merge(left, right, key_func, reverse):
    """Merge two already-sorted lists into one sorted list."""
    result = []
    i = 0  # pointer for left list
    j = 0  # pointer for right list

    while i < len(left) and j < len(right):
        left_value = key_func(left[i])
        right_value = key_func(right[j])

        # Decide which item should come first
        if reverse:
            take_left = left_value >= right_value     # biggest first
        else:
            take_left = left_value <= right_value     # smallest first

        if take_left:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    # One list is finished; copy whatever is left in the other one
    result.extend(left[i:])
    result.extend(right[j:])
    return result


def merge_sort(items, key_func, reverse=False):
    """
    Sort a list WITHOUT changing the original.

    key_func : tells what to sort by.
               e.g. lambda e: e["amount"]        -> sort by amount
                    lambda e: e["name"].lower()  -> sort by name
    reverse  : False = small to big (A-Z), True = big to small (Z-A)
    """
    # Base case: 0 or 1 item is already sorted
    if len(items) <= 1:
        return items[:]

    middle = len(items) // 2
    left_half = merge_sort(items[:middle], key_func, reverse)
    right_half = merge_sort(items[middle:], key_func, reverse)
    return merge(left_half, right_half, key_func, reverse)


# Two ready-made helpers used by the interface
def sort_by_amount(expenses, reverse=False):
    return merge_sort(expenses, lambda e: e["amount"], reverse)


def sort_by_name(expenses, reverse=False):
    return merge_sort(expenses, lambda e: e["name"].lower(), reverse)
