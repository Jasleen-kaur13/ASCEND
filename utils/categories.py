import streamlit as st


def merged_categories(defaults, df):
    in_data = []
    if df is not None and len(df) > 0 and "category" in df.columns:
        in_data = sorted(set(df["category"].dropna().astype(str)))

    # Organisation's own upload: show only its categories, not yours
    if st.session_state.get("db_name"):
        return in_data or list(defaults)

    # Demo data: your defaults plus anything extra added later
    return list(defaults) + [c for c in in_data if c not in defaults]