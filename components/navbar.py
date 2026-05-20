"""
components/navbar.py — Premium top navigation bar for MoodFlicks.
Glassmorphism sticky nav with gradient logo, pill nav links, and avatar.
"""

import streamlit as st


def render_navbar():
    """Render the premium top navigation bar."""
    watchlist_count = len(st.session_state.get("watchlist", []))
    watchlist_label = f"🎞 My List ({watchlist_count})" if watchlist_count > 0 else "🎞 My List"

    view = st.session_state.get("current_view", "home")

    # Logo column + nav buttons + avatar
    col_logo, col_home, col_movies, col_list, col_avatar = st.columns([3, 1, 1, 1.3, 1.5])

    with col_logo:
        st.markdown("""
            <div class="moodflicks-logo" style="padding-top: 6px;">
                <span class="moodflicks-logo-icon">🎬</span>
                <span class="moodflicks-logo-text">MoodFlicks</span>
            </div>
        """, unsafe_allow_html=True)

    with col_home:
        if st.button("🏠 Home", key="nav_home", use_container_width=True,
                     type="primary" if view == "home" else "secondary"):
            st.session_state.current_view = "home"
            st.session_state.selected_movie_id = None
            st.session_state.show_detail = False
            st.rerun()

    with col_movies:
        if st.button("🎥 Movies", key="nav_movies", use_container_width=True,
                     type="secondary"):
            st.session_state.current_view = "home"
            st.session_state.selected_movie_id = None
            st.session_state.show_detail = False
            st.rerun()

    with col_list:
        if st.button(watchlist_label, key="nav_watchlist", use_container_width=True,
                     type="primary" if view == "watchlist" else "secondary"):
            st.session_state.current_view = "watchlist"
            st.session_state.selected_movie_id = None
            st.session_state.show_detail = False
            st.rerun()

    with col_avatar:
        st.markdown("""
            <div style="display:flex; justify-content:flex-end; align-items:center; height:100%; padding-top:4px; gap:12px;">
                <div style="
                    width: 38px; height: 38px;
                    border-radius: 50%;
                    background: linear-gradient(135deg, #3b82f6, #8b5cf6);
                    display: flex; align-items: center; justify-content: center;
                    font-weight: 800; color: white; font-size: 15px;
                    box-shadow: 0 0 16px rgba(59,130,246,0.5), 0 0 0 2px rgba(59,130,246,0.2);
                    cursor: pointer;
                    transition: box-shadow 0.3s ease;
                ">U</div>
            </div>
        """, unsafe_allow_html=True)

    # Animated gradient divider
    st.markdown("""
        <div style="
            height: 1px;
            background: linear-gradient(90deg, transparent, rgba(59,130,246,0.4), rgba(139,92,246,0.4), transparent);
            margin: 6px 0 24px 0;
        "></div>
    """, unsafe_allow_html=True)
