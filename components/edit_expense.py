import streamlit as st
from datetime import datetime, date

from database.db import update_expense, load_expenses
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


def edit_expense(filtered_df):

    st.divider()
    st.subheader("✏️ Edit Expense")

    if filtered_df.empty:
        st.info("No expenses available to edit.")
        return

    edit_index = st.selectbox(
        "Select Expense",
        filtered_df.index,
        format_func=lambda i:
            f"{filtered_df.loc[i,'category']} | "
            f"₹{filtered_df.loc[i,'amount']} | "
            f"{filtered_df.loc[i,'date']}",
        key="edit_expense"
    )

    current_category = filtered_df.loc[edit_index, "category"]

    cat_options = merged_categories(DEFAULT_CATEGORIES, load_expenses())
    if current_category not in cat_options:
        cat_options.append(current_category)

    new_category = st.selectbox(
        "Category",
        cat_options,
        index=cat_options.index(current_category)
    )

    new_amount = st.number_input(
        "Amount",
        min_value=1.0,
        value=float(filtered_df.loc[edit_index, "amount"])
    )

    expense_date = filtered_df.loc[edit_index, "date"]

    try:
        default_date = datetime.strptime(
            expense_date,
            "%d-%m-%Y"
        ).date()
    except Exception:
        default_date = date.today()

    new_date = st.date_input(
        "Date",
        value=default_date
    )

    if st.button("Update Expense"):

        expense_id = filtered_df.loc[edit_index, "id"]

        update_expense(
            expense_id,
            new_category,
            new_amount,
            new_date.strftime("%d-%m-%Y")
        )

        st.success("Expense updated successfully!")

        st.rerun()