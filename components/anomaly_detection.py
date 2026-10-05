import streamlit as st

def show_anomaly_detection(filtered_df):
    
    st.divider()
    st.subheader("🚨 AI Anomaly Detection")

    if len(filtered_df) >= 5:

        mean_amount = filtered_df["amount"].mean()
        std_amount = filtered_df["amount"].std()

        threshold = mean_amount + (2 * std_amount)

        anomalies = filtered_df[
            filtered_df["amount"] > threshold
        ]

        if len(anomalies) > 0:

            st.error(
                f"{len(anomalies)} unusual expense(s) detected."
            )

            st.dataframe(anomalies)

            for _, row in anomalies.iterrows():

                st.warning(
                    f"{row['category']} expense of ₹{row['amount']} "
                    f"on {row['date']} is unusually high."
                )

        else:

            st.success(
                "No unusual expenses detected."
            )

    else:

        st.info(
            "Add at least 5 expenses for anomaly detection."
        )