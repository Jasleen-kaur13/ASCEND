"""
ai_tab.py - drop-in 'AI Insights' tab for ASCEND.
"""
import os

import pandas as pd
import streamlit as st

import ai_engine as ai


def _load_secrets():
    for k in ("LLM_API_KEY", "LLM_BASE_URL", "LLM_MODEL"):
        if not os.getenv(k):
            try:
                if k in st.secrets:
                    os.environ[k] = str(st.secrets[k])
            except Exception:
                pass


def render_ai_insights(df, monthly_budget, monthly_income):
    _load_secrets()
    st.header("AI Insights")

    if df is None or len(df) == 0 or ai.prepare(df).empty:
        st.info("Add some expenses first to unlock AI insights.")
        return

    st.session_state.setdefault("proposals", [])
    st.session_state.setdefault("category_budgets", {})
    st.session_state.setdefault("ai_chat", [])

    # ---------------- Forecast ----------------
    st.subheader("Next-month forecast")
    f = ai.forecast_next_month(df)
    c1, c2 = st.columns(2)
    c1.metric(f"Forecast for {f['next_month']}", f"Rs {f['forecast']:,.0f}")
    c2.caption(f"Method: {f['method']}")
    hist = pd.DataFrame({"month": list(f["history"]), "spend": list(f["history"].values())})
    hist.loc[len(hist)] = [f["next_month"] + " (forecast)", f["forecast"]]
    st.bar_chart(hist.set_index("month"))

    # ---------------- Anomalies ----------------
    st.subheader("Unusual expenses")
    anomalies = ai.detect_anomalies(df)
    if anomalies:
        st.dataframe(pd.DataFrame(anomalies), use_container_width=True, hide_index=True)
    else:
        st.success("No unusual expenses found.")

    # ---------------- Auto insights ----------------
    st.subheader("Quick insights")
    for note in ai.rule_based_insights(df, monthly_budget, monthly_income):
        st.write("- " + note)

    # ---------------- Ask the AI ----------------
    st.subheader("Ask ASCEND")
    if not ai.llm_available():
        st.warning("AI chat is off: set LLM_API_KEY. "
                   "Forecast, anomalies and insights above work without it.")
    else:
        for m in st.session_state["ai_chat"]:
            with st.chat_message(m["role"]):
                st.write(m["content"])

        q = st.chat_input("e.g. Why was my spending high in July? How can I save more?")
        if q:
            with st.chat_message("user"):
                st.write(q)
            with st.chat_message("assistant"):
                with st.spinner("Analysing your data..."):
                    try:
                        ans, trace = ai.run_agent(
                            q, df, monthly_budget, monthly_income,
                            st.session_state["proposals"],
                            history=st.session_state["ai_chat"][-6:])
                    except Exception as e:
                        ans, trace = f"AI error: {e}", []
                st.write(ans)
                if trace:
                    st.caption("Tools used: " + ", ".join(t[0] for t in trace))
            st.session_state["ai_chat"] += [{"role": "user", "content": q},
                                            {"role": "assistant", "content": ans}]
            if any(p["status"] == "pending" for p in st.session_state["proposals"]):
                st.rerun()

    # ---------------- Human-in-the-loop ----------------
    pending = [p for p in st.session_state["proposals"] if p["status"] == "pending"]
    if pending:
        st.subheader("Suggestions waiting for your approval")
        for i, p in enumerate(st.session_state["proposals"]):
            if p["status"] != "pending":
                continue
            with st.container(border=True):
                st.write(f"**{p['category']}**: set monthly limit to Rs {p['new_limit']:,.0f}")
                st.caption(p["reason"])
                a, b = st.columns(2)
                if a.button("Approve", key=f"ok_{i}"):
                    p["status"] = "approved"
                    st.session_state["category_budgets"][p["category"]] = p["new_limit"]
                    st.rerun()
                if b.button("Reject", key=f"no_{i}"):
                    p["status"] = "rejected"
                    st.rerun()

        if st.session_state["category_budgets"]:
            st.subheader("Approved category limits")
        limits = st.session_state["category_budgets"]
        st.table(pd.DataFrame(
            [(c, int(v)) for c, v in limits.items()],
            columns=["Category", "Monthly limit (Rs)"]
        ))

        d = ai.prepare(df)
        latest = d["month"].max()
        spent = d[d["month"] == latest].groupby("category")["amount"].sum()
        for cat, lim in limits.items():
            s = float(spent.get(cat, 0))
            if s > lim:
                st.error(f"{cat}: Rs {s:,.0f} spent in {latest} vs limit Rs {lim:,.0f}, "
                         f"over by Rs {s - lim:,.0f}")
            else:
                st.success(f"{cat}: Rs {s:,.0f} of Rs {lim:,.0f} used in {latest}")