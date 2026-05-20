"""
components/movie_detail.py — Premium expanded movie detail view.
Cinematic backdrop, styled poster, cast chips, and action buttons.
"""

import streamlit as st
from tmdb_api import (
    fetch_movie_details, get_poster_url, get_backdrop_url, get_trailer_url
)
from config import get_watch_links


def render_movie_detail():
    movie_id = st.session_state.get("selected_movie_id")
    if not movie_id:
        return

    details = fetch_movie_details(movie_id)
    if not details:
        st.error("Failed to load movie details.")
        if st.button("← Back"):
            st.session_state.show_detail = False
            st.rerun()
        return

    # Back Button
    col_back, _ = st.columns([1, 9])
    with col_back:
        if st.button("← Back", key="back_btn", type="secondary"):
            st.session_state.show_detail = False
            st.rerun()

    # Data extraction
    title        = details.get("title", "Unknown")
    tagline      = details.get("tagline", "")
    overview     = details.get("overview", "")
    rating       = details.get("vote_average", 0)
    vote_count   = details.get("vote_count", 0)
    release      = details.get("release_date", "")[:4]
    runtime_mins = details.get("runtime", 0)
    runtime_str  = f"{runtime_mins // 60}h {runtime_mins % 60}m" if runtime_mins else "N/A"
    language     = details.get("original_language", "en").upper()
    budget       = details.get("budget", 0)
    budget_str   = f"${budget / 1_000_000:.1f}M" if budget > 0 else "N/A"

    backdrop     = get_backdrop_url(details.get("backdrop_path"))
    poster       = get_poster_url(details.get("poster_path"), "w500")

    genres       = details.get("genres", [])
    genre_badges = "".join([
        f'<span class="detail-genre-badge">{g["name"]}</span>'
        for g in genres
    ])

    credits   = details.get("credits", {})
    cast      = [c.get("name") for c in credits.get("cast", [])[:6]]
    director  = next(
        (c.get("name") for c in credits.get("crew", []) if c.get("job") == "Director"),
        "Unknown"
    )

    videos      = details.get("videos", {})
    trailer_url = get_trailer_url(videos, title)
    watch_urls  = get_watch_links(title)

    # Rating stars
    star_count = min(5, round(rating / 2))
    stars_html = "★" * star_count + "☆" * (5 - star_count)

    # Cast chips HTML
    cast_chips = "".join([
        f'<span class="cast-chip">{name}</span>'
        for name in cast
    ])

    bg_style = f'background-image: url("{backdrop}");' if backdrop else \
        'background: linear-gradient(135deg, #0d0d1a, #07070f);'

    tagline_html = f"""
        <p class="detail-tagline">"{tagline}"</p>
    """ if tagline else ""

    st.markdown(f"""
    <div class="movie-detail-container">
        <div class="detail-backdrop" style='{bg_style}'>
            <div class="detail-backdrop-overlay"></div>
        </div>
        <div class="detail-content">
            <div class="detail-poster-col">
                <img src="{poster}" class="detail-poster"
                     onerror="this.src='https://placehold.co/500x750/111120/475569?text=No+Poster'"
                     alt="{title}" />
            </div>
            <div class="detail-info-col">
                <h1 class="detail-title">{title}</h1>
                {tagline_html}

                <div class="detail-meta-row">
                    <span class="meta-pill">{release}</span>
                    <span class="meta-pill">{runtime_str}</span>
                    <span class="meta-pill">{language}</span>
                    <span class="meta-pill">Budget: {budget_str}</span>
                </div>

                <div class="detail-rating">
                    <div>
                        <div class="detail-score-big">{rating:.1f}</div>
                        <div class="detail-score-sub">/ 10 · {vote_count:,} votes</div>
                    </div>
                    <div>
                        <div class="detail-stars" style="letter-spacing:3px; font-size:18px;">{stars_html}</div>
                    </div>
                </div>

                <div class="detail-genres">{genre_badges}</div>

                <p class="detail-overview">{overview}</p>

                <div class="detail-info-row">
                    <span class="detail-label">Director</span>
                    <span style="color:#f1f5f9; font-weight:500;">{director}</span>
                </div>

                <div style="margin-bottom: 22px;">
                    <span class="detail-label" style="display:block; margin-bottom:8px;">Cast</span>
                    <div class="cast-chips">{cast_chips}</div>
                </div>

                <div class="detail-actions">
                    <a href="{watch_urls['hotstar']}" target="_blank" style="text-decoration:none;">
                        <button class="btn-primary hero-btn" style="font-size:14px; padding:11px 22px;">
                            ▶&nbsp; Watch on Hotstar
                        </button>
                    </a>
                    <a href="{trailer_url}" target="_blank" style="text-decoration:none;">
                        <button class="btn-outline hero-btn" style="font-size:14px; padding:11px 22px; border:1.5px solid rgba(255,255,255,0.2)!important;">
                            🎬&nbsp; Watch Trailer
                        </button>
                    </a>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Watchlist Streamlit button
    in_list = any(m["id"] == movie_id for m in st.session_state.get("watchlist", []))
    btn_text = "✓ Remove from My List" if in_list else "+ Add to My List"

    col_btn, _ = st.columns([3, 7])
    with col_btn:
        if st.button(btn_text, key=f"detail_list_{movie_id}", use_container_width=True,
                     type="primary" if not in_list else "secondary"):
            if "watchlist" not in st.session_state:
                st.session_state.watchlist = []
            if not in_list:
                basic_movie = {
                    "id": details["id"],
                    "title": details["title"],
                    "poster_path": details.get("poster_path"),
                    "vote_average": details.get("vote_average"),
                    "release_date": details.get("release_date", ""),
                }
                st.session_state.watchlist.append(basic_movie)
                st.toast(f"✅ {title} added to My List!", icon="🎬")
            else:
                st.session_state.watchlist = [
                    m for m in st.session_state.watchlist if m["id"] != movie_id
                ]
                st.toast(f"❌ {title} removed from My List!")
            st.rerun()

    # Similar Movies
    st.markdown("""
        <div style="height:1px; background:linear-gradient(90deg,transparent,rgba(59,130,246,0.2),transparent); margin:32px 0 0 0;"></div>
        <h3 style="
            font-family:'Outfit',sans-serif; font-size:20px; font-weight:800;
            color:#f1f5f9; margin:28px 0 18px 0;
            display:flex; align-items:center; gap:10px;
        ">
            <span style="display:inline-block;width:3px;height:20px;background:linear-gradient(180deg,#3b82f6,#8b5cf6);border-radius:999px;flex-shrink:0;"></span>
            🎬 Similar Movies
        </h3>
    """, unsafe_allow_html=True)

    similar = details.get("similar", {}).get("results", [])[:6]
    if similar:
        from components.carousel import render_movie_grid
        render_movie_grid(similar, section=f"sim_{movie_id}")
    else:
        st.info("No similar movies found.")
