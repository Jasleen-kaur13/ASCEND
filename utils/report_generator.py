def generate_category_report(df):

    return (
        df.groupby("category")["amount"]
        .sum()
    )