import os
import requests
import base64
import pandas as pd
import logging
from dotenv import load_dotenv
from typing import List, Dict


load_dotenv()
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

ARTIST_NAMES = ["Taylor Swift", "Linkin Park", "Ariana Grande"]

ARTIST_OUTPUT_PATH = "data_lake/processed/spotify_artists.parquet"
ALBUM_OUTPUT_PATH = "data_lake/processed/spotify_albums.parquet"

def authenticate_spotify(client_id: str, client_secret: str) -> str:
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + base64.b64encode(f"{client_id}:{client_secret}".encode()).decode(),
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}

    response = requests.post(url, headers=headers, data=data)
    if response.status_code != 200:
        raise Exception(f"Authentication failed: {response.json()}")

    return response.json()["access_token"]

def get_artist_info(artist_name: str, token: str) -> Dict:
    search_url = f"https://api.spotify.com/v1/search?q={artist_name}&type=artist&limit=1"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(search_url, headers=headers)

    if response.status_code != 200:
        raise Exception(f"Error searching artist: {response.json()}")

    items = response.json()["artists"]["items"]
    if not items:
        raise Exception(f"Artist {artist_name} not found.")

    artist = items[0]
    return {
        "artist_id": artist["id"],
        "name": artist["name"],
        "followers": artist["followers"]["total"],
        "popularity": artist["popularity"],
        "genres": ", ".join(artist["genres"])
    }

def get_albums_by_artist(artist_id: str, token: str) -> List[Dict]:
    url = f"https://api.spotify.com/v1/artists/{artist_id}/albums?limit=50"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        raise Exception(f"Error fetching albums: {response.json()}")

    albums = response.json()["items"]
    album_data = []

    for album in albums:
        album_data.append({
            "album_id": album["id"],
            "name": album["name"],
            "release_date": album["release_date"],
            "total_tracks": album["total_tracks"],
            "album_type": album["album_type"],
            "artist_id": artist_id
        })

    return album_data

def save_parquet(df: pd.DataFrame, path: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df.to_parquet(path, compression="snappy", index=False)
    logging.info(f"Saved file: {path}")

if __name__ == "__main__":
    logging.info("Starting Spotify data extraction...")

    token = authenticate_spotify(CLIENT_ID, CLIENT_SECRET)

    artist_records = []
    album_records = []

    for name in ARTIST_NAMES:
        try:
            artist_info = get_artist_info(name, token)
            artist_records.append(artist_info)

            albums = get_albums_by_artist(artist_info["artist_id"], token)
            album_records.extend(albums)

            logging.info(f"{artist_info['name']} - {len(albums)} albums retrieved")

        except Exception as e:
            logging.warning(f"Error with artist '{name}': {e}")

    artist_df = pd.DataFrame(artist_records)
    album_df = pd.DataFrame(album_records)

    save_parquet(artist_df, ARTIST_OUTPUT_PATH)
    save_parquet(album_df, ALBUM_OUTPUT_PATH)

    logging.info("Spotify data extraction completed.")
