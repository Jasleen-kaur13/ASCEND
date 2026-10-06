import streamlit as st

def show_overview(filtered_df, budget):
    
    # Hero Section
    st.markdown("""
    <div class="hero">
        <h1>💼 ASCEND Financial Intelligence</h1>
        <p>
            Monitor Performance • Analyze Spending • Predict Trends
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # ==========================
    # Expense Statistics
    # ==========================
    st.divider()

    total = filtered_df["amount"].sum()

    if len(filtered_df) > 0:

        average = filtered_df["amount"].mean()
        highest = filtered_df["amount"].max()
        lowest = filtered_df["amount"].min()

    else:

        average = 0
        highest = 0
        lowest = 0
        
    # Metric Cards
    st.markdown("## 📊 Overview")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h3>💸</h3>
            <h4>Total Spending</h4>
            <h2>₹{total:,.0f}</h2>
            <p style="color:#10B981;font-size:13px;">
            Monthly Summary
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <h3>📈</h3>
            <h4>Average Expense</h4>
            <h2>₹{average:,.0f}</h2>
            <p style="color:#2563EB;font-size:13px;">
            Per Transaction
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <h3>🔥</h3>
            <h4>Highest Expense</h4>
            <h2>₹{highest:,.0f}</h2>
            <p style="color:#EF4444;font-size:13px;">
            Largest Expense
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <h3>💰</h3>
            <h4>Lowest Expense</h4>
            <h2>₹{lowest:,.0f}</h2>
            <p style="color:#F59E0B;font-size:13px;">
            Smallest Expense
            </p>
        </div>
        """, unsafe_allow_html=True)
        
    # ==========================
    # Monthly Income
    # ==========================

    st.divider()

    if total > budget:

        st.error(
            f"⚠ Budget Exceeded by ₹{total-budget}"
        )

    else:

        st.success(
            f"₹{budget-total} Budget Remaining"
        )
    return total, average, highest, lowest