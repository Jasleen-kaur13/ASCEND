import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

def show_prediction_chart(model, months, spendings, prediction):
        # Prediction Graph
    
        fig3, ax3 = plt.subplots(figsize=(8, 5))

        future_range = pd.DataFrame({
        "month": list(range(1, len(months) + 2))
    })

        ax3.plot(
            future_range["month"],
            model.predict(future_range),
            linewidth=3,
            color="#4F46E5",
            label="Prediction"
        )

        ax3.scatter(
            months,
            spendings,
            color="#10B981",
            s=90,
            label="Actual"
        )

        ax3.scatter(
            len(months)+1,
            prediction,
            color="#EF4444",
            s=120,
            label="Next Month"
        )

        ax3.legend()
        ax3.grid(alpha=.3)

        ax3.set_title("Expense Prediction")
        ax3.set_xlabel("Month Number")
        ax3.set_ylabel("Spending")

        fig3.savefig("prediction_chart.png")
        st.pyplot(fig3)
    
        show_prediction_chart(
        model,
        months,
        spendings,
        prediction
    )
    