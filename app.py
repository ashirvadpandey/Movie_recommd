import streamlit as st
import pickle
import pandas as pd
import requests
from pprint import pprint
import json


def fetch_poster(id):
    api_key = '9cef986f8a47bedfd29259cabb215cef'
    language = 'en-US'

    response = requests.get(f"https://api.themoviedb.org/3/movie/{id}",
                            params={'api_key': api_key,
                                    'language': language})

    if response.status_code == 200:
        data = response.json()
        if 'poster_path' in data and data['poster_path'] is not None:
            poster_url = "https://image.tmdb.org/t/p/w300" + data['poster_path']
            return poster_url
        else:
            st.warning("Poster not available for this movie.")
            return None
    else:
        st.error("Failed to fetch movie details from API.")
        return None


def recommend(movie):

    if movie not in movies['title'].values:
        st.error("Sorry!  Movie not found.")
        return [], []


    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[:11]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].id
        recommended_movies.append(movies.iloc[i[0]].title)
        # fetch poster from api
        recommended_movies_posters.append(fetch_poster(movie_id))
        # fetch overview from api

    return recommended_movies, recommended_movies_posters


movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))
st.title('Movie Recommender System')

# Apply the CSS style using st.markdown
css_style = """
<style>
@media (min-width: 1250px) {
    h2 {
        font-size: 1.25rem;
    }
}
.movie-poster {
    margin-top: 87px;
}
</style>
"""
st.markdown(css_style, unsafe_allow_html=True)

selected_movie_name = st.selectbox(
    'Select a movie:',
    movies['title'].values
)
if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)

    # Create a container to display the selected movie
    st.header("Selected Movie:")
    selected_movie_index = names.index(selected_movie_name)
    selected_movie_poster = posters[selected_movie_index]
    st.markdown(f'<div class="selected-movie-poster"><img src="{selected_movie_poster}"></div>',
                unsafe_allow_html=True)

    # Create a container for the recommended movies
    st.header("Recommended Movies:")
    num_cols = 3  # Number of columns to display the recommended movies
    num_movies = len(names)

    for idx in range(0, num_movies, num_cols):
        cols = st.columns(num_cols)
        for col_idx, col in enumerate(cols):
            movie_idx = idx + col_idx
            if movie_idx < num_movies and posters[movie_idx]:
                col.header(names[movie_idx])
                col.image(posters[movie_idx], caption="", use_column_width=True)
