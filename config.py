"""
config.py — API keys, genre mappings, and app constants for MoodFlicks.
"""

import os
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

# ── TMDB API Configuration ──────────────────────────────────────────────────
# Prefer secrets.toml, fallback to .env, then system env vars
def get_api_key():
    try:
        return st.secrets["TMDB_API_KEY"]
    except:
        pass
    return os.getenv("TMDB_API_KEY", "")

TMDB_API_KEY = get_api_key()
TMDB_BASE_URL = "https://api.themoviedb.org/3"
TMDB_IMAGE_BASE = "https://image.tmdb.org/t/p/w500"
TMDB_BACKDROP_BASE = "https://image.tmdb.org/t/p/original"
TMDB_POSTER_SMALL = "https://image.tmdb.org/t/p/w342"
TMDB_POSTER_THUMB = "https://image.tmdb.org/t/p/w185"

# ── Mood → Genre Mapping ────────────────────────────────────────────────────
MOOD_GENRE_MAP = {
    "😂 Comedy":       {"id": 35,    "name": "Comedy"},
    "😢 Emotional":    {"id": 18,    "name": "Drama"},
    "😱 Thriller":     {"id": 53,    "name": "Thriller"},
    "❤️ Romance":      {"id": 10749, "name": "Romance"},
    "🚀 Sci-Fi":       {"id": 878,   "name": "Science Fiction"},
    "👻 Horror":       {"id": 27,    "name": "Horror"},
    "💪 Action":       {"id": 28,    "name": "Action"},
    "🧠 Mind-Bending": {"id": 9648,  "name": "Mystery"},
    "🎵 Musical":      {"id": 10402, "name": "Music"},
    "🌍 World Cinema": {"id": None,  "name": "World Cinema"},
}

# ── App Constants ────────────────────────────────────────────────────────────
APP_NAME = "MoodFlicks"
APP_ICON = "🎬"
HERO_ROTATE_INTERVAL = 5  # seconds
CACHE_TTL = 3600  # 1 hour

GENRE_ID_TO_NAME = {
    28: "Action", 12: "Adventure", 16: "Animation", 35: "Comedy",
    80: "Crime", 99: "Documentary", 18: "Drama", 10751: "Family",
    14: "Fantasy", 36: "History", 27: "Horror", 10402: "Music",
    9648: "Mystery", 10749: "Romance", 878: "Science Fiction",
    10770: "TV Movie", 53: "Thriller", 10752: "War", 37: "Western",
}

# Real Watch Links Generation
from urllib.parse import quote

def get_watch_links(movie_title):
    encoded_title = quote(movie_title)
    return {
        "hotstar": f"https://www.hotstar.com/in/search?q={encoded_title}",
        "justwatch": f"https://www.justwatch.com/in/search?q={encoded_title}",
        "google": f"https://www.google.com/search?q={encoded_title}+watch+on+hotstar"
    }
