import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def show_monthly_trend(sorted_months):
    
    # ==========================
    # Monthly Expense Trend
    # ==========================

    st.divider()
    st.subheader("📈 Monthly Expense Trend")

    if len(sorted_months) > 0:

        trend_df = pd.DataFrame({
            "Month": [m for m, _ in sorted_months],
            "Expense": [v for _, v in sorted_months]
        })

        fig, ax = plt.subplots(figsize=(9,5))

        ax.plot(
            trend_df["Month"],
            trend_df["Expense"],
            marker="o",
            linewidth=3,
            color="#4F46E5"
        )

        for x, y in zip(
            trend_df["Month"],
            trend_df["Expense"]
        ):

            ax.text(
                x,
                y,
                f"₹{y:.0f}",
                ha="center",
                va="bottom"
            )

        ax.set_title(
            "Monthly Expense Trend",
            fontsize=16,
            fontweight="bold"
        )

        ax.grid(alpha=.3)

        st.pyplot(fig)
        st.markdown('<div class="chart-box">',unsafe_allow_html=True)

        st.pyplot(fig)

        st.markdown("</div>",unsafe_allow_html=True)

    else:
        st.info("No monthly data available.")