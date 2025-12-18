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

    # Try converting numeric columns safely
    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="ignore")

    return df
