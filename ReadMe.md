# 🎬 Movie Recommendation System

## Overview

The **Movie Recommendation System** is an intelligent application that suggests movies based on user preferences. Using advanced similarity algorithms and natural language processing techniques, it helps users discover movies they are most likely to enjoy.

This system leverages movie metadata and content-based filtering to provide accurate and personalized recommendations.

---

## Features

* **Search Movies:** Users can search for movies by name.
* **Personalized Recommendations:** Provides top similar movies based on selected movie.
* **Thumbnail Display:** Fetches and displays movie posters for a better user experience.
* **Easy-to-Use Interface:** Built using Streamlit for interactive and user-friendly design.
* **Fuzzy Matching:** Handles misspellings or partial inputs to find the closest movie matches.

---

## Technologies Used

* **Programming Language:** Python
* **Web Framework:** Streamlit
* **Libraries:**

  * `pandas` for data manipulation
  * `scikit-learn` for cosine similarity
  * `difflib` for fuzzy string matching
  * `pickle` for saving and loading precomputed data
  * `requests` for fetching movie posters (optional)

---

## How It Works

1. Load the dataset containing movie titles, IDs, and metadata.
2. Precompute a similarity matrix to compare movies based on content or features.
3. When a user selects a movie:

   * Find the closest match using fuzzy matching.
   * Retrieve the top N similar movies using the similarity matrix.
4. Display the recommendations along with thumbnails and titles.

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/movie-recommendation-system.git
cd movie-recommendation-system
```

2. Install the required packages:

```bash
pip install -r requirements.txt
```

3. Run the Streamlit app:

```bash
streamlit run app.py
```

---

## Dataset

* The system uses a CSV file containing movie details:

  * `movie_id`
  * `title`
  * `tags` or metadata for similarity computation
* Example:

```
movie_id,title,tags
19995,Avatar,action|adventure|sci-fi
285,Pirates of the Caribbean: At World's End,adventure|fantasy|action
```

---

## Folder Structure

```
movie-recommendation-system/
│
├── app.py                # Main Streamlit application
├── movies.csv            # Movie dataset
├── similarity.pkl        # Precomputed similarity matrix
├── requirements.txt      # Python dependencies
└── README.md             # Project documentation
```

---

## Future Improvements

* Integrate **collaborative filtering** for more personalized recommendations.
* Add **user ratings and reviews** to improve suggestions.
* Fetch **thumbnails dynamically** using TMDB API or Google search.
* Deploy the system online for public access.

---

## Author

**Samruddhi Magdum**

* LinkedIn: https://in.linkedin.com/in/samruddhi-magdum-377259258
* GitHub: https://github.com/samruddhi2026


