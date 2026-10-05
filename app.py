from ai_tab import render_ai_insights

from config import setup_page
from database.db import create_table

from utils.upload import render_upload_box

# ==========================
# Imports
# ==========================

import pandas as pd

import streamlit as st

from data.loader import load_expenses

from components.sidebar import sidebar_filters
from components.overview import show_overview
from components.finance import show_finance_dashboard
from components.goal_tracker import show_goal_tracker
from components.expense_table import show_expense_table
from components.delete_expense import delete_expense
from components.edit_expense import edit_expense
from components.clear_database import clear_database
from components.add_expense import add_expense
from components.category_dashboard import show_category_dashboard
from components.analytics_dashboard import show_analytics_dashboard
from components.ai_dashboard import show_ai_dashboard
from components.reports_dashboard import show_reports_dashboard

from utils.report_generator import generate_category_report

# ==========================
# App Setup
# ==========================

setup_page()
render_upload_box()
create_table()

# ==========================
# Load Data
# ==========================

expenses, df = load_expenses()

# Sidebar (always visible)
filtered_df, budget, income = sidebar_filters(df, expenses)

# months covered by the selected data, so income/budget match total spending
if filtered_df is not None and len(filtered_df) > 0:
    n_months = max(
        pd.to_datetime(filtered_df["date"], dayfirst=True, errors="coerce")
        .dt.to_period("M").nunique(), 1)
else:
    n_months = 1
period_income = income * n_months
period_budget = budget * n_months


# ==========================
# Tabs
# ==========================

tab_dashboard, tab_analytics, tab_ai, tab_reports = st.tabs([
    "🏠 Dashboard",
    "📊 Analytics",
    "🤖 AI Insights",
    "📄 Reports"
])

# ======================================================
# Dashboard
# ======================================================

with tab_dashboard:

    total, average, highest, lowest = show_overview(filtered_df, period_budget)

    show_finance_dashboard(total, period_budget, period_income)

    current_savings = show_goal_tracker(total, period_income)

    search_df = show_expense_table(filtered_df)

    # Generate report for other tabs
    report = generate_category_report(search_df)

    delete_expense(filtered_df)

    edit_expense(filtered_df)

    add_expense(expenses)

    clear_database(expenses)

# ======================================================
# Analytics
# ======================================================

with tab_analytics:

    show_category_dashboard(
        search_df,
        report,
        total
    )

    prediction, score, months, spendings, sorted_months, model = (
        show_analytics_dashboard(
            expenses,
            filtered_df
        )
    )

# ======================================================
# AI Insights
# ======================================================

with tab_ai:

    (
        score,
        highest_category,
        highest_amount,
        risk_level,
        recommended_budget,
        suggested_savings,
    ) = show_ai_dashboard(
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
    )
    
    st.divider()
    
    render_ai_insights(df, budget, income)

# ======================================================
# Reports
# ======================================================

with tab_reports:

    show_reports_dashboard(
        filtered_df,
        total,
        period_income,
        current_savings,
        period_budget,
        score,
        report,
        prediction,
        months,
        risk_level,
        highest_category,
        recommended_budget
    )

# ==========================
# Footer
# ==========================

st.markdown("""
---
<center>
Built with ❤️ using Streamlit | AI Expense Analytics Dashboard
</center>
""", unsafe_allow_html=True)