import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity

# Load dataset csv into music_data
music_data = pd.read_csv('dataset.csv')

# Use MinMax scaling to normalize data attributes
scaler = MinMaxScaler()
music_features = music_data[['danceability', 'energy', 'key',
                             'loudness', 'mode', 'speechiness', 'acousticness',
                             'instrumentalness', 'liveness', 'valence', 'tempo']].values
music_features_scaled = scaler.fit_transform(music_features)

# Function to get content-based recommendations based on music features


def content_based_recommendations(input_song_name, num_recommendations=5):
    if input_song_name not in music_data['track_name'].values:
        print(
            f"'{input_song_name}' not found in the dataset. Please enter a valid song name.")
        return

    # Get all indices of the input song in the music database
    input_song_indices = music_data[music_data['track_name']
                                    == input_song_name].index.tolist()

    # Calculate the similarity scores based on music features (cosine similarity)
    similarity_scores = cosine_similarity(
        music_features_scaled[input_song_indices[0]:input_song_indices[0]+1], music_features_scaled)

    # Get the indices of the most similar songs, excluding the input song's indices
    similar_song_indices = similarity_scores.argsort()[0][::-1]
    # Exclude input song indices and ensure no repeated songs
    similar_song_indices = [
        i for i in similar_song_indices if i not in input_song_indices][:num_recommendations + len(input_song_indices)]
    # Get the names of the most similar songs based on content-based filtering, excluding the input song
    recommendations_df = music_data.iloc[similar_song_indices][[
        'track_name', 'artists', 'album_name', 'popularity']]
    # Remove duplicates
    recommendations_df = recommendations_df.drop_duplicates(
        subset=['track_name', 'artists'], keep='first').head(num_recommendations)

    return recommendations_df


def main():
    # Replace with a song from your dataset
    input_song_name = "I'm Good (Blue)"
    recommendations = content_based_recommendations(
        input_song_name, num_recommendations=15)
    print(f"Recommended songs for '{input_song_name}':")
    print(recommendations)


if __name__ == "__main__":
    main()
