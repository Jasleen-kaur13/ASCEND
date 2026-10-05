from pathlib import Path
import streamlit as st

BASE_DIR = Path(__file__).parent

def setup_page():
    st.set_page_config(
        page_title="ASCEND",
        page_icon="📈",
        layout="wide"
    )

    st.title("ASCEND")
    st.subheader("Built to Rise. Built to Lead.")

    st.markdown("""
    ### AI Financial Intelligence Platform for Small Businesses

    ASCEND helps businesses track expenses, analyze spending patterns,
    predict future costs, optimize budgets, and make smarter financial
    decisions using AI-powered insights.

    **Powered by HK Sekhon Holdings**
    """)

    css_file = BASE_DIR / "style.css"

    with open(css_file, "r", encoding="utf-8") as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )