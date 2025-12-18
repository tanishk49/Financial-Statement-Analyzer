from flask import Flask, render_template, request, redirect, url_for, send_file
import os

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


app = Flask(__name__)

# ------------------------
# Configuration
# ------------------------
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "uploads")
PLOT_FOLDER = os.path.join(BASE_DIR, "static", "plots")
REPORT_FOLDER = os.path.join(BASE_DIR, "static", "reports")

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


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
        # Generate Charts
        # ------------------------
        plot_paths = generate_trend_plots(
            trend_df,
            PLOT_FOLDER
        )

        # ------------------------
        # Generate PDF Report
        # ------------------------
        pdf_path = os.path.join(REPORT_FOLDER, "financial_analysis_report.pdf")

        generate_pdf_report(
            output_path=pdf_path,
            summary_metrics=summary_metrics,
            plot_paths=plot_paths
        )

        return render_template(
            "metrics.html",
            summary_metrics=summary_metrics,
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


# ------------------------
# App Entry Point
# ------------------------
if __name__ == "__main__":
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    os.makedirs(PLOT_FOLDER, exist_ok=True)
    os.makedirs(REPORT_FOLDER, exist_ok=True)

    app.run(debug=True)
