# 🎬 CineMatch — FastAPI + Streamlit Movie Recommender

A full-stack movie recommendation app built with:
- **FastAPI** — Backend API with TF-IDF cosine similarity + TMDB integration
- **Streamlit** — Beautiful frontend with cinematic dark UI
- **TMDB API** — Live posters, backdrops, ratings, genres

---

## 📁 Project Structure

```
movie_fastapi/
│
├── main.py              ← FastAPI backend
├── app.py               ← Streamlit frontend
├── requirements.txt     ← All dependencies
├── .env                 ← TMDB API key
│
├── df.pkl               ← Movie DataFrame (45k+ movies)
├── indices.pkl          ← Title → Index mapping
├── tfidf.pkl            ← Trained TF-IDF vectorizer
└── tfidf_matrix.pkl     ← TF-IDF sparse matrix
```

---

## ⚙️ Setup & Run

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Start the FastAPI backend
```bash
uvicorn main:app --reload --port 8000
```
API docs will be at: http://localhost:8000/docs

### 3. Start the Streamlit frontend (new terminal)
```bash
streamlit run app.py
```
App will open at: http://localhost:8501

---

## 🌐 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check + movie count |
| GET | `/home?category=trending` | Home feed (trending/popular/top_rated/now_playing/upcoming) |
| GET | `/tmdb/search?query=batman` | TMDB keyword search (for autocomplete + grid) |
| GET | `/movie/id/{tmdb_id}` | Full movie details by TMDB ID |
| GET | `/movie/search?query=Inception` | Bundle: details + TF-IDF recs + genre recs |
| GET | `/recommend/tfidf?title=Inception` | TF-IDF recommendations only |
| GET | `/recommend/genre?tmdb_id=27205` | Genre-based recommendations |

---

## ✨ Features

- 🔍 **Keyword search** with dropdown suggestions + poster grid
- 🎯 **TF-IDF recommendations** from your 45k movie dataset
- 🎭 **Genre recommendations** via TMDB Discover API
- 🖼️ **Live posters & backdrops** from TMDB
- ⭐ **Ratings, runtime, tagline, genres** per movie
- 🔁 **Click any recommendation** → opens its details + recommendations
- 📺 **Tabbed recommendations** (Similar / Genre)
- 📂 **Home feed** by category (Trending, Popular, etc.)

---

## 🔑 API Key

Set in `.env`:
```
TMDB_API_KEY=4a57f906b6b4337c0a502c2441372cee
```

---

## 🚀 Deploy to Render (optional)

1. Push the project to GitHub
2. Create a **Web Service** on [render.com](https://render.com)
3. Set **Start Command**: `uvicorn main:app --host 0.0.0.0 --port 10000`
4. Add environment variable: `TMDB_API_KEY=your_key`
5. Update `API_BASE` in `app.py` to your Render URL
6. Deploy Streamlit separately on [streamlit.io/cloud](https://streamlit.io/cloud)
