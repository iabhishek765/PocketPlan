"""
calculations.py
---------------
Simple maths on the expense list: totals, remaining budget, category totals.
"""

from sample_data import MANDATORY_CATEGORIES


def total_expenses(expenses):
    """Add up the 'amount' of every expense."""
    total = 0
    for expense in expenses:
        total += expense["amount"]
    return total


def remaining_budget(budget, expenses):
    """Budget minus total expenses. A negative answer means overspending."""
    return budget - total_expenses(expenses)


def category_totals(expenses):
    """
    Return a dictionary like {"Rent": 8000, "Groceries": 4500, ...}
    Used for the category-wise chart.
    """
    totals = {}
    for expense in expenses:
        category = expense["category"]
        if category in totals:
            totals[category] += expense["amount"]
        else:
            totals[category] = expense["amount"]
    return totals


def split_expenses(expenses):
    """
    Separate the list into (mandatory_list, optional_list).
    Rent, bills etc. go to mandatory. Entertainment etc. go to optional.
    """
    mandatory = []
    optional = []
    for expense in expenses:
        if expense["category"] in MANDATORY_CATEGORIES:
            mandatory.append(expense)
        else:
            optional.append(expense)
    return mandatory, optional
