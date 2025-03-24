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
RAW_DATA = "data_lake/raw/songs.csv"
PROCESSED_PATH = "data_lake/processed/songs.parquet"
EXPECTED_COLUMNS = ["song_id", "title", "artist_name", "duration", "release_date"]

def read_csv(path: str) -> pd.DataFrame:
    """
    Reads a CSV file from the given path.
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
    """
    missing = [col for col in expected_cols if col not in df.columns]
    if missing:
        raise ValueError(f"Missing expected columns: {missing}")

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Applies cleaning logic specific to the dataset.
    This function must be customized for each dataset.
    """
    df = df.copy()

    # Remove spaces
    df["title"] = df["title"].str.strip()
    df["artist_name"] = df["artist_name"].str.strip()

    # release_date to datetime
    df["release_date"] = pd.to_datetime(df["release_date"], errors="coerce")

    # Delete duplicates
    df = df.drop_duplicates()

    # Duration format: mm:ss
    df["duration"] = df["duration"].astype(str).str.strip()

    return df

def save_parquet(df: pd.DataFrame, path: str) -> None:
    """
    Saves the DataFrame as a Parquet file with snappy compression.
    """
    try:
        df.to_parquet(path, compression='snappy', index=False)
    except Exception as e:
        logging.error(f"Error saving Parquet: {e}")
        raise

if __name__ == "__main__":
    os.makedirs(os.path.dirname(PROCESSED_PATH), exist_ok=True)

    logging.info(f"Starting ingestion: {RAW_DATA}")

    df = read_csv(RAW_DATA)
    validate_columns(df, EXPECTED_COLUMNS)
    df_clean = clean_data(df)
    save_parquet(df_clean, PROCESSED_PATH)

    logging.info(f"File saved to {PROCESSED_PATH}")