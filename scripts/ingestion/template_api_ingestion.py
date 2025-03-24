"""
Template for ingesting data from a public API and saving it to the Data Lake.
This script provides a reusable structure for authentication, extraction,
cleaning, and saving.
"""

import os
import requests
import pandas as pd
import logging
from dotenv import load_dotenv
from typing import Dict, List

# ───────────────────────────────
# CONFIGURATION & LOGGING
# ───────────────────────────────

load_dotenv()
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

API_KEY = os.getenv("API_KEY")  # Replace with actual env variable
BASE_URL = "https://api.example.com"  # Replace with real API
OUTPUT_PATH = "data_lake/processed/api_output.parquet"

# ───────────────────────────────
# AUTHENTICATION (if required)
# ───────────────────────────────

def get_auth_token(api_key: str) -> str:
    """
    Returns a token or same API key for authentication.
    Customize this if the API uses OAuth/token exchange.

    Args:
        api_key (str): API key or credentials from .env

    Returns:
        str: Auth token or API key
    """
    return api_key

# ───────────────────────────────
# EXTRACTION
# ───────────────────────────────

def fetch_data(endpoint: str, token: str) -> Dict:
    """
    Fetches data from an API endpoint.

    Args:
        endpoint (str): API endpoint (e.g., "top-news").
        token (str): API key or token for auth.

    Returns:
        dict: Raw JSON response
    """
    headers = {"Authorization": f"Bearer {token}"}
    url = f"{BASE_URL}/{endpoint}"

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"API request failed: {response.status_code} - {response.text}")

    return response.json()

# ───────────────────────────────
# CLEANING / TRANSFORMATION
# ───────────────────────────────

def clean_data(raw_data: Dict) -> pd.DataFrame:
    """
    Transforms raw JSON into a DataFrame.

    Args:
        raw_data (dict): Raw API response

    Returns:
        pd.DataFrame: Cleaned dataset
    """
    records = raw_data.get("results", [])  # Modify as needed
    df = pd.DataFrame(records)
    return df

# ───────────────────────────────
# SAVE TO PARQUET
# ───────────────────────────────

def save_parquet(df: pd.DataFrame, path: str):
    """
    Saves DataFrame as compressed Parquet.

    Args:
        df (pd.DataFrame): Cleaned data
        path (str): Output path
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df.to_parquet(path, compression="snappy", index=False)
    logging.info(f"Saved file: {path}")

# ───────────────────────────────
# MAIN SCRIPT
# ───────────────────────────────

if __name__ == "__main__":
    logging.info("Starting API ingestion...")

    token = get_auth_token(API_KEY)
    raw_json = fetch_data(endpoint="data", token=token)  # Change "data"
    df = clean_data(raw_json)
    save_parquet(df, OUTPUT_PATH)

    logging.info("Ingestion complete.")
