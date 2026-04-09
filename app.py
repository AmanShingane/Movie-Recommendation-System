import requests
import streamlit as st

# ==============================
# CONFIG
# ==============================
API_BASE  = "http://127.0.0.1:8000"   # change to your Render/deployed URL in prod
TMDB_IMG  = "https://image.tmdb.org/t/p/w500"

st.set_page_config(
    page_title="CineMatch",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ==============================
# GLOBAL STYLES
# ==============================
st.markdown("""
<style>
/* ── Import fonts ── */
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Sans:wght@300;400;500&display=swap');

/* ── Root variables ── */
:root {
    --bg:        #060810;
    --surface:   #0d1120;
    --surface2:  #141828;
    --accent:    #e8a838;
    --accent2:   #ff6b35;
    --text:      #e8e4da;
    --muted:     #5a5f72;
}

/* ── Full-page dark background ── */
.stApp { background: var(--bg) !important; color: var(--text) !important; }
section[data-testid="stSidebar"] { background: var(--surface) !important; }
.block-container { padding-top: 1.5rem; padding-bottom: 3rem; max-width: 1400px; }

/* ── Typography ── */
h1, h2, h3, h4 {
    font-family: 'Bebas Neue', sans-serif !important;
    letter-spacing: 2px !important;
    color: var(--text) !important;
}
p, div, span, label, .stMarkdown {
    font-family: 'DM Sans', sans-serif !important;
    color: var(--text) !important;
}

/* ── Inputs ── */
.stTextInput > div > div > input {
    background: var(--surface2) !important;
    border: 1px solid rgba(232,168,56,0.25) !important;
    color: var(--text) !important;
    border-radius: 6px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 15px !important;
}
.stTextInput > div > div > input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 2px rgba(232,168,56,0.15) !important;
}
.stSelectbox > div > div {
    background: var(--surface2) !important;
    border: 1px solid rgba(232,168,56,0.2) !important;
    color: var(--text) !important;
    border-radius: 6px !important;
}

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, var(--accent), var(--accent2)) !important;
    color: #060810 !important;
    border: none !important;
    border-radius: 6px !important;
    font-family: 'Bebas Neue', sans-serif !important;
    font-size: 15px !important;
    letter-spacing: 1.5px !important;
    padding: 6px 18px !important;
    transition: opacity 0.2s, transform 0.1s !important;
}
.stButton > button:hover { opacity: 0.88 !important; transform: translateY(-1px) !important; }
.stButton > button:active { transform: scale(0.97) !important; }

/* ── Sidebar buttons & selectors ── */
section[data-testid="stSidebar"] .stButton > button {
    width: 100% !important;
}
section[data-testid="stSidebar"] h2 {
    color: var(--accent) !important;
    font-size: 22px !important;
}

/* ── Divider ── */
hr { border-color: rgba(232,168,56,0.15) !important; margin: 1rem 0 !important; }

/* ── Movie cards ── */
.movie-card {
    background: var(--surface);
    border: 1px solid rgba(232,168,56,0.12);
    border-radius: 10px;
    overflow: hidden;
    transition: transform 0.2s, box-shadow 0.2s;
    margin-bottom: 4px;
}
.movie-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 32px rgba(0,0,0,0.5), 0 0 16px rgba(232,168,56,0.12);
}
.movie-title-text {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.82rem;
    font-weight: 500;
    line-height: 1.2rem;
    height: 2.4rem;
    overflow: hidden;
    color: var(--text);
    margin-top: 6px;
}
.movie-meta {
    font-size: 0.75rem;
    color: var(--muted);
    margin-top: 2px;
    margin-bottom: 6px;
}
.rating-badge {
    color: var(--accent);
    font-weight: 500;
    font-size: 0.78rem;
}

/* ── Detail card ── */
.detail-card {
    background: var(--surface);
    border: 1px solid rgba(232,168,56,0.15);
    border-radius: 12px;
    padding: 24px 28px;
    box-shadow: 0 0 40px rgba(232,168,56,0.06);
}
.detail-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 2.4rem;
    letter-spacing: 3px;
    color: var(--accent);
    line-height: 1;
    margin-bottom: 6px;
}
.detail-tagline {
    font-style: italic;
    color: var(--muted);
    font-size: 0.9rem;
    margin-bottom: 12px;
}
.detail-meta-row {
    display: flex;
    gap: 18px;
    flex-wrap: wrap;
    margin-bottom: 14px;
    font-size: 0.85rem;
    color: var(--muted);
}
.detail-meta-row span.highlight { color: var(--accent); font-weight: 500; }
.genre-chip {
    display: inline-block;
    background: rgba(232,168,56,0.1);
    border: 1px solid rgba(232,168,56,0.25);
    color: var(--accent);
    border-radius: 20px;
    padding: 3px 12px;
    font-size: 0.75rem;
    margin: 2px 3px 2px 0;
    letter-spacing: 0.5px;
}
.section-label {
    font-size: 0.7rem;
    letter-spacing: 5px;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 14px;
    margin-top: 10px;
}

/* ── Logo banner ── */
.logo-banner {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 2.8rem;
    letter-spacing: 5px;
    background: linear-gradient(135deg, #e8a838, #ff6b35);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1;
    margin-bottom: 2px;
}
.logo-sub {
    font-size: 0.7rem;
    letter-spacing: 5px;
    text-transform: uppercase;
    color: var(--muted);
    font-family: 'DM Sans', sans-serif;
}

/* ── Info / warning overrides ── */
.stAlert { background: var(--surface2) !important; border-radius: 8px !important; }

/* ── Backdrop image ── */
.backdrop-img { border-radius: 10px; overflow: hidden; margin-top: 12px; }
</style>
""", unsafe_allow_html=True)


# ==============================
# SESSION STATE + ROUTING
# ==============================
if "view" not in st.session_state:
    st.session_state.view = "home"
if "selected_tmdb_id" not in st.session_state:
    st.session_state.selected_tmdb_id = None

qp_view = st.query_params.get("view")
qp_id   = st.query_params.get("id")
if qp_view in ("home", "details"):
    st.session_state.view = qp_view
if qp_id:
    try:
        st.session_state.selected_tmdb_id = int(qp_id)
        st.session_state.view = "details"
    except Exception:
        pass


def goto_home():
    st.session_state.view = "home"
    st.query_params["view"] = "home"
    if "id" in st.query_params:
        del st.query_params["id"]
    st.rerun()


def goto_details(tmdb_id: int):
    st.session_state.view = "details"
    st.session_state.selected_tmdb_id = int(tmdb_id)
    st.query_params["view"]  = "details"
    st.query_params["id"]    = str(int(tmdb_id))
    st.rerun()


# ==============================
# API HELPERS
# ==============================
@st.cache_data(ttl=60)
def api_get(path: str, params: dict | None = None):
    try:
        r = requests.get(f"{API_BASE}{path}", params=params, timeout=25)
        if r.status_code >= 400:
            return None, f"HTTP {r.status_code}: {r.text[:300]}"
        return r.json(), None
    except Exception as e:
        return None, f"Request failed: {e}"


def parse_search_to_suggestions(data, keyword: str, limit: int = 24):
    """
    Handles both raw TMDB shape {"results":[...]} and plain list [{tmdb_id,...}].
    Returns:
        suggestions: list[(label, tmdb_id)]
        cards:       list[{tmdb_id, title, poster_url, release_date}]
    """
    kw = keyword.strip().lower()

    if isinstance(data, dict) and "results" in data:
        raw = []
        for m in data.get("results") or []:
            tmdb_id = m.get("id")
            title   = (m.get("title") or "").strip()
            if not title or not tmdb_id:
                continue
            raw.append({
                "tmdb_id":      int(tmdb_id),
                "title":        title,
                "poster_url":   f"{TMDB_IMG}{m['poster_path']}" if m.get("poster_path") else None,
                "release_date": m.get("release_date", ""),
                "vote_average": m.get("vote_average", 0),
            })
    elif isinstance(data, list):
        raw = []
        for m in data:
            tmdb_id = m.get("tmdb_id") or m.get("id")
            title   = (m.get("title") or "").strip()
            if not title or not tmdb_id:
                continue
            raw.append({
                "tmdb_id":      int(tmdb_id),
                "title":        title,
                "poster_url":   m.get("poster_url"),
                "release_date": m.get("release_date", ""),
                "vote_average": m.get("vote_average", 0),
            })
    else:
        return [], []

    matched = [x for x in raw if kw in x["title"].lower()]
    final   = matched if matched else raw

    suggestions = []
    for x in final[:10]:
        year  = (x.get("release_date") or "")[:4]
        label = f"{x['title']} ({year})" if year else x["title"]
        suggestions.append((label, x["tmdb_id"]))

    cards = [
        {
            "tmdb_id":    x["tmdb_id"],
            "title":      x["title"],
            "poster_url": x["poster_url"],
            "release_date": x.get("release_date",""),
            "vote_average": x.get("vote_average", 0),
        }
        for x in final[:limit]
    ]
    return suggestions, cards


def tfidf_cards(tfidf_items):
    out = []
    for x in tfidf_items or []:
        tmdb = x.get("tmdb") or {}
        if tmdb.get("tmdb_id"):
            out.append({
                "tmdb_id":    tmdb["tmdb_id"],
                "title":      tmdb.get("title") or x.get("title") or "Untitled",
                "poster_url": tmdb.get("poster_url"),
                "vote_average": tmdb.get("vote_average", 0),
                "release_date": tmdb.get("release_date",""),
            })
    return out


# ==============================
# POSTER GRID RENDERER
# ==============================
def poster_grid(cards, cols=6, key_prefix="grid"):
    if not cards:
        st.info("No movies to show.")
        return

    rows = (len(cards) + cols - 1) // cols
    idx  = 0
    for r in range(rows):
        colset = st.columns(cols, gap="small")
        for c in range(cols):
            if idx >= len(cards):
                break
            m       = cards[idx]
            idx    += 1
            tmdb_id = m.get("tmdb_id")
            title   = m.get("title", "Untitled")
            poster  = m.get("poster_url")
            year    = (m.get("release_date") or "")[:4]
            rating  = m.get("vote_average") or 0

            with colset[c]:
                if poster:
                    st.image(poster, use_column_width=True)
                else:
                    st.markdown(
                        "<div style='background:#141828;border-radius:8px;"
                        "aspect-ratio:2/3;display:flex;align-items:center;"
                        "justify-content:center;font-size:2rem;color:#5a5f72'>🎬</div>",
                        unsafe_allow_html=True,
                    )

                if tmdb_id:
                    if st.button("▶ Open", key=f"{key_prefix}_{r}_{c}_{idx}"):
                        goto_details(tmdb_id)

                rating_span = f"<span class='rating-badge'>⭐ {round(rating, 1)}</span>" if rating else ""
                st.markdown(
                    f"<div class='movie-title-text'>{title}</div>"
                    f"<div class='movie-meta'>"
                    f"{year or '—'} &nbsp; {rating_span}"
                    f"</div>",
                    unsafe_allow_html=True,
                )


# ==============================
# SIDEBAR
# ==============================
with st.sidebar:
    st.markdown("<div class='logo-banner'>CINEMATCH</div><div class='logo-sub'>Recommendation Engine</div>", unsafe_allow_html=True)
    st.markdown("---")

    if st.button("🏠  Home"):
        goto_home()

    st.markdown("---")
    st.markdown("### Feed Category")
    home_category = st.selectbox(
        "Browse by",
        ["trending", "popular", "top_rated", "now_playing", "upcoming"],
        format_func=lambda x: x.replace("_", " ").title(),
        index=0,
    )
    grid_cols = st.slider("Grid columns", 3, 8, 5)

    st.markdown("---")
    st.markdown(
        "<div style='font-size:0.72rem;color:#5a5f72;line-height:1.6'>"
        "TF-IDF · Cosine Similarity<br>TMDB API · FastAPI · Streamlit"
        "</div>",
        unsafe_allow_html=True,
    )


# ==============================
# HEADER BAR (home view only)
# ==============================
if st.session_state.view == "home":
    hcol1, hcol2 = st.columns([3, 1])
    with hcol1:
        st.markdown("<h1 style='font-size:2.6rem;margin-bottom:0'>🎬 CineMatch</h1>", unsafe_allow_html=True)
        st.markdown(
            "<div style='color:#5a5f72;font-size:0.85rem;margin-top:-4px'>"
            "Search any movie → get AI-powered recommendations"
            "</div>",
            unsafe_allow_html=True,
        )
    st.markdown("<hr>", unsafe_allow_html=True)


# ============================================================
# VIEW: HOME
# ============================================================
if st.session_state.view == "home":

    typed = st.text_input(
        "",
        placeholder="🔍  Search: Inception, Batman, Titanic...",
        label_visibility="collapsed",
    )

    st.markdown("<hr>", unsafe_allow_html=True)

    # ── SEARCH MODE ──
    if typed.strip():
        if len(typed.strip()) < 2:
            st.caption("Type at least 2 characters.")
        else:
            with st.spinner("Searching..."):
                data, err = api_get("/tmdb/search", params={"query": typed.strip()})

            if err or data is None:
                st.error(f"Search failed: {err}")
            else:
                suggestions, cards = parse_search_to_suggestions(data, typed.strip(), limit=24)

                if suggestions:
                    labels   = ["── Select a title ──"] + [s[0] for s in suggestions]
                    selected = st.selectbox("Matching titles", labels, index=0)
                    if selected != "── Select a title ──":
                        label_to_id = {s[0]: s[1] for s in suggestions}
                        goto_details(label_to_id[selected])
                else:
                    st.info("No suggestions found. Try a different keyword.")

                st.markdown("<div class='section-label'>Search Results</div>", unsafe_allow_html=True)
                poster_grid(cards, cols=grid_cols, key_prefix="search_results")
        st.stop()

    # ── HOME FEED MODE ──
    st.markdown(
        f"<div class='section-label'>{home_category.replace('_',' ').upper()}</div>",
        unsafe_allow_html=True,
    )

    with st.spinner("Loading feed..."):
        home_cards, err = api_get("/home", params={"category": home_category, "limit": 24})

    if err or not home_cards:
        st.error(f"Home feed failed: {err or 'Unknown error'}")
        st.stop()

    poster_grid(home_cards, cols=grid_cols, key_prefix="home_feed")


# ============================================================
# VIEW: DETAILS
# ============================================================
elif st.session_state.view == "details":
    tmdb_id = st.session_state.selected_tmdb_id

    if not tmdb_id:
        st.warning("No movie selected.")
        if st.button("← Back to Home"):
            goto_home()
        st.stop()

    # ── Top bar ──
    bar_l, bar_r = st.columns([6, 1])
    with bar_l:
        st.markdown("<h2 style='margin-bottom:0'>📄 Movie Details</h2>", unsafe_allow_html=True)
    with bar_r:
        if st.button("← Home"):
            goto_home()

    st.markdown("<hr>", unsafe_allow_html=True)

    # ── Load details ──
    with st.spinner("Fetching details..."):
        data, err = api_get(f"/movie/id/{tmdb_id}")

    if err or not data:
        st.error(f"Could not load details: {err or 'Unknown'}")
        st.stop()

    # ── Poster + Info layout ──
    col_poster, col_info = st.columns([1, 2.6], gap="large")

    with col_poster:
        if data.get("poster_url"):
            st.image(data["poster_url"], use_column_width=True)
        else:
            st.markdown(
                "<div style='background:#141828;border-radius:10px;aspect-ratio:2/3;"
                "display:flex;align-items:center;justify-content:center;"
                "font-size:3rem;color:#5a5f72'>🎬</div>",
                unsafe_allow_html=True,
            )

    with col_info:
        st.markdown("<div class='detail-card'>", unsafe_allow_html=True)

        # Title
        st.markdown(
            f"<div class='detail-title'>{data.get('title','')}</div>",
            unsafe_allow_html=True,
        )

        # Tagline
        if data.get("tagline"):
            st.markdown(
                f"<div class='detail-tagline'>\"{data['tagline']}\"</div>",
                unsafe_allow_html=True,
            )

        # Meta row
        year    = (data.get("release_date") or "")[:4]
        runtime = data.get("runtime")
        rating  = data.get("vote_average")
        votes   = data.get("vote_count")

        meta_parts = []
        if year:    meta_parts.append(f"<span>📅 {year}</span>")
        if runtime: meta_parts.append(f"<span>⏱ {runtime} min</span>")
        if rating:  meta_parts.append(f"<span class='highlight'>⭐ {round(rating,1)}</span>")
        if votes:   meta_parts.append(f"<span>{votes:,} votes</span>")

        if meta_parts:
            st.markdown(
                f"<div class='detail-meta-row'>{'  ·  '.join(meta_parts)}</div>",
                unsafe_allow_html=True,
            )

        # Genres
        genres = data.get("genres", [])
        if genres:
            chips = "".join([f"<span class='genre-chip'>{g['name']}</span>" for g in genres])
            st.markdown(chips, unsafe_allow_html=True)

        st.markdown("<hr>", unsafe_allow_html=True)

        # Overview
        st.markdown("**Overview**")
        st.write(data.get("overview") or "No overview available.")

        st.markdown("</div>", unsafe_allow_html=True)

    # ── Backdrop ──
    if data.get("backdrop_url"):
        st.markdown("<div class='backdrop-img'>", unsafe_allow_html=True)
        st.image(data["backdrop_url"], use_column_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    # ── Recommendations ──
    title = (data.get("title") or "").strip()
    if title:
        with st.spinner("Finding similar movies..."):
            bundle, err2 = api_get(
                "/movie/search",
                params={"query": title, "tfidf_top_n": 12, "genre_limit": 12},
            )

        if not err2 and bundle:
            tfidf_list = tfidf_cards(bundle.get("tfidf_recommendations"))
            genre_list = bundle.get("genre_recommendations", [])

            tab1, tab2 = st.tabs(["🔎  Similar Movies (TF-IDF)", "🎭  More Like This (Genre)"])

            with tab1:
                st.markdown("<div class='section-label'>Content-based recommendations</div>", unsafe_allow_html=True)
                poster_grid(tfidf_list, cols=grid_cols, key_prefix="tfidf_recs")

            with tab2:
                st.markdown("<div class='section-label'>Genre-based recommendations</div>", unsafe_allow_html=True)
                poster_grid(genre_list, cols=grid_cols, key_prefix="genre_recs")

        else:
            st.markdown("<div class='section-label'>Genre Recommendations</div>", unsafe_allow_html=True)
            with st.spinner("Loading genre recommendations..."):
                genre_only, err3 = api_get(
                    "/recommend/genre", params={"tmdb_id": tmdb_id, "limit": 18}
                )
            if not err3 and genre_only:
                poster_grid(genre_only, cols=grid_cols, key_prefix="genre_fallback")
            else:
                st.warning("No recommendations available right now.")
    else:
        st.warning("No title available to compute recommendations.")
