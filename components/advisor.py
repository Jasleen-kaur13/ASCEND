import streamlit as st

def show_advisor(report, total, budget):

    st.divider()
    st.subheader("AI Financial Advisor")

    # Default values
    score = 0
    highest_category = "None"
    highest_amount = 0
    risk_level = "Low"
    recommended_budget = budget
    suggested_savings = 0

    if len(report) > 0 and total > 0:

        highest_category = report.idxmax()
        highest_amount = report.max()

        if highest_amount > total * 0.4:
            st.warning(
                f"You are spending {highest_amount/total*100:.1f}% "
                f"of your budget on {highest_category}. "
                f"Consider reducing this category."
            )
        else:
            st.success(
                "Your spending is reasonably balanced across categories."
            )

        suggested_savings = total * 0.10

        st.info(
            f"Suggested Monthly Savings Goal: ₹{suggested_savings:.0f}"
        )

        for category, amount in report.items():
            percentage = amount / total * 100

            if percentage > 50:
                st.error(
                    f"High Spending Alert: {category} "
                    f"accounts for {percentage:.1f}% of spending."
                )

        score = 100

        if total > budget:
            score -= 30

        if len(report) <= 2:
            score -= 20

        if highest_amount > total * 0.5:
            score -= 20

        score = max(score, 0)

        st.subheader("Financial Health Score")
        st.metric("Score", f"{score}/100")

        st.subheader("Recommendations")

        recommendations = []

        if total > budget:
            recommendations.append(
                "Reduce monthly spending to stay within budget."
            )

        if highest_amount > total * 0.4:
            recommendations.append(
                f"Try reducing spending in {highest_category}."
            )

        if not recommendations:
            recommendations.append(
                "Great job! Your spending habits look healthy."
            )

        for item in recommendations:
            st.write("✅", item)

        if score >= 80:
            risk_level = "Low"
        elif score >= 50:
            risk_level = "Medium"
        else:
            risk_level = "High"

    else:
        st.warning("No expense data available for financial advice.")

        score = 0
        highest_category = "None"
        highest_amount = 0

    print("Advisor returning:", score, highest_category, highest_amount)

    return (
        score,
        highest_category,
        highest_amount
    )