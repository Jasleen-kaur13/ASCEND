import streamlit as st

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image
)

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch

def show_pdf_report(
    total,
    income,
    current_savings,
    budget,
    score,
    report,
    prediction,
    months,
    risk_level,
    highest_category,
    recommended_budget
):

    st.divider()
    st.subheader("📄 Export PDF Report")

    if st.button("Generate PDF Report"):

        doc = SimpleDocTemplate("Expense_Report.pdf")
        styles = getSampleStyleSheet()
        story = []

        # -------------------------
        # Title
        # -------------------------

        story.append(
            Paragraph(
                "<b><font size=20>Expense Analytics Report</font></b>",
                styles["Title"]
            )
        )
        story.append(Spacer(1,20))

        data = [
            ["Item","Value"],
            ["Total Spending", f"₹{total:.0f}"],
            ["Income", f"₹{income:.0f}"],
            ["Savings", f"₹{current_savings:.0f}"],
            ["Budget", f"₹{budget:.0f}"],
            ["Health Score", f"{score}/100"]
        ]

        table = Table(data)

        table.setStyle(TableStyle([
            ("BACKGROUND",(0,0),(-1,0),colors.blue),
            ("TEXTCOLOR",(0,0),(-1,0),colors.white),
            ("GRID",(0,0),(-1,-1),1,colors.black),
            ("BACKGROUND",(0,1),(-1,-1),colors.beige),
            ("ALIGN",(0,0),(-1,-1),"CENTER"),
        ]))

        story.append(table)
        story.append(Spacer(1,20))
    
        story.append(
            Paragraph("<b>Category Summary</b>", styles["Heading2"])
        )

        category_data = [["Category","Amount"]]

        for category, amount in report.items():
            category_data.append([category, f"₹{amount:.0f}"])

        category_table = Table(category_data)

        category_table.setStyle(TableStyle([
            ("BACKGROUND",(0,0),(-1,0),colors.green),
            ("TEXTCOLOR",(0,0),(-1,0),colors.white),
            ("GRID",(0,0),(-1,-1),1,colors.black),
            ("ALIGN",(0,0),(-1,-1),"CENTER"),
        ]))

        story.append(category_table)
        story.append(Spacer(1,20))

        story.append(
            Paragraph("<b>Expense Distribution</b>", styles["Heading2"])
        )

        story.append(
            Image(
                "pie_chart.png",
                width=4*inch,
                height=4*inch
            )
        )

        story.append(Spacer(1,20))
    
        story.append(
            Paragraph("<b>Category Comparison</b>", styles["Heading2"])
        )

        story.append(
            Image(
                "bar_chart.png",
                width=5.5*inch,
                height=3.5*inch
            )
        )

        story.append(Spacer(1,20))
    
        if len(months) >= 2:

            story.append(
                Paragraph("<b>AI Prediction</b>", styles["Heading2"])
            )

            story.append(
                Paragraph(
                    f"Predicted Next Month Spending: ₹{prediction:.2f}",
                    styles["Normal"]
                )
            )

            story.append(
                Image(
                    "prediction_chart.png",
                    width=5.5*inch,
                    height=3.5*inch
                )   
            )

            story.append(Spacer(1,20))
        
        story.append(
            Paragraph("<b>Financial Summary</b>", styles["Heading2"])
        )

        story.append(
            Paragraph(
                f"""
                Total Spending: ₹{total:.0f}<br/>
                Savings: ₹{current_savings:.0f}<br/>
                Risk Level: {risk_level}<br/>
                Highest Spending Category: {highest_category}<br/>
                Recommended Budget: ₹{recommended_budget:.0f}
                """,
                styles["BodyText"]
            )
        )

        story.append(Spacer(1,20))

        doc.build(story)

        with open("Expense_Report.pdf","rb") as pdf:
            st.download_button(
                "Download PDF",
                pdf,
                "Expense_Report.pdf",
                "application/pdf"
            )