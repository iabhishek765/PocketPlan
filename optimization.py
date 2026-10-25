"""
optimization.py
---------------
Budget optimization for OPTIONAL expenses only.
(Rent, bills and other mandatory expenses are paid first and kept separate.)

Problem: we have a limit of money for optional things. Each optional item has
    amount  = its cost
    benefit = how useful it is (score 1-10)
Which items should we choose to get the MOST total benefit within the limit?

    1. Greedy Algorithm        - fast, but may not give the best answer.
    2. Dynamic Programming     - 0/1 Knapsack, always gives the best answer.
"""

import math
from sorting import merge_sort


def greedy_allocation(optional_items, limit):
    """
    Greedy strategy: "best value for money first".

    1. Compute ratio = benefit / amount for each item.
    2. Sort items by ratio, highest first (we reuse our own merge_sort).
    3. Go down the list and buy an item if it still fits in the limit.

    Time: O(n log n)  (because of the sorting)

    Returns: (selected_items, total_cost, total_benefit)
    """
    candidates = [item for item in optional_items if item["amount"] > 0]
    ranked = merge_sort(candidates,
                        lambda item: item["benefit"] / item["amount"],
                        reverse=True)

    selected = []
    total_cost = 0
    total_benefit = 0

    for item in ranked:
        if total_cost + item["amount"] <= limit:      # does it still fit?
            selected.append(item)
            total_cost += item["amount"]
            total_benefit += item["benefit"]

    return selected, total_cost, total_benefit


def knapsack_dp(optional_items, limit):
    """
    Dynamic Programming - 0/1 Knapsack ("0/1" = take an item fully or not at all).

    dp[i][w] = best total benefit using only the first i items
               when the money limit is w rupees.

    For every item we have two choices:
        SKIP it : dp[i][w] = dp[i-1][w]
        TAKE it : dp[i][w] = dp[i-1][w - cost] + benefit      (only if cost <= w)
    We keep the bigger of the two.

    Time: O(n x W)   Space: O(n x W)    (n = items, W = money limit in rupees)

    Costs are rounded UP to whole rupees so the answer never crosses the limit.

    Returns: (selected_items, total_cost, total_benefit)
    """
    items = [item for item in optional_items if item["amount"] > 0]
    n = len(items)
    costs = [math.ceil(item["amount"]) for item in items]

    # Money above the cost of ALL items is never useful, so cap the table size
    capacity = min(int(limit), sum(costs))
    if capacity < 0:
        capacity = 0

    # Build the table: (n + 1) rows, (capacity + 1) columns, all zeros
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        cost = costs[i - 1]
        benefit = items[i - 1]["benefit"]
        for w in range(capacity + 1):
            dp[i][w] = dp[i - 1][w]                       # choice 1: skip
            if cost <= w:
                take = dp[i - 1][w - cost] + benefit      # choice 2: take
                if take > dp[i][w]:
                    dp[i][w] = take

    # Backtrack through the table to find WHICH items were taken
    selected = []
    w = capacity
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:        # value changed -> item i was taken
            selected.append(items[i - 1])
            w -= costs[i - 1]
    selected.reverse()

    total_cost = sum(item["amount"] for item in selected)
    total_benefit = dp[n][capacity]
    return selected, total_cost, total_benefit
