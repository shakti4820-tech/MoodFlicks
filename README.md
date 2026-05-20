# 🎬 MoodFlicks - Premium Movie Discovery Web App

A highly-functional, high-fidelity Mood-Based Movie Discovery application inspired by Netflix and Hotstar. Built with **Streamlit** and the **TMDB API**, featuring real-time data, watch redirects, trailers, and a fully interactive UI.

## 🚀 Key Features

- **Real Movie Data**: Fetches live posters, ratings, cast, and backdrops from TMDB.
- **Smart Watch Links**: Automatically generates search queries to watch the movie on Hotstar.
- **Official Trailers**: Fetches and embeds YouTube trailers for movies natively.
- **Interactive Carousels**: Netflix/Hotstar-style horizontal carousels that expand into rich detail views when clicked.
- **My List (Watchlist)**: Save movies to a personal watchlist natively tracked through session state.
- **Mood Selector**: Filter the entire application's carousels by clicking dynamic mood pills.
- **Live Search**: Integrated movie search API.
- **Cinematic UI**: Custom CSS to completely hide Streamlit's native chrome and replace it with a premium glass-morphic dark mode layout.

## 🛠️ Installation & Local Setup

1. **Clone or Download** the project.
2. **Install Requirements**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Add TMDB API Key**:
   - Get a free API key from [The Movie Database (TMDB)](https://www.themoviedb.org/settings/api).
   - Open `.streamlit/secrets.toml` and add your key:
     ```toml
     TMDB_API_KEY = "your_actual_tmdb_api_key_here"
     ```
4. **Run the Application**:
   ```bash
   streamlit run app.py
   ```

## 🌐 Deployment Ready (Antigravity & Beyond)

This application is fully prepared for remote deployment.
- It includes `Procfile`, `runtime.txt`, `requirements.txt`.
- It includes `.streamlit/config.toml` set to headless server mode.
- It relies securely on Streamlit secrets. Just input the `TMDB_API_KEY` into your hosting provider's Secrets Management interface.

## 📂 Architecture

```text
cinmaAI/
├── app.py                  # Main entry + routing state
├── config.py               # Constants & Link Generators
├── tmdb_api.py             # Live API handlers with @st.cache_data
├── requirements.txt        # Dependency locks
├── runtime.txt             # Python runtime declaration
├── Procfile                # WSGI command for deployments
├── .streamlit/
│   ├── config.toml         # Dark mode and headless config
│   └── secrets.toml        # Secret API Key injection
├── styles/
│   └── main.css            # 300+ lines of custom glass-morphism UI
└── components/
    ├── navbar.py           # Top nav with Watchlist active counts
    ├── hero.py             # Featured cinematic banner
    ├── mood_selector.py    # State-driven filters
    ├── carousel.py         # Visual rows with hidden Streamlit buttons
    ├── movie_detail.py     # Full page modal with trailers & links
    └── footer.py           # Legal & links
```

*Built with ♥ using Python & Streamlit.*
