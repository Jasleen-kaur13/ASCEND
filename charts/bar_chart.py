import streamlit as st
import matplotlib.pyplot as plt

def show_bar_chart(report):
    
    # Bar Chart

    st.divider()
    st.subheader("Category Comparison")

    if len(report) > 0:

        fig2, ax2 = plt.subplots(figsize=(8, 5))

        bars = ax2.bar(
            report.index,
            report.values,
            color="#4F46E5"
        )

        for bar in bars:

            height = bar.get_height()

            ax2.text(
                bar.get_x() + bar.get_width()/2,
                height,
                f"₹{height:.0f}",
                ha="center",
                va="bottom",
                fontsize=10
            )

        ax2.set_title("Expense Comparison")
        ax2.set_xlabel("Category")
        ax2.set_ylabel("Amount")

        fig2.savefig("bar_chart.png")
        st.pyplot(fig2)

    else:
        st.warning("No category data available.")