import streamlit as st

def show_goal_tracker(total, income):

    # ==========================
    # Goal-Based Savings Tracker
    # ==========================
    st.divider()
    st.subheader("🎯 Savings Goal Tracker")

    goal = st.number_input(
        "Enter Your Savings Goal (₹)",
        min_value=1000,
        value=100000,
        step=1000
    )

    current_savings = max(income - total, 0)

    progress = current_savings / goal

    st.progress(min(progress, 1.0))

    col1, col2 = st.columns(2)

    col1.metric(
        "Current Savings",
        f"₹{current_savings:.0f}"
    )

    col2.metric(
        "Goal",
        f"₹{goal:.0f}"
    )

    remaining = goal - current_savings

    if remaining <= 0:
        st.success("🎉 Congratulations! You achieved your savings goal.")
    else:
        st.info(f"₹{remaining:.0f} more needed to reach your goal.")

    return current_savings