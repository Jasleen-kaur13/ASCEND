import streamlit as st

def show_expense_table(filtered_df):
    
    # Search Expenses
    st.subheader("Search Expenses")

    search = st.text_input(
        "Search by Category"
    )

    search_df = filtered_df.copy()

    if search.strip() != "":
        search_df = filtered_df[
            filtered_df["category"].str.contains(
                search,
                case=False,
                na=False
            )
        ]

    # Expense Records
    st.divider()
    st.subheader("Expense Records")
    display_df = search_df.reset_index(drop=True)

    display_df.index = display_df.index + 1

    with st.expander("📄 Expense Records", expanded=True):
        st.dataframe(display_df)
    return search_df