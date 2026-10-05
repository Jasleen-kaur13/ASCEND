import os
import tempfile
import uuid

import pandas as pd
import streamlit as st

from database import db

TEMPLATE = "date,category,amount\n02-04-2026,Marketing,15000\n10-04-2026,Salaries,42000\n"


def _guess(cols, keys):
    for c in cols:
        if any(k in str(c).lower() for k in keys):
            return c
    return None


def _clean(raw, dcol, ccol, acol, negative):
    d = pd.DataFrame(index=raw.index)
    d["date"] = pd.to_datetime(raw[dcol], dayfirst=True, errors="coerce")
    d["amount"] = pd.to_numeric(
        raw[acol].astype(str).str.replace(r"[^\d.\-]", "", regex=True),
        errors="coerce")
    if ccol:
        cat = raw[ccol].fillna("").astype(str).str.strip()
        d["category"] = cat.mask(cat.str.lower().isin(["", "nan", "none"]),
                                 "Uncategorised")
    else:
        d["category"] = "Uncategorised"
    d = d.dropna(subset=["date", "amount"])
    d = d[d["amount"] < 0] if negative else d[d["amount"] > 0]
    d["amount"] = d["amount"].abs()
    d["date"] = d["date"].dt.strftime("%d-%m-%Y")
    return d.head(5000)[["category", "amount", "date"]]


def _reset():
    path = st.session_state.pop("db_name", None)
    st.session_state.pop("upload_summary", None)
    if path and os.path.exists(path):
        try:
            os.remove(path)
        except OSError:
            pass


def render_upload_box():
    with st.sidebar.expander("🏢 Use your organisation's data"):
        if st.session_state.get("db_name"):
            st.success("Using your uploaded data")
            s = st.session_state.get("upload_summary")
            if s:
                st.caption(f"Rows read: {s['read']} | imported: {s['imported']} | "
                           f"skipped: {s['skipped']} (invalid or over 5,000)")
                st.caption(f"Possible duplicates: {s['duplicates']}")
                st.caption(f"Period: {s['start']} to {s['end']}")
                st.caption(f"Total spend: Rs {s['total']:,.0f}")
            if st.button("Back to demo data", key="reset_demo"):
                _reset()
                st.rerun()
            return

        st.caption("Upload a CSV or Excel file of expenses. "
                   "It stays in your session only.")
        st.download_button("Download template", TEMPLATE,
                           "ascend_template.csv", key="tpl")
        f = st.file_uploader("CSV or Excel", type=["csv", "xlsx"], key="org_file")
        if f is None:
            return
        try:
            raw = (pd.read_csv(f) if f.name.lower().endswith(".csv")
                   else pd.read_excel(f))
        except Exception as e:
            st.error(f"Could not read file: {e}")
            return

        cols = list(raw.columns)
        g_date = _guess(cols, ["date", "time"])
        g_amt = _guess(cols, ["amount", "debit", "value", "cost"])
        g_cat = _guess(cols, ["categ", "type", "head", "dept"])

        dcol = st.selectbox("Date column", cols,
                            index=cols.index(g_date) if g_date else 0)
        acol = st.selectbox("Amount column", cols,
                            index=cols.index(g_amt) if g_amt else 0)
        cat_opts = ["(none)"] + cols
        ccol = st.selectbox("Category column", cat_opts,
                            index=cat_opts.index(g_cat) if g_cat else 0)
        negative = st.checkbox("Expenses are negative numbers (bank statement)")

        if st.button("Import and analyse", key="do_import"):
            clean = _clean(raw, dcol, None if ccol == "(none)" else ccol,
                           acol, negative)
            if clean.empty:
                st.error("No valid rows found. Check the column choices.")
                return
            dates = pd.to_datetime(clean["date"], format="%d-%m-%Y")
            st.session_state["upload_summary"] = {
                "read": len(raw),
                "imported": len(clean),
                "skipped": len(raw) - len(clean),
                "duplicates": int(clean.duplicated().sum()),
                "start": dates.min().strftime("%d-%m-%Y"),
                "end": dates.max().strftime("%d-%m-%Y"),
                "total": float(clean["amount"].sum()),
            }
            path = os.path.join(tempfile.gettempdir(),
                                f"ascend_{uuid.uuid4().hex}.db")
            st.session_state["db_name"] = path
            db.create_table()
            conn = db.get_connection()
            conn.cursor().executemany(
                "INSERT INTO expenses(category, amount, date) VALUES (?, ?, ?)",
                list(clean.itertuples(index=False, name=None)))
            conn.commit()
            conn.close()
            st.rerun()