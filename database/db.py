import sqlite3
import os
import pandas as pd

import streamlit as st

DB_NAME = "expenses.db"


def get_connection():
    db_path = st.session_state.get("db_name") or os.path.abspath(DB_NAME)
    return sqlite3.connect(db_path)


def create_table():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT,
            amount REAL,
            date TEXT
        )
    """)

    conn.commit()
    conn.close()


def add_expense(category, amount, date):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO expenses(category, amount, date)
        VALUES (?, ?, ?)
        """,
        (category, amount, date)
    )

    conn.commit()
    conn.close()


def load_expenses():

    conn = get_connection()

    df = pd.read_sql(
        "SELECT * FROM expenses",
        conn
    )

    conn.close()

    return df


def update_expense(expense_id, category, amount, date):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE expenses
        SET category=?,
            amount=?,
            date=?
        WHERE id=?
        """,
        (
            category,
            amount,
            date,
            expense_id
        )
    )

    print("Rows Updated:", cursor.rowcount)

    conn.commit()
    conn.close()


def delete_expense_db(expense_id):

    conn = get_connection()
    cursor = conn.cursor()

    print("Deleting ID:", expense_id)

    cursor.execute(
        """
        DELETE FROM expenses
        WHERE id=?
        """,
        (int(expense_id),)
    )

    print("Rows Deleted:", cursor.rowcount)

    conn.commit()
    conn.close()


def clear_database_db():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM expenses")

    print("Rows Deleted:", cursor.rowcount)

    conn.commit()
    conn.close()

    print("Database Cleared Successfully")