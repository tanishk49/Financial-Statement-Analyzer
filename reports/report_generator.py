import os
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image,
    Table,
    TableStyle
)
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors


def generate_pdf_report(
    output_path: str,
    summary_metrics: dict,
    plot_paths: dict
):
    """
    Generate a PDF financial analysis report
    """

    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()
    elements = []

    # ------------------------
    # Title
    # ------------------------
    elements.append(
        Paragraph(
            "<b>Financial Statement Analysis Report</b>",
            styles["Title"]
        )
    )
    elements.append(Spacer(1, 20))

    # ------------------------
    # Summary Metrics Table
    # ------------------------
    elements.append(
        Paragraph(
            "<b>Key Financial Metrics (Latest Year)</b>",
            styles["Heading2"]
        )
    )
    elements.append(Spacer(1, 10))

    table_data = [["Metric", "Value"]]
    for key, value in summary_metrics.items():
        table_data.append([key, str(value)])

    table = Table(table_data, colWidths=[200, 200])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ("ALIGN", (1, 1), (-1, -1), "CENTER"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold")
    ]))

    elements.append(table)
    elements.append(Spacer(1, 20))

    # ------------------------
    # Trend Charts
    # ------------------------
    elements.append(
        Paragraph(
            "<b>Multi-Year Financial Trends</b>",
            styles["Heading2"]
        )
    )
    elements.append(Spacer(1, 10))

    for metric, path in plot_paths.items():
        if os.path.exists(path):
            img = Image(path, width=400, height=250)
            elements.append(img)
            elements.append(Spacer(1, 15))

    # Build PDF
    doc.build(elements)
