"""
components/hero.py — Cinematic hero banner with auto-rotating featured movies.
Premium glassmorphism overlay with animated content.
"""

import streamlit as st
import time
from tmdb_api import get_poster_url, get_backdrop_url, get_genre_names, fetch_popular_movies
from config import HERO_ROTATE_INTERVAL, get_watch_links


def render_hero():
    featured_movies = fetch_popular_movies()[:6]
    if not featured_movies:
        st.warning("No featured movies found. Please check your API key.")
        return

    if "hero_index" not in st.session_state:
        st.session_state.hero_index = 0
    if "hero_last_update" not in st.session_state:
        st.session_state.hero_last_update = time.time()

    # Auto-rotate
    now = time.time()
    if now - st.session_state.hero_last_update > HERO_ROTATE_INTERVAL:
        st.session_state.hero_index = (st.session_state.hero_index + 1) % len(featured_movies)
        st.session_state.hero_last_update = now

    idx = st.session_state.hero_index % len(featured_movies)
    movie = featured_movies[idx]

    backdrop = get_backdrop_url(movie.get("backdrop_path"))
    title = movie.get("title", "Featured Movie")
    overview = movie.get("overview", "")
    if len(overview) > 220:
        overview = overview[:220] + "…"

    rating = movie.get("vote_average", 0)
    release = movie.get("release_date", "")[:4]
    genres = get_genre_names(movie.get("genre_ids", []))
    watch_urls = get_watch_links(title)
    hotstar_url = watch_urls["hotstar"]

    bg_image = backdrop or get_poster_url(movie.get("poster_path"))
    bg_style = f'background-image: url("{bg_image}");' if bg_image else \
        'background: linear-gradient(135deg, #07070f 0%, #0d0d1a 100%);'

    # Genre badges HTML
    genre_badges = "".join([
        f'<span class="hero-genre-badge">{g}</span>'
        for g in genres[:4]
    ])

    # Rating stars (filled up to half stars)
    star_count = min(5, round(rating / 2))
    stars_html = "★" * star_count + "☆" * (5 - star_count)

    # Navigation dots
    dots_html = "".join([
        f'<div class="hero-dot{"  active" if i == idx else ""}"></div>'
        for i in range(len(featured_movies))
    ])

    hero_html = f"""
    <div class="hero-section" style='{bg_style}'>
        <div class="hero-content">
            <div class="hero-badge-row">
                <span class="hero-live-badge">✦ Featured</span>
                <span class="hero-rating-badge">⭐ {rating:.1f}</span>
            </div>
            <h1 class="hero-title">{title}</h1>
            <div class="hero-meta">
                <span class="meta-pill">{release}</span>
                <span class="hero-meta-dot"></span>
                <span style="color:#94a3b8;">{' · '.join(genres[:3])}</span>
                <span class="hero-meta-dot"></span>
                <span style="color:#f59e0b; letter-spacing:1px;">{stars_html}</span>
            </div>
            <p class="hero-overview">{overview}</p>
            <div class="hero-genre-badges">{genre_badges}</div>
            <div class="hero-cta">
                <a href="{hotstar_url}" target="_blank" style="text-decoration: none;">
                    <button class="btn-primary hero-btn">▶&nbsp; Watch Now</button>
                </a>
            </div>
            <div class="hero-dots">{dots_html}</div>
        </div>
    </div>
    """
    st.markdown(hero_html, unsafe_allow_html=True)

    # Functional Streamlit buttons (overlaid via CSS)
    col1, col2, col3, col_spacer = st.columns([2, 2, 2, 8])
    with col1:
        if st.button("ℹ️ View Details", key="hero_info_btn", use_container_width=True,
                     type="secondary"):
            st.session_state.selected_movie_id = movie["id"]
            st.session_state.show_detail = True
            st.rerun()
    with col2:
        in_list = any(m["id"] == movie["id"] for m in st.session_state.get("watchlist", []))
        btn_text = "✓ In My List" if in_list else "+ Add to List"
        if st.button(btn_text, key="hero_list_btn", use_container_width=True,
                     type="primary" if in_list else "secondary"):
            if "watchlist" not in st.session_state:
                st.session_state.watchlist = []
            if not in_list:
                st.session_state.watchlist.append(movie)
                st.toast(f"✅ {title} added to My List!", icon="🎬")
            else:
                st.session_state.watchlist = [
                    m for m in st.session_state.watchlist if m["id"] != movie["id"]
                ]
                st.toast(f"❌ {title} removed from My List!")
            st.rerun()
    with col3:
        if st.button("⏭ Next", key="hero_next_btn", use_container_width=True,
                     type="secondary"):
            st.session_state.hero_index = (st.session_state.hero_index + 1) % len(featured_movies)
            st.session_state.hero_last_update = time.time()
            st.rerun()
