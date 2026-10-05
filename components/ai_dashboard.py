from components.advisor import show_advisor
from components.intelligence import show_spending_intelligence
from components.smart_budget import show_smart_budget
from components.spending_coach import show_spending_coach
from components.oracle import show_oracle


def show_ai_dashboard(
    df,
    filtered_df,
    report,
    total,
    average,
    budget,
    income,
    score,
    prediction,
    months,
    spendings,
    sorted_months
):

    # ----------------------------
    # AI Financial Advisor
    # ----------------------------

    advisor_result = show_advisor(
        report,
        total,
        budget
    )

    if advisor_result is None:
        score = 0
        highest_category = "None"
        highest_amount = 0
    else:
        score, highest_category, highest_amount = advisor_result

    # ----------------------------
    # Spending Intelligence
    # ----------------------------

    intelligence_result = show_spending_intelligence(
        df,
        report,
        total,
        budget,
        prediction,
        months,
        spendings,
        sorted_months
    )

    if intelligence_result is None:
        current_month_total = 0
        current_month_report = {}
        highest_category = "None"
        highest_amount = 0
        risk_level = "Low Risk"
    else:
        (
            current_month_total,
            current_month_report,
            highest_category,
            highest_amount,
            risk_level
        ) = intelligence_result

    # ----------------------------
    # Smart Budget
    # ----------------------------

    budget_result = show_smart_budget(
        spendings,
        current_month_total,
        current_month_report
    )

    if budget_result is None:
        recommended_budget = budget
        suggested_savings = 0
    else:
        recommended_budget, suggested_savings = budget_result

    # ----------------------------
    # Spending Coach
    # ----------------------------

    show_spending_coach(
        sorted_months,
        current_month_total,
        budget,
        prediction,
        current_month_report,
        suggested_savings,
        risk_level
    )

    # ----------------------------
    # Expense Oracle
    # ----------------------------

    show_oracle(
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
    )

    # ----------------------------
    # Return values
    # ----------------------------

    return (
        score,
        highest_category,
        highest_amount,
        risk_level,
        recommended_budget,
        suggested_savings
    )