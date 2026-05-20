"""
components/mood_selector.py — Premium mood pill strip for genre filtering.
Styled pills with emoji, smooth hover effects, and active glow.
"""

import streamlit as st
from config import MOOD_GENRE_MAP


def render_mood_selector():
    st.markdown("""
        <div style="padding: 4px 50px 0 50px;">
            <p style="
                font-family: 'Outfit', sans-serif;
                font-size: 18px;
                font-weight: 700;
                color: #f1f5f9;
                margin: 0 0 14px 0;
                letter-spacing: -0.2px;
                display: flex;
                align-items: center;
                gap: 8px;
            ">
                <span style="
                    display: inline-block;
                    width: 3px; height: 18px;
                    background: linear-gradient(180deg, #3b82f6, #8b5cf6);
                    border-radius: 999px;
                    margin-right: 4px;
                "></span>
                🎭 What's Your Mood?
            </p>
        </div>
    """, unsafe_allow_html=True)

    moods = list(MOOD_GENRE_MAP.keys())
    selected = st.session_state.get("selected_mood", None)

    # Render in 2 rows of 5 columns to prevent text crowding
    row1_moods = moods[:5]
    row2_moods = moods[5:]

    # Row 1
    cols1 = st.columns(5)
    for i, mood in enumerate(row1_moods):
        with cols1[i]:
            is_active = mood == selected
            if st.button(
                mood,
                key=f"mood_btn_{i}",
                use_container_width=True,
                type="primary" if is_active else "secondary"
            ):
                if st.session_state.get("selected_mood") == mood:
                    st.session_state.selected_mood = None
                else:
                    st.session_state.selected_mood = mood
                st.rerun()

    # Spacer between rows
    st.markdown('<div style="height: 8px;"></div>', unsafe_allow_html=True)

    # Row 2
    cols2 = st.columns(5)
    for i, mood in enumerate(row2_moods):
        with cols2[i]:
            idx = i + 5
            is_active = mood == selected
            if st.button(
                mood,
                key=f"mood_btn_{idx}",
                use_container_width=True,
                type="primary" if is_active else "secondary"
            ):
                if st.session_state.get("selected_mood") == mood:
                    st.session_state.selected_mood = None
                else:
                    st.session_state.selected_mood = mood
                st.rerun()

    st.markdown('<div style="height: 12px;"></div>', unsafe_allow_html=True)
