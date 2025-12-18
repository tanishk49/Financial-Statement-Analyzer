# analysis/preprocess.py
import pandas as pd


def load_financial_data(file_path: str) -> pd.DataFrame:
    """
    Load raw financial statement CSV file into a DataFrame
    """
    df = pd.read_csv(file_path)
    return df


def clean_financial_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and standardize financial statement data 
    """

    # Standardize column names
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    # Remove completely empty rows
    df = df.dropna(how="all")

    # Convert numeric columns safely
    for col in df.columns:
        if col != "year":
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Sort by year if present
    if "year" in df.columns:
        df["year"] = df["year"].astype(int)
        df = df.sort_values("year")

    return df
