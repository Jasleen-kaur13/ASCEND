import streamlit as st

def show_category_summary(search_df):

    st.divider()
    st.subheader("Category Summary")

    category_summary = (
        search_df.groupby("category")["amount"]
        .sum()
        .reset_index()
    )

    st.dataframe(category_summary)