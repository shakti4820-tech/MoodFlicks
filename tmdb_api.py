"""
tmdb_api.py — All TMDB API interaction functions for MoodFlicks.
Handles fetching movies, details, search, and similar titles with caching.
"""

import requests
import streamlit as st
from config import (
    TMDB_API_KEY, TMDB_BASE_URL, TMDB_IMAGE_BASE, TMDB_BACKDROP_BASE,
    CACHE_TTL, GENRE_ID_TO_NAME,
)
from urllib.parse import quote
from mock_data import MOCK_MOVIES, MOCK_MOVIE_DETAILS

def _has_api_key():
    """Check if a valid TMDB API key is configured."""
    return bool(TMDB_API_KEY) and "paste_your_tmdb_api_key_here" not in TMDB_API_KEY and "your_tmdb_api_key_here" not in TMDB_API_KEY


def _make_request(endpoint, params=None):
    """Make a GET request to TMDB API and return JSON response."""
    if not _has_api_key():
        # Fallback to mock data if API key is missing
        if "/movie/" in endpoint and not endpoint.endswith("/similar") and "popular" not in endpoint and "top_rated" not in endpoint and "now_playing" not in endpoint:
            # Details request (e.g., /movie/12345)
            return MOCK_MOVIE_DETAILS
        elif "/search/movie" in endpoint:
            query = params.get("query", "").lower() if params else ""
            results = [m for m in MOCK_MOVIES if query in m["title"].lower()]
            return {"results": results}
        else:
            # Everything else (discover, popular, etc) returns a list of mock movies
            return {"results": MOCK_MOVIES}

    url = f"{TMDB_BASE_URL}{endpoint}"
    default_params = {"api_key": TMDB_API_KEY, "language": "en-US"}
    if params:
        default_params.update(params)
    try:
        response = requests.get(url, params=default_params, timeout=10)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 401:
            st.error("🚨 Unauthorized: Invalid TMDB API Key.")
        else:
            st.warning(f"⚠️ TMDB API Error: {response.status_code}")
        return None
    except requests.RequestException as e:
        st.error(f"🚨 Network Error: {e}")
        return None


def get_poster_url(poster_path, size="w500"):
    """Get full poster URL from a TMDB poster_path."""
    if poster_path:
        if poster_path.startswith("/mock_poster"):
            # Map mock poster IDs to unique high-fidelity unsplash images
            mock_id = poster_path[-1]
            return f"https://images.unsplash.com/photo-1536440136628-849c177e76a1?w=500&h=750&fit=crop&q=80&random={mock_id}"
        return f"https://image.tmdb.org/t/p/{size}{poster_path}"
    return "https://via.placeholder.com/500x750/1a1a2e/1f80e0?text=No+Poster"


def get_backdrop_url(backdrop_path):
    """Get full backdrop URL from a TMDB backdrop_path."""
    if backdrop_path:
        if backdrop_path.startswith("/mock_backdrop"):
            mock_id = backdrop_path[-1]
            return f"https://images.unsplash.com/photo-1440404653325-ab127d49abc1?w=1280&h=720&fit=crop&q=80&random={mock_id}"
        return f"{TMDB_BACKDROP_BASE}{backdrop_path}"
    return None


@st.cache_data(ttl=CACHE_TTL, show_spinner=False)
def fetch_popular_movies(page=1):
    # Cache busted
    data = _make_request("/movie/popular", {"page": page})
    return data.get("results", [])[:20] if data else []


@st.cache_data(ttl=CACHE_TTL, show_spinner=False)
def fetch_top_rated(page=1):
    # Cache busted
    data = _make_request("/movie/top_rated", {"page": page})
    return data.get("results", [])[:20] if data else []


@st.cache_data(ttl=CACHE_TTL, show_spinner=False)
def fetch_now_playing(page=1):
    data = _make_request("/movie/now_playing", {"page": page})
    return data.get("results", [])[:20] if data else []


@st.cache_data(ttl=CACHE_TTL, show_spinner=False)
def fetch_movies_by_genre(genre_id, page=1, sort_by="popularity.desc"):
    # Cache busted
    data = _make_request("/discover/movie", {
        "with_genres": genre_id,
        "sort_by": sort_by,
        "page": page,
        "vote_count.gte": 50,
    })
    return data.get("results", [])[:20] if data else []


@st.cache_data(ttl=CACHE_TTL, show_spinner=False)
def fetch_world_cinema(page=1):
    data = _make_request("/discover/movie", {
        "with_original_language": "hi|ko|ja|fr|es|de|it|pt|zh|ta|te|ml",
        "sort_by": "popularity.desc",
        "page": page,
        "vote_count.gte": 100,
    })
    if data and "results" in data:
        results = [m for m in data["results"] if m.get("original_language", "en") != "en"]
        return results[:20] if results else data["results"][:20]
    return []


@st.cache_data(ttl=CACHE_TTL, show_spinner=False)
def fetch_top_rated_by_genre(genre_id, page=1):
    data = _make_request("/discover/movie", {
        "with_genres": genre_id,
        "sort_by": "vote_average.desc",
        "page": page,
        "vote_count.gte": 200,
    })
    return data.get("results", [])[:20] if data else []


@st.cache_data(ttl=CACHE_TTL, show_spinner=False)
def fetch_critically_acclaimed(page=1):
    data = _make_request("/discover/movie", {
        "sort_by": "vote_average.desc",
        "vote_count.gte": 1000,
        "vote_average.gte": 8.0,
        "page": page,
    })
    return data.get("results", [])[:20] if data else []


@st.cache_data(ttl=CACHE_TTL, show_spinner=False)
def fetch_movie_details(movie_id):
    data = _make_request(f"/movie/{movie_id}", {"append_to_response": "credits,videos,similar"})
    return data


@st.cache_data(ttl=CACHE_TTL, show_spinner=False)
def fetch_similar_movies(movie_id):
    data = _make_request(f"/movie/{movie_id}/similar")
    return data.get("results", [])[:8] if data else []


@st.cache_data(ttl=CACHE_TTL, show_spinner=False)
def search_movies(query, page=1):
    if not query or not query.strip():
        return []
    data = _make_request("/search/movie", {"query": query.strip(), "page": page})
    return data.get("results", [])[:12] if data else []


def get_genre_names(genre_ids):
    return [GENRE_ID_TO_NAME.get(gid, "") for gid in genre_ids if gid in GENRE_ID_TO_NAME]


def get_trailer_url(videos_data, movie_title):
    """Extract YouTube trailer URL from TMDB video results, with fallback to YouTube search."""
    if videos_data and "results" in videos_data:
        trailers = [v for v in videos_data["results"] if v.get("site") == "YouTube" and v.get("type") in ("Trailer", "Teaser")]
        if trailers:
            return f"https://www.youtube.com/watch?v={trailers[0]['key']}"
            
        # Fallback to any YouTube video attached to the movie
        youtube_vids = [v for v in videos_data["results"] if v.get("site") == "YouTube"]
        if youtube_vids:
             return f"https://www.youtube.com/watch?v={youtube_vids[0]['key']}"
             
    # Ultimate fallback: Construct a YouTube search query
    encoded_title = quote(movie_title)
    return f"https://www.youtube.com/results?search_query={encoded_title}+official+trailer"
