import pandas as pd
from database.db import load_expenses as load_db


def load_expenses():

    df = load_db()

    expenses = df.to_dict("records")

    return expenses, df