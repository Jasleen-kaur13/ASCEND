import streamlit as st
from datetime import datetime

def show_header():

    today = datetime.now().strftime("%d %B %Y")

    st.markdown(
        f"""
            # 💰 Expense Analytics Dashboard

            ### AI Powered Personal Finance Assistant

            📅 **{today}** &nbsp;&nbsp;&nbsp; 👤 **User**
        """,
        unsafe_allow_html=False,
    )