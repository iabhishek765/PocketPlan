"""
test_algorithms.py
------------------
Simple tests for every algorithm. Run with:   python test_algorithms.py
If everything is fine you will see "All tests passed".
"""

import itertools
import random

from calculations import category_totals, remaining_budget, split_expenses, total_expenses
from optimization import greedy_allocation, knapsack_dp
from sample_data import get_sample_expenses
from searching import binary_search, linear_search
from sorting import sort_by_amount, sort_by_name


def test_calculations():
    data = get_sample_expenses()
    assert total_expenses(data) == 28198
    assert remaining_budget(30000, data) == 1802
    assert remaining_budget(20000, data) < 0                 # overspending
    assert category_totals(data)["Rent"] == 8000
    mandatory, optional = split_expenses(data)
    assert total_expenses(mandatory) == 17299
    assert len(mandatory) + len(optional) == len(data)
    assert total_expenses([]) == 0                           # empty list


def test_sorting():
    data = get_sample_expenses()
    amounts = [e["amount"] for e in sort_by_amount(data)]
    assert amounts == sorted(amounts)
    amounts_desc = [e["amount"] for e in sort_by_amount(data, reverse=True)]
    assert amounts_desc == sorted(amounts_desc, reverse=True)
    names = [e["name"].lower() for e in sort_by_name(data)]
    assert names == sorted(names)
    assert sort_by_amount([]) == []                          # empty list


def test_searching():
    data = get_sample_expenses()
    positions, comparisons = linear_search(data, "rent")
    assert comparisons == len(data)
    assert data[positions[0]]["name"] == "House Rent"
    assert linear_search(data, "zzz")[0] == []

    by_name = sort_by_name(data)
    index, steps = binary_search(by_name, "movie night")
    assert by_name[index]["name"] == "Movie Night"
    assert binary_search(by_name, "zzz")[0] == -1
    # Binary search must find every item that exists
    for e in data:
        i, _ = binary_search(by_name, e["name"])
        assert by_name[i]["name"] == e["name"]


def test_optimization_demo():
    _, optional = split_expenses(get_sample_expenses())
    # Default demo: budget 22000 - mandatory 17299 = 4701 for optional items
    _, g_cost, g_benefit = greedy_allocation(optional, 4701)
    _, d_cost, d_benefit = knapsack_dp(optional, 4701)
    assert g_benefit == 33 and d_benefit == 36
    assert g_cost <= 4701 and d_cost <= 4701


def test_dp_is_optimal_vs_brute_force():
    """Compare DP with checking every possible combination (small random cases)."""
    random.seed(1)
    for _ in range(200):
        n = random.randint(0, 8)
        items = [{"name": str(i), "amount": float(random.randint(1, 50)),
                  "benefit": random.randint(1, 10)} for i in range(n)]
        limit = random.randint(0, 150)

        best = 0
        for r in range(n + 1):
            for combo in itertools.combinations(items, r):
                if sum(c["amount"] for c in combo) <= limit:
                    best = max(best, sum(c["benefit"] for c in combo))

        _, d_cost, d_benefit = knapsack_dp(items, limit)
        _, g_cost, g_benefit = greedy_allocation(items, limit)
        assert d_benefit == best, (items, limit)
        assert d_cost <= limit and g_cost <= limit
        assert g_benefit <= d_benefit                        # greedy never beats DP


def test_edge_cases():
    assert knapsack_dp([], 1000) == ([], 0, 0)
    assert greedy_allocation([], 1000) == ([], 0, 0)
    items = [{"name": "A", "amount": 500.0, "benefit": 5}]
    assert knapsack_dp(items, 0)[2] == 0                     # zero budget
    assert greedy_allocation(items, 0)[2] == 0
    assert knapsack_dp(items, 10 ** 9)[2] == 5               # huge budget is fine


if __name__ == "__main__":
    test_calculations()
    test_sorting()
    test_searching()
    test_optimization_demo()
    test_dp_is_optimal_vs_brute_force()
    test_edge_cases()
    print("All tests passed")
