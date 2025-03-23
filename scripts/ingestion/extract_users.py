import pandas as pd
import os
import logging
from typing import List

# Configure logging
logging.basicConfig(
    level=logging.INFO, 
    format="%(asctime)s - %(levelname)s - %(message)s"
    )

# File paths
RAW_DATA = "data_lake/raw/users.csv"
PROCESSED_PATH = "data_lake/processed/users.parquet"

def read_csv(path: str) -> pd.DataFrame:
    """
    Reads a CSV file from the given path.

    Args:
        path (str): Path to the CSV file.

    Returns:
        pd.DataFrame: Loaded dataframe.
    """
    try:
        return pd.read_csv(path)
    except FileNotFoundError:
        logging.error(f"File not found: {path}")
        raise
    except Exception as e:
        logging.error(f"Error reading CSV: {e}")
        raise

def validate_columns(df: pd.DataFrame, expected_cols: List[str]) -> None:
    """
    Validates if all expected columns are present in the DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame to validate.
        expected_cols (List[str]): List of expected column names.

    Raises:
        ValueError: If any expected column is missing.
    """
    missing_cols = [col for col in expected_cols if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Missing expected columns: {missing_cols}")

def clean_users(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans the users dataset by fixing formats and removing duplicates.

    Args:
        df (pd.DataFrame): Raw DataFrame.

    Returns:
        pd.DataFrame: Cleaned DataFrame.
    """
    df = df.copy()

    # signup_date to datetime
    df['signup_date'] = pd.to_datetime(df['signup_date'], errors='coerce')
    
    # Delete duplicates
    df = df.drop_duplicates()
    #df = df.drop_duplicates(subset=['columna1', '...'])

    # Remove spaces
    df['name'] = df['name'].str.strip()
    df['email'] = df['email'].str.strip()

    return df

def save_processed(df: pd.DataFrame, path: str) -> None:
    """
    Saves the DataFrame to a Parquet file with snappy compression.

    Args:
        df (pd.DataFrame): The cleaned DataFrame.
        path (str): Output path for Parquet file.
    """
    try:
        df.to_parquet(path, compression='snappy', index=False)
    except Exception as e:
        logging.error(f"Failed to save processed file: {e}")
        raise

if __name__ == "__main__":
    os.makedirs(os.path.dirname(PROCESSED_PATH), exist_ok=True)

    expected_cols = ["user_id", "name", "email", "signup_date", "country"]

    logging.info("Starting ingestion for users.csv")

    df = read_csv(RAW_DATA)
    validate_columns(df, expected_cols)
    df_clean = clean_users(df)
    save_processed(df_clean, PROCESSED_PATH)

    logging.info("users.parquet created successfully!")