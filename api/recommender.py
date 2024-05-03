import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity
from pathlib import Path
from flask import Flask, request

app = Flask(__name__)

file = Path(__file__).parent / "dataset.csv"

# Load dataset csv into music_data
music_data = pd.read_csv(file)

# Use MinMax scaling to normalize data attributes
scaler = MinMaxScaler()
music_features = music_data[['danceability', 'energy', 'key',
                             'loudness', 'mode', 'speechiness', 'acousticness',
                             'instrumentalness', 'liveness', 'valence', 'tempo']].values
music_features_scaled = scaler.fit_transform(music_features)

# Function to get music recommendations based on music features (content-based), genre, and popularity

# Music Recommender API Route


@app.route('/recommender')
def hybrid_recommendations():
    # Get arguments as query parameters
    input_song_name = request.args.get('input_song_name')
    num_recommendations = int(request.args.get('num_recommendations', 5))
    genre_weight = float(request.args.get('genre_weight', 0.5))
    popularity_weight = float(request.args.get('popularity_weight', 0.3))

    # Print message and return if input track does not exist in database
    if input_song_name not in music_data['track_name'].values:
        print(
            f"'{input_song_name}' not found in the dataset. Please enter a valid song name.")
        return

    # Get all indices of the input song in the music database
    input_song_indices = music_data[music_data['track_name']
                                    == input_song_name].index.tolist()
    # Features of input song
    input_song_features = music_features_scaled[input_song_indices[0]]

    input_song_genre = music_data.iloc[input_song_indices[0]]['track_genre']

    # Calculate the similarity scores based on music features (cosine similarity)
    similarity_scores = cosine_similarity(
        [input_song_features], music_features_scaled).flatten()

    similar_song_indices = []
    # Incorporate genre and popularity weights into the similarity scores
    for i, idx in enumerate(similar_song_indices):
        song_genre = music_data.loc[idx, 'track_genre']
        song_popularity = music_data.loc[idx, 'popularity']

        # Apply weighted combination of content-based similarity, genre similarity, and popularity
        similarity_scores[i] = (1 - genre_weight) * similarity_scores[i] + \
            genre_weight * (song_genre == input_song_genre)
        similarity_scores[i] = (1 - popularity_weight) * similarity_scores[i] + \
            popularity_weight * (song_popularity / 100.0)

    # Get indices of most similar songs, excluding input song index
    similar_song_indices = similarity_scores.argsort()[
        ::-1][:num_recommendations]

    # Get recommendations based on hybrid similarity scores
    recommendations_df = music_data.iloc[similar_song_indices][[
        'track_name', 'artists', 'album_name', 'popularity']]

    # Remove duplicates
    recommendations_df = recommendations_df.drop_duplicates(
        subset=['track_name', 'artists'], keep='first')

    return recommendations_df.to_json(orient='records')


def main():
    return hybrid_recommendations()


if __name__ == "__main__":
    app.run(debug=True)
