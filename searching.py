"""
searching.py
------------
Two searching algorithms (DAA):
    1. Linear Search  - checks every item one by one.      Time: O(n)
    2. Binary Search  - halves the search area each step.  Time: O(log n)
                        (the list MUST be sorted by name first)
"""


def linear_search(expenses, query):
    """
    Linear Search by name.

    Looks at every expense from start to end and collects the position of
    each expense whose name CONTAINS the query text (ignoring capital letters).

    Returns: (list_of_positions, number_of_comparisons)
    Works on any list, sorted or not.
    """
    query = query.strip().lower()
    found_positions = []
    comparisons = 0

    for index in range(len(expenses)):          # visit every item
        comparisons += 1
        if query in expenses[index]["name"].lower():
            found_positions.append(index)

    return found_positions, comparisons


def binary_search(sorted_expenses, target_name):
    """
    Binary Search by exact name.

    IMPORTANT: sorted_expenses must already be sorted by name (A -> Z).

    Idea: look at the middle item.
        - If it matches        -> done.
        - If target is smaller -> search only the left half.
        - If target is larger  -> search only the right half.

    Returns: (position or -1 if not found, number_of_steps)
    """
    target = target_name.strip().lower()
    low = 0
    high = len(sorted_expenses) - 1
    steps = 0

    while low <= high:
        steps += 1
        mid = (low + high) // 2                       # middle position
        mid_name = sorted_expenses[mid]["name"].lower()

        if mid_name == target:
            return mid, steps
        elif target < mid_name:
            high = mid - 1                            # ignore the right half
        else:
            low = mid + 1                             # ignore the left half

    return -1, steps                                  # not found
