from charts.pie_chart import show_pie_chart
from charts.bar_chart import show_bar_chart

from components.category_summary import show_category_summary
from components.top_Category import show_top_Category

def show_category_dashboard(
    search_df,
    report,
    total
):

    show_pie_chart(report)

    show_bar_chart(report)

    show_category_summary(search_df)

    show_top_Category(
        report,
        total
    )