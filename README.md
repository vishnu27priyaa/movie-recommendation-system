# Movie Recommendation System

A simple **content-based movie recommendation system** built with Python and Streamlit.

This project uses the TMDB 5000 Movies Dataset to build a similarity model based on movie metadata (overview, genres, keywords, cast). It can recommend movies that are most similar to a selected movie.

---

## ✅ Features

- Search movies via dropdown
- Recommend top 5 similar movies
- Display movie posters (via TMDB API)
- Clean and interactive Streamlit UI
- Modular code with reusable recommendation logic

---

## 🧠 How it Works

1. Load `movies.csv` and `credits.csv`.
2. Combine key text fields (overview, genres, keywords, cast) into a single `tags` column.
3. Vectorize the tags with `CountVectorizer` and compute cosine similarity.
4. Given a movie title, find the most similar movies.
5. Use TMDB API to fetch movie posters.

---

## 📦 Project Structure

```
movie-recommendation-system/
├── app.py
├── recommend.py
├── model/
│   ├── build_model.py
│   ├── movies.pkl
│   └── similarity.pkl
├── dataset/
│   ├── movies.csv
│   └── credits.csv
├── requirements.txt
└── README.md
```

---

## 🚀 Getting Started

### 1) Install dependencies

```bash
pip install -r requirements.txt
```

### 2) Generate the model artifacts

```bash
python model/build_model.py
```

This creates the model files `model/movies.pkl` and `model/similarity.pkl`.

### 3) Run the Streamlit app

```bash
streamlit run app.py
```

Then open your browser to:

```
http://localhost:8501
```

---

## 🔑 TMDB API Key (for posters)

To display movie posters, you need a TMDB API key.

1. Create an account at https://www.themoviedb.org.
2. Generate an API key.

### Set the API key

You can set it via an environment variable:

```bash
export TMDB_API_KEY="YOUR_KEY_HERE"
```

Or for Windows PowerShell:

```powershell
$env:TMDB_API_KEY = "YOUR_KEY_HERE"
```

Or use Streamlit secrets by adding a `.streamlit/secrets.toml` file:

```toml
TMDB_API_KEY = "YOUR_KEY_HERE"
```

---

## 🧩 Customizing the Dataset

To use the full TMDB 5000 Movies dataset, replace the files under `dataset/` with the official `movies.csv` and `credits.csv`.

Then rerun:

```bash
python model/build_model.py
```

---

## 🛠 Notes

- This is a **content-based** recommender (not collaborative filtering).
- The recommendation quality depends on the richness of metadata in the dataset.
