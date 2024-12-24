import pickle
import streamlit as st
import requests

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data.get('poster_path')
    if poster_path:
        full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
        return full_path
    else:
        return None

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        poster = fetch_poster(movie_id)
        if poster:
            recommended_movie_posters.append(poster)
        else:
            recommended_movie_posters.append("https://via.placeholder.com/150")  # Placeholder image
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names, recommended_movie_posters

# Streamlit app
st.title('Movie Recommender System')
st.write('Using Machine Learning to recommend movies based on your preferences.')

# Load the movie list and similarity matrix
movies = pickle.load(open('Artifacts/movie_list.pkl', 'rb'))
similarity = pickle.load(open('Artifacts/similarity.pkl', 'rb'))

# Movie selection
movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

# Number of recommendations
num_recommendations = st.slider('Number of recommendations', 1, 10, 5)

# Display recommendations
if st.button('Recommend'):
    names, posters = recommend(selected_movie)
    st.write(f"Top {num_recommendations} recommendations for {selected_movie}:")
    for i in range(num_recommendations):
        st.image(posters[i], width=150)
        st.write(names[i])