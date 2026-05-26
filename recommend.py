"""Movie recommendation logic.

This module provides a simple content-based recommendation engine based on a
precomputed similarity matrix.

To regenerate the model artifacts (movies.pkl and similarity.pkl), run:
    python model/build_model.py
"""

import os
import pickle
from typing import List, Optional, Tuple

import requests


def _load_pickle(path: str):
    with open(path, "rb") as f:
        return pickle.load(f)


def load_model(root_dir: Optional[str] = None) -> Tuple[list, list]:
    """Load movie metadata and similarity matrix."""

    if root_dir is None:
        root_dir = os.path.dirname(os.path.abspath(__file__))

    movies_path = os.path.join(root_dir, "model", "movies.pkl")
    similarity_path = os.path.join(root_dir, "model", "similarity.pkl")

    movies = _load_pickle(movies_path)
    similarity = _load_pickle(similarity_path)

    return movies, similarity


def recommend(movie_title: str, movies, similarity, top_n: int = 5) -> list:
    """Recommend movies most similar to the given movie title."""

    # Find the index of the movie in the precomputed movie list
    indices = movies[movies["title"].str.lower() == movie_title.strip().lower()].index
    if len(indices) == 0:
        return []

    idx = indices[0]

    # Get similarity scores for the requested movie
    sim_scores = list(enumerate(similarity[idx]))

    # Sort movies by similarity score in descending order
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Skip the first one since it is the movie itself, then pick the top_n
    top_indices = [i for i, _ in sim_scores[1 : top_n + 1]]

    recommended = movies.iloc[top_indices][["movie_id", "title"]].to_dict(orient="records")
    return recommended


def fetch_poster(movie_id: int, api_key: str) -> Optional[str]:
    """Fetch the TMDB poster path for the given movie ID."""

    if not api_key:
        return None

    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        poster_path = data.get("poster_path")
        if poster_path:
            return f"https://image.tmdb.org/t/p/w500{poster_path}"
    except Exception:
        # If the TMDB API fails (rate limit, missing key, etc.), return None
        return None

    return None


def get_movie_list(movies) -> list:
    """Return a sorted list of movie titles."""

    return sorted(movies["title"].unique().tolist())
