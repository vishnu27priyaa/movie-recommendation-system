"""Streamlit app for Movie Recommendation System."""

import os

import streamlit as st

from recommend import fetch_poster, get_movie_list, load_model, recommend


@st.cache_data(show_spinner=False)
def load_data():
    movies, similarity = load_model()
    return movies, similarity


def get_tmdb_api_key() -> str:
    """Retrieve the TMDB API key from Streamlit secrets or environment variables."""

    api_key = ""

    # Prefer the Streamlit secrets mechanism if available.
    try:
        api_key = st.secrets.get("TMDB_API_KEY", "")
    except Exception:
        # No secrets file is present, or the key is missing.
        api_key = ""

    if not api_key:
        api_key = os.environ.get("TMDB_API_KEY", "")

    return api_key


def main() -> None:
    st.set_page_config(page_title="Movie Recommendation System", layout="wide")

    st.title("🎬 Movie Recommendation System")
    st.write(
        "Select a movie and get top recommendations based on content similarity (genres, overview, cast, keywords)."
    )

    movies, similarity = load_data()
    movie_list = get_movie_list(movies)

    selected_movie = st.selectbox("Select a movie", movie_list)

    api_key = get_tmdb_api_key()
    api_key = st.text_input("TMDB API Key (optional, for posters)", value=api_key, type="password")

    if st.button("Recommend"):
        with st.spinner("Finding similar movies..."):
            recommendations = recommend(selected_movie, movies, similarity, top_n=5)

        if not recommendations:
            st.warning("No recommendations found. Try another movie.")
            return

        api_key = get_tmdb_api_key()

        cols = st.columns(5)
        for idx, rec in enumerate(recommendations):
            with cols[idx]:
                poster_url = fetch_poster(rec["movie_id"], api_key) if api_key else None
                if poster_url:
                    st.image(poster_url, use_column_width=True)
                else:
                    st.write("(Poster not available)")

                st.markdown(f"**{rec['title']}**")


if __name__ == "__main__":
    main()
