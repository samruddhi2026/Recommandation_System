import streamlit as st
import pickle
import pandas as pd
from difflib import get_close_matches
import time
import requests

BACKGROUND_COLOR = "#F0F2F6"
ACCENT_COLOR = "#3A86FF"
TEXT_COLOR = "#000000"
TITLE_COLOR = "#1C304A"

st.markdown(f"""
<style>
.stApp {{
    background-color: {BACKGROUND_COLOR};
    color: {TEXT_COLOR};
}}
.stTextInput label {{
    font-size: 1.25rem;
    font-weight: bold;
    color: {TITLE_COLOR};
}}
div[data-baseweb="input"] {{
    background-color: #FFFFFF;
    border: 1px solid #CCCCCC;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    transition: all 0.3s ease;
}}
div[data-baseweb="input"] input {{
    background-color: transparent !important;
    color: {TEXT_COLOR};
    font-size: 1.1rem;
}}
div[data-baseweb="input"]:focus-within {{
    border-color: {ACCENT_COLOR};
    box-shadow: 0 0 8px rgba(58, 134, 255, 0.6);
}}
h1 {{
    color: {TITLE_COLOR};
    text-align: center;
    padding-bottom: 20px;
}}
.stSuccess {{
    background-color: #FFFFFF;
    border-left: 5px solid {ACCENT_COLOR};
    border-radius: 5px;
    padding: 10px;
    margin: 5px 0;
    color: {TEXT_COLOR};
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}}
.stButton>button {{
    background-color: {ACCENT_COLOR} !important;
    color: #FFFFFF !important;
    border: 1px solid {ACCENT_COLOR};
    font-weight: bold;
}}
.stButton>button:hover {{
    opacity: 0.9;
    box-shadow: 0 0 10px {ACCENT_COLOR} !important;
}}
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_data():
    movies = pickle.load(open('movies.pkl', 'rb'))
    similarity = pickle.load(open('similarity.pkl', 'rb'))
    if isinstance(movies, pd.DataFrame):
        movies.reset_index(drop=True, inplace=True)
    else:
        movies = pd.DataFrame(movies)
        movies.reset_index(drop=True, inplace=True)
    return movies, similarity

movies, similarity = load_data()

def fetch_poster(movie_id):
    api_key = "20d637100f4f007c3bd78525ad476b75"
    response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US')
    data = response.json()
    if 'poster_path' in data and data['poster_path']:
        return "http://image.tmdb.org/t/p/w500" + data['poster_path']
    else:
        return "https://via.placeholder.com/500x750?text=No+Image"

def recommend(movie_name):
    search_name = movie_name.strip().lower()
    all_titles = movies['title'].str.lower().tolist()
    close_matches = get_close_matches(search_name, all_titles, n=1, cutoff=0.5)
    if not close_matches:
        st.warning(f"No close match found for '{movie_name}'. Try another title.")
        return []
    best_match = close_matches[0]
    movie_index = movies[movies['title'].str.lower() == best_match].index[0]
    matched_movie_title = movies.iloc[movie_index]['title']
    distances = similarity[movie_index]
    similar_movies = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies = []
    for i in similar_movies:
        movie_id = movies.iloc[i[0]].movie_id
        poster = fetch_poster(movie_id)
        recommended_movies.append((movies.iloc[i[0]].title, poster))
    st.info(f"Showing recommendations for: **{matched_movie_title}**")
    return recommended_movies

st.title('🎬 Movie Recommender System')

is_input_empty = 'movie_input_value' not in st.session_state or st.session_state.movie_input_value == ""
if is_input_empty:
    input_placeholder = "🔍 Start typing a movie name here..."
    input_label = "Search for a Movie"
else:
    input_placeholder = ""
    input_label = ""

selected_movie_name = st.text_input(
    input_label,
    placeholder=input_placeholder,
    key="movie_input_value"
)

if 'button_clicked' not in st.session_state:
    st.session_state.button_clicked = False

def click_button():
    st.session_state.button_clicked = True

st.button('Show Recommendations', use_container_width=True, on_click=click_button)

if selected_movie_name and (st.session_state.button_clicked or st.session_state.movie_input_value):
    st.session_state.button_clicked = False
    progress_bar = st.progress(0, text="Searching for recommendations...")
    for percent_complete in range(100):
        time.sleep(0.005)
        progress_bar.progress(percent_complete + 1, text=f"Processing... {percent_complete + 1}%")
    time.sleep(0.1)
    progress_bar.empty()
    recommendations = recommend(selected_movie_name)
    if recommendations:
        st.markdown("## Top 5 Recommendations:")
        cols = st.columns(5)
        for idx, (movie, poster) in enumerate(recommendations):
            with cols[idx]:
                st.image(poster, use_container_width=True)
                st.caption(movie)
else:
    if st.session_state.button_clicked:
        st.warning("Please enter a movie name to get recommendations.")
        st.session_state.button_clicked = False
