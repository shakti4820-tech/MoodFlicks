"""
mock_data.py — High-fidelity dummy content for MoodFlicks when TMDB API is missing.
"""

MOCK_MOVIES = [
    {
        "id": 100001,
        "title": "Neon Genesis: The Awakening",
        "overview": "In a cyberpunk future, a rogue AI discovers human emotions. As it navigates the complex neon-lit city, it must decide between its digital origins and its newfound humanity.",
        "poster_path": "/mock_poster_1",
        "backdrop_path": "/mock_backdrop_1",
        "vote_average": 9.2,
        "release_date": "2024-11-20",
        "genre_ids": [878, 28, 18],  # Sci-Fi, Action, Drama
        "original_language": "en"
    },
    {
        "id": 100002,
        "title": "Whispers of the Valley",
        "overview": "A quiet drama set in the rolling hills of Tuscany. Two estranged siblings reunite to save their family vineyard, uncovering secrets from the past.",
        "poster_path": "/mock_poster_2",
        "backdrop_path": "/mock_backdrop_2",
        "vote_average": 8.5,
        "release_date": "2023-05-14",
        "genre_ids": [18, 10749],  # Drama, Romance
        "original_language": "en"
    },
    {
        "id": 100003,
        "title": "Quantum Heist",
        "overview": "A team of elite thieves uses experimental time-manipulation technology to pull off the ultimate bank job. But messing with time has unpredictable consequences.",
        "poster_path": "/mock_poster_3",
        "backdrop_path": "/mock_backdrop_3",
        "vote_average": 8.8,
        "release_date": "2025-01-10",
        "genre_ids": [28, 878, 53],  # Action, Sci-Fi, Thriller
        "original_language": "en"
    },
    {
        "id": 100004,
        "title": "The Last Laugh",
        "overview": "A retired comedian is forced back onto the stage for one final show by an eccentric billionaire. A hilarious and heartwarming journey ensues.",
        "poster_path": "/mock_poster_4",
        "backdrop_path": "/mock_backdrop_4",
        "vote_average": 7.9,
        "release_date": "2024-03-22",
        "genre_ids": [35, 18],  # Comedy, Drama
        "original_language": "en"
    },
    {
        "id": 100005,
        "title": "Shadow Protocol",
        "overview": "An intelligence operative is disavowed after a mission goes wrong. She must clear her name while being hunted by her own agency across Europe.",
        "poster_path": "/mock_poster_5",
        "backdrop_path": "/mock_backdrop_5",
        "vote_average": 8.1,
        "release_date": "2023-11-05",
        "genre_ids": [28, 53],  # Action, Thriller
        "original_language": "en"
    },
    {
        "id": 100006,
        "title": "Starlight Symphony",
        "overview": "A struggling musician finds inspiration when she crosses paths with an enigmatic astronomer. A beautiful blend of music and cosmos.",
        "poster_path": "/mock_poster_6",
        "backdrop_path": "/mock_backdrop_6",
        "vote_average": 8.7,
        "release_date": "2024-08-14",
        "genre_ids": [10402, 10749, 18],  # Music, Romance, Drama
        "original_language": "en"
    },
    {
        "id": 100007,
        "title": "Echoes in the Dark",
        "overview": "A supernatural thriller where a family moves into a house that reflects their darkest fears. They must confront their past to survive the night.",
        "poster_path": "/mock_poster_7",
        "backdrop_path": "/mock_backdrop_7",
        "vote_average": 7.5,
        "release_date": "2023-10-31",
        "genre_ids": [27, 53, 9648],  # Horror, Thriller, Mystery
        "original_language": "en"
    },
    {
        "id": 100008,
        "title": "Tokyo Drifter",
        "overview": "An underground street racer in Tokyo gets entangled with the Yakuza. A high-octane visual spectacle.",
        "poster_path": "/mock_poster_8",
        "backdrop_path": "/mock_backdrop_8",
        "vote_average": 8.3,
        "release_date": "2024-06-18",
        "genre_ids": [28, 80],  # Action, Crime
        "original_language": "ja"
    }
]

MOCK_MOVIE_DETAILS = {
    "title": "Neon Genesis: The Awakening",
    "overview": "In a cyberpunk future, a rogue AI discovers human emotions. As it navigates the complex neon-lit city, it must decide between its digital origins and its newfound humanity. The visual effects and sound design create a truly immersive experience that questions the very nature of existence.",
    "poster_path": "/mock_poster_1",
    "backdrop_path": "/mock_backdrop_1",
    "vote_average": 9.2,
    "release_date": "2024-11-20",
    "runtime": 142,
    "genres": [{"id": 878, "name": "Science Fiction"}, {"id": 28, "name": "Action"}, {"id": 18, "name": "Drama"}],
    "credits": {
        "cast": [
            {"name": "Elena Rostova", "character": "Aria (The AI)", "profile_path": None},
            {"name": "Marcus Kane", "character": "Detective Reynolds", "profile_path": None},
            {"name": "Li Wei", "character": "The Architect", "profile_path": None}
        ]
    },
    "videos": {
        "results": []
    },
    "similar": {
        "results": MOCK_MOVIES[1:5]
    }
}
