"""
app.py — Main entry point for MoodFlicks, a premium AI-powered movie discovery app.
"""

import streamlit as st

st.set_page_config(
    page_title="MoodFlicks | Discover Movies For Your Mood",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

from config import MOOD_GENRE_MAP
from tmdb_api import (
    fetch_popular_movies, fetch_top_rated, fetch_now_playing,
    fetch_movies_by_genre, fetch_world_cinema, fetch_top_rated_by_genre,
    fetch_critically_acclaimed, search_movies
)
from components.navbar import render_navbar
from components.hero import render_hero
from components.mood_selector import render_mood_selector
from components.carousel import render_carousel, render_movie_grid
from components.movie_detail import render_movie_detail
from components.footer import render_footer


def load_css():
    """Load the custom stylesheet and inject Google Fonts."""
    # Inject Google Fonts
    st.markdown("""
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Outfit:wght@300;400;600;700;900&display=swap" rel="stylesheet">
    """, unsafe_allow_html=True)

    try:
        with open("styles/main.css", "r") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning("Custom CSS file not found.")


def render_search_bar():
    """Render a premium styled search bar with session-state and suggestions."""
    if "search_query" not in st.session_state:
        st.session_state.search_query = ""

    st.markdown("""
        <div style="padding: 0 50px; margin-bottom: 4px;">
            <p style="
                font-family: 'Outfit', sans-serif;
                font-size: 18px;
                font-weight: 700;
                color: #f1f5f9;
                margin: 0 0 10px 0;
                display: flex;
                align-items: center;
                gap: 8px;
            ">
                <span style="
                    display:inline-block;width:3px;height:18px;
                    background:linear-gradient(180deg,#3b82f6,#8b5cf6);
                    border-radius:999px;margin-right:4px;
                "></span>
                🔍 Search Movies
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Wrap input in padding container
    col_search, _ = st.columns([6, 4])
    with col_search:
        query = st.text_input(
            label="search",
            value=st.session_state.search_query,
            placeholder="e.g. Inception, RRR, Interstellar, Dune…",
            label_visibility="collapsed",
            key="search_input_widget"
        )

    # Render popular searches row
    popular_searches = ["Inception", "Interstellar", "RRR", "Dune", "Avengers"]
    
    st.markdown("""
        <style>
        .try-searching-container {
            display: flex;
            align-items: center;
            gap: 8px;
            padding: 4px 50px 12px 50px;
            flex-wrap: wrap;
        }
        .try-searching-label {
            color: #475569;
            font-size: 13px;
            font-weight: 600;
            margin-right: 4px;
        }
        </style>
    """, unsafe_allow_html=True)

    cols = st.columns([2, 1.2, 1.4, 0.8, 0.8, 1.2, 4.6])
    with cols[0]:
        st.markdown('<p style="color: #64748b; font-size: 13px; font-weight: 600; margin-top: 6px; padding-left: 50px; white-space: nowrap;">💡 Popular Searches:</p>', unsafe_allow_html=True)
    
    for idx, name in enumerate(popular_searches):
        with cols[idx + 1]:
            if st.button(name, key=f"pop_{name}", use_container_width=True):
                st.session_state.search_query = name
                st.rerun()

    # Sync user manual input back to session state
    if query != st.session_state.search_query:
        st.session_state.search_query = query
        st.rerun()

    return query


def render_watchlist_empty():
    """Render a beautiful empty watchlist state."""
    st.markdown("""
        <div style="
            text-align: center;
            padding: 100px 20px;
            animation: fadeIn 0.5s ease;
        ">
            <div style="font-size: 72px; margin-bottom: 20px; opacity: 0.4;">🎞</div>
            <h2 style="
                font-family: 'Outfit', sans-serif;
                font-size: 26px; font-weight: 800;
                color: #475569; margin: 0 0 10px 0;
            ">Your list is empty</h2>
            <p style="color: #334155; font-size: 15px; max-width: 360px; margin: 0 auto 28px auto; line-height:1.6;">
                Browse movies and tap <strong style="color:#3b82f6;">+ Add to List</strong>
                to save them here for later.
            </p>
        </div>
    """, unsafe_allow_html=True)


def render_search_results(query, results):
    """Render search results with a styled header."""
    st.markdown(f"""
        <div style="padding: 0 50px 6px 50px;">
            <h2 style="
                font-family: 'Outfit', sans-serif;
                font-size: 20px; font-weight: 800;
                color: #f1f5f9; margin: 0 0 6px 0;
                display: flex; align-items: center; gap: 10px;
            ">
                <span style="display:inline-block;width:3px;height:20px;
                    background:linear-gradient(180deg,#3b82f6,#8b5cf6);
                    border-radius:999px;flex-shrink:0;"></span>
                Results for &ldquo;{query}&rdquo;
                <span style="
                    font-size: 13px; font-weight: 600;
                    color: #475569; background: rgba(255,255,255,0.05);
                    border: 1px solid rgba(255,255,255,0.08);
                    padding: 3px 10px; border-radius: 999px;
                ">{len(results)} found</span>
            </h2>
        </div>
    """, unsafe_allow_html=True)
    render_movie_grid(results, section="search")


def main():
    load_css()

    # Session State Init
    if "current_view" not in st.session_state:
        st.session_state.current_view = "home"
    if "selected_movie_id" not in st.session_state:
        st.session_state.selected_movie_id = None
    if "show_detail" not in st.session_state:
        st.session_state.show_detail = False
    if "watchlist" not in st.session_state:
        st.session_state.watchlist = []
    if "rating_filter" not in st.session_state:
        st.session_state.rating_filter = "All"

    render_navbar()

    # ── Movie Detail View ──────────────────────────────────
    if st.session_state.show_detail and st.session_state.selected_movie_id:
        render_movie_detail()

    # ── Watchlist View ──────────────────────────────────────
    elif st.session_state.current_view == "watchlist":
        st.markdown("""
            <h2 style="
                font-family:'Outfit',sans-serif;
                font-size:24px; font-weight:900;
                color:#f1f5f9; margin:0 0 20px 50px;
                display:flex; align-items:center; gap:10px;
            ">
                <span style="display:inline-block;width:3px;height:24px;
                    background:linear-gradient(180deg,#3b82f6,#8b5cf6);
                    border-radius:999px;"></span>
                🎞 My List
            </h2>
        """, unsafe_allow_html=True)

        if st.session_state.watchlist:
            render_movie_grid(st.session_state.watchlist, section="watchlist")
        else:
            render_watchlist_empty()

    # ── Home View ───────────────────────────────────────────
    else:
        search_query = render_search_bar()

        if search_query:
            results = search_movies(search_query)
            if results:
                render_search_results(search_query, results)
            else:
                st.markdown("""
                    <div style="text-align:center; padding:60px 20px; color:#475569;">
                        <div style="font-size:48px; margin-bottom:12px;">🔍</div>
                        <p style="font-size:16px; font-weight:600;">No movies found for that search.</p>
                        <p style="font-size:14px; margin-top:6px;">Try a different title or keyword.</p>
                    </div>
                """, unsafe_allow_html=True)
        else:
            render_hero()

            # Separator
            st.markdown("""
                <div style="height:1px; background:linear-gradient(90deg,transparent,
                    rgba(59,130,246,0.15),transparent); margin:8px 0 24px 0;"></div>
            """, unsafe_allow_html=True)

            render_mood_selector()

            # Render Rating Filter Bar
            st.markdown("""
                <div style="padding: 0 50px; margin-bottom: 12px; display: flex; align-items: center; gap: 8px;">
                    <p style="
                        font-family: 'Outfit', sans-serif;
                        font-size: 14px;
                        font-weight: 700;
                        color: #64748b;
                        margin: 0;
                        display: flex;
                        align-items: center;
                        gap: 6px;
                    ">
                        <span style="
                            display:inline-block;width:3px;height:12px;
                            background:linear-gradient(180deg,#3b82f6,#8b5cf6);
                            border-radius:999px;margin-right:2px;
                        "></span>
                        ⭐ Filter Quality:
                    </p>
                </div>
            """, unsafe_allow_html=True)

            filter_options = ["All Quality", "⭐ 7.0+ High Rated", "⭐ 8.0+ Masterpieces"]
            cols_filter = st.columns([1.5, 1.8, 2.0, 6.7])
            for idx, opt in enumerate(filter_options):
                with cols_filter[idx]:
                    is_active = opt == st.session_state.rating_filter
                    if st.button(opt, key=f"filter_btn_{idx}", use_container_width=True,
                                 type="primary" if is_active else "secondary"):
                        st.session_state.rating_filter = opt
                        st.rerun()

            # Space
            st.markdown('<div style="height: 16px;"></div>', unsafe_allow_html=True)

            # Rating threshold logic
            min_rating = 0.0
            if st.session_state.rating_filter == "⭐ 7.0+ High Rated":
                min_rating = 7.0
            elif st.session_state.rating_filter == "⭐ 8.0+ Masterpieces":
                min_rating = 8.0

            selected_mood = st.session_state.get("selected_mood")

            if selected_mood and selected_mood in MOOD_GENRE_MAP:
                genre_id   = MOOD_GENRE_MAP[selected_mood]["id"]
                genre_name = MOOD_GENRE_MAP[selected_mood]["name"]

                if genre_id:
                    trending_mood  = fetch_movies_by_genre(genre_id, page=1)
                    top_rated_mood = fetch_top_rated_by_genre(genre_id, page=1)
                    more_mood      = fetch_movies_by_genre(genre_id, page=2)

                    # Apply filter
                    if min_rating > 0:
                        trending_mood  = [m for m in trending_mood if m.get("vote_average", 0) >= min_rating]
                        top_rated_mood = [m for m in top_rated_mood if m.get("vote_average", 0) >= min_rating]
                        more_mood      = [m for m in more_mood if m.get("vote_average", 0) >= min_rating]

                    render_carousel(f"🔥 Trending in {genre_name}", trending_mood, f"trending_{genre_id}")
                    render_carousel(f"⭐ Top Rated {genre_name}", top_rated_mood, f"top_{genre_id}")
                    render_carousel(f"🎬 More {genre_name} Picks", more_mood, f"more_{genre_id}")
                else:
                    world_cinema = fetch_world_cinema(page=1)
                    top_world    = fetch_world_cinema(page=2)

                    # Apply filter
                    if min_rating > 0:
                        world_cinema = [m for m in world_cinema if m.get("vote_average", 0) >= min_rating]
                        top_world    = [m for m in top_world if m.get("vote_average", 0) >= min_rating]

                    render_carousel("🌍 Explore World Cinema", world_cinema, "world_1")
                    render_carousel("⭐ Critically Acclaimed International", top_world, "world_2")

            else:
                # Default home carousels
                trending    = fetch_popular_movies()
                top_rated   = fetch_top_rated()
                new_releases = fetch_now_playing()
                acclaimed   = fetch_critically_acclaimed()

                # Apply filter
                if min_rating > 0:
                    trending     = [m for m in trending if m.get("vote_average", 0) >= min_rating]
                    top_rated    = [m for m in top_rated if m.get("vote_average", 0) >= min_rating]
                    new_releases = [m for m in new_releases if m.get("vote_average", 0) >= min_rating]
                    acclaimed    = [m for m in acclaimed if m.get("vote_average", 0) >= min_rating]

                render_carousel("🔥 Trending Now", trending,     "trending_now")
                render_carousel("🆕 New Releases",  new_releases, "new_releases")
                render_carousel("⭐ Top Rated",      top_rated,   "top_rated")
                render_carousel("🏆 Critically Acclaimed", acclaimed, "critically_acclaimed")

    render_footer()


if __name__ == "__main__":
    main()
