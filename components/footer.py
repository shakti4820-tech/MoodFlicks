"""
components/footer.py — Premium footer for MoodFlicks.
Gradient top border, glowing brand logo, social icons, and clean bottom row.
"""

import streamlit as st


def render_footer():
    """Render the premium app footer."""
    footer_html = """
    <div class="footer-section">
        <div class="footer-glow"></div>

        <div class="footer-content">
            <div class="footer-brand">
                <div class="footer-logo-row">
                    <span class="footer-logo-icon">🎬</span>
                    <span class="footer-name">MoodFlicks</span>
                </div>
                <p class="footer-tagline">
                    Discover the perfect movie for every moment. 
                    Powered by real-time data from TMDB.
                </p>
            </div>

            <div class="footer-links">
                <div class="footer-col">
                    <h4 class="footer-heading">Explore</h4>
                    <a href="#" class="footer-link">Trending</a>
                    <a href="#" class="footer-link">Top Rated</a>
                    <a href="#" class="footer-link">New Releases</a>
                    <a href="#" class="footer-link">Genres</a>
                </div>
                <div class="footer-col">
                    <h4 class="footer-heading">Company</h4>
                    <a href="#" class="footer-link">About Us</a>
                    <a href="#" class="footer-link">Careers</a>
                    <a href="#" class="footer-link">Contact</a>
                </div>
                <div class="footer-col">
                    <h4 class="footer-heading">Legal</h4>
                    <a href="#" class="footer-link">Privacy Policy</a>
                    <a href="#" class="footer-link">Terms of Use</a>
                    <a href="#" class="footer-link">Cookie Policy</a>
                </div>
                <div class="footer-col">
                    <h4 class="footer-heading">Connect</h4>
                    <div class="footer-socials">
                        <span class="social-icon" title="Twitter / X">𝕏</span>
                        <span class="social-icon" title="Instagram">📷</span>
                        <span class="social-icon" title="YouTube">▶</span>
                        <span class="social-icon" title="GitHub">⌨</span>
                    </div>
                </div>
            </div>
        </div>

        <div class="footer-bottom">
            <p>© 2026 MoodFlicks. All rights reserved. Built with ❤️ using Streamlit.</p>
            <p class="footer-disclaimer" style="text-align:right;">
                Data provided by
                <a href="https://www.themoviedb.org" target="_blank"
                   style="color:#3b82f6; text-decoration:none;">TMDB</a>.
                Not endorsed or certified by TMDB.
            </p>
        </div>
    </div>
    """
    st.markdown(footer_html, unsafe_allow_html=True)
