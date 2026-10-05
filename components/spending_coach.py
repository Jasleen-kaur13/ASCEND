import streamlit as st


def show_spending_coach(
    sorted_months,
    current_month_total,
    budget,
    prediction,
    current_month_report,
    suggested_savings,
    risk_level
):

    st.divider()
    st.subheader("🧠 AI Spending Coach")

    if len(sorted_months) < 2:
        st.info(
            "Add expense data for at least 2 months to use the AI Spending Coach."
        )
        return

    advice = []

    # ==========================
    # Budget Analysis
    # ==========================

    if current_month_total > budget:
        advice.append(
            f"⚠ You exceeded your monthly budget by ₹{current_month_total - budget:.0f}."
        )
    else:
        advice.append(
            "✅ You are within your monthly budget."
        )

    # ==========================
    # AI Prediction
    # ==========================

    if prediction is not None:

        predicted_amount = prediction

        if predicted_amount > current_month_total:
            advice.append(
                f"📈 AI predicts your next month's spending may increase to ₹{predicted_amount:.0f}."
            )
        else:
            advice.append(
                f"📉 AI predicts your next month's spending may remain around ₹{predicted_amount:.0f} or decrease."
            )

    else:

        advice.append(
            "🤖 AI prediction is unavailable. Add at least two months of expense data."
        )

    # ==========================
    # Highest Spending Category
    # ==========================

    if len(current_month_report) > 0:

        highest_category = current_month_report.idxmax()
        highest_amount = current_month_report.max()

        advice.append(
            f"💰 Highest spending category: {highest_category} (₹{highest_amount:.0f})."
        )

    else:

        advice.append(
            "No spending categories available."
        )

    # ==========================
    # Daily Savings Goal
    # ==========================

    if suggested_savings > 0:
        daily_save = suggested_savings / 30
    else:
        daily_save = (budget * 0.20) / 30

    advice.append(
        f"🏦 Save approximately ₹{daily_save:.0f} per day to achieve your monthly savings goal."
    )

    # ==========================
    # Risk Advice
    # ==========================

    if risk_level == "High Risk":
        advice.append(
            "🚨 Your financial risk is HIGH. Reduce unnecessary expenses immediately."
        )

    elif risk_level == "Medium Risk":
        advice.append(
            "⚠ Your financial risk is MEDIUM. Monitor your spending carefully."
        )

    else:
        advice.append(
            "🎉 Great! Your spending pattern looks healthy."
        )

    # ==========================
    # Display Tips
    # ==========================

    for tip in advice:
        st.write(tip)