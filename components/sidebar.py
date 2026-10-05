import streamlit as st


def _month_sort_key(m):
    """Sort 'MM-YYYY' labels by year first, then month."""
    try:
        mm, yyyy = m.split("-")
        return (int(yyyy), int(mm))
    except ValueError:
        return (0, 0)


def sidebar_filters(df, expenses):

    st.sidebar.markdown("""
    <div style="
    text-align:center;
    padding:15px;
    margin-bottom:20px;
    background:white;
    border-radius:15px;
    box-shadow:0 4px 10px rgba(0,0,0,.08);
    ">
    <h2>💰</h2>
    <h3>Expense Tracker</h3>
    <p>AI Powered Analytics</p>
    </div>
    """, unsafe_allow_html=True)

    st.sidebar.markdown("## ⚙️ Dashboard Controls")

    available_months = []

    for expense in expenses:

        if "date" not in expense:
            continue

        if not isinstance(expense["date"], str):
            continue

        parts = expense["date"].split("-")

        if len(parts) != 3:
            continue

        month_year = parts[1] + "-" + parts[2]

        if month_year not in available_months:
            available_months.append(month_year)

    selected_month = st.sidebar.selectbox(
        "Select Month",
        ["All"] + sorted(available_months, key=_month_sort_key)
    )

    filtered_df = df.copy()

    if selected_month != "All":

        filtered_df = df[
            df["date"].apply(
                lambda x:
                "-".join(str(x).split("-")[1:])
                if len(str(x).split("-")) == 3
                else ""
            ) == selected_month
        ]

    budget = st.sidebar.number_input(
        "Monthly Budget (₹)",
        min_value=0,
        value=9000,
        step=1000
    )

    income = st.sidebar.number_input(
        "Monthly Income (₹)",
        min_value=0,
        value=50000,
        step=1000
    )

    return filtered_df, budget, income