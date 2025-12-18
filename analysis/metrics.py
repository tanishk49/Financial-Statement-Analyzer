import pandas as pd


# =========================================================
# Individual Metric Functions
# =========================================================

def calculate_roe(net_income, shareholders_equity):
    """
    Return on Equity (ROE)
    ROE = Net Income / Shareholders' Equity
    """
    try:
        if shareholders_equity == 0 or pd.isna(shareholders_equity):
            return None
        return net_income / shareholders_equity
    except Exception:
        return None


def calculate_roa(net_income, total_assets):
    """
    Return on Assets (ROA)
    ROA = Net Income / Total Assets
    """
    try:
        if total_assets == 0 or pd.isna(total_assets):
            return None
        return net_income / total_assets
    except Exception:
        return None


def calculate_debt_equity(total_liabilities, shareholders_equity):
    """
    Debt to Equity Ratio
    Debt-Equity = Total Liabilities / Shareholders' Equity
    """
    try:
        if shareholders_equity == 0 or pd.isna(shareholders_equity):
            return None
        return total_liabilities / shareholders_equity
    except Exception:
        return None


def calculate_net_profit_margin(net_income, revenue):
    """
    Net Profit Margin
    Net Profit Margin = Net Income / Revenue
    """
    try:
        if revenue == 0 or pd.isna(revenue):
            return None
        return net_income / revenue
    except Exception:
        return None


def calculate_current_ratio(current_assets, current_liabilities):
    """
    Current Ratio
    Current Ratio = Current Assets / Current Liabilities
    """
    try:
        if current_liabilities == 0 or pd.isna(current_liabilities):
            return None
        return current_assets / current_liabilities
    except Exception:
        return None


def calculate_ebitda_margin(ebitda, revenue):
    """
    EBITDA Margin
    EBITDA Margin = EBITDA / Revenue
    """
    try:
        if revenue == 0 or pd.isna(revenue):
            return None
        return ebitda / revenue
    except Exception:
        return None


# =========================================================
# Multi-Year Financial Metrics (Trend Analysis)
# =========================================================

def compute_financial_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute year-wise financial metrics for trend analysis.

    Required columns:
    - year
    - revenue
    - net_income
    - total_assets
    - total_liabilities
    - shareholders_equity

    Optional columns:
    - current_assets
    - current_liabilities
    - ebitda
    """

    metrics_df = df.copy()

    # Profitability & leverage
    metrics_df["roe"] = metrics_df.apply(
        lambda x: calculate_roe(
            x["net_income"], x["shareholders_equity"]
        ),
        axis=1
    )

    metrics_df["roa"] = metrics_df.apply(
        lambda x: calculate_roa(
            x["net_income"], x["total_assets"]
        ),
        axis=1
    )

    metrics_df["debt_equity"] = metrics_df.apply(
        lambda x: calculate_debt_equity(
            x["total_liabilities"], x["shareholders_equity"]
        ),
        axis=1
    )

    metrics_df["net_profit_margin"] = metrics_df.apply(
        lambda x: calculate_net_profit_margin(
            x["net_income"], x["revenue"]
        ),
        axis=1
    )

    # Optional: Liquidity
    if {"current_assets", "current_liabilities"}.issubset(metrics_df.columns):
        metrics_df["current_ratio"] = metrics_df.apply(
            lambda x: calculate_current_ratio(
                x["current_assets"], x["current_liabilities"]
            ),
            axis=1
        )

    # Optional: Operating performance
    if {"ebitda", "revenue"}.issubset(metrics_df.columns):
        metrics_df["ebitda_margin"] = metrics_df.apply(
            lambda x: calculate_ebitda_margin(
                x["ebitda"], x["revenue"]
            ),
            axis=1
        )
        metrics_df["ebitda_margin"] *= 100

    # Convert to percentages
    metrics_df["roe"] *= 100
    metrics_df["roa"] *= 100
    metrics_df["net_profit_margin"] *= 100

    return metrics_df


# =========================================================
# Latest-Year Summary Metrics (Dashboard KPIs)
# =========================================================

def compute_latest_metrics(df: pd.DataFrame) -> dict:
    """
    Compute latest-year snapshot financial metrics for dashboard.
    """

    latest = df.iloc[-1]
    metrics = {}

    # Core KPIs
    roe = calculate_roe(latest["net_income"], latest["shareholders_equity"])
    roa = calculate_roa(latest["net_income"], latest["total_assets"])
    de = calculate_debt_equity(
        latest["total_liabilities"], latest["shareholders_equity"]
    )
    npm = calculate_net_profit_margin(
        latest["net_income"], latest["revenue"]
    )

    metrics["ROE (%)"] = round(roe * 100, 2) if roe else None
    metrics["ROA (%)"] = round(roa * 100, 2) if roa else None
    metrics["Debt-Equity"] = round(de, 2) if de else None
    metrics["Net Profit Margin (%)"] = round(npm * 100, 2) if npm else None

    # Optional KPIs
    if {"current_assets", "current_liabilities"}.issubset(df.columns):
        cr = calculate_current_ratio(
            latest["current_assets"], latest["current_liabilities"]
        )
        metrics["Current Ratio"] = round(cr, 2) if cr else None

    if "ebitda" in df.columns:
        em = calculate_ebitda_margin(latest["ebitda"], latest["revenue"])
        metrics["EBITDA Margin (%)"] = round(em * 100, 2) if em else None

    return metrics
