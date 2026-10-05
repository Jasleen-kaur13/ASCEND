"""
ai_engine.py - the AI brain of ASCEND.
Expects a DataFrame with columns: id, category, amount, date
"""
import json
import os

import numpy as np
import pandas as pd


def prepare(df: pd.DataFrame) -> pd.DataFrame:
    d = df.copy()
    d["amount"] = pd.to_numeric(d["amount"], errors="coerce")
    d["date"] = pd.to_datetime(d["date"], dayfirst=True, errors="coerce")
    d = d.dropna(subset=["amount", "date"])
    d["month"] = d["date"].dt.to_period("M").astype(str)
    return d


def monthly_totals(df):
    d = prepare(df)
    return d.groupby("month")["amount"].sum().round(2).to_dict()


def spending_by_category(df, month=None):
    d = prepare(df)
    if month:
        d = d[d["month"] == month]
    return d.groupby("category")["amount"].sum().sort_values(ascending=False).round(2).to_dict()


def compare_months(df, month_a, month_b):
    a, b = spending_by_category(df, month_a), spending_by_category(df, month_b)
    cats = set(a) | set(b)
    return {
        "month_a": month_a,
        "month_b": month_b,
        "month_a_total": round(sum(a.values()), 2),
        "month_b_total": round(sum(b.values()), 2),
        "change_by_category": {c: round(b.get(c, 0) - a.get(c, 0), 2) for c in cats},
    }


def forecast_next_month(df):
    totals = monthly_totals(df)
    if not totals:
        return {"error": "no data"}
    months = sorted(totals)
    y = np.array([totals[m] for m in months], dtype=float)
    if len(y) >= 3:
        slope, intercept = np.polyfit(range(len(y)), y, 1)
        pred, method = slope * len(y) + intercept, "linear trend"
    else:
        pred, method = y.mean(), "average of past months"
    nxt = (pd.Period(months[-1]) + 1).strftime("%Y-%m")
    return {"next_month": nxt, "forecast": round(max(float(pred), 0), 2),
            "method": method, "history": totals}


def detect_anomalies(df, factor=1.5, max_rows=10):
    """Small data: simple rule vs overall median.
    Large data: compare each expense to its OWN category's normal (robust z-score)."""
    d = prepare(df)
    if len(d) < 4:
        return []
    if len(d) < 50:
        med = d["amount"].median()
        flagged = d[d["amount"] > factor * med].copy()
        flagged["_score"] = flagged["amount"] / med
        flagged["_ref"] = med
        flagged["_label"] = "expense"
    else:
        parts = []
        for cat, g in d.groupby("category"):
            if len(g) < 8:
                continue
            med = g["amount"].median()
            scale = 1.4826 * (g["amount"] - med).abs().median()
            if scale == 0:
                scale = g["amount"].std()
            if not scale or scale != scale:
                continue
            z = (g["amount"] - med) / scale
            hit = g[(z > 3.5) & (g["amount"] > 1.5 * med)].copy()
            hit["_score"] = z[hit.index]
            hit["_ref"] = med
            hit["_label"] = f"{cat} expense"
            parts.append(hit)
        if not parts:
            return []
        flagged = pd.concat(parts)
    flagged = flagged.sort_values("_score", ascending=False).head(max_rows)
    return [
        {"id": int(r["id"]) if "id" in d else None, "category": r["category"],
         "amount": float(r["amount"]), "date": r["date"].strftime("%d-%m-%Y"),
         "why": f"{r['amount'] / r['_ref']:.1f}x the typical {r['_label']}"}
        for _, r in flagged.iterrows()
    ]



def budget_status(df, monthly_budget, monthly_income):
    totals = monthly_totals(df)
    if not totals:
        return {"error": "no data"}
    latest = sorted(totals)[-1]
    spent = totals[latest]
    return {
        "month": latest, "spent": spent, "budget": monthly_budget,
        "remaining": round(monthly_budget - spent, 2),
        "over_budget": spent > monthly_budget,
        "savings_this_month": round(monthly_income - spent, 2),
        "savings_rate_pct": round((monthly_income - spent) / monthly_income * 100, 1)
        if monthly_income else None,
    }


def rule_based_insights(df, monthly_budget, monthly_income):
    notes = []
    if prepare(df).empty:
        return ["Add some expenses to see insights."]
    cats = spending_by_category(df)
    top, top_amt = next(iter(cats.items()))
    share = top_amt / sum(cats.values()) * 100
    notes.append(f"{top} is your biggest category: Rs {top_amt:,.0f} ({share:.0f}% of spending).")
    bs = budget_status(df, monthly_budget, monthly_income)
    if bs["over_budget"]:
        notes.append(f"{bs['month']}: over budget by Rs {-bs['remaining']:,.0f}.")
    else:
        notes.append(f"{bs['month']}: Rs {bs['remaining']:,.0f} left in budget.")
    f = forecast_next_month(df)
    notes.append(f"Forecast for {f['next_month']}: about Rs {f['forecast']:,.0f} ({f['method']}).")
    for a in detect_anomalies(df):
        notes.append(f"Unusual: {a['category']} Rs {a['amount']:,.0f} on {a['date']} ({a['why']}).")
    return notes


# ---------------- LLM access: the ONLY place that talks to a model ----------------
def llm_available():
    return bool(os.getenv("LLM_API_KEY"))


def llm_chat(messages, tools=None, tool_choice="auto"):
    from openai import OpenAI

    client = OpenAI(
        base_url=os.getenv("LLM_BASE_URL") or None,
        api_key=os.getenv("LLM_API_KEY"),
    )
    kwargs = dict(model=os.getenv("LLM_MODEL", "gpt-4o-mini"),
                  messages=messages, temperature=0.2)
    if tools:
        kwargs["tools"] = tools
        kwargs["tool_choice"] = tool_choice
    return client.chat.completions.create(**kwargs)


# ---------------- Agent with tools + human-in-the-loop ----------------
SYSTEM_PROMPT = (
    "You are ASCEND, a careful financial assistant for small businesses in India. "
    "Currency is INR. Use the tools to get numbers; never guess or invent figures. "
    "Be efficient: make at most 3 tool calls, then answer. Do not repeat a tool call. "
    "RULE: whenever you recommend a spending limit or cap for a category, or the user "
    "asks to suggest, set, cap or propose one, you MUST call propose_budget_change "
    "with the category, the number and a short reason. Never state a limit in text "
    "without calling it. It only creates a proposal the user must approve. "
    "Typical flow: spending_by_category once, then propose_budget_change, then explain "
    "in 3-5 short lines. Months are formatted YYYY-MM.  "
    "Never ask the user for data; you can fetch everything with your tools. "
)

TOOLS = [
    {"type": "function", "function": {
        "name": "spending_by_category",
        "description": "Total spend per category across ALL months.",
        "parameters": {"type": "object", "properties": {}}}},
    {"type": "function", "function": {
        "name": "spending_in_month",
        "description": "Total spend per category for ONE month, given as YYYY-MM.",
        "parameters": {"type": "object", "properties": {
            "month": {"type": "string", "description": "YYYY-MM, e.g. 2026-07"}},
            "required": ["month"]}}},
    {"type": "function", "function": {
        "name": "monthly_totals",
        "description": "Total spend for every month.",
        "parameters": {"type": "object", "properties": {}}}},
    {"type": "function", "function": {
        "name": "compare_months",
        "description": "Compare spending between two months (YYYY-MM), per category.",
        "parameters": {"type": "object", "properties": {
            "month_a": {"type": "string"}, "month_b": {"type": "string"}},
            "required": ["month_a", "month_b"]}}},
    {"type": "function", "function": {
        "name": "forecast_next_month",
        "description": "Forecast total spending for next month.",
        "parameters": {"type": "object", "properties": {}}}},
    {"type": "function", "function": {
        "name": "detect_anomalies",
        "description": "List unusually large expenses.",
        "parameters": {"type": "object", "properties": {}}}},
    {"type": "function", "function": {
        "name": "budget_status",
        "description": "Latest month's spend vs budget and savings rate.",
        "parameters": {"type": "object", "properties": {}}}},
    {"type": "function", "function": {
        "name": "propose_budget_change",
        "description": "Propose a monthly limit for a category. Needs user approval.",
        "parameters": {"type": "object", "properties": {
            "category": {"type": "string"},
            "new_limit": {"type": "number"},
            "reason": {"type": "string"}},
            "required": ["category", "new_limit", "reason"]}}},
]


def _tool_runner(df, budget, income, proposals):
    def run(name, args):
        if name == "spending_by_category":
            return spending_by_category(df)
        if name == "spending_in_month":
            return spending_by_category(df, args.get("month") or None)
        if name == "monthly_totals":
            return monthly_totals(df)
        if name == "compare_months":
            return compare_months(df, args["month_a"], args["month_b"])
        if name == "forecast_next_month":
            return forecast_next_month(df)
        if name == "detect_anomalies":
            return detect_anomalies(df)
        if name == "budget_status":
            return budget_status(df, budget, income)
        if name == "propose_budget_change":
            proposals.append({"category": args["category"],
                              "new_limit": float(args["new_limit"]),
                              "reason": args["reason"], "status": "pending"})
            return {"result": "Proposal created. Waiting for user approval."}
        return {"error": f"unknown tool {name}"}
    return run


def run_agent(question, df, monthly_budget, monthly_income, proposals, history=None):
    """Returns (answer_text, tool_trace). `proposals` is mutated in place."""
    run = _tool_runner(df, monthly_budget, monthly_income, proposals)
    msgs = [{"role": "system", "content": SYSTEM_PROMPT}] + (history or []) \
        + [{"role": "user", "content": question}]
    trace = []
    for step in range(5):
        choice = "required" if step == 0 else "auto"
        msg = llm_chat(msgs, TOOLS, choice).choices[0].message
        if not msg.tool_calls:
            return msg.content, trace
        msgs.append(msg)
        for tc in msg.tool_calls:
            args = json.loads(tc.function.arguments or "{}")
            trace.append((tc.function.name, args))
            result = run(tc.function.name, args)
            msgs.append({"role": "tool", "tool_call_id": tc.id,
                         "content": json.dumps(result, default=str)})
    # safety net: out of steps, force a final answer
    msgs.append({"role": "user", "content":
                 "Stop calling tools. Give your final answer now using the data above."})
    final = llm_chat(msgs).choices[0].message.content
    return final, trace