-- #############################################
-- SoundWave Analytics - Star Schema (PostgreSQL)
-- #############################################

-- Drop schema if exists for clean setup
DROP SCHEMA IF EXISTS soundwave_dw CASCADE;
CREATE SCHEMA soundwave_dw;
SET search_path TO soundwave_dw;

-- ======================
-- Dimension Tables
-- ======================

CREATE TABLE dim_user (
    user_id INT PRIMARY KEY,
    name VARCHAR(50),
    email VARCHAR(50),
    signup_date TIMESTAMP,
    country VARCHAR(30)
);

CREATE TABLE dim_song (
    song_id INT PRIMARY KEY,
    title VARCHAR(100),
    duration INT, -- seconds
    release_date DATE
);

CREATE TABLE dim_artist (
    artist_id INT PRIMARY KEY,
    name VARCHAR(50),
    followers INT,
    popularity INT,
    genres TEXT
);

CREATE TABLE dim_album (
    album_id INT PRIMARY KEY,
    name VARCHAR(50),
    release_date DATE,
    total_tracks INT,
    album_type TEXT
);

CREATE TABLE dim_device (
    device_id INT PRIMARY KEY,
    name VARCHAR(50)
);

CREATE TABLE dim_date (
    date_id DATE PRIMARY KEY,
    year INT,
    month INT,
    day INT,
    weekday VARCHAR(10)
);

-- ======================
-- Fact Table
-- ======================

CREATE TABLE fact_plays (
    play_id SERIAL PRIMARY KEY,
    user_id INT,
    song_id INT,
    artist_id INT,
    album_id INT,
    device_id INT,
    date_id DATE,
    FOREIGN KEY (user_id) REFERENCES dim_user(user_id),
    FOREIGN KEY (song_id) REFERENCES dim_song(song_id),
    FOREIGN KEY (artist_id) REFERENCES dim_artist(artist_id),
    FOREIGN KEY (album_id) REFERENCES dim_album(album_id),
    FOREIGN KEY (device_id) REFERENCES dim_device(device_id),
    FOREIGN KEY (date_id) REFERENCES dim_date(date_id)
);