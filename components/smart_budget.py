import streamlit as st 

def show_smart_budget(
    spendings,
    current_month_total,
    current_month_report
):

    suggested_savings = 0
    recommended_budget = 0

    st.divider()
    st.subheader("Smart Budget Recommendation")

    if len(spendings) >= 3:

        # Average of last 3 months
        avg_last3 = sum(spendings[-3:]) / 3

        # Recommend 10% lower than average spending
        recommended_budget = avg_last3 * 0.90

        st.metric(
            "Recommended Budget for Next Month",
            f"₹{recommended_budget:.0f}"
        )

        # Suggested savings
    
        st.divider()
        suggested_savings = recommended_budget * 0.20

        st.metric(
            "Suggested Savings Target",
            f"₹{suggested_savings:.0f}"
        )
        st.subheader("Category Budget Suggestions")

        total_current = current_month_total

        if total_current > 0:

            for category, amount in current_month_report.items():

                percentage = amount / total_current
                suggested_amount = recommended_budget * percentage
                
                st.write(
                    f"• {category}: ₹{suggested_amount:.0f}"
                )
                if suggested_amount > 0 and amount > suggested_amount:
                    st.warning(
                        f"Reduce {category} by ₹{amount - suggested_amount:.0f}"
                    )
    else:
        st.info(
            "Add expense data for at least 3 months to receive smart budget recommendations."
        )
        
    return (
        recommended_budget,
        suggested_savings
    )