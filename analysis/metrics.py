import pandas as pd


def calculate_roe(net_income, shareholders_equity):
    """
    Return on Equity (ROE)
    ROE = Net Income / Shareholders' Equity
    """
    try:
        if shareholders_equity == 0:
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
        if total_assets == 0:
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
        if shareholders_equity == 0:
            return None
        return total_liabilities / shareholders_equity
    except Exception:
        return None


def compute_financial_metrics(df: pd.DataFrame) -> dict:
    """
    Compute all key financial metrics from a DataFrame
    Expected columns:
    - net_income
    - total_assets
    - total_liabilities
    - shareholders_equity
    """

    metrics = {}

    try:
        metrics["ROE"] = calculate_roe(
            df["net_income"].iloc[-1],
            df["shareholders_equity"].iloc[-1]
        )

        metrics["ROA"] = calculate_roa(
            df["net_income"].iloc[-1],
            df["total_assets"].iloc[-1]
        )

        metrics["Debt_Equity"] = calculate_debt_equity(
            df["total_liabilities"].iloc[-1],
            df["shareholders_equity"].iloc[-1]
        )

    except KeyError:
        # Missing required columns
        pass

    return metrics
