import streamlit as st
import pickle
import pandas as pd
from difflib import get_close_matches
import time

# --- Define the new professional color palette ---
BACKGROUND_COLOR = "#F0F2F6"  # Light Gray/Off-White
ACCENT_COLOR = "#3A86FF"  # Professional, Muted Blue
TEXT_COLOR = "#000000"  # Black for input text
TITLE_COLOR = "#1C304A"  # Dark Navy/Slate for headings

# -----------------------------
# Custom CSS for Styling
# -----------------------------
st.markdown(f"""
<style>
/* --- General Background and Layout --- */
.stApp {{
    background-color: {BACKGROUND_COLOR};
    color: {TEXT_COLOR};
}}

/* Style the main label (will only show when text is entered) */
.stTextInput label {{
    font-size: 1.25rem;
    font-weight: bold;
    color: {TITLE_COLOR}; /* Dark Navy for the label */
}}

/* --- Custom Search Box Style (st.text_input) --- */
div[data-baseweb="input"] {{
    background-color: #FFFFFF; /* White background for input field */
    border: 1px solid #CCCCCC;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    transition: all 0.3s ease;
}}

/* Target the actual text input field inside the container */
div[data-baseweb="input"] input {{
    background-color: transparent !important;
    color: {TEXT_COLOR}; /* CRUCIAL: Input text is BLACK */
    font-size: 1.1rem;
}}

/* --- Hover/Focus Effect for Text Input (Mouse Hover) --- */
div[data-baseweb="input"]:focus-within {{
    border-color: {ACCENT_COLOR}; /* Blue Accent on focus */
    box-shadow: 0 0 8px rgba(58, 134, 255, 0.6); /* Blue glow */
}}

/* --- Custom Title Styling --- */
h1 {{
    color: {TITLE_COLOR}; /* Dark Navy for title */
    text-shadow: none;
    text-align: center;
    padding-bottom: 20px;
}}

/* --- Recommendation Boxes (st.success) --- */
.stSuccess {{
    background-color: #FFFFFF; /* White background for recommendations */
    border-left: 5px solid {ACCENT_COLOR}; /* Blue Accent bar */
    border-radius: 5px;
    padding: 10px;
    margin: 5px 0;
    color: {TEXT_COLOR};
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}}

/* --- Button Styling --- */
.stButton>button {{
    background-color: {ACCENT_COLOR} !important;
    color: #FFFFFF !important; /* White text on blue button */
    border: 1px solid {ACCENT_COLOR};
    font-weight: bold;
}}
.stButton>button:hover {{
    opacity: 0.9;
    box-shadow: 0 0 10px {ACCENT_COLOR} !important;
}}
</style>
""", unsafe_allow_html=True)


# -----------------------------
# Load Data (Using st.cache_resource)
# -----------------------------
@st.cache_resource
def load_data():
    """Loads and preprocesses data, using Streamlit's cache for efficiency."""
    try:
        movies = pickle.load(open('movies.pkl', 'rb'))
        similarity = pickle.load(open('similarity.pkl', 'rb'))

        # Ensure DataFrame has a clean, 0-based index
        if isinstance(movies, pd.DataFrame):
            movies.reset_index(drop=True, inplace=True)
        else:
            movies = pd.DataFrame(movies)
            movies.reset_index(drop=True, inplace=True)

        return movies, similarity
    except Exception as e:
        st.error(
            f"❌ Error loading data: {e}. Ensure 'movies.pkl' and 'similarity.pkl' are correct and in the same directory.")
        st.stop()


movies, similarity = load_data()


# -----------------------------
# Recommendation Function (Corrected Indexing)
# -----------------------------
def recommend(movie_name):
    search_name = movie_name.strip().lower()
    all_titles = movies['title'].str.lower().tolist()

    close_matches = get_close_matches(search_name, all_titles, n=1, cutoff=0.5)

    if not close_matches:
        st.warning(f"No close match found for '{movie_name}'. Try another title.")
        return []

    best_match = close_matches[0]

    # FIX: Get POSITIONAL INDEX
    movie_index = movies[movies['title'].str.lower() == best_match].index[0]

    matched_movie_title = movies.iloc[movie_index]['title']
    distances = similarity[movie_index]

    similar_movies = sorted(
        list(enumerate(distances)), reverse=True, key=lambda x: x[1]
    )[1:6]

    recommended_movies = [movies.iloc[i[0]].title for i in similar_movies]

    st.info(f"Showing recommendations for: **{matched_movie_title}**")
    return recommended_movies


# -----------------------------
# Streamlit UI and Logic
# -----------------------------
st.title('🎬 Movie Recommender System')

# --- Check if the input is currently empty ---
is_input_empty = 'movie_input_value' not in st.session_state or st.session_state.movie_input_value == ""

# Define placeholder based on state
if is_input_empty:
    input_placeholder = "🔍 Start typing a movie name here..."
    input_label = "Search for a Movie"
else:
    # When text is present, the label acts as the instruction
    input_placeholder = ""
    input_label = ""

# Use st.text_input for the search bar
selected_movie_name = st.text_input(
    input_label,
    placeholder=input_placeholder,
    key="movie_input_value"  # Use a key to track the value for the Enter key logic
)

# Use st.session_state to track if the button was clicked
if 'button_clicked' not in st.session_state:
    st.session_state.button_clicked = False


def click_button():
    st.session_state.button_clicked = True


# Button to trigger the recommendation explicitly
st.button('Show Recommendations', use_container_width=True, on_click=click_button)

# --- Conditional Trigger (Handles Enter Key and Button Click) ---
# Check if the text input is not empty AND (the button was clicked OR the script was rerun due to Enter)
if selected_movie_name and (st.session_state.button_clicked or st.session_state.movie_input_value):

    # Clear the button click state to prevent perpetual reruns
    st.session_state.button_clicked = False

    # --- Progress Bar Implementation ---
    progress_bar = st.progress(0, text="Searching for recommendations...")

    # Simulate loading/processing time with the progress bar
    for percent_complete in range(100):
        time.sleep(0.005)
        progress_bar.progress(percent_complete + 1, text=f"Processing... {percent_complete + 1}%")

    time.sleep(0.1)
    progress_bar.empty()

    # --- Run Recommendation ---
    recommendations = recommend(selected_movie_name)

    if recommendations:
        st.markdown("## Top 5 Recommendations:")
        for i, movie in enumerate(recommendations, 1):
            st.success(f"{i}. {movie}")
else:
    # Display warning if the button was clicked but the input was empty
    if st.session_state.button_clicked:
        st.warning("Please enter a movie name to get recommendations.")
        st.session_state.button_clicked = False