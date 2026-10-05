import streamlit as st

def show_top_Category(report, total):

    # ==========================
    # Top Spending Category
    # ==========================


    st.divider()
    st.subheader("🏆 Top Spending Category")

    if len(report) > 0:

        top_category = report.idxmax()
        top_amount = report.max()

        percentage = (top_amount / total) * 100 if total > 0 else 0

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Category",
            top_category
        )

        col2.metric(
            "Amount",
            f"₹{top_amount:.0f}"
        )

        col3.metric(
            "Share",
            f"{percentage:.1f}%"
        )

        if percentage >= 50:
            st.error(
                f"⚠ {top_category} accounts for more than half of your total spending."
            )

        elif percentage >= 30:
            st.warning(
                f"{top_category} is your largest expense category."
            )

        else:
            st.success(
                "Your expenses are well distributed."
            )

    else:

        st.info("No expense data available.")