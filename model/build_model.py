"""Build and serialize the movie similarity model.

This script reads the dataset CSVs, preprocesses text fields into a single "tags" column,
vectorizes the text using CountVectorizer, computes cosine similarity, and saves the
movies DataFrame and similarity matrix as pickled objects.

Run:
    python model/build_model.py
"""

import os
import pickle

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def load_datasets(movies_path: str, credits_path: str) -> pd.DataFrame:
    """Load and merge the movies and credits datasets."""

    movies = pd.read_csv(movies_path)
    credits = pd.read_csv(credits_path)

    # Ensure the merge key has the same dtype on both sides
    movies["movie_id"] = movies["movie_id"].astype(int)
    credits["movie_id"] = credits["movie_id"].astype(int)

    # Merge the datasets on movie_id; keep the title from the movies list as the canonical title
    merged = movies.merge(
        credits,
        on="movie_id",
        how="left",
        suffixes=("_movie", "_credit"),
    )

    # Prefer the title from the movies dataset if it exists
    if "title_movie" in merged.columns:
        merged["title"] = merged["title_movie"].fillna(merged.get("title_credit"))
    elif "title" in merged.columns:
        merged["title"] = merged["title"]

    return merged


def preprocess(df: pd.DataFrame) -> pd.DataFrame:
    """Create a "tags" column by combining key text fields."""

    # IMPORTANT: we keep the original title and movie_id for later use
    df = df.copy()

    # Fill NaNs with empty strings to avoid concatenation issues
    for col in ["overview", "genres", "keywords", "cast"]:
        if col in df.columns:
            df[col] = df[col].fillna("")

    # Combine relevant text features into a single "tags" column
    df["tags"] = (
        df["overview"].astype(str)
        + " "
        + df["genres"].astype(str)
        + " "
        + df["keywords"].astype(str)
        + " "
        + df["cast"].astype(str)
    )

    # Lowercase + remove spaces to create a normalized text field
    df["tags"] = df["tags"].str.lower().str.replace(" ", "", regex=False)

    return df


def build_similarity_matrix(df: pd.DataFrame, max_features: int = 5000) -> np.ndarray:
    """Convert tags to vectors and compute cosine similarity."""

    vectorizer = CountVectorizer(max_features=max_features, stop_words="english")
    vectors = vectorizer.fit_transform(df["tags"]).toarray()

    similarity = cosine_similarity(vectors)
    return similarity


def save_pickle(obj, path: str) -> None:
    """Save an object to disk using pickle."""

    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        pickle.dump(obj, f)


def main() -> None:
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    movies_path = os.path.join(root, "dataset", "movies.csv")
    credits_path = os.path.join(root, "dataset", "credits.csv")

    print("Loading datasets...")
    df = load_datasets(movies_path, credits_path)
    print(f"Loaded {len(df)} movies")

    print("Preprocessing...")
    df = preprocess(df)

    print("Building similarity matrix...")
    similarity = build_similarity_matrix(df)

    # Drop columns that are not needed at runtime to reduce memory footprint
    df_to_store = df[["movie_id", "title"]].copy()

    print("Saving model artifacts...")
    save_pickle(df_to_store, os.path.join(root, "model", "movies.pkl"))
    save_pickle(similarity, os.path.join(root, "model", "similarity.pkl"))

    print("Done. Model artifacts created in model/")


if __name__ == "__main__":
    main()
