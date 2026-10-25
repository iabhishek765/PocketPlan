"""
sample_data.py
--------------
Holds the fixed lists (categories) and the sample household expenses.

Every expense is a Python dictionary:
    {"name": "Rent", "category": "Rent", "amount": 8000.0, "benefit": 0}

- "benefit" is a score from 1 to 10 that tells how useful an OPTIONAL expense is.
  Mandatory expenses (rent, bills ...) do not need a benefit, so we store 0.
"""

# All categories the user can choose from
CATEGORIES = [
    "Groceries",
    "Vegetables",
    "Rent",
    "Electricity",
    "Transport",
    "Mobile Recharge",
    "Household Items",
    "Entertainment",
    "Other",
]

# Mandatory = must be paid every month (cannot be skipped)
MANDATORY_CATEGORIES = [
    "Groceries",
    "Vegetables",
    "Rent",
    "Electricity",
    "Transport",
    "Mobile Recharge",
]

# Optional = nice to have (can be reduced or skipped if money is short)
OPTIONAL_CATEGORIES = [
    "Household Items",
    "Entertainment",
    "Other",
]

# Default monthly budget used when the app starts
DEFAULT_BUDGET = 22000.0


def get_sample_expenses():
    """Return a fresh list of sample expenses (a new copy every time)."""
    return [
        # ----- Mandatory expenses -----
        {"name": "House Rent",        "category": "Rent",            "amount": 8000.0, "benefit": 0},
        {"name": "Electricity Bill",  "category": "Electricity",     "amount": 1800.0, "benefit": 0},
        {"name": "Monthly Groceries", "category": "Groceries",       "amount": 4500.0, "benefit": 0},
        {"name": "Vegetables",        "category": "Vegetables",      "amount": 1500.0, "benefit": 0},
        {"name": "Bus and Petrol",    "category": "Transport",       "amount": 1200.0, "benefit": 0},
        {"name": "Mobile Recharge",   "category": "Mobile Recharge", "amount": 299.0,  "benefit": 0},
        # ----- Optional expenses (each has a benefit score 1-10) -----
        {"name": "Cleaning Supplies",    "category": "Household Items", "amount": 400.0,  "benefit": 8},
        {"name": "Kitchen Mixer",        "category": "Household Items", "amount": 3000.0, "benefit": 8},
        {"name": "Movie Night",          "category": "Entertainment",   "amount": 600.0,  "benefit": 7},
        {"name": "Streaming Subscription", "category": "Entertainment", "amount": 499.0,  "benefit": 6},
        {"name": "Dining Out",           "category": "Entertainment",   "amount": 1200.0, "benefit": 6},
        {"name": "Weekend Trip",         "category": "Entertainment",   "amount": 2500.0, "benefit": 9},
        {"name": "Books",                "category": "Other",           "amount": 700.0,  "benefit": 6},
        {"name": "New Headphones",       "category": "Other",           "amount": 2000.0, "benefit": 5},
    ]
