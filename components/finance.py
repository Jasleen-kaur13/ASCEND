import streamlit as st


def show_finance_dashboard(
    total,
    budget,
    income
):
    # ==========================
    # Income & Savings Dashboard
    # ==========================

    st.divider()
    st.subheader("💵 Income & Savings Dashboard")

    savings = income - total

    expense_ratio = (
        (total / income) * 100
        if income > 0 else 0
    )

    saving_ratio = (
        (savings / income) * 100
        if income > 0 else 0
    )

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Income",
        f"₹{income:.0f}"
    )

    col2.metric(
        "Savings",
        f"₹{savings:.0f}"
    )

    col3.metric(
        "Savings Rate",
        f"{saving_ratio:.1f}%"
    )

    st.progress(
        min(expense_ratio / 100, 1.0)
    )

    st.write(
        f"Expense Ratio: {expense_ratio:.1f}%"
    )

    # =====================================
    # Budget Progress
    # =====================================

    st.divider()
    st.subheader("📈 Budget Progress")

    if budget > 0:
        budget_used = min(total / budget, 1.0)
    else:
        budget_used = 0

    st.progress(budget_used)

    st.write(
        f"₹{total:.0f} spent out of ₹{budget:.0f}"
    )

    # =====================================
    # Savings Progress
    # =====================================

    st.divider()
    st.subheader("💰 Savings Progress")

    if income > 0:
        savings_progress = max(savings / income, 0)
    else:
        savings_progress = 0

    st.progress(savings_progress)

    st.write(
        f"₹{savings:.0f} saved from ₹{income:.0f}"
    )

    return savings