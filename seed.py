from database.db import create_table, add_expense, load_expenses

ROWS = [
    ("Rent", 15000, "02-04-2026"), ("Food", 2200, "10-04-2026"), ("Travel", 1500, "18-04-2026"),
    ("Rent", 15000, "02-05-2026"), ("Utilities", 2100, "12-05-2026"), ("Shopping", 1800, "20-05-2026"),
    ("Rent", 15000, "02-06-2026"), ("Food", 2600, "14-06-2026"), ("Utilities", 2300, "22-06-2026"),
    ("Rent", 15000, "02-07-2026"), ("Food", 2400, "11-07-2026"), ("Travel", 3200, "19-07-2026"),
    ("Rent", 15000, "02-08-2026"), ("Shopping", 7500, "09-08-2026"), ("Utilities", 2400, "17-08-2026"),
]

create_table()
existing = {(r.category, float(r.amount), r.date) for r in load_expenses().itertuples()}

added = 0
for cat, amt, date in ROWS:
    if (cat, float(amt), date) not in existing:
        add_expense(cat, amt, date)
        added += 1

print(f"Added {added} expenses")