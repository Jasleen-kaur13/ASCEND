import streamlit as st
from database.db import delete_expense_db


def delete_expense(filtered_df):

    st.divider()
    st.subheader("🗑 Delete Expense")

    if filtered_df.empty:
        st.info("No expenses available.")
        return

    delete_index = st.selectbox(
        "Select Expense",
        filtered_df.index,
        format_func=lambda i:
            f"{filtered_df.loc[i,'category']} | "
            f"₹{filtered_df.loc[i,'amount']} | "
            f"{filtered_df.loc[i,'date']}",
        key="delete_expense"
    )

    if st.button("Delete Selected Expense"):

        expense_id = filtered_df.loc[delete_index, "id"]

        delete_expense_db(expense_id)

        st.success("Expense deleted successfully!")

        st.rerun()