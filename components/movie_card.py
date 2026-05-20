"""
components/movie_card.py — Individual movie card component.
Generates HTML for a single movie card with poster, hover overlay, and metadata.
"""

import streamlit as st
from tmdb_api import get_poster_url, get_genre_names


def render_movie_card_html(movie, card_index=0):
    """Generate HTML for a single movie card.

    Args:
        movie: Dictionary with movie data from TMDB.
        card_index: Unique index for this card.

    Returns:
        HTML string for the movie card.
    """
    title = movie.get("title", "Unknown")
    poster = get_poster_url(movie.get("poster_path"), "w342")
    rating = movie.get("vote_average", 0)
    release = movie.get("release_date", "")[:4]
    movie_id = movie.get("id", 0)
    genres = get_genre_names(movie.get("genre_ids", []))

    # Rating color
    if rating >= 7.5:
        rating_color = "#4caf50"
    elif rating >= 5.5:
        rating_color = "#ff9800"
    else:
        rating_color = "#f44336"

    genre_text = genres[0] if genres else ""

    card_html = f"""
    <div class="movie-card" data-movie-id="{movie_id}" id="card-{movie_id}">
        <div class="movie-card-poster">
            <img src="{poster}" alt="{title}" loading="lazy" onerror="this.src='https://via.placeholder.com/342x513/1e1e2e/666666?text=No+Poster'"/>
            <div class="movie-card-overlay">
                <div class="overlay-content">
                    <p class="overlay-title">{title}</p>
                    <p class="overlay-meta">{release} &nbsp;•&nbsp; {genre_text}</p>
                    <div class="overlay-rating" style="color: {rating_color};">⭐ {rating:.1f}</div>
                    <button class="overlay-play-btn">▶ Play</button>
                </div>
            </div>
        </div>
        <div class="movie-card-info">
            <p class="movie-card-title">{title}</p>
            <div class="movie-card-meta">
                <span class="movie-card-year">{release}</span>
                <span class="movie-card-rating" style="color: {rating_color};">⭐ {rating:.1f}</span>
            </div>
        </div>
    </div>
    """
    return card_html


def render_clickable_card(movie, col_key=""):
    """Render a clickable movie card using Streamlit components.

    Args:
        movie: Dictionary with movie data from TMDB.
        col_key: Unique key prefix for this card's widgets.
    """
    movie_id = movie.get("id", 0)
    title = movie.get("title", "Unknown")
    poster = get_poster_url(movie.get("poster_path"), "w342")
    rating = movie.get("vote_average", 0)
    release = movie.get("release_date", "")[:4]

    # Use markdown + button for clickable card
    st.markdown(f"""
    <div class="st-card-wrapper">
        <img src="{poster}" class="st-card-img" alt="{title}"
             onerror="this.src='https://via.placeholder.com/342x513/1e1e2e/666666?text=No+Poster'"/>
        <div class="st-card-title">{title}</div>
        <div class="st-card-meta">{release} &nbsp;•&nbsp; ⭐ {rating:.1f}</div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("View Details", key=f"view_{col_key}_{movie_id}", use_container_width=True):
        st.session_state.selected_movie = movie_id
        st.rerun()
