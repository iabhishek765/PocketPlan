"""
performance.py
--------------
Measures how long the algorithms take using time.perf_counter().
Random data is used so we can test with many items (100, 1000, 5000 ...).
All times are in milliseconds (ms).
"""

import random
import time

from searching import linear_search, binary_search
from sorting import merge_sort
from optimization import greedy_allocation, knapsack_dp


def make_random_expenses(n):
    """Create n random expenses with unique names like 'Item 000042'."""
    random.seed(42)                                   # same data every run
    expenses = []
    for i in range(n):
        expenses.append({
            "name": "Item " + str(i).zfill(6),
            "category": "Other",
            "amount": float(random.randint(50, 5000)),
            "benefit": random.randint(1, 10),
        })
    random.shuffle(expenses)                          # unsorted on purpose
    return expenses


def compare_searching(sizes, repeats=50):
    """Time Linear vs Binary search for the LAST item (worst case for linear)."""
    rows = []
    for n in sizes:
        data = merge_sort(make_random_expenses(n), lambda e: e["name"].lower())
        target = data[-1]["name"]

        start = time.perf_counter()
        for _ in range(repeats):
            linear_search(data, target)
        linear_ms = (time.perf_counter() - start) * 1000 / repeats

        start = time.perf_counter()
        for _ in range(repeats):
            binary_search(data, target)
        binary_ms = (time.perf_counter() - start) * 1000 / repeats

        rows.append({
            "Expenses (n)": n,
            "Linear Search (ms)": round(linear_ms, 4),
            "Binary Search (ms)": round(binary_ms, 4),
        })
    return rows


def compare_sorting(sizes):
    """Time our Merge Sort against Python's built-in sorted() (for reference)."""
    rows = []
    for n in sizes:
        data = make_random_expenses(n)

        start = time.perf_counter()
        merge_sort(data, lambda e: e["amount"])
        merge_ms = (time.perf_counter() - start) * 1000

        start = time.perf_counter()
        sorted(data, key=lambda e: e["amount"])
        builtin_ms = (time.perf_counter() - start) * 1000

        rows.append({
            "Expenses (n)": n,
            "Merge Sort (ms)": round(merge_ms, 4),
            "Python sorted() (ms)": round(builtin_ms, 4),
        })
    return rows


def compare_optimization(item_counts, limit=5000):
    """Time Greedy vs Dynamic Programming and compare the benefit they achieve."""
    rows = []
    for n in item_counts:
        random.seed(n)
        items = [{"name": "Item " + str(i),
                  "category": "Other",
                  "amount": float(random.randint(100, 1500)),
                  "benefit": random.randint(1, 10)} for i in range(n)]

        start = time.perf_counter()
        _, _, greedy_benefit = greedy_allocation(items, limit)
        greedy_ms = (time.perf_counter() - start) * 1000

        start = time.perf_counter()
        _, _, dp_benefit = knapsack_dp(items, limit)
        dp_ms = (time.perf_counter() - start) * 1000

        rows.append({
            "Optional items": n,
            "Greedy time (ms)": round(greedy_ms, 4),
            "DP time (ms)": round(dp_ms, 4),
            "Greedy benefit": greedy_benefit,
            "DP benefit": dp_benefit,
        })
    return rows
