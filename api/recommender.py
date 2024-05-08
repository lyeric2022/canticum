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
def hybrid_recommendations():
    try:
        # Retrieve query parameters
        input_song_name = request.args.get('input_song_name')
        num_recommendations = int(request.args.get('num_recommendations', 5))
        genre_weight = float(request.args.get('genre_weight', 0.5))
        popularity_weight = float(request.args.get('popularity_weight', 0.3))

        # Check if the song is in the dataset
        if input_song_name not in music_data['track_name'].values:
            return jsonify({'error': 'Song not found'}), 404

        # Find the indices of the input song
        input_song_indices = music_data[music_data['track_name'] == input_song_name].index.tolist()
        input_song_features = music_features_scaled[input_song_indices[0]]
        input_song_genre = music_data.iloc[input_song_indices[0]]['track_genre']

        # Calculate cosine similarity
        similarity_scores = cosine_similarity([input_song_features], music_features_scaled).flatten()

        # Adjust similarity scores based on genre and popularity
        for i in range(len(similarity_scores)):
            if i in input_song_indices:
                continue  # Skip the input song
            song_genre = music_data.iloc[i]['track_genre']
            song_popularity = music_data.iloc[i]['popularity']
            # Incorporate more nuanced genre similarity
            genre_similarity = (song_genre == input_song_genre) * 1.0  # Binary similarity, could be improved
            similarity_scores[i] = ((1 - genre_weight) * similarity_scores[i] +
                                    genre_weight * genre_similarity) * \
                                   ((1 - popularity_weight) + popularity_weight * (song_popularity / 100))

        # Get indices of most similar songs, excluding input song index
        top_indices = np.argsort(similarity_scores)[::-1][1:num_recommendations+1]  # Exclude the input song

        # Compile recommendations based on indices
        recommendations_df = music_data.iloc[top_indices][['track_name', 'artists', 'album_name', 'popularity']]
        recommendations_df = recommendations_df.drop_duplicates(subset=['track_name', 'artists'], keep='first')

        # Return recommendations as JSON
        return jsonify(recommendations_df.to_dict(orient='records')), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
