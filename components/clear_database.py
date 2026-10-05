import streamlit as st
from database.db import clear_database_db

def clear_database(expenses):

    st.sidebar.divider()
    st.sidebar.markdown("## 🗄 Database")

    if st.sidebar.button("🗑 Clear All Expenses"):

        st.write("BUTTON CLICKED")          # On the page
        print("BUTTON CLICKED")             # In terminal

        clear_database_db()

        st.write("DATABASE CLEARED")        # On the page
        print("DATABASE CLEARED")           # In terminal

        st.sidebar.success("All expenses deleted successfully!")

        st.rerun()