"""
components/carousel.py — Horizontal carousel row builder for movie sections.
Premium card design with rating badges, hover overlays, and smooth animations.
"""

import streamlit as st
from tmdb_api import get_poster_url


def render_movie_grid(movies, section=""):
    """Render a responsive grid of movie cards."""
    if not movies:
        return

    num_movies = len(movies)
    cols_per_row = 5

    for i in range(0, num_movies, cols_per_row):
        row_movies = movies[i:i + cols_per_row]
        cols = st.columns(cols_per_row)

        for j, movie in enumerate(row_movies):
            with cols[j]:
                movie_id = movie.get("id")
                title = movie.get("title", "Unknown")
                display_title = title[:18] + "…" if len(title) > 18 else title
                rating = movie.get("vote_average", 0)
                release = movie.get("release_date", "")[:4]
                poster_url = get_poster_url(movie.get("poster_path"), "w342")

                # Rating color
                if rating >= 7.5:
                    rating_color = "#4ade80"  # green
                elif rating >= 5.5:
                    rating_color = "#f59e0b"  # amber
                else:
                    rating_color = "#f87171"  # red

                # Card HTML
                st.markdown(f"""
                <div class="movie-card" id="card-{movie_id}-{section}">
                    <div style="position:relative; overflow:hidden; border-radius: 10px 10px 0 0;">
                        <img
                            src="{poster_url}"
                            class="card-img"
                            alt="{display_title}"
                            loading="lazy"
                            onerror="this.src='https://placehold.co/342x513/111120/475569?text=No+Image'"
                            style="width:100%; aspect-ratio:2/3; object-fit:cover; display:block; transition: transform 0.4s ease, filter 0.4s ease;"
                        />
                        <div style="
                            position: absolute;
                            top: 7px; right: 7px;
                            background: rgba(7,7,15,0.85);
                            backdrop-filter: blur(6px);
                            border: 1px solid rgba(245,158,11,0.35);
                            border-radius: 6px;
                            padding: 2px 7px;
                            font-size: 11px;
                            font-weight: 700;
                            color: {rating_color};
                            z-index: 5;
                        ">⭐ {rating:.1f}</div>
                        <div class="card-overlay">
                            <p style="font-weight:700; margin:0 0 3px 0; font-size:13px; color:white; line-height:1.3;">{display_title}</p>
                            <span style="color:{rating_color}; font-size:12px; font-weight:600;">⭐ {rating:.1f}</span>
                            <span style="color:#94a3b8; font-size:11px; margin-left:6px;">{release}</span>
                        </div>
                    </div>
                    <div style="padding: 9px 8px 6px 8px; background: #111120; border-radius: 0 0 10px 10px;">
                        <p style="font-size:13px; font-weight:700; margin:0 0 3px 0; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; color:#f1f5f9;">{display_title}</p>
                        <div style="display:flex; justify-content:space-between; align-items:center;">
                            <span style="font-size:11px; color:#475569;">{release}</span>
                            <span style="font-size:11px; font-weight:700; color:{rating_color};">⭐ {rating:.1f}</span>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                # Invisible Streamlit button for interaction
                if st.button("View", key=f"btn_{movie_id}_{section}_{i}_{j}",
                             use_container_width=True):
                    st.session_state.selected_movie_id = movie_id
                    st.session_state.show_detail = True
                    st.rerun()


def render_carousel(title, movies, section_key=""):
    """Render a titled carousel section of movie cards."""
    if not movies:
        return

    # Section title with accent bar
    st.markdown(f"""
    <h2 style="
        font-family: 'Outfit', sans-serif;
        font-size: 20px;
        font-weight: 800;
        color: #f1f5f9;
        margin: 8px 0 14px 0;
        padding-left: 50px;
        letter-spacing: -0.3px;
        display: flex;
        align-items: center;
        gap: 10px;
    ">
        <span style="
            display: inline-block;
            width: 3px; height: 20px;
            background: linear-gradient(180deg, #3b82f6, #8b5cf6);
            border-radius: 999px;
            flex-shrink: 0;
        "></span>
        {title}
    </h2>
    """, unsafe_allow_html=True)

    render_movie_grid(movies[:10], section_key)

    # Spacer
    st.markdown('<div style="height: 12px;"></div>', unsafe_allow_html=True)
