"""
app.py
------
The Streamlit user interface of PocketPlan.
Run with:   streamlit run app.py

This file only builds the screen. All the real work is done by the other files:
    calculations.py  -> totals and remaining budget
    searching.py     -> linear search, binary search
    sorting.py       -> merge sort
    optimization.py  -> greedy and 0/1 knapsack (dynamic programming)
    performance.py   -> timing with time.perf_counter()
"""

import time

import matplotlib.pyplot as plt
import streamlit as st

from calculations import (category_totals, remaining_budget, split_expenses,
                          total_expenses)
from optimization import greedy_allocation, knapsack_dp
from performance import compare_optimization, compare_searching, compare_sorting
from sample_data import (CATEGORIES, DEFAULT_BUDGET, OPTIONAL_CATEGORIES,
                         get_sample_expenses)
from searching import binary_search, linear_search
from sorting import sort_by_amount, sort_by_name

st.set_page_config(page_title="PocketPlan", page_icon="💰", layout="wide")


# ---------------------------------------------------------------------------
# 1. Session state = memory of the app. Streamlit re-runs this file on every
#    click, so we keep the budget and expense list inside st.session_state.
# ---------------------------------------------------------------------------
if "expenses" not in st.session_state:
    st.session_state.expenses = get_sample_expenses()
if "budget" not in st.session_state:
    st.session_state.budget = DEFAULT_BUDGET


# ---------------------------------------------------------------------------
# 2. Small helper functions (called when buttons are clicked)
# ---------------------------------------------------------------------------
def load_sample():
    st.session_state.expenses = get_sample_expenses()
    st.session_state.budget = DEFAULT_BUDGET


def clear_all():
    st.session_state.expenses = []


def add_expense():
    """Read the form values, check them, and add a new expense dictionary."""
    name = st.session_state.new_name.strip()
    amount = st.session_state.new_amount
    category = st.session_state.new_category

    if name == "" or amount <= 0:
        st.session_state.add_message = ("error",
                                        "Please enter a name and an amount greater than 0.")
        return

    # Only optional categories use the benefit score
    if category in OPTIONAL_CATEGORIES:
        benefit = st.session_state.get("new_benefit", 5)
    else:
        benefit = 0

    st.session_state.expenses.append(
        {"name": name, "category": category, "amount": float(amount), "benefit": benefit})
    st.session_state.add_message = ("success", "Added: " + name)
    st.session_state.new_name = ""          # clear the form
    st.session_state.new_amount = 0.0


def delete_expense():
    index = st.session_state.delete_index
    if index is not None and index < len(st.session_state.expenses):
        removed = st.session_state.expenses.pop(index)
        st.session_state.add_message = ("success", "Removed: " + removed["name"])


def to_table(expenses):
    """Turn the list of expense dictionaries into rows for display."""
    rows = []
    for number, e in enumerate(expenses, start=1):
        rows.append({
            "No.": number,
            "Expense": e["name"],
            "Category": e["category"],
            "Amount (₹)": e["amount"],
            "Benefit": str(e["benefit"]) if e["category"] in OPTIONAL_CATEGORIES else "-",
        })
    return rows


def draw_category_chart(expenses):
    """Bar chart: total money spent in each category (Matplotlib)."""
    totals = category_totals(expenses)
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(list(totals.keys()), list(totals.values()), color="#4C9F70")
    ax.set_xlabel("Category")
    ax.set_ylabel("Amount (Rs.)")
    ax.set_title("Category-wise Expenses")
    plt.xticks(rotation=30, ha="right")
    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)


def draw_line_chart(rows, x_key, y_keys, title, y_label):
    fig, ax = plt.subplots(figsize=(6, 3.5))
    for key in y_keys:
        ax.plot([r[x_key] for r in rows], [r[key] for r in rows], marker="o", label=key)
    ax.set_xlabel(x_key)
    ax.set_ylabel(y_label)
    ax.set_title(title)
    ax.legend()
    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)


# ---------------------------------------------------------------------------
# 3. Sidebar: budget and data buttons
# ---------------------------------------------------------------------------
st.sidebar.title("💰 PocketPlan")
st.sidebar.caption("Smart Budget Planner using DAA")
st.sidebar.number_input("Monthly budget / income (₹)", min_value=0.0, step=500.0,
                        key="budget")
st.sidebar.button("Load sample data", on_click=load_sample)
st.sidebar.button("Clear all expenses", on_click=clear_all)

budget = st.session_state.budget
expenses = st.session_state.expenses

st.title("PocketPlan: Smart Budget Planner")

tab_dash, tab_add, tab_search, tab_opt, tab_perf = st.tabs(
    ["📊 Dashboard", "➕ Add / Remove", "🔎 Sort & Search", "🧮 Budget Optimizer", "⏱ Performance"])


# ---------------------------------------------------------------------------
# TAB 1: Dashboard - totals, warning, table, chart
# ---------------------------------------------------------------------------
with tab_dash:
    total = total_expenses(expenses)
    remaining = remaining_budget(budget, expenses)

    c1, c2, c3 = st.columns(3)
    c1.metric("Monthly Budget", f"₹ {budget:,.2f}")
    c2.metric("Total Expenses", f"₹ {total:,.2f}")
    c3.metric("Remaining Budget", f"₹ {remaining:,.2f}")

    if remaining < 0:
        st.error(f"⚠ Warning: your expenses exceed your budget by ₹ {-remaining:,.2f}. "
                 "Try the Budget Optimizer tab to choose which optional expenses to keep.")
    else:
        st.success("✅ You are within your budget.")

    if expenses:
        st.subheader("All Expenses")
        st.dataframe(to_table(expenses), width="stretch", hide_index=True)
        st.subheader("Category-wise Chart")
        draw_category_chart(expenses)
    else:
        st.info("No expenses yet. Add some in the 'Add / Remove' tab or load sample data.")


# ---------------------------------------------------------------------------
# TAB 2: Add and remove expenses
# ---------------------------------------------------------------------------
with tab_add:
    st.subheader("Add a New Expense")
    st.text_input("Expense name", key="new_name", placeholder="e.g. Milk and Bread")
    st.selectbox("Category", CATEGORIES, key="new_category")
    st.number_input("Amount (₹)", min_value=0.0, step=50.0, key="new_amount")

    # Benefit score is needed only for optional categories
    if st.session_state.new_category in OPTIONAL_CATEGORIES:
        st.slider("Benefit score (1 = low, 10 = high)", 1, 10, 5, key="new_benefit")
    st.button("Add expense", on_click=add_expense)

    message = st.session_state.pop("add_message", None)
    if message:
        if message[0] == "success":
            st.success(message[1])
        else:
            st.error(message[1])

    st.divider()
    st.subheader("Remove an Expense")
    if expenses:
        st.selectbox("Choose an expense", range(len(expenses)), key="delete_index",
                     format_func=lambda i: f"{i + 1}. {expenses[i]['name']} (₹{expenses[i]['amount']:,.0f})")
        st.button("Remove selected", on_click=delete_expense)
    else:
        st.caption("Nothing to remove.")


# ---------------------------------------------------------------------------
# TAB 3: Sorting (Merge Sort) and Searching (Linear / Binary)
# ---------------------------------------------------------------------------
with tab_search:
    st.subheader("Sort Expenses (Merge Sort)")
    col_a, col_b = st.columns(2)
    sort_field = col_a.radio("Sort by", ["Amount", "Name"], horizontal=True)
    sort_order = col_b.radio("Order", ["Ascending", "Descending"], horizontal=True)
    descending = (sort_order == "Descending")

    if sort_field == "Amount":
        sorted_list = sort_by_amount(expenses, descending)
    else:
        sorted_list = sort_by_name(expenses, descending)
    st.dataframe(to_table(sorted_list), width="stretch", hide_index=True)

    st.divider()
    st.subheader("Search an Expense")
    method = st.radio("Search method", ["Linear Search", "Binary Search"], horizontal=True)
    query = st.text_input("Expense name to search", placeholder="e.g. rent")

    if query.strip() != "":
        if method == "Linear Search":
            # Works on the list as it is (no sorting needed); partial match allowed
            positions, comparisons = linear_search(expenses, query)
            st.write(f"Comparisons made: **{comparisons}**")
            if positions:
                st.success(f"Found {len(positions)} match(es).")
                st.dataframe(to_table([expenses[p] for p in positions]),
                             width="stretch", hide_index=True)
            else:
                st.warning("No expense found.")
        else:
            # Binary search needs a list sorted by name (A-Z) and an exact name
            by_name = sort_by_name(expenses)
            position, steps = binary_search(by_name, query)
            st.caption("The list is first sorted by name using Merge Sort, "
                       "because Binary Search only works on sorted data.")
            st.write(f"Steps taken: **{steps}**")
            if position != -1:
                st.success(f"Found at position {position + 1} of the name-sorted list.")
                st.dataframe(to_table([by_name[position]]),
                             width="stretch", hide_index=True)
            else:
                st.warning("No exact match found (Binary Search needs the full name).")


# ---------------------------------------------------------------------------
# TAB 4: Budget Optimizer (Greedy vs 0/1 Knapsack)
# ---------------------------------------------------------------------------
with tab_opt:
    st.subheader("Optional Expense Optimizer")
    mandatory, optional = split_expenses(expenses)
    mandatory_total = total_expenses(mandatory)
    available = max(0.0, budget - mandatory_total)

    m1, m2, m3 = st.columns(3)
    m1.metric("Mandatory expenses", f"₹ {mandatory_total:,.2f}")
    m2.metric("Left for optional items", f"₹ {available:,.2f}")
    m3.metric("Optional items", len(optional))

    if mandatory_total > budget:
        st.error("Even mandatory expenses are more than your budget. "
                 "Increase the budget or reduce mandatory costs.")

    with st.expander("Mandatory expenses (kept separate, always paid)"):
        st.dataframe(to_table(mandatory), width="stretch", hide_index=True)

    if not optional:
        st.info("No optional expenses (Household Items / Entertainment / Other) to optimize.")
    else:
        st.write("Optional expenses (with benefit score):")
        st.dataframe(to_table(optional), width="stretch", hide_index=True)

        limit = st.number_input("Money available for optional expenses (₹)",
                                min_value=0.0, value=float(available), step=100.0)

        # Run both algorithms and time them
        t0 = time.perf_counter()
        g_items, g_cost, g_benefit = greedy_allocation(optional, limit)
        greedy_ms = (time.perf_counter() - t0) * 1000

        t0 = time.perf_counter()
        d_items, d_cost, d_benefit = knapsack_dp(optional, limit)
        dp_ms = (time.perf_counter() - t0) * 1000

        left, right = st.columns(2)
        with left:
            st.markdown("### Greedy (benefit ÷ cost)")
            st.write(f"Total cost: **₹ {g_cost:,.0f}**")
            st.write(f"Total benefit: **{g_benefit}**")
            st.write(f"Time: {greedy_ms:.4f} ms")
            st.dataframe(to_table(g_items), width="stretch", hide_index=True)
        with right:
            st.markdown("### Dynamic Programming (0/1 Knapsack)")
            st.write(f"Total cost: **₹ {d_cost:,.0f}**")
            st.write(f"Total benefit: **{d_benefit}**")
            st.write(f"Time: {dp_ms:.4f} ms")
            st.dataframe(to_table(d_items), width="stretch", hide_index=True)

        if d_benefit > g_benefit:
            st.info(f"Dynamic Programming found a better combination "
                    f"(benefit {d_benefit} vs {g_benefit}). Greedy is faster but not always optimal.")
        else:
            st.info("Both algorithms gave the same benefit for this input.")


# ---------------------------------------------------------------------------
# TAB 5: Performance comparison
# ---------------------------------------------------------------------------
with tab_perf:
    st.subheader("Algorithm Performance Comparison")
    st.caption("Timed with time.perf_counter() on random data.")

    if st.button("Run comparison"):
        search_rows = compare_searching([100, 500, 1000, 5000])
        sort_rows = compare_sorting([100, 500, 1000, 5000])
        opt_rows = compare_optimization([5, 10, 15, 20])

        st.markdown("#### Linear Search vs Binary Search")
        st.dataframe(search_rows, hide_index=True)
        draw_line_chart(search_rows, "Expenses (n)",
                        ["Linear Search (ms)", "Binary Search (ms)"],
                        "Searching time", "Time (ms)")

        st.markdown("#### Merge Sort")
        st.dataframe(sort_rows, hide_index=True)
        draw_line_chart(sort_rows, "Expenses (n)",
                        ["Merge Sort (ms)", "Python sorted() (ms)"],
                        "Sorting time", "Time (ms)")

        st.markdown("#### Greedy vs Dynamic Programming (limit ₹5000)")
        st.dataframe(opt_rows, hide_index=True)
        draw_line_chart(opt_rows, "Optional items",
                        ["Greedy time (ms)", "DP time (ms)"],
                        "Optimization time", "Time (ms)")
