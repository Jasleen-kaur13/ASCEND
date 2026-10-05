import streamlit as st
import matplotlib.pyplot as plt

def show_pie_chart(report):

    st.divider()
    st.subheader("Expense Distribution")

    if len(report) > 0:

        fig1, ax1 = plt.subplots(figsize=(6,6))

        chart_colors = [
            "#4F46E5",
            "#06B6D4",
            "#10B981",
            "#F59E0B",
            "#EF4444",
            "#8B5CF6",
            "#EC4899",
            "#14B8A6",
            "#64748B"
        ]

        ax1.pie(
            report,
            labels=report.index,
            autopct="%1.1f%%",
            startangle=90,
            colors=chart_colors[:len(report)],
            wedgeprops=dict(width=0.45)
        )

        ax1.set_title("Expense Distribution")

        fig1.savefig("pie_chart.png")

        st.pyplot(fig1)

    else:

        st.warning("No data available for chart.")