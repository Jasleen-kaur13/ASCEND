import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

def show_prediction(expenses):
    
    st.divider()
    monthly_report = {}

    for expense in expenses:

        if "date" not in expense:
            continue

        parts = expense["date"].split("-")

        if len(parts) != 3:
            continue

        month = parts[1]
        year = parts[2]

        key = month + "-" + year

        if key in monthly_report:
            monthly_report[key] += expense["amount"]
        else:
            monthly_report[key] = expense["amount"]

    sorted_months = sorted(
        monthly_report.items(),
        key=lambda x: (
            int(x[0].split("-")[1]),
            int(x[0].split("-")[0])
        )
    )

    months = []
    spendings = []

    count = 1

    for key, value in sorted_months:
        months.append(count)
        spendings.append(value)
        count += 1
        
    prediction = None
    score = 0
    model = None    

    if len(months) >= 2:

        df_ml = pd.DataFrame({
            "month": months,
            "spending": spendings
        })

        x = df_ml[["month"]]
        y = df_ml[["spending"]]

        model = LinearRegression()
        model.fit(x, y)

        future_month = pd.DataFrame({
            "month": [len(months) + 1]
        })

        prediction = model.predict(future_month)

        # Convert prediction to a normal float
        prediction = float(prediction.ravel()[0])

        st.subheader("AI Prediction")

        st.metric(
            "Predicted Next Month Spending",
            f"₹{prediction:.2f}"
        )
        
        # -------------------------
        # Save Prediction Chart
        # -------------------------

        plt.figure(figsize=(6,4))

        plt.plot(months, spendings,
            marker="o",
            linewidth=2,
            label="Actual Spending")

        plt.scatter(
            len(months)+1,
            prediction,
            color="red",
            s=120,
            label="Prediction"
        )

        plt.xlabel("Month")
        plt.ylabel("Spending (₹)")
        plt.title("Monthly Spending Prediction")
        plt.legend()
        plt.grid(True)

        plt.savefig("prediction_chart.png")
        plt.close()
    
        score = model.score(x, y)

        st.metric(
            "Model Accuracy (R²)",
            f"{score:.2f}"
        )
    
        if score > 0.8:
            st.success("Prediction reliability is good.")
        elif score > 0.5:
            st.warning("Prediction reliability is moderate.")
        else:
            st.error("Prediction reliability is low.")
    
        

    else:
        st.warning("Add data from at least 2 different months for AI prediction.")
        
    return (
        prediction,
        score,
        months,
        spendings,
        sorted_months,
        model
    )