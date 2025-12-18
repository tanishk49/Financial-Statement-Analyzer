from flask import Flask, render_template, request, redirect, url_for, send_file
import os

# ------------------------
# Imports
# ------------------------

# Preprocessing
from analysis.preprocess import load_financial_data, clean_financial_data

# Metrics
from analysis.metrics import (
    compute_financial_metrics,
    compute_latest_metrics
)

# Visualizations
from analysis.visualizations import generate_trend_plots

# PDF Report
from reports.report_generator import generate_pdf_report


# ------------------------
# App Initialization
# ------------------------

app = Flask(__name__)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "uploads")
PLOT_FOLDER = os.path.join(BASE_DIR, "static", "plots")
REPORT_FOLDER = os.path.join(BASE_DIR, "static", "reports")

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


# ------------------------
# Helper: Financial Interpretation
# ------------------------

def generate_interpretation(summary_metrics: dict) -> dict:
    insights = {}

    roe = summary_metrics.get("ROE (%)")
    cr = summary_metrics.get("Current Ratio")
    de = summary_metrics.get("Debt-Equity")

    # Profitability
    if roe is not None:
        if roe >= 20:
            insights["profitability"] = (
                "The company demonstrates strong profitability with healthy returns on equity."
            )
        else:
            insights["profitability"] = (
                "Profitability remains moderate, indicating scope for operational efficiency improvements."
            )

    # Liquidity
    if cr is not None:
        if cr >= 1.5:
            insights["liquidity"] = (
                "Liquidity position is comfortable, suggesting the firm can meet short-term obligations effectively."
            )
        else:
            insights["liquidity"] = (
                "Liquidity appears tight, which may pose short-term solvency risks."
            )

    # Leverage
    if de is not None:
        if de <= 1.5:
            insights["leverage"] = (
                "Leverage is well-controlled, indicating a balanced capital structure."
            )
        else:
            insights["leverage"] = (
                "Higher leverage levels indicate increased financial risk."
            )

    return insights


# ------------------------
# Routes
# ------------------------

@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        file = request.files.get("file")

        if not file or file.filename == "":
            return redirect(request.url)

        file_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(file_path)

        # ------------------------
        # Data Pipeline
        # ------------------------
        df_raw = load_financial_data(file_path)
        df_clean = clean_financial_data(df_raw)

        trend_df = compute_financial_metrics(df_clean)
        summary_metrics = compute_latest_metrics(df_clean)

        # ------------------------
        # Save Computed Metrics (CSV Export)
        # ------------------------
        metrics_csv_path = os.path.join(
            REPORT_FOLDER, "computed_financial_metrics.csv"
        )
        trend_df.round(2).to_csv(metrics_csv_path, index=False)

        # ------------------------
        # Generate Charts
        # ------------------------
        plot_paths = generate_trend_plots(
            trend_df,
            PLOT_FOLDER
        )

        # ------------------------
        # Generate PDF Report
        # ------------------------
        pdf_path = os.path.join(
            REPORT_FOLDER, "financial_analysis_report.pdf"
        )

        generate_pdf_report(
            output_path=pdf_path,
            summary_metrics=summary_metrics,
            plot_paths=plot_paths
        )

        # ------------------------
        # Generate Financial Interpretation
        # ------------------------
        interpretation = generate_interpretation(summary_metrics)

        return render_template(
            "metrics.html",
            summary_metrics=summary_metrics,
            interpretation=interpretation,
            tables=[
                trend_df.round(2).to_html(
                    classes="table table-striped",
                    index=False
                )
            ],
            plots=[os.path.basename(p) for p in plot_paths.values()],
            pdf_available=True
        )

    return render_template("upload.html")


@app.route("/download-report")
def download_report():
    pdf_path = os.path.join(
        REPORT_FOLDER, "financial_analysis_report.pdf"
    )
    return send_file(pdf_path, as_attachment=True)


@app.route("/download-metrics")
def download_metrics():
    csv_path = os.path.join(
        REPORT_FOLDER, "computed_financial_metrics.csv"
    )
    return send_file(csv_path, as_attachment=True)


# ------------------------
# App Entry Point
# ------------------------

if __name__ == "__main__":
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    os.makedirs(PLOT_FOLDER, exist_ok=True)
    os.makedirs(REPORT_FOLDER, exist_ok=True)

    app.run(debug=True)
