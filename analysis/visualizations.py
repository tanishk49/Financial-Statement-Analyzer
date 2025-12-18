import matplotlib
matplotlib.use("Agg")

import os
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


def generate_trend_plots(
    df: pd.DataFrame,
    output_dir: str
) -> dict:
    """
    Generate multi-year trend plots for financial metrics

    Returns:
        dict: metric_name -> saved image path
    """

    os.makedirs(output_dir, exist_ok=True)

    sns.set(style="whitegrid")

    plots = {}

    metrics_config = {
        "roe": "Return on Equity (%)",
        "roa": "Return on Assets (%)",
        "debt_equity": "Debt-Equity Ratio",
        "net_profit_margin": "Net Profit Margin (%)",
        "current_ratio": "Current Ratio",
        "ebitda_margin": "EBITDA Margin (%)"
    }

    for metric, title in metrics_config.items():
        if metric not in df.columns:
            continue

        plt.figure(figsize=(6, 4))
        sns.lineplot(
            x="year",
            y=metric,
            data=df,
            marker="o"
        )

        plt.title(title)
        plt.xlabel("Year")
        plt.ylabel(title)
        plt.tight_layout()

        file_path = os.path.join(output_dir, f"{metric}_trend.png")
        plt.savefig(file_path)
        plt.close()

        plots[metric] = file_path

    return plots
