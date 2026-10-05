from components.export_report import show_export_report
from components.pdf_report import show_pdf_report


def show_reports_dashboard(
    filtered_df,
    total,
    income,
    current_savings,
    budget,
    score,
    report,
    prediction,
    months,
    risk_level,
    highest_category,
    recommended_budget
):

    show_export_report(filtered_df)

    show_pdf_report(
        total,
        income,
        current_savings,
        budget,
        score,
        report,
        prediction,
        months,
        risk_level,
        highest_category,
        recommended_budget
    )