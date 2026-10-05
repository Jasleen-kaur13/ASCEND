import streamlit as st
from datetime import date

from database.db import add_expense as add_expense_db, load_expenses
from utils.categories import merged_categories

DEFAULT_CATEGORIES = [
    "Food",
    "Travel",
    "Shopping",
    "Clothing",
    "Healthcare",
    "Education",
    "Entertainment",
    "Bills",
    "Other",
]

NEW = "➕ Add new category..."


def add_expense(expenses):

    st.sidebar.divider()
    st.sidebar.markdown("## ➕ Add Expense")

    options = merged_categories(DEFAULT_CATEGORIES, load_expenses()) + [NEW]

    choice = st.sidebar.selectbox(
        "Category",
        options,
        key="add_category"
    )

    if choice == NEW:
        category = st.sidebar.text_input(
            "New category name",
            key="add_new_category"
        ).strip().title()
    else:
        category = choice

    amount = st.sidebar.number_input(
        "Amount",
        min_value=1.0,
        step=1.0,
        key="add_amount"
    )

    expense_date = st.sidebar.date_input(
        "Select Date",
        value=date.today(),
        key="add_date"
    )

    if st.sidebar.button("Add Expense"):

        if not category:
            st.sidebar.error("Please enter a category name")
        else:
            add_expense_db(
                category,
                amount,
                expense_date.strftime("%d-%m-%Y")
            )

            st.sidebar.success("Expense Added Successfully!")
            st.rerun()