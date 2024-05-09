import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity
from pathlib import Path
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Apply CORS to all routes and all origins by default

# Define the path to the dataset
file = Path(__file__).parent / "dataset.csv"

# Load dataset csv into music_data DataFrame
music_data = pd.read_csv(file)

# Use MinMax scaling to normalize data attributes
scaler = MinMaxScaler()
music_features = music_data[['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness',
                             'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo']].values
music_features_scaled = scaler.fit_transform(music_features)


@app.route('/recommender', methods=['GET'])
# Music Recommender function
def hybrid_recommendations():
    try:
        # Retrieve query parameters
        input_song_name = request.args.get('input_song_name', '')
        input_artist = request.args.get('input_artist', '')

        # Constant definitions
        num_recommendations = 20
        genre_weight = 0.3
        popularity_weight = 0.2

        # Find song in dataset
        matching_song = music_data[(music_data['track_name'] == input_song_name) & (
            music_data['artists'] == input_artist)]

        # Return error if song not found in dataset
        if matching_song.empty:
            return jsonify({'error': 'Song not found'}), 404

        # Find the indices of the input song (put in list since there may be duplicates)
        input_song_indices = music_data[
            (music_data['track_name'] == input_song_name) &
            (music_data['artists'] == input_artist)
        ].index.tolist()

        # Get scaled music features of input song
        input_song_features = music_features_scaled[input_song_indices[0]]
        # Get input song genre
        input_song_genre = music_data.iloc[input_song_indices[0]
                                           ]['track_genre']

        # Calculate cosine similarity
        similarity_scores = cosine_similarity(
            [input_song_features], music_features_scaled).flatten()

        # Adjust similarity scores based on genre and popularity
        for i in range(len(similarity_scores)):
            if i in input_song_indices:
                continue  # Skip the input song
            song_genre = music_data.iloc[i]['track_genre']
            song_popularity = music_data.iloc[i]['popularity']
            genre_similarity = (song_genre == input_song_genre) * 1.0
            similarity_scores[i] = ((1 - genre_weight) * similarity_scores[i] +
                                    genre_weight * genre_similarity) * \
                                   ((1 - popularity_weight) +
                                    popularity_weight * (song_popularity / 100))

        # Get indices of most similar songs, excluding input song index
        top_indices = np.argsort(similarity_scores)[
            ::-1][1:num_recommendations+1]

        # Compile recommendations based on indices
        recommendations_df = music_data.iloc[top_indices][[
            'track_name', 'artists', 'track_genre', 'popularity', 'track_id',
            'danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness',
            'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo']]
        recommendations_df['similarity_score'] = similarity_scores[top_indices]     # Add similarity scores

        # Remove duplicate songs if any
        recommendations_df = recommendations_df.drop_duplicates(
            subset=['track_name', 'artists'], keep='first')

        # Return recommendations as JSON object
        return jsonify(recommendations_df.to_dict(orient='records')), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/search', methods=['GET'])
# Song search function; find tracks matching input_song_name in dataset
def search_songs():
    # Get search query from api request
    query = request.args.get('query', '')
    # Return empty if no tracks found
    if not query:
        return jsonify({'results': []})

    # Perform a case-insensitive search for matching songs
    matching_songs = music_data[music_data['track_name'].str.contains(
        query, case=False, na=False)]

    return jsonify({'results': matching_songs.to_dict(orient='records')})


if __name__ == "__main__":
    app.run(debug=True)
