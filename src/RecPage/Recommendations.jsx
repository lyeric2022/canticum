import React, { useEffect, useState } from "react";
import { useLocation } from "react-router-dom";
import "./rec.css";

function Recommendations() {
  const location = useLocation();
  const { selectedSong } = location.state || {};
  const [recommendations, setRecommendations] = useState([]);

  useEffect(() => {
    if (selectedSong) {
      fetch(
        `http://127.0.0.1:5000/recommender?input_song_name=${encodeURIComponent(
          selectedSong.track_name
        )}&input_artist=${encodeURIComponent(selectedSong.artists)}`
      )
        .then((response) => response.json())
        .then((data) => setRecommendations(data))
        .catch((error) => {
          console.error("Error fetching recommendations:", error);
          alert("Failed to fetch recommendations.");
        });
    }
  }, [selectedSong]);

  const handleSongClick = (trackName) => {
    const url = `https://www.youtube.com/results?search_query=${encodeURIComponent(trackName)}`;
    window.open(url, '_blank');
  };

  return (
    <div>
      <button className="back-home-link">
        <a href="/">Return Home</a>
      </button>
      <h1>Curated Music Picks for You 🎵</h1>
      {recommendations && recommendations.length > 0 ? (
        <ul id="recommendations-list">
          {recommendations.map((rec, index) => (
            <li className="song-section" key={index}>
              <div className="song-section-info">
                <p><strong>Track:</strong> {rec.track_name}</p>
                <p><strong>Artist:</strong> {rec.artists}</p>
                <p><strong>Genre:</strong> {rec.track_genre}</p>
                <p><strong>Popularity:</strong> {rec.popularity}</p>
                <p><strong>Similarity Score:</strong> {100 * rec.similarity_score.toFixed(2)}%</p>
              </div>
              <div className="song-section-features">
                <div className="song-features">
                  <p><strong>Danceability:</strong> {rec.danceability}</p>
                  <p><strong>Energy:</strong> {rec.energy}</p>
                  <p><strong>Key:</strong> {rec.key}</p>
                  <p><strong>Loudness:</strong> {rec.loudness}</p>
                  <p><strong>Speechiness:</strong> {rec.speechiness}</p>
                  <p><strong>Acousticness:</strong> {rec.acousticness}</p>
                </div>
              </div>
              <div className="song-section-features">
                <div className="song-features">
                  <p><strong>Instrumentalness:</strong> {rec.instrumentalness.toFixed(4)}</p>
                  <p><strong>Liveness:</strong> {rec.liveness}</p>
                  <p><strong>Valence:</strong> {rec.valence}</p>
                  <p><strong>Tempo:</strong> {rec.tempo}</p>
                  <button className="listen-button" onClick={() => handleSongClick(rec.track_name)}>Listen on YouTube</button>

                </div>
              </div>
            </li>
          ))}
        </ul>
      ) : (
        <p id="no-rec-text">Loading Recommendations...</p>
      )}
    </div>
  );
}

export default Recommendations;