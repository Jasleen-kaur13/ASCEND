import streamlit as st


def show_spending_intelligence(
    df,
    report,
    total,
    budget,
    prediction,
    months,
    spendings,
    sorted_months
):

    st.divider()
    st.subheader("🧠 Spending Intelligence Engine")

    # -------------------------
    # Default values
    # -------------------------
    current_month_total = 0
    current_month_report = {}
    highest_category = "N/A"
    highest_amount = 0
    risk_level = "Low Risk"

    if len(sorted_months) >= 2:

        current_month_name, current_month_total = sorted_months[-1]
        previous_month_name, previous_month_total = sorted_months[-2]

        difference = current_month_total - previous_month_total

        if previous_month_total != 0:
            percent_change = (difference / previous_month_total) * 100
        else:
            percent_change = 0

        # -------------------------
        # Month Comparison
        # -------------------------

        st.divider()
        st.subheader("📈 Month-to-Month Change")

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Previous Month",
            f"₹{previous_month_total:.0f}"
        )

        col2.metric(
            "Current Month",
            f"₹{current_month_total:.0f}"
        )

        col3.metric(
            "Change",
            f"{percent_change:.1f}%"
        )

        if difference > 0:
            st.warning(
                f"Your spending increased by ₹{difference:.0f} ({percent_change:.1f}%)."
            )

        elif difference < 0:

            st.success(
                f"Your spending decreased by ₹{abs(difference):.0f} ({abs(percent_change):.1f}%)."
            )

        else:
            st.info("Your spending is unchanged.")

        # -------------------------
        # Current Month Report
        # -------------------------

        current_month_df = df[
            df["date"].apply(
                lambda x:
                "-".join(str(x).split("-")[1:])
                if len(str(x).split("-")) == 3
                else ""
            ) == current_month_name
        ]

        current_month_report = current_month_df.groupby(
            "category"
        )["amount"].sum()

        if len(current_month_report) > 0:

            highest_category = current_month_report.idxmax()
            highest_amount = current_month_report.max()

        # -------------------------
        # Risk Score
        # -------------------------

        risk_score = 0

        if current_month_total > budget:
            risk_score += 2

        if highest_amount > total * 0.5:
            risk_score += 2

        elif highest_amount > total * 0.35:
            risk_score += 1

        if difference > 0:
            risk_score += 1

        if len(months) >= 3:

            if spendings[-1] > spendings[-2] > spendings[-3]:
                risk_score += 2

        if risk_score >= 5:

            risk_level = "High Risk"
            st.error(f"Risk Level : {risk_level}")

        elif risk_score >= 3:

            risk_level = "Medium Risk"
            st.warning(f"Risk Level : {risk_level}")

        else:

            risk_level = "Low Risk"
            st.success(f"Risk Level : {risk_level}")

        # -------------------------
        # Prediction
        # -------------------------

        if prediction is not None:
            predicted_value = float(prediction)
        else:
            predicted_value = current_month_total

        st.divider()
        st.subheader("📊 Trend Analysis")

        if difference > 0 and predicted_value > current_month_total:

            st.warning(
                "Spending is increasing and AI predicts another increase."
            )

        elif difference > 0:

            st.info(
                "Spending increased but AI predicts stabilization."
            )

        elif difference < 0 and predicted_value < current_month_total:

            st.success(
                "Spending is decreasing and AI predicts further improvement."
            )

        else:

            st.info(
                "Your spending trend is stable."
            )

        # -------------------------
        # Category Alerts
        # -------------------------

        st.divider()
        st.subheader("⚠ Category Danger Detector")

        for category, amount in current_month_report.items():

            percentage = amount / current_month_total * 100

            if percentage >= 50:

                st.error(
                    f"{category} uses {percentage:.1f}% of your spending."
                )

            elif percentage >= 30:

                st.warning(
                    f"{category} uses {percentage:.1f}% of your spending."
                )

        # -------------------------
        # AI Summary
        # -------------------------

        st.divider()
        st.subheader("🤖 AI Summary")

        summary = (
            f"Current Month Spending: ₹{current_month_total:.0f}\n\n"
            f"Previous Month Spending: ₹{previous_month_total:.0f}\n\n"
            f"Risk Level: {risk_level}\n\n"
            f"Highest Spending Category: {highest_category}"
        )

        st.info(summary)

    else:

        st.warning(
            "Add expense data for at least 2 months to use the Spending Intelligence Engine."
        )

    return (
        current_month_total,
        current_month_report,
        highest_category,
        highest_amount,
        risk_level
    )