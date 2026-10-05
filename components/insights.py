import streamlit as st

def show_insights(sorted_months):
    
    st.divider()
    st.subheader("📊 Expense Insights")

    if len(sorted_months) > 0:

        values = [v for _, v in sorted_months]

        highest_month, highest_value = max(
            sorted_months,
            key=lambda x: x[1]
        )

        lowest_month, lowest_value = min(
            sorted_months,
            key=lambda x: x[1]
        )

        average_monthly = sum(values) / len(values)

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Highest Month",
            f"{highest_month}",
            f"₹{highest_value:.0f}"
        )

        col2.metric(
            "Lowest Month",
            f"{lowest_month}",
            f"₹{lowest_value:.0f}"
        )

        col3.metric(
            "Average Monthly",
            f"₹{average_monthly:.0f}"
        )

        if highest_value > average_monthly * 1.5:
            st.warning(
                f"{highest_month} had unusually high spending."
            )

        if lowest_value < average_monthly * 0.5:
            st.success(
                f"{lowest_month} was your most economical month."
            )

    else:
        st.info("No monthly expense data available.")