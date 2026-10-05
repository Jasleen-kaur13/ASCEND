import streamlit as st

def show_export_report(filtered_df):

    st.divider()
    st.subheader("📥 Export Expense Report")

    csv = filtered_df.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="Download CSV Report",
        data=csv,
        file_name="Expense_Report.csv",
        mime="text/csv"
    )