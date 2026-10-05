from components.prediction import show_prediction
from components.insights import show_insights
from components.anomaly_detection import show_anomaly_detection

from charts.monthly_trend import show_monthly_trend


def show_analytics_dashboard(
    expenses,
    filtered_df
):

    prediction, score, months, spendings, sorted_months, model = show_prediction(expenses)

    show_monthly_trend(sorted_months)

    show_insights(sorted_months)

    show_anomaly_detection(filtered_df)

    return (
        prediction,
        score,
        months,
        spendings,
        sorted_months,
        model
    )