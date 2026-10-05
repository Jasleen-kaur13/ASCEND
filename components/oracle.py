import streamlit as st

import os

def show_oracle(
    filtered_df,
    total,
    average,
    budget,
    income,
    score,
    risk_level,
    prediction,
    months,
    report,
    highest_category,
    highest_amount
):
    
    try:
        ai_on = bool(os.getenv("LLM_API_KEY") or st.secrets["LLM_API_KEY"])
    except Exception:
        ai_on = False

    if ai_on:
        return  # the AI agent chat (Ask ASCEND) replaces this

    st.divider()
    st.subheader("🔮 Expense Oracle")

    question = st.text_input(
        "Ask about your finances"
    )

    if not question:
        return

    q = question.lower()

    # ==========================
    # Total Spending
    # ==========================

    if "total" in q or "spent" in q:

        st.success(
            f"Total spending is ₹{total:.2f}."
        )

    # ==========================
    # Average Spending
    # ==========================

    elif "average" in q:

        st.info(
            f"Average expense is ₹{average:.2f}."
        )

    # ==========================
    # Highest Expense
    # ==========================

    elif "highest expense" in q:

        if not filtered_df.empty:
            highest = filtered_df["amount"].max()
        else:
            highest = 0

        st.success(
            f"Highest expense is ₹{highest:.2f}."
        )

    # ==========================
    # Lowest Expense
    # ==========================

    elif "lowest expense" in q:

        if not filtered_df.empty:
            lowest = filtered_df["amount"].min()
        else:
            lowest = 0

        st.success(
            f"Lowest expense is ₹{lowest:.2f}."
        )

    # ==========================
    # Highest Category
    # ==========================

    elif "highest category" in q or "most" in q:

        st.success(
            f"Highest spending category is {highest_category} (₹{highest_amount:.2f})."
        )

    # ==========================
    # Budget
    # ==========================

    elif "budget" in q:

        if total > budget:

            st.error(
                f"You exceeded your budget by ₹{total - budget:.2f}."
            )

        else:

            st.success(
                f"Budget remaining: ₹{budget - total:.2f}"
            )

    # ==========================
    # Savings
    # ==========================

    elif "save" in q or "saving" in q:

        savings = max(income - total, 0)

        st.info(
            f"Current savings: ₹{savings:.2f}"
        )

    # ==========================
    # Health Score
    # ==========================

    elif "health" in q or "score" in q:

        st.info(
            f"Financial Health Score: {score}/100"
        )

    # ==========================
    # Risk
    # ==========================

    elif "risk" in q:

        st.warning(
            f"Current Risk Level: {risk_level}"
        )

    # ==========================
    # AI Prediction
    # ==========================

    elif "prediction" in q or "predict" in q:

        if prediction is not None:

            st.info(
                f"Predicted next month's spending: ₹{prediction:.2f}"
            )

        else:

            st.warning(
                "Prediction is unavailable. Add expense data for at least two months."
            )

    # ==========================
    # Number of Expenses
    # ==========================

    elif "count" in q or "expenses" in q:

        st.info(
            f"You have {len(filtered_df)} expense records."
        )

    # ==========================
    # Category Report
    # ==========================

    elif "category" in q:

        if len(report) > 0:
            st.write(report)
        else:
            st.info("No category report available.")

    # ==========================
    # Help
    # ==========================

    else:

        st.info(
            """
You can ask me:

• Total spending
• Average expense
• Highest expense
• Lowest expense
• Highest category
• Budget
• Savings
• Prediction
• Financial health score
• Risk level
• Expense count
• Category report
            """
        )